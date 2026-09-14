"""Phase 2: LinkML validation gate (design: CIMTBL_DESIGN.md §2.1, §12.2).

RawRecord (§12.1) -> <Class>Row (§12.2). The generated LinkML class
(schema/generated/main.py) does the real validation: required fields,
str->float/int coercion, and rejecting unknown columns. This module wraps
that with a fail-fast, profile-anchored error message (naming the closest
valid attribute on an unknown column, per §8's Phase 2 exit criterion) and
unwraps the validated instance into the plain <Class>Row dataclass pinned by
§12.2 - binding every physical-quantity field (§4.3: a named float-based type
like Voltage/ActivePower/ResistancePerLength, not bare `float` itself) into a
Qty using the record's units (§3.2), which the LinkML schema itself does not
carry.

FK slots (BaseVoltage, PerLengthImpedance, LoadResponse, ...) keep the real
cimhub_2026 class's own object-valued range (rows.yaml does not narrow
them) so `is_a` composition preserves the full real CIM attribute set. That
means they can't be passed into the generated LinkML class's constructor -
its dataclass inheritance chain would try to build a live object out of the
raw name string and crash (see rows.yaml's description for the exact
mechanism). So reference slots are excluded before construction and their
raw string value is spliced into the output row unchanged - resolving a
name into a live object is Phase 4/5's job (NameIndex.get, §5.5), never
Phase 2's. Per design intent, an FK's string value is not otherwise
validated here; if it's malformed, that's a Phase 4/5 resolution error.
"""

import dataclasses
import difflib
from pathlib import Path
from typing import Any

from linkml_runtime.utils.schemaview import SchemaView

from cimbuilder.core.units import Qty
from cimbuilder.dsl import records
from cimbuilder.dsl.schema.generated import main as generated

_SCHEMA_PATH = Path(__file__).parent / 'schema' / 'main.yaml'
_schema_view = SchemaView(str(_SCHEMA_PATH))

_row_dataclasses: dict[str, type] = {}


class CimtblValidationError(ValueError):
    """Fail-fast, profile-anchored validation error (§8 Phase 2 exit criterion)."""


def _is_quantity_range(range_name: str | None) -> bool:
    """True for a physical-quantity type (Voltage, ActivePower, ResistancePerLength,
    ...) - a named type whose base is float, but not the bare `float` type itself
    (dimensionless values like ZIP coefficients stay plain floats, not Qty)."""
    if range_name is None or range_name == 'float':
        return False
    range_type = _schema_view.get_type(range_name)
    return range_type is not None and range_type.base == 'float'


def _quantity_slots(row_cls_name: str) -> set[str]:
    """Names of the class's physical-quantity slots (§4.3) - every one may
    carry a unit suffix on its .cimtbl column header and is bound into a Qty."""
    return {
        slot_name
        for slot_name in _schema_view.class_slots(row_cls_name)
        if _is_quantity_range(_schema_view.induced_slot(slot_name, row_cls_name).range)
    }


def _reference_slots(row_cls_name: str) -> set[str]:
    """Names of the class's FK slots - slots whose range is itself a CIM
    class (BaseVoltage, PerLengthImpedance, LoadResponse, ...) rather than a
    scalar type. These stay unresolved name strings at this phase (§3.3,
    §12.2) and must never reach the generated LinkML class's constructor."""
    return {
        slot_name
        for slot_name in _schema_view.class_slots(row_cls_name)
        if _schema_view.get_class(_schema_view.induced_slot(slot_name, row_cls_name).range) is not None
    }


_LINKML_BASE_TO_PYTHON: dict[str, type] = {
    'int': int,
    'float': float,
    'bool': bool,
    'str': str,
}


