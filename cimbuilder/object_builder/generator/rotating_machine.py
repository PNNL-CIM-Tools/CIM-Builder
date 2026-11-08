from abc import ABC

import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.short_circuit as SC
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import Qty, connectivity, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class RotatingMachineBuilder(ObjectBuilder, ABC):
    cim_class_name = "RotatingMachine"

    def add_connectivity(
        self,
        machine: CN.RotatingMachine,
        *,
        node: str,
        EquipmentContainer: str | None = None,
        BaseVoltage: str,
    ) -> tuple[CN.RotatingMachine, CN.Terminal]:
        """
        Adds base connectivity layer of terminals, base voltage, phasing
        * node: mRID of the ConnectivityNode or TopologicalNode
        * EquipmentContainer: mRID of the VoltageLevel or Feeder containing the machine.
        * BaseVoltage: mRID string of the BaseVoltage
        """
        cn: CN = self.cim  # type: ignore

        if EquipmentContainer is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=machine,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=EquipmentContainer,
            )
        else:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=machine,
                profile_part=CN,
                association_name="EquipmentContainer",
                target_class=cn.EquipmentContainer,
                target_mRID=self.container.mRID,
            )

        if len(machine.Terminals) != 1:
            terminals = connectivity.add_connectivity(
                network=self.network,
                equipment=machine,
                node_cols={"node": node},
                equipment_container=machine.EquipmentContainer,
            )

        if BaseVoltage is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=machine,
                profile_part=CN,
                association_name="BaseVoltage",
                target_class=cn.BaseVoltage,
                target_mRID=BaseVoltage,
            )
        return machine, terminals[0]

    def add_electrical(
        self,
        machine: EL_BAL.RotatingMachine,
        *,
        ratedS: float | Qty | None = None,
    ) -> EL_BAL.RotatingMachine:
        """Adds electrical_balanced.RotatingMachine's fixed-machine parameters.
        * ratedS: nameplate apparent power rating, float in VAr or Qty('kVAr'|'MVAr')
        """

        graph_write.set_attr(machine, EL_BAL, "ratedS", ratedS)
        return machine

    def add_ssh(
        self,
        machine: SSH.RotatingMachine,
        *,
        p: float | Qty | None = None,
        q: float | Qty | None = None,
        inService: bool | None = None,
    ) -> SSH.RotatingMachine:
        """
        Adds real-time p/q values from measurement or basecase.
        Use load sign convention (positive = flow out of node), motor is positive, generator is negative
        * p: instantaneous active power, float in watts or Qty('kW'|'MW')
        * q: instantaneous reactive power, float in VArs or Qty('kVAr'|'MVAr')
        * inService: boolean, machine is de-energized if false
        """
        graph_write.set_attr(machine, SSH, "p", p)
        graph_write.set_attr(machine, SSH, "q", q)
        graph_write.set_attr(machine, SSH, "inService", inService)
        return machine

    def add_short_circuit(
        self,
        machine: SC.RotatingMachine,
        *,
        ratedU: float | Qty | None = None,
        ratedPowerFactor: float | None = None,
    ) -> SC.RotatingMachine:
        graph_write.set_attr(machine, SC, "ratedU", ratedU)
        graph_write.set_attr(machine, SC, "ratedPowerFactor", ratedPowerFactor)
        return machine
