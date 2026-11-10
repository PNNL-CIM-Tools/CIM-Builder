import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.short_circuit as SC
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import Qty, connectivity, graph_write

from cimbuilder.core.sort_terminals import sort_terminals_by_sequence
from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class EnergySourceBuilder(ObjectBuilder):
    """
    Builder for voltage sources, e.g. the substation equivalent at the head of a feeder.
    Builder functions to be called in the following order:
    * create() - instantiate the EnergySource, e.g. src_<name>
    * add_connectivity() - Terminal, phases, nominal voltage and BaseVoltage
    * add_electrical() - positive sequence source impedance
    * add_short_circuit() - zero and negative sequence source impedance
    * add_ssh() - voltage magnitude and angle
    """

    cim_class_name = "EnergySource"

    def add_connectivity(
        self,
        source: CN.EnergySource,
        *,
        node: mRID,
        nominalVoltage: float | Qty,
        phases: str | None = None,
        grounded: bool | None = None,
        EquipmentContainer: mRID | None = None,
        BaseVoltage: mRID,
    ) -> tuple[CN.EnergySource, CN.Terminal, list[CN.EnergySourcePhase]]:
        """
        Adds base connectivity layer of terminals, base voltage, phasing
        * node: mRID of the ConnectivityNode or TopologicalNode
        * nominalVoltage: phase-to-phase nominal voltage, float in V or Qty('kV')
        * phases: phase-code string in conductor order (e.g. ABC). None sets no EnergySourcePhase objects
        * grounded: boolean, source is grounded if true
        * EquipmentContainer: mRID of the VoltageLevel or Feeder containing the source.
        * BaseVoltage: mRID string of the BaseVoltage
        """
        cn: CN = self.cim  # type: ignore

        graph_write.set_attr(source, CN, "nominalVoltage", nominalVoltage)
        graph_write.set_attr(source, CN, "grounded", grounded)

        if EquipmentContainer is None:
            EquipmentContainer = self.container.mRID
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=source,
            profile_part=CN,
            association_name="EquipmentContainer",
            target_class=cn.EquipmentContainer,
            target_mRID=EquipmentContainer,
        )

        if len(source.Terminals) != 1:
            terminals = connectivity.add_connectivity(
                network=self.network,
                equipment=source,
                node_cols={"node": node},
                equipment_container=source.EquipmentContainer,
            )
        else:
            terminals = sort_terminals_by_sequence(source)

        if phases is not None:
            connectivity.add_phase_children(self.network, source, terminals, phases=phases)

        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=source,
            profile_part=CN,
            association_name="BaseVoltage",
            target_class=cn.BaseVoltage,
            target_mRID=BaseVoltage,
        )
        return source, terminals[0], source.EnergySourcePhase

    def add_electrical(
        self,
        source: EL_BAL.EnergySource,
        *,
        r: float | Qty | None = None,
        x: float | Qty | None = None,
        pMax: float | Qty | None = None,
        pMin: float | Qty | None = None,
    ) -> EL_BAL.EnergySource:
        """
        Adds positive sequence Thevenin impedance
        * r: positive sequence resistance, float in ohm or Qty('ohm'|'pu') or Qty('pu', base='system')
        * x: positive sequence reactance, float in ohm or Qty('ohm'|'pu') or Qty('pu', base='system')
        * pMax: maximum active power, float in W or Qty('kW'|'MW')
        * pMin: minimum active power, float in W or Qty('kW'|'MW')
        """
        graph_write.set_attr(source, EL_BAL, "r", r, system_base=self.network.base_power)
        graph_write.set_attr(source, EL_BAL, "x", x, system_base=self.network.base_power)
        graph_write.set_attr(source, EL_BAL, "pMax", pMax)
        graph_write.set_attr(source, EL_BAL, "pMin", pMin)
        return source

    def add_short_circuit(
        self,
        source: SC.EnergySource,
        *,
        r0: float | Qty | None = None,
        x0: float | Qty | None = None,
        r2: float | Qty | None = None,
        x2: float | Qty | None = None,
    ) -> SC.EnergySource:
        """
        Adds zero and negative sequence Thevenin impedance
        * r0: zero sequence resistance, float in ohm or Qty('ohm'|'pu') or Qty('pu', base='system')
        * x0: zero sequence reactance, float in ohm or Qty('ohm'|'pu') or Qty('pu', base='system')
        * r2: negative sequence resistance, float in ohm or Qty('ohm'|'pu') or Qty('pu', base='system')
        * x2: negative sequence reactance, float in ohm or Qty('ohm'|'pu') or Qty('pu', base='system')
        """
        graph_write.set_attr(source, SC, "r0", r0, system_base=self.network.base_power)
        graph_write.set_attr(source, SC, "x0", x0, system_base=self.network.base_power)
        graph_write.set_attr(source, SC, "r2", r2, system_base=self.network.base_power)
        graph_write.set_attr(source, SC, "x2", x2, system_base=self.network.base_power)
        return source

    def add_ssh(
        self,
        source: SSH.EnergySource,
        *,
        voltageMagnitude: float | Qty | None = None,
        voltageAngle: float | Qty | None = None,
        activePower: float | Qty | None = None,
        reactivePower: float | Qty | None = None,
    ) -> SSH.EnergySource:
        """
        Adds the source setpoint from measurement or basecase.
        Use load sign convention (positive = flow out of node)
        * voltageMagnitude: phase-to-phase voltage magnitude, float in V or Qty('kV')
        * voltageAngle: voltage angle, float in radians or Qty('deg')
        * activePower: active power injection, float in W or Qty('kW'|'MW')
        * reactivePower: reactive power injection, float in VAr or Qty('kVAr'|'MVAr')
        """
        graph_write.set_attr(source, SSH, "voltageMagnitude", voltageMagnitude)
        graph_write.set_attr(source, SSH, "voltageAngle", voltageAngle)
        graph_write.set_attr(source, SSH, "activePower", activePower)
        graph_write.set_attr(source, SSH, "reactivePower", reactivePower)
        return source