def _slot_python_type(row_cls_name: str, slot_name: str) -> type:
    """The plain Python type a non-reference, non-quantity slot's value
    holds at runtime (§12.2: "already the correct Python type"). The
    generated LinkML class does the str->int/float/bool coercion already
    (Bool.__new__ and friends return a plain bool/int/float, not a wrapper);
    this only mirrors that in the <Class>Row dataclass's own annotation."""
    range_name = _schema_view.induced_slot(slot_name, row_cls_name).range
    range_type = _schema_view.get_type(range_name) if range_name else None
    base = range_type.base if range_type else None
    return _LINKML_BASE_TO_PYTHON.get(base, str)


def _row_dataclass(row_cls_name: str) -> type:
    """The plain <Class>Row dataclass (§12.2), built once per class from the
    LinkML schema's slots - float slots become Qty | None, everything else
    keeps its schema range. Generated, not hand-written, so it can't drift
    from the schema (§10 open question #1)."""
    if row_cls_name in _row_dataclasses:
        return _row_dataclasses[row_cls_name]

    quantity_slots = _quantity_slots(row_cls_name)
    fields: list[tuple[str, Any, dataclasses.Field]] = [
        ('name', str, dataclasses.field()),
    ]
    for slot_name in _schema_view.class_slots(row_cls_name):
        if slot_name == 'name':
            continue
        if slot_name in quantity_slots:
            field_type = Qty
        else:
            field_type = _slot_python_type(row_cls_name, slot_name)
        fields.append((slot_name, field_type | None, dataclasses.field(default=None)))
    fields.append(('source_file', str, dataclasses.field(default='')))
    fields.append(('source_line', int, dataclasses.field(default=0)))

    row_cls = dataclasses.make_dataclass(row_cls_name, fields)
    _row_dataclasses[row_cls_name] = row_cls
    return row_cls


def _closest_attribute_error(row_cls_name: str, bad_column: str, source_file: str, source_line: int) -> CimtblValidationError:
    valid = list(_schema_view.class_slots(row_cls_name))
    matches = difflib.get_close_matches(bad_column, valid, n=1)
    suggestion = f" - did you mean {matches[0]!r}?" if matches else ''
    return CimtblValidationError(
        f"{source_file}:{source_line}: {row_cls_name} has no attribute {bad_column!r}{suggestion}"
    )


def validate(record: records.RawRecord) -> object:
    """RawRecord -> validated <Class>Row (§12.2), or raises CimtblValidationError."""
    row_cls_name = f'{record.cim_class}Row'
    if not hasattr(generated, row_cls_name):
        raise CimtblValidationError(
            f"{record.source_file}:{record.source_line}: "
            f"unknown CIM class {record.cim_class!r} (not in the cimtbl schema)"
        )
    linkml_cls = getattr(generated, row_cls_name)
    reference_slots = _reference_slots(row_cls_name)
    construct_fields = {k: v for k, v in record.fields.items() if k not in reference_slots}

    try:
        validated = linkml_cls(**construct_fields)
    except TypeError as exc:
        message = str(exc)
        marker = 'unexpected keyword argument '
        if marker in message:
            bad_column = message.split(marker, 1)[1].strip("'")
            raise _closest_attribute_error(
                row_cls_name, bad_column, record.source_file, record.source_line
            ) from exc
        raise CimtblValidationError(f"{record.source_file}:{record.source_line}: {message}") from exc
    except ValueError as exc:
        raise CimtblValidationError(f"{record.source_file}:{record.source_line}: {exc}") from exc

    row_cls = _row_dataclass(row_cls_name)
    quantity_slots = _quantity_slots(row_cls_name)
    row_kwargs: dict[str, Any] = {'source_file': record.source_file, 'source_line': record.source_line}
    for slot_name in _schema_view.class_slots(row_cls_name):
        if slot_name in reference_slots:
            row_kwargs[slot_name] = record.fields.get(slot_name)
            continue
        value = getattr(validated, slot_name)
        if value is None:
            row_kwargs[slot_name] = None
        elif slot_name in quantity_slots:
            row_kwargs[slot_name] = Qty(float(value), record.units.get(slot_name) or '')
        else:
            row_kwargs[slot_name] = value

    return row_cls(**row_kwargs)
