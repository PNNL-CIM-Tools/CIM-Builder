"""Create a CIM PowerTransformer (without ends — pair with new_power_transformer_end)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_power_transformer(
    network: GraphModel,
    container: "cim.EquipmentContainer",
    name: str,
    *,
    vector_group: str | None = None,
    is_part_of_generator_unit: bool | None = None,
    template: "cim.PowerTransformerInfo | None" = None,
) -> "cim.PowerTransformer":
    """Create a PowerTransformer shell and add it to ``network``.

    A PowerTransformer is the *container* for one PowerTransformerEnd per
    winding plus optional TransformerTanks.  After creating it, build each end
    with ``new_power_transformer_end`` and the composite builder
    ``new_tap_changing_transformer`` (Phase 2) chains the whole thing together.

    Args:
        network:                    Graph model to add to.
        container:                  EquipmentContainer.
        name:                       Human-readable name; seeds the UUID.
        vector_group:               Vector-group string (e.g. ``'Dyn1'``).
        is_part_of_generator_unit:  Whether this transformer is the GSU of a
                                    generating unit.
        template:                   Optional cimhub_2026 ``PowerTransformerInfo``
                                    to source nameplate data from.  Phase 6
                                    wiring; currently a no-op stub.

    Returns:
        The created ``cim.PowerTransformer``.  No terminals or ends are created
        yet — callers add them via ``new_power_transformer_end``.
    """
    cim = get_cim()

    if template is not None:
        _log.info(
            "PowerTransformer %r: template arg accepted but not yet consumed "
            "(Phase 6 will load nameplate from cim-asset-catalog).",
            name,
        )

    xfmr = cim.PowerTransformer(name=name)
    xfmr.uuid(name=name)
    xfmr.EquipmentContainer = container

    if vector_group is not None:
        xfmr.vectorGroup = vector_group
    if is_part_of_generator_unit is not None:
        xfmr.isPartOfGeneratorUnit = is_part_of_generator_unit

    network.add_to_graph(xfmr)
    return xfmr
