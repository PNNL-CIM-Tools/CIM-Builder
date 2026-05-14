"""Create or look up a CIM BaseVoltage."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_base_voltage(
    network: GraphModel,
    nominal_voltage_kV: float,
    name: str | None = None,
) -> "cim.BaseVoltage":
    """Create a BaseVoltage with the given nominal voltage and add it to ``network``.

    This always creates a new BaseVoltage object.  Use
    ``cimbuilder.utils.base_voltage.get_or_create_base_voltage`` if you want to
    reuse an existing matching BaseVoltage.

    Args:
        network:            Graph model to add to.
        nominal_voltage_kV: Nominal line-to-line voltage, in kV.
        name:               Optional name; defaults to ``"BaseV_<voltage>"``.

    Returns:
        The created ``cim.BaseVoltage``.
    """
    cim = get_cim()

    if name is None:
        name = f"BaseV_{nominal_voltage_kV}kV"

    bv = cim.BaseVoltage(name=name, nominalVoltage=cim.Voltage(nominal_voltage_kV, "kV"))
    bv.uuid(name=name)
    network.add_to_graph(bv)
    return bv
