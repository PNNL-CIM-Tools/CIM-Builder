import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import sys


def sort_terminals_by_sequence(equipment: CN.ConductingEquipment):
    terminals_by_sequence = {
        terminal.sequenceNumber: terminal for terminal in equipment.Terminals
    }
    n = len(equipment.Terminals)
    if set(terminals_by_sequence) != set(range(1, n + 1)):
        raise ValueError(
            f"{equipment.mRID!r}: existing terminals need continuous sequenceNumbers from 1 to {n}, "
            f"got {[terminal.sequenceNumber for terminal in equipment.Terminals]}"
        )

    terminals = [terminals_by_sequence[i] for i in range(1, n + 1)]
    return terminals


def sort_terminals_by_node(
    equipment: CN.ConductingEquipment,
    node: str | CN.ConnectivityNode | CN.TopologicalNode,
) -> CN.Terminal | None:
    """Finds and returns the terminal of a piece of equipment connected to a specific node."""

    # Extract the mRID string if an object was passed
    if not isinstance(node, str):
        if hasattr(node, "mRID"):
            node = node.mRID  # type:ignore
        else:
            raise TypeError(
                f"{node} must be a string mRID, ConnectivityNode, or TopologicalNode"
            )

    # Find and return the matching terminal
    for terminal in equipment.Terminals:
        if (
            terminal.ConnectivityNode is not None
            and terminal.ConnectivityNode.mRID == node
        ):
            return terminal

    return None
