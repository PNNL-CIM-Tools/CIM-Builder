"""Create CIM Analog measurements."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_analog(
    network: GraphModel,
    equipment: "cim.Equipment",
    terminal: "cim.Terminal",
    phase: "cim.PhaseCode",
    measurementType: str,
    name: str | None = None,
    *,
    check_duplicate: bool = True,
) -> "cim.Analog | None":
    """Create an Analog measurement on ``equipment``/``terminal`` and add it to ``network``.

    A duplicate-check is performed by default: if the equipment already has a
    measurement with the same terminal, phase and ``measurementType``, the
    existing measurement is returned and no new one is created.

    For ``measurementType='PNV'`` (phase-neutral voltage) on equipment that is
    NOT a load/PEC/shunt, the duplicate check looks across the
    ConnectivityNode's far terminals so multiple loads on the same bus share
    one PNV measurement.

    Args:
        network:            Graph model to add to.
        equipment:          Equipment that owns the measurement.
        terminal:           Terminal the measurement is sampled at.
        phase:              ``cim.PhaseCode`` for the measurement.
        measurementType:    CIM measurement-type tag (e.g. ``'VA'``, ``'PNV'``,
                            ``'SoC'``).
        name:               Optional human-readable name.  If None, a name is
                            generated from equipment / type / phase.
        check_duplicate:    Whether to skip creation when a duplicate exists.

    Returns:
        The created or existing Analog.
    """
    cim = get_cim()

    if measurementType == "PNV" and not isinstance(
        equipment,
        (cim.EnergyConsumer, cim.PowerElectronicsConnection, cim.LinearShuntCompensator),
    ):
        for far_terminal in terminal.ConnectivityNode.Terminals:
            for far_meas in far_terminal.Measurements:
                if far_meas.measurementType == "PNV":
                    return far_meas
    elif check_duplicate:
        for meas in equipment.Measurements:
            if (
                terminal.identifier == meas.Terminal.identifier
                and phase == meas.phases
                and measurementType == meas.measurementType
            ):
                return meas

    meas = cim.Analog()
    seed = f"{equipment.__class__.__name__}_{equipment.name}_{measurementType}"
    if measurementType != "SoC":
        seed += f"_{terminal.sequenceNumber}_{phase.value}"

    if name is not None:
        meas.uuid(name=seed + name)
        meas.name = name
    else:
        meas.uuid(name=seed)

    meas.Terminal = terminal
    meas.PowerSystemResource = equipment
    meas.measurementType = measurementType
    meas.phases = phase

    equipment.Measurements.append(meas)
    terminal.Measurements.append(meas)
    network.add_to_graph(meas)

    return meas


def create_all_analog(
    network: GraphModel,
    equipment: "cim.ConductingEquipment",
    measurementType: str,
) -> list:
    """Create one Analog measurement per terminal of ``equipment``.

    Returns the list of created measurements.
    """
    cim = get_cim()
    meas_list = []
    for counter, terminal in enumerate(equipment.Terminals, start=1):
        meas = cim.Analog(
            name=f"{equipment.__class__.__name__}_{equipment.name}_{measurementType}_{counter}",
        )
        meas.Terminal = terminal
        meas.PowerSystemResource = equipment
        meas.measurementType = measurementType
        equipment.Measurements.append(meas)
        terminal.Measurements.append(meas)
        network.add_to_graph(meas)
        meas_list.append(meas)
    return meas_list
