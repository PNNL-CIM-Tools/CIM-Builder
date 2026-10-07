"""Phase 2 reflection validation gate tests (design: CIMTBL_DESIGN.md §8 exit criterion).

validate.validate() turns a RawRecord (§12.1) into a validated <Class>Row
(§12.2). Covers: unknown class, unknown column with closest-match
suggestion, Qty binding for physical-quantity slots, FK pass-through as
unresolved name strings, and correct native Python typing (int/bool/float)
for plain scalar slots.
"""

import pytest

from cimbuilder.core.units import Qty
from cimbuilder.dsl import records, validate


def _record(cim_class, fields, units=None, form='Table', line=1):
    return records.RawRecord(
        form=form, cim_class=cim_class, fields=fields, units=units or {},
        source_file='<test>', source_line=line,
    )


def test_unknown_class_raises_with_source_location():
    with pytest.raises(validate.CimtblValidationError, match=r'<test>:7: unknown CIM class .Nonexistent.'):
        validate.validate(_record('Nonexistent', {'name': 'x'}, line=7))


def test_unknown_column_suggests_closest_match():
    with pytest.raises(validate.CimtblValidationError, match=r"no attribute 'frequancy' - did you mean 'frequency'"):
        validate.validate(_record('BaseFrequency', {'name': 'x', 'frequancy': '60'}))


def test_object_form_scalar_fields():
    row = validate.validate(_record('BaseFrequency', {'name': 'base_freq', 'frequency': '60'}, form='Object'))
    assert row.name == 'base_freq'
    # frequency is a physical-quantity slot (§4.3) - always a Qty, even with
    # no unit on the .cimtbl column (blank unit string, not a bare float).
    assert row.frequency == Qty(60.0, '')


def test_quantity_slot_binds_qty_with_unit():
    row = validate.validate(
        _record('BasePower', {'name': 'sbase', 'basePower': '100'}, units={'basePower': 'MVA'}, form='Object')
    )
    assert row.basePower == Qty(100.0, 'MVA')


def test_quantity_slot_blank_cell_is_none():
    row = validate.validate(
        _record('EnergyConsumer', {
            'name': 'load_634', 'node': '634', 'p': None, 'q': None,
            'phaseConnection': 'Y', 'BaseVoltage': 'base_480', 'LoadResponse': 'zip_constantPQ',
        }, units={'p': 'kW', 'q': 'kVAr'})
    )
    assert row.p is None
    assert row.q is None


def test_fk_slot_passes_through_as_unresolved_string():
    row = validate.validate(
        _record('EnergyConsumerPhase', {
            'name': 'load_634a', 'phase': 'A', 'p': '160', 'q': '110', 'EnergyConsumer': 'load_634',
        }, units={'p': 'kW', 'q': 'kW'})
    )
    assert row.EnergyConsumer == 'load_634'
    assert isinstance(row.EnergyConsumer, str)


def test_integer_slot_is_native_int_not_str():
    row = validate.validate(
        _record('ACLineSegment', {
            'name': 'line_1_2', 'bus1': 'topo_bus_1', 'bus2': 'topo_bus_2', 'circuitNumber': '1',
            'r': '1.93800E-2', 'x': '5.91700E-2', 'bch': '0.05280', 'BaseVoltage': 'base_115',
        }, units={'r': 'pu', 'x': 'pu', 'bch': 'pu'})
    )
    assert row.circuitNumber == 1
    assert isinstance(row.circuitNumber, int)


def test_boolean_slot_is_native_bool_not_str():
    row = validate.validate(
        _record('Fuse', {
            'name': 'fuse_1', 'node1': '633', 'node2': 'XF1', 'ratedCurrent': '100.0',
            'open': 'false', 'normalOpen': 'false',
        }, units={'ratedCurrent': 'A'})
    )
    assert row.open is False
    assert row.normalOpen is False
    assert isinstance(row.open, bool)
    # regression guard: str(False) == 'False' is truthy - a stringified bool
    # would silently break every downstream `if row.open:` check.
    assert not row.open


def test_two_header_shapes_of_same_class_both_validate():
    by_sequence = validate.validate(
        _record('ACLineSegment', {
            'name': 'line_1_2', 'bus1': 'topo_bus_1', 'bus2': 'topo_bus_2', 'circuitNumber': '1',
            'r': '1.93800E-2', 'x': '5.91700E-2', 'bch': '0.05280', 'BaseVoltage': 'base_115',
        }, units={'r': 'pu', 'x': 'pu', 'bch': 'pu'})
    )
    by_per_length = validate.validate(
        _record('ACLineSegment', {
            'name': '650632', 'node1': 'RG60', 'node2': '362', 'phases': 'ABCN',
            'length': '2000', 'PerLengthImpedance': 'mtx601', 'BaseVoltage': 'base_4160',
        }, units={'length': 'ft'})
    )
    assert by_sequence.bus1 == 'topo_bus_1'
    assert by_sequence.node1 is None
    assert by_per_length.node1 == 'RG60'
    assert by_per_length.bus1 is None


def test_row_dataclass_is_cached_per_class():
    cls_a = validate._row_dataclass('BaseFrequencyRow', 'cimhub_2026')
    cls_b = validate._row_dataclass('BaseFrequencyRow', 'cimhub_2026')
    assert cls_a is cls_b


def test_comma_spec_merged_profile_validates(monkeypatch):
    # cim-graph's CIMG_CIM_PROFILE may be a comma-separated list of sub-profiles
    # merged at runtime; validation must resolve it through get_cim_profile()
    # (the same call that yields network.cim), not importlib on the raw string.
    from cimgraph.core.env_vars import get_cim_profile
    monkeypatch.setenv(
        'CIMG_CIM_PROFILE',
        'cimgraph.data_profile.cim18gmdm.connectivity,cimgraph.data_profile.cim18gmdm.electrical',
    )
    try:
        row = validate.validate(
            _record('BaseVoltage', {'name': 'bv', 'nominalVoltage': '115'}, units={'nominalVoltage': 'kV'}, form='Object')
        )
        assert row.nominalVoltage == Qty(115.0, 'kV')
        # regression guard: a field named like its type (BaseVoltage) must still
        # resolve to the class, not to its own None default.
        assert 'BaseVoltage' in validate.reference_slots('EnergyConsumerRow')
    finally:
        get_cim_profile.cache_clear()
