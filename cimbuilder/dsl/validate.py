"""Phase 2: pure-Python reflection validation gate (design: CIMTBL_DESIGN.md
§2.1, §12.2 - reflection on the live profile, no LinkML; see
development/PROFILE_RESOLUTION.md).

RawRecord (§12.1) -> <Class>Row (§12.2). Validation reflects directly on the
live CIM dataclass named by the record (resolved from whichever profile
Profile= selected, via cim-graph's own get_cim_profile()) instead of
constructing a generated LinkML class - any class in the selected profile is
automatically valid, with no per-version curation file to maintain. The only
columns a CIM profile can never explain are the DSL's own connectivity/phases/
Template shorthand (dsl/synthetic.py), which are added to every <Class>Row
unconditionally.

A field is classified the same way core/graph_write.py already classifies one
when writing to a live object: `metadata['serialize'] is False` marks a pure
reverse/derived association cimgraph itself never constructs from
(Measurements, Terminals, ...) - excluded entirely, never a column. Of the
rest, a field whose type union contains a CIMUnit subclass (Voltage,
ActivePower, ...) is a physical-quantity slot (§4.3) and becomes a Qty; a
field whose type union contains another CIM dataclass is a reference/FK slot
(§3.3) and stays an unresolved name string, exactly as before - resolving a
name into a live object is still Phase 4/5's job (NameIndex.get, §5.5), never
Phase 2's; everything else is a plain scalar, coerced from the record's raw
string with _coerce.
"""

import dataclasses
import difflib
import importlib
import os
import typing
from enum import Enum
from typing import Any

from cimgraph.core.env_vars import get_cim_profile
from cimgraph.data_profile.units.units import CIMUnit

from cimbuilder.core.units import Qty
from cimbuilder.dsl import records, synthetic

_row_dataclasses: dict[tuple[str, str], type] = {}
_SKIP_FIELDS = {'name', 'identifier'}


class CimtblValidationError(ValueError):
    """Fail-fast, profile-anchored validation error (§8 Phase 2 exit criterion)."""


class _FieldKind:
    SCALAR = 'scalar'
    QUANTITY = 'quantity'
    REFERENCE = 'reference'


def _qualify(path: str) -> str:
    return path if '.' in path else 'cimgraph.data_profile.' + path


def _cim_module(profile: str | None):
    """The CIM profile module for `profile`.

    The active profile (`profile` is None, or equals CIMG_CIM_PROFILE) is
    always resolved through cim-graph's get_cim_profile() - the same call that
    produces network.cim - so comma-spec merged profiles work and the module
    is the identical object. get_cim_profile() takes no argument and is
    @cache'd off the env var, so the cache is cleared when the env var has
    changed since it was filled (what cim-graph's own connections do).

    Only an explicit profile that differs from the env var (e.g. validating
    against 'cim17v40' while the env names another) is imported directly, as a
    single module name; that avoids mutating process-global state."""
    active = os.environ.get('CIMG_CIM_PROFILE')
    if profile is not None and profile != active:
        return importlib.import_module(_qualify(profile))
    if active is None:
        raise CimtblValidationError(
            'no CIM profile selected - set Profile= in the .cimtbl file or CIMG_CIM_PROFILE'
        )
    spec, module = get_cim_profile()
    if spec != active:
        get_cim_profile.cache_clear()
        _, module = get_cim_profile()
    return module


def _classify(hint: Any) -> tuple[str, type]:
    """A field's (_FieldKind, extra) from its resolved type hint - extra is
    the CIMUnit subclass for a quantity, the CIM dataclass for a reference,
    or the real scalar type (str/int/float/bool/an Enum subclass) otherwise."""
    args = typing.get_args(hint) or (hint,)
    real_args = [a for a in args if isinstance(a, type) and a is not type(None)]
    for arg in real_args:
        if issubclass(arg, CIMUnit):
            return _FieldKind.QUANTITY, arg
    for arg in real_args:
        if dataclasses.is_dataclass(arg):
            return _FieldKind.REFERENCE, arg
    return _FieldKind.SCALAR, (real_args[0] if real_args else str)


def _real_fields(cim_cls: type, cim_module) -> dict[str, tuple[str, type]]:
    """{field_name: (kind, extra)} for every column a .cimtbl row may set on
    this CIM class - every dataclass field except pure reverse/derived
    associations (serialize=False) and identity bookkeeping (name/identifier,
    handled separately)."""
    try:
        hints = typing.get_type_hints(cim_cls)
    except NameError:
        # A runtime-merged profile's classes live in cimgraph's merge module,
        # whose globals lack the names (Optional, the profile's own classes)
        # their annotations use - the resolved profile module has them all.
        # localns={} matters: left as None it defaults to the class's own
        # attributes, where a field named like its type (BaseVoltage = None)
        # would shadow the class it is annotated with.
        hints = typing.get_type_hints(
            cim_cls, globalns={**vars(typing), **vars(cim_module)}, localns={}
        )
    classified = {}
    for field in dataclasses.fields(cim_cls):
        if field.name in _SKIP_FIELDS or field.metadata.get('serialize') is False:
            continue
        classified[field.name] = _classify(hints[field.name])
    return classified


def reference_slots(row_cls_name: str, *, profile: str | None = None) -> set[str]:
    """Names of the class's FK slots - slots whose range is itself a CIM
    class (BaseVoltage, PerLengthImpedance, LoadResponse, ...) rather than a
    scalar type. These stay unresolved name strings at this phase (§3.3,
    §12.2) and must never reach the CIM class's own constructor.

    Public: Phase 4/5's generic bind_row (cimbuilder/core/binder.py) also
    uses this to tell an FK column apart from a plain scalar, with no
    per-class FK list to maintain."""
    cim_cls_name = row_cls_name.removesuffix('Row')
    cim_module = _cim_module(profile)
    cim_cls = getattr(cim_module, cim_cls_name)
    return {
        name for name, (kind, _) in _real_fields(cim_cls, cim_module).items()
        if kind == _FieldKind.REFERENCE
    }


