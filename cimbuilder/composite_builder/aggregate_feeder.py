"""Build an aggregate feeder representation (Feeder + load + BTM PV + FTM PV + head breaker)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from cimgraph.models import GraphModel

from cimbuilder._profile import get_cim
from cimbuilder.object_builder.load.new_energy_consumer import new_energy_consumer
from cimbuilder.composite_builder.feeder_head_breaker import new_feeder_head_breaker
from cimbuilder.composite_builder.btm_pv_unit import new_btm_pv_unit
from cimbuilder.composite_builder.ftm_pv_unit import new_ftm_pv_unit
from cimbuilder.composite_builder.wind_unit import new_wind_unit
from cimbuilder.object_builder.measurement.new_analog import new_analog

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim

_log = logging.getLogger(__name__)


def new_aggregate_feeder(
    network: GraphModel,
    feeder_name: str,
    breaker_name: str,
    substation: "cim.Substation",
    node: "cim.ConnectivityNode | str",
    base_voltage: "cim.BaseVoltage | float",
    total_load_kw: float = 0,
    total_load_kvar: float = 0,
    total_btm_pv_kw: float = 0,
    total_ftm_pv_kw: float = 0,
    total_btm_wind_kw: float = 0,
    total_ftm_wind_kw: float = 0,
    distributed: bool = True,
) -> "tuple[cim.Feeder, cim.EnergyConsumer, cim.Breaker]":
    """Create an aggregate feeder with load, BTM PV/wind, and FTM PV/wind.

    Backwards-compatible with the old ``feeder_builder.aggregate_feeder``
    signature — same positional args, same return value.

    Args:
        network:            Graph model to add to.
        feeder_name:        Name of the Feeder container.
        breaker_name:       Name of the head breaker.
        substation:         Parent Substation.
        node:               Substation-side ConnectivityNode (or name string).
        base_voltage:       BaseVoltage object or numeric kV/V value.
        total_load_kw:      Aggregate load, kW.
        total_load_kvar:    Aggregate load, kVAr.
        total_btm_pv_kw:    BTM PV nameplate, kW.
        total_ftm_pv_kw:    FTM PV nameplate, kW.
        total_btm_wind_kw:  BTM wind nameplate, kW.
        total_ftm_wind_kw:  FTM wind nameplate, kW.
        distributed:        Wrap feeder in ConnectivityArea for distributed scheduling.

    Returns:
        (feeder, load, breaker)
    """
    cim = get_cim()

    base_voltage_obj = _resolve_base_voltage(network, base_voltage, cim)

    # Feeder container
    feeder = cim.Feeder(name=feeder_name)
    feeder.uuid(name=feeder_name)
    feeder.NormalEnergizingSubstation = substation
    network.add_to_graph(feeder)

    # Head breaker + feeder-side node + optional FeederArea + measurements
    head = new_feeder_head_breaker(
        network, feeder, breaker_name,
        substation_node=node,
        base_voltage=base_voltage_obj,
        distributed=distributed,
        add_measurements=True,
    )
    breaker = head["breaker"]
    feeder_node = head["feeder_node"]
    feeder_area = head["feeder_area"]

    # Aggregate load
    load = new_energy_consumer(
        network, feeder, f"{feeder_name}_aggr_load", feeder_node,
        base_voltage=base_voltage_obj,
        p_kW=total_load_kw,
        q_kVAr=total_load_kvar,
    )
    if distributed and feeder_area is not None:
        load.SubSchedulingArea = feeder_area
    new_analog(
        network, equipment=load,
        terminal=load.Terminals[0],
        phase=cim.PhaseCode.ABC,
        measurementType="VA",
        name=f"GrossLoad(MW)_{feeder_name}",
        check_duplicate=False,
    )

    # BTM PV
    btm_pv_kw = total_btm_pv_kw + total_btm_wind_kw
    btm = new_btm_pv_unit(
        network, feeder, f"{feeder_name}_aggr_btm_pv", feeder_node,
        base_voltage=base_voltage_obj,
        p_kW=btm_pv_kw,
        max_p_kW=total_btm_pv_kw,
        add_measurements=True,
    )
    if distributed and feeder_area is not None:
        btm["pec"].SubSchedulingArea = feeder_area
        btm["pv_unit"].SubSchedulingArea = feeder_area

    # BTM wind (add to same PEC if present)
    if total_btm_wind_kw:
        wind_btm = _new_wind_unit_on_pec(
            network, btm["pec"], f"{feeder_name}_aggr_btm_wind",
            max_p_kW=total_btm_wind_kw, cim=cim,
        )
        if distributed and feeder_area is not None:
            wind_btm.SubSchedulingArea = feeder_area

    _update_analog_name(
        network, btm["pec"], f"BTMGeneration(MW)_{feeder_name}", cim,
    )

    # FTM PV
    ftm_pv_kw = total_ftm_pv_kw + total_ftm_wind_kw
    ftm = new_ftm_pv_unit(
        network, feeder, f"{feeder_name}_aggr_ftm_pv", feeder_node,
        base_voltage=base_voltage_obj,
        p_kW=ftm_pv_kw,
        max_p_kW=total_ftm_pv_kw,
        add_measurements=True,
    )
    if distributed and feeder_area is not None:
        ftm["pec"].SubSchedulingArea = feeder_area
        ftm["pv_unit"].SubSchedulingArea = feeder_area

    # FTM wind
    if total_ftm_wind_kw:
        wind_ftm = _new_wind_unit_on_pec(
            network, ftm["pec"], f"{feeder_name}_aggr_ftm_wind",
            max_p_kW=total_ftm_wind_kw, cim=cim,
        )
        if distributed and feeder_area is not None:
            wind_ftm.SubSchedulingArea = feeder_area

    _update_analog_name(
        network, ftm["pec"], f"FTMGeneration(MW)_{feeder_name}", cim,
    )

    return feeder, load, breaker


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _resolve_base_voltage(network: GraphModel, base_voltage, cim) -> "cim.BaseVoltage":
    """Accept BaseVoltage object or numeric value; return a BaseVoltage."""
    if isinstance(base_voltage, (int, float)):
        val = float(base_voltage)
        for bv in network.graph.get(cim.BaseVoltage, {}).values():
            bv_v = float(bv.nominalVoltage) if bv.nominalVoltage is not None else None
            if bv_v is not None and (bv_v == val or bv_v == val * 1000):
                return bv
        _log.warning("No BaseVoltage %s found; creating one.", base_voltage)
        bv_obj = cim.BaseVoltage(name=f"BaseV_{base_voltage}")
        bv_obj.uuid(name=f"BaseV_{base_voltage}")
        bv_obj.nominalVoltage = cim.Voltage(val, "V") if val > 1000 else cim.Voltage(val, "kV")
        network.add_to_graph(bv_obj)
        return bv_obj
    return base_voltage


def _new_wind_unit_on_pec(
    network: GraphModel,
    pec: "cim.PowerElectronicsConnection",
    name: str,
    *,
    max_p_kW: float | None,
    cim,
) -> "cim.PowerElectronicsWindUnit":
    """Attach a PowerElectronicsWindUnit directly to an existing PEC."""
    unit = cim.PowerElectronicsWindUnit(name=name)
    unit.uuid(name=name)
    unit.minP = cim.ActivePower(0.0, "kW")
    if max_p_kW is not None:
        unit.maxP = cim.ActivePower(max_p_kW, "kW")
    unit.PowerElectronicsConnection = pec
    pec.PowerElectronicsUnit.append(unit)
    network.add_to_graph(unit)
    return unit


def _update_analog_name(
    network: GraphModel,
    pec: "cim.PowerElectronicsConnection",
    new_name: str,
    cim,
) -> None:
    """Rename the most-recently-added VA Analog on ``pec`` to ``new_name``."""
    from cimbuilder._profile import get_cim as _get_cim
    cim_rt = _get_cim()
    for meas in network.graph.get(cim_rt.Analog, {}).values():
        if getattr(meas, "PowerSystemResource", None) is pec:
            if getattr(meas, "measurementType", None) == "VA":
                if meas.name and meas.name.endswith("_VA"):
                    meas.name = new_name
                    return
