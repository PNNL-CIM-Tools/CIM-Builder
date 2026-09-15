"""Phase 1: Lark grammar -> records (design: CIMTBL_DESIGN.md §3, §12.1)."""

import os
from pathlib import Path

import lark

from cimbuilder.dsl.records import RawRecord

_GRAMMAR_PATH = Path(__file__).parent / 'grammar.lark'
_LARK_PARSER = lark.Lark(
    _GRAMMAR_PATH.read_text(),
    parser='lalr',
    propagate_positions=True,
)


def _cell_text(cell_node: lark.Tree) -> str | None:
    """A `cell` node is either `value` (one VALUE token, possibly with
    incidental leading/trailing whitespace the grammar doesn't strip) or
    `blank` (no token at all). Either way, empty-after-stripping = None
    (§12.1) - a lone space between two commas is indistinguishable in
    intent from no character at all."""
    if cell_node.data == 'blank':
        return None
    text = str(cell_node.children[0]).strip()
    return text or None


def _header_cell_name_unit_default(header_cell_node: lark.Tree) -> tuple[str, str | None, str | None]:
    """A header_cell is NAME unit? ("=" cell)? - unpack whichever of the two
    optional children are present by node type rather than position, since
    either, both, or neither may appear."""
    name = str(header_cell_node.children[0])
    unit: str | None = None
    default: str | None = None
    for child in header_cell_node.children[1:]:
        if child.data == 'unit':
            unit = str(child.children[0]).strip()
        else:
            default = _cell_text(child)
    return name, unit, default


class _RecordBuilder(lark.Transformer):
    """Parse tree -> flat list[RawRecord] (§12.1). Table statements expand
    to one RawRecord per data row, sharing that table's cim_class/units;
    Object statements become exactly one RawRecord. Import/Profile
    statements are handled by the driver functions below, not here - they
    never become RawRecords themselves."""

    def __init__(self, source_file: str):
        super().__init__()
        self.source_file = source_file

    def object_stmt(self, children: list) -> RawRecord:
        keyword_token, name_token, assignment_list = children
        fields: dict[str, str | None] = {}
        units: dict[str, str | None] = {}
        for assignment in assignment_list.children:
            name = str(assignment.children[0])
            has_unit = len(assignment.children) == 3
            unit = str(assignment.children[1].children[0]).strip() if has_unit else None
            cell_node = assignment.children[-1]
            fields[name] = _cell_text(cell_node)
            units[name] = unit
        return RawRecord(
            form='Object', cim_class=str(name_token), fields=fields, units=units,
            source_file=self.source_file, source_line=name_token.line,
        )

    def table_stmt(self, children: list) -> list[RawRecord]:
        keyword_token, name_token, header_list, *table_rows = children
        cim_class = str(name_token)

        columns: list[str] = []  # header order, for fields dict ordering
        row_columns: list[str] = []  # non-defaulted columns - always consume a row-cell position
        defaulted_columns: list[str] = []  # header order - a row may override in this order too
        units: dict[str, str | None] = {}
        constants: dict[str, str | None] = {}
        for header_cell in header_list.children:
            name, unit, default = _header_cell_name_unit_default(header_cell)
            columns.append(name)
            units[name] = unit
            has_default = len(header_cell.children) > 1 and header_cell.children[-1].data != 'unit'
            if has_default:
                constants[name] = default
                defaulted_columns.append(name)
            else:
                row_columns.append(name)

        # A row's cells fill row_columns first (positional, always present),
        # then any *extra* trailing cells fill defaulted_columns in header
        # order - letting a row override a subset of the header's defaults
        # (e.g. `load_sub`'s own EquipmentContainer cell in ieee13.cimtbl).
        records: list[RawRecord] = []
        for row in table_rows:
            cell_nodes = row.children
            row_values = {
                col: _cell_text(cell_nodes[i])
                for i, col in enumerate(row_columns) if i < len(cell_nodes)
            }
            overrides = {
                col: _cell_text(cell_nodes[len(row_columns) + i])
                for i, col in enumerate(defaulted_columns) if len(row_columns) + i < len(cell_nodes)
            }
            fields = {
                col: row_values[col] if col in row_values
                else overrides[col] if col in overrides
                else constants.get(col)
                for col in columns
            }
            records.append(RawRecord(
                form='Table', cim_class=cim_class, fields=fields, units=dict(units),
                source_file=self.source_file, source_line=row.meta.line,
            ))
        return records

def _ensure_trailing_newline(text: str) -> str:
    return text if text.endswith('\n') else text + '\n'


def parse_text(text: str, source_file: str) -> tuple[list[RawRecord], str | None]:
    """Parse `.cimtbl` source already in memory. Returns (records, profile)
    - `profile` is the file's own `Profile=` value (§3.9), or None if absent.
    Import statements are NOT resolved here (no filesystem access at this
    layer); use parse_file for a real file that may contain them."""
    tree = _LARK_PARSER.parse(_ensure_trailing_newline(text))

    profile: str | None = None
    statements: list[RawRecord | list[RawRecord] | tuple[str, str]] = []
    for statement in tree.children:
        node = statement.children[0]
        if node.data == 'profile_stmt':
            profile = str(node.children[1])
            continue
        if node.data == 'import_stmt':
            statements.append(('__import__', str(node.children[1])))
            continue
        statements.append(node)

    builder = _RecordBuilder(source_file)
    records: list[RawRecord] = []
    for item in statements:
        if isinstance(item, tuple):
            records.append(RawRecord(
                form='Table', cim_class='__import__', fields={'path': item[1]}, units={},
                source_file=source_file, source_line=0,
            ))
        else:
            built = builder.transform(item)
            if isinstance(built, list):
                records.extend(built)
            else:
                records.append(built)
    return records, profile


def parse_file(path: str | Path) -> tuple[list[RawRecord], str | None]:
    """The public Phase 1 entry point (§12.1): a .cimtbl file -> the fully-
    composed, ordered RawRecord list Phase 2 consumes, plus the active
    Profile (§3.9) if any statement in the file/Import chain set one.

    Import statements (§3.3) are resolved here by textual composition: each
    imported file is recursively parsed (relative to the importing file's
    directory) and its records spliced in at that position. Import records
    never reach the returned list themselves. Profile= is consumed before
    any RawRecord is built; one per file/Import chain (§3.9) - an imported
    file declaring a *different* Profile= than one already set earlier in
    the chain is a fail-fast error, not a silent override.
    """
    path = Path(path)
    text = path.read_text()
    raw_records, profile = parse_text(text, source_file=str(path))

    records: list[RawRecord] = []
    for record in raw_records:
        if record.cim_class == '__import__':
            import_path = path.parent / record.fields['path']
            imported_records, imported_profile = parse_file(import_path)
            records.extend(imported_records)
            if profile is None:
                profile = imported_profile
            elif imported_profile is not None and imported_profile != profile:
                raise ValueError(
                    f"Profile mismatch: {path} declares {profile!r} but "
                    f"import {import_path} declares {imported_profile!r}"
                )
            continue
        records.append(record)

    if profile is not None:
        os.environ['CIMG_CIM_PROFILE'] = profile

    return records, profile