def reference_target_class(row_cls_name: str, slot_name: str, *, profile: str | None = None) -> str:
    """The CIM class name a reference slot resolves against (e.g.
    'BaseVoltage', 'LoadResponseCharacteristic', 'EquipmentContainer') - what
    Phase 4/5 needs to call graph_write.resolve()/resolve_any_subclass()
    generically, with no per-class FK table to maintain."""
    cim_cls_name = row_cls_name.removesuffix('Row')
    cim_module = _cim_module(profile)
    cim_cls = getattr(cim_module, cim_cls_name)
    _, target_cls = _real_fields(cim_cls, cim_module)[slot_name]
    return target_cls.__name__


def _coerce(raw: str, py_type: type) -> Any:
    """record.fields values are always raw strings off the parser (§12.1) -
    this is the str->real-type coercion a generated LinkML class used to do
    for us."""
    if py_type is bool:
        return raw.strip().lower() in ('true', '1')
    if py_type in (int, float):
        return py_type(raw)
    if isinstance(py_type, type) and issubclass(py_type, Enum):
        return py_type(raw)
    return raw


def _row_dataclass(row_cls_name: str, profile: str) -> type:
    """The plain <Class>Row dataclass (§12.2), built once per (profile,
    class) from the live CIM dataclass's own fields plus the DSL's synthetic
    columns - reflects the real profile, so it can't drift from it."""
    key = (profile, row_cls_name)
    if key in _row_dataclasses:
        return _row_dataclasses[key]

    cim_cls_name = row_cls_name.removesuffix('Row')
    cim_module = _cim_module(profile)
    cim_cls = getattr(cim_module, cim_cls_name, None)
    if cim_cls is None:
        raise CimtblValidationError(
            f"unknown CIM class {cim_cls_name!r} (not in profile {profile!r})"
        )

    fields: list[tuple[str, Any, dataclasses.Field]] = [
        ('name', str, dataclasses.field()),
    ]
    for field_name, (kind, extra) in _real_fields(cim_cls, cim_module).items():
        if kind == _FieldKind.QUANTITY:
            field_type = Qty
        elif kind == _FieldKind.REFERENCE:
            field_type = str
        else:
            field_type = extra
        fields.append((field_name, field_type | None, dataclasses.field(default=None)))
    for col_name, col_type in synthetic.SYNTHETIC_COLUMNS.items():
        fields.append((col_name, col_type | None, dataclasses.field(default=None)))
    fields.append(('source_file', str, dataclasses.field(default='')))
    fields.append(('source_line', int, dataclasses.field(default=0)))

    row_cls = dataclasses.make_dataclass(row_cls_name, fields)
    _row_dataclasses[key] = row_cls
    return row_cls


def _closest_attribute_error(valid: list[str], bad_column: str, source_file: str, source_line: int, row_cls_name: str) -> CimtblValidationError:
    matches = difflib.get_close_matches(bad_column, valid, n=1)
    suggestion = f" - did you mean {matches[0]!r}?" if matches else ''
    return CimtblValidationError(
        f"{source_file}:{source_line}: {row_cls_name} has no attribute {bad_column!r}{suggestion}"
    )


def validate(record: records.RawRecord, *, profile: str | None = None) -> object:
    """RawRecord -> validated <Class>Row (§12.2), or raises CimtblValidationError."""
    profile = profile or os.environ.get('CIMG_CIM_PROFILE')
    row_cls_name = f'{record.cim_class}Row'
    cim_cls_name = record.cim_class
    cim_module = _cim_module(profile)
    cim_cls = getattr(cim_module, cim_cls_name, None)
    if cim_cls is None:
        raise CimtblValidationError(
            f"{record.source_file}:{record.source_line}: "
            f"unknown CIM class {record.cim_class!r} (not in profile {profile!r})"
        )

    real_fields = _real_fields(cim_cls, cim_module)
    valid_columns = {*real_fields, *synthetic.SYNTHETIC_COLUMNS, 'name'}

    for bad_column in record.fields:
        if bad_column not in valid_columns:
            raise _closest_attribute_error(
                sorted(valid_columns), bad_column, record.source_file, record.source_line, row_cls_name
            )

    row_cls = _row_dataclass(row_cls_name, profile)
    row_kwargs: dict[str, Any] = {
        'name': record.fields.get('name'),
        'source_file': record.source_file,
        'source_line': record.source_line,
    }

    for col_name in synthetic.SYNTHETIC_COLUMNS:
        row_kwargs[col_name] = record.fields.get(col_name)

    for field_name, (kind, extra) in real_fields.items():
        raw = record.fields.get(field_name)
        if raw is None:
            row_kwargs[field_name] = None
        elif kind == _FieldKind.REFERENCE:
            row_kwargs[field_name] = raw
        elif kind == _FieldKind.QUANTITY:
            try:
                row_kwargs[field_name] = Qty(float(raw), record.units.get(field_name) or '')
            except ValueError as exc:
                raise CimtblValidationError(
                    f"{record.source_file}:{record.source_line}: {field_name!r} expected a number, got {raw!r}"
                ) from exc
        else:
            try:
                row_kwargs[field_name] = _coerce(raw, extra)
            except ValueError as exc:
                raise CimtblValidationError(
                    f"{record.source_file}:{record.source_line}: {field_name!r}: {exc}"
                ) from exc

    return row_cls(**row_kwargs)
