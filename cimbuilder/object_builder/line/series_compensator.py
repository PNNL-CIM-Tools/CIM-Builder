import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.short_circuit as SC
from cimtables import Qty, connectivity, graph_write

from cimbuilder.core.sort_terminals import sort_terminals_by_sequence
from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str


class SeriesCompensatorBuilder(ObjectBuilder):
    """
    Builder for a series reactor or capacitor (OpenDSS series Reactor, GDM DistributionReactor). Builder functions to
    be called in the following order:
    * create() - instantiate the compensator, e.g. rx_<name>
    * add_connectivity() - two terminals, phasing, base voltage
    * add_electrical() - positive sequence r, x
    * add_short_circuit() - zero sequence r0, x0
    SeriesCompensator has no per-phase class, so its phases live on its Terminals only.
    """

    cim_class_name = "SeriesCompensator"

    def add_connectivity(
        self,
        compensator: CN.SeriesCompensator,
        *,
        node1: mRID,
        node2: mRID,
        phases: str | None = None,
        EquipmentContainer: mRID | None = None,
        BaseVoltage: mRID,
    ) -> tuple[CN.SeriesCompensator, list[CN.Terminal]]:
        """
        Adds connectivity_unbalanced profile layer: terminals/nodes, phasing, base voltage
        * node1: mRID of the "from" ConnectivityNode or TopologicalNode
        * node2: mRID of the "to" ConnectivityNode or TopologicalNode
        * phases: phase string on both Terminals (e.g. 'B'); None (balanced ABC) writes no Terminal phases
        * EquipmentContainer: mRID of the VoltageLevel or Feeder containing the compensator
        * BaseVoltage: mRID string of the BaseVoltage
        """
        cn: CN = self.cim  # type: ignore

        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=compensator,
            profile_part=CN,
            association_name="EquipmentContainer",
            target_class=cn.EquipmentContainer,
            target_mRID=EquipmentContainer if EquipmentContainer is not None else self.container.mRID,
        )

        if len(compensator.Terminals) != 2:
            terminals = connectivity.add_connectivity(
                network=self.network,
                equipment=compensator,
                node_cols={"node1": node1, "node2": node2},
                equipment_container=compensator.EquipmentContainer,
            )
        else:
            terminals = sort_terminals_by_sequence(compensator)

        if phases is not None:
            code = cn.PhaseCode(connectivity.phase_code(connectivity.parse_phases(phases)))
            for terminal in terminals:
                graph_write.set_attr(terminal, CN, "phases", code)

        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=compensator,
            profile_part=CN,
            association_name="BaseVoltage",
            target_class=cn.BaseVoltage,
            target_mRID=BaseVoltage,
        )
        return compensator, terminals

    def add_electrical(
        self,
        compensator: EL_BAL.SeriesCompensator,
        *,
        r: float | Qty | None = None,
        x: float | Qty | None = None,
    ) -> EL_BAL.SeriesCompensator:
        """
        Adds positive sequence impedance values:
        * r: positive sequence resistance, float in ohm or Qty('ohm'|'pu')
        * x: positive sequence reactance, float in ohm or Qty('ohm'|'pu')
        """
        graph_write.set_attr(compensator, EL_BAL, "r", r, system_base=self.network.base_power)
        graph_write.set_attr(compensator, EL_BAL, "x", x, system_base=self.network.base_power)
        return compensator

    def add_short_circuit(
        self,
        compensator: SC.SeriesCompensator,
        *,
        r0: float | Qty | None = None,
        x0: float | Qty | None = None,
    ) -> SC.SeriesCompensator:
        """
        Adds zero sequence impedance values:
        * r0: zero sequence resistance, float in ohm or Qty('ohm'|'pu')
        * x0: zero sequence reactance, float in ohm or Qty('ohm'|'pu')
        """
        graph_write.set_attr(compensator, SC, "r0", r0, system_base=self.network.base_power)
        graph_write.set_attr(compensator, SC, "x0", x0, system_base=self.network.base_power)
        return compensator
