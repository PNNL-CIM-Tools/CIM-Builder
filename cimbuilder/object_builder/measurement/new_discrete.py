"""Create CIM Discrete measurements."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_discrete(
    network: GraphModel,
    equipment: "cim.Equipment",
    terminal: "cim.ACDCTerminal",
    phase: "cim.PhaseCode",
    measurementType: str,
    *,
    mRID: str | None = None,
) -> "cim.Discrete | None":
    """Create a Discrete measurement on ``equipment``/``terminal``.

    Returns the existing measurement if a duplicate (same terminal/phase/type)
    is already present.

    Args:
        network:            Graph model to add to.
        equipment:          Equipment that owns the measurement.
        terminal:           Terminal the measurement is sampled at.
        phase:              ``cim.PhaseCode``.
        measurementType:    CIM measurement-type tag (e.g. ``'Pos'``).
        mRID:               Optional explicit mRID; otherwise UUID-seeded.

    Returns:
        The created or existing Discrete measurement.
    """
    cim = get_cim()

    for meas in equipment.Measurements:
        if (
            terminal.identifier == meas.Terminal.identifier
            and phase == meas.phases
            and measurementType == meas.measurementType
        ):
            return meas

    meas = cim.Discrete()
    seed = (
        f"{equipment.__class__.__name__}_{equipment.name}_{measurementType}_"
        f"{terminal.sequenceNumber}_{phase.value}"
    )
    meas.uuid(name=seed, mRID=mRID)
    meas.Terminal = terminal
    meas.PowerSystemResource = equipment
    meas.measurementType = measurementType
    meas.phases = phase

    equipment.Measurements.append(meas)
    terminal.Measurements.append(meas)
    network.add_to_graph(meas)

    return meas
