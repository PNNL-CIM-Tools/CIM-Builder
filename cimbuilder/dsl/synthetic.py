"""DSL-only columns that are not real CIM attributes under any profile
(design: CIMTBL_DESIGN.md §3.5-§3.7) - connectivity shorthand, the phases
compound string, and the Template FK. Fixed regardless of which CIM version
Profile= selects; every other column is resolved by reflecting on the live
profile module (dsl/validate.py) instead of a curated allowlist."""

SYNTHETIC_COLUMNS: dict[str, type] = {
    'node': str, 'node1': str, 'node2': str,
    'bus1': str, 'bus2': str,
    'phases': str,
    'Template': str,
}


def is_connectivity_column(name: str) -> bool:
    """§3.5's naming rule: node* -> ConnectivityNode, bus* -> TopologicalNode."""
    return name.startswith('node') or name.startswith('bus')
