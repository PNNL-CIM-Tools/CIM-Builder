import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN


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
