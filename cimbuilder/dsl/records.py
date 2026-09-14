"""Phase 1: intermediate record dataclasses (design: CIMTBL_DESIGN.md §12.1)."""

from dataclasses import dataclass
from typing import Literal


@dataclass
class RawRecord:
    """One Object/Table row, straight off the grammar. Every cell is still a
    str (or None for a blank cell) - no CIM knowledge, no coercion. Phase 2
    is the only consumer."""

    form: Literal['Object', 'Table']
    cim_class: str
    fields: dict[str, str | None]
    units: dict[str, str | None]
    source_file: str
    source_line: int
