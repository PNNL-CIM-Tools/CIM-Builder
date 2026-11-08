from cimtables.units import Qty

from cimbuilder.object_builder.topology import BusbarSectionBuilder, JuntionBuilder


def test_busbar_section_add_connectivity(network, container, base_voltage):
    builder = BusbarSectionBuilder(network=network, container=container)
    busbar = builder.create(mRID="bus1")

    busbar, terminal = builder.add_connectivity(
        busbar, node="bus1_node", BaseVoltage=base_voltage.mRID
    )
    assert terminal.ConductingEquipment is busbar


def test_busbar_section_add_short_circuit(network, container):
    builder = BusbarSectionBuilder(network=network, container=container)
    busbar = builder.create(mRID="bus1")

    builder.add_short_circuit(busbar, ipMax=Qty(40, "kA"))
    assert float(busbar.ipMax.to("kA")) == 40


def test_junction_builder_add_connectivity(network, container, base_voltage):
    """JuntionBuilder is a known misspelled Python class name
    (cim_class_name = "Junction" is correct - only the identifier itself
    is typo'd), left untouched per the typo-sweep scope."""
    builder = JuntionBuilder(network=network, container=container)
    junction = builder.create(mRID="j1")

    junction, terminal = builder.add_connectivity(
        junction, node="j1_node", BaseVoltage=base_voltage.mRID
    )
    assert terminal.ConductingEquipment is junction
