"""BaseVoltage lookup / creation helper."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def get_or_create_base_voltage(
    network: GraphModel,
    base_voltage: "int | float | cim.BaseVoltage",
) -> "cim.BaseVoltage":
    """Return a BaseVoltage matching ``base_voltage``, creating one if needed.

    If ``base_voltage`` is already a ``cim.BaseVoltage`` it is returned as-is.

    If it is numeric, the network's existing BaseVoltage objects are searched
    for a match in either volts or kilovolts (a value of 115 matches an
    existing 115000 V BaseVoltage, and vice versa).  If no match is found, a
    new BaseVoltage is created with the numeric value stored as-given.

    Args:
        network:        GraphModel to search / add to.
        base_voltage:   Either a BaseVoltage object or a numeric voltage.

    Returns:
        A BaseVoltage object.
    """
    cim = get_cim()

    if isinstance(base_voltage, (int, float)):
        if cim.BaseVoltage in network.graph:
            network.get_all_attributes(cim.BaseVoltage)
            for bv in network.graph[cim.BaseVoltage].values():
                nominal = float(bv.nominalVoltage)
                if nominal == base_voltage or nominal == base_voltage * 1000:
                    return bv

        _log.info(
            "Could not find a BaseVoltage with nominalVoltage %s. Creating new object.",
            base_voltage,
        )
        bv = cim.BaseVoltage(name=f"BaseV_{base_voltage}", nominalVoltage=base_voltage)
        bv.uuid(name=f"BaseV_{base_voltage}")
        network.add_to_graph(bv)
        return bv

    return base_voltage
