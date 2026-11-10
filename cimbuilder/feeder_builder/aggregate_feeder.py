"""
An aggregate feeder: one breaker, one aggregate load and aggregate behind-the-meter (BTM) and
front-of-the-meter (FTM) inverters standing in for a whole distribution feeder in a transmission
model, with the feeder-head measurements a UFLS study reads.
"""

import cimprofiles.cim18.cim18v17 as cim
import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
from cimgraph.models import GraphModel
from cimtables.units import Qty

from cimbuilder.object_builder import (
    AnalogBuilder,
    BreakerBuilder,
    ConnectivityNodeBuilder,
    DiscreteBuilder,
    EnergyConsumerBuilder,
    FeederBuilder,
    PhotoVoltaicUnitBuilder,
    PowerElectronicsConnectionBuilder,
    PowerElectronicsWindUnitBuilder,
)
from cimbuilder.object_builder.measurement.analog import THREE_PHASE_ACTIVE_POWER
from cimbuilder.object_builder.measurement.discrete import switch_position
from cimbuilder.object_builder.measurement.measurement import (
    MeasurementBuilder,
    MeasurementKind,
)

mRID = str


def new_aggregate_feeder(
    network: GraphModel,
    *,
    mRID: str,
    name: str | None = None,
    breaker_name: str | None = None,
    NormalEnergizingSubstation: mRID,
    node: mRID,
    BaseVoltage: mRID,
    load_p: float | Qty = 0.0,
    load_q: float | Qty = 0.0,
    btm_pv_p: float | Qty = 0.0,
    btm_wind_p: float | Qty = 0.0,
    ftm_pv_p: float | Qty = 0.0,
    ftm_wind_p: float | Qty = 0.0,
) -> tuple[CN.Feeder, CN.EnergyConsumer, CN.Breaker]:
    """
    Adds an aggregate feeder below node, returning the Feeder, its aggregate load and head breaker.
    Child mRIDs are prefixed by the feeder mRID, e.g. <mRID>_brk, <mRID>_load.
    * mRID: string identifier of the Feeder
    * name: human-readable name of the Feeder, used as prefix of the measurement names; default mRID
    * breaker_name: human-readable name of the head breaker; default <name>_brk
    * NormalEnergizingSubstation: mRID of the Substation feeding this feeder
    * node: mRID of the existing substation ConnectivityNode the head breaker connects to
    * BaseVoltage: mRID string of the BaseVoltage of the feeder
    * load_p, load_q: total load, float in W/VAr or Qty('MW')/Qty('MVAr')
    * btm_pv_p, btm_wind_p: total behind-the-meter PV and wind, float in W or Qty('MW')
    * ftm_pv_p, ftm_wind_p: total front-of-the-meter PV and wind, float in W or Qty('MW')
    """
    name = name or mRID

    feeder_builder = FeederBuilder(network, network.container)
    feeder: CN.Feeder = feeder_builder.create(mRID=mRID, name=name)  # type: ignore

    node_builder = ConnectivityNodeBuilder(network, feeder)
    feeder_node = node_builder.create(mRID=f"{mRID}_node_1", name=f"{name}_node_1")
    node_builder.add_connectivity(feeder_node, BaseVoltage=BaseVoltage)  # type: ignore

    breaker_builder = BreakerBuilder(network, feeder)
    breaker: CN.Breaker = breaker_builder.create(
        mRID=f"{mRID}_brk", name=breaker_name or f"{name}_brk"
    )  # type: ignore
    _, breaker_terminals, _ = breaker_builder.add_connectivity(
        breaker, node1=node, node2=feeder_node.mRID, BaseVoltage=BaseVoltage  # type: ignore
    )
    head_terminal = breaker_terminals[1]
    feeder_builder.add_connectivity(
        feeder,
        NormalEnergizingSubstation=NormalEnergizingSubstation,
        NormalHeadTerminal=head_terminal.mRID,
    )

    load_builder = EnergyConsumerBuilder(network, feeder)
    load: CN.EnergyConsumer = load_builder.create(mRID=f"{mRID}_load", name=f"{name}_aggr_load")  # type: ignore
    _, load_terminal, _ = load_builder.add_connectivity(
        load, node=feeder_node.mRID, aggregate=True, BaseVoltage=BaseVoltage  # type: ignore
    )
    load_builder.add_ssh(load, p=load_p, q=load_q)

    btm_inverter, btm_terminal = _add_aggregate_inverter(
        network, feeder, mRID=f"{mRID}_btm", name=f"{name}_aggr_btm", node=feeder_node.mRID,
        BaseVoltage=BaseVoltage, pv_p=btm_pv_p, wind_p=btm_wind_p,
    )
    ftm_inverter, ftm_terminal = _add_aggregate_inverter(
        network, feeder, mRID=f"{mRID}_ftm", name=f"{name}_aggr_ftm", node=feeder_node.mRID,
        BaseVoltage=BaseVoltage, pv_p=ftm_pv_p, wind_p=ftm_wind_p,
    )

    # Feeder-head measurements, named as the GridAPPS-D UFLS application expects
    discrete_builder = DiscreteBuilder(network, feeder)
    analog_builder = AnalogBuilder(network, feeder)
    _add_measurement(
        discrete_builder, switch_position("XCBR"), mRID=f"{mRID}_brk_pos",
        name=f"Pos_{name}", resource=breaker, terminal=head_terminal,
    )
    for suffix, label, resource, terminal in [
        ("net_load", "NetLoad(MW)", breaker, head_terminal),
        ("excess_generation", "ExcessGeneration(MW)", breaker, head_terminal),
        ("total_generation", "TotalGeneration(MW)", breaker, head_terminal),
        ("gross_load", "GrossLoad(MW)", load, load_terminal),
        ("btm_generation", "BTMGeneration(MW)", btm_inverter, btm_terminal),
        ("ftm_generation", "FTMGeneration(MW)", ftm_inverter, ftm_terminal),
    ]:
        _add_measurement(
            analog_builder, THREE_PHASE_ACTIVE_POWER, mRID=f"{mRID}_{suffix}",
            name=f"{label}_{name}", resource=resource, terminal=terminal,
        )

    return feeder, load, breaker


def _add_aggregate_inverter(
    network: GraphModel,
    feeder: CN.Feeder,
    *,
    mRID: str,
    name: str,
    node: mRID,
    BaseVoltage: mRID,
    pv_p: float | Qty,
    wind_p: float | Qty,
) -> tuple[CN.PowerElectronicsConnection, CN.Terminal]:
    """An aggregate inverter with a PV unit, and a wind unit if wind_p is not zero"""
    inverter_builder = PowerElectronicsConnectionBuilder(network, feeder)
    inverter: CN.PowerElectronicsConnection = inverter_builder.create(mRID=mRID, name=name)  # type: ignore
    _, terminal, _ = inverter_builder.add_connectivity(
        inverter, node=node, aggregate=True, BaseVoltage=BaseVoltage
    )
    inverter_builder.add_ssh(inverter, p=_watts(pv_p) + _watts(wind_p), q=0.0)

    pv_builder = PhotoVoltaicUnitBuilder(network, feeder)
    pv_unit = pv_builder.create(mRID=f"{mRID}_pv", name=f"{name}_pv")
    pv_builder.add_electrical(
        pv_unit, minP=0.0, maxP=pv_p, aggregate=True, PowerElectronicsConnection=mRID  # type: ignore
    )
    if _watts(wind_p) != 0:
        wind_builder = PowerElectronicsWindUnitBuilder(network, feeder)
        wind_unit = wind_builder.create(mRID=f"{mRID}_wind", name=f"{name}_wind")
        wind_builder.add_electrical(
            wind_unit, minP=0.0, maxP=wind_p, aggregate=True, PowerElectronicsConnection=mRID  # type: ignore
        )
    return inverter, terminal


def _add_measurement(
    builder: MeasurementBuilder,
    kind: MeasurementKind,
    *,
    mRID: str,
    name: str,
    resource: CN.PowerSystemResource,
    terminal: CN.Terminal,
) -> None:
    """One three-phase (ABC) measurement of kind, with the IEC 61850 name as description"""
    measurement = builder.create(mRID=mRID, name=name, description=kind.iec61850_name(None))
    builder.add_measurement(
        measurement,  # type: ignore
        measurementType=kind.measurementType,
        PowerSystemResource=resource.mRID,
        Terminal=terminal.mRID,
        phases="ABC",
        unitSymbol=kind.unitSymbol,
    )


def _watts(power: float | Qty) -> float:
    """power in W, a float is already W"""
    if isinstance(power, Qty):
        return float(cim.ActivePower(power.value, power.unit).to("W"))
    return float(power)
