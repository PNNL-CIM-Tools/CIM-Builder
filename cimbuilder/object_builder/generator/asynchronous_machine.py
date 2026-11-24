import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.short_circuit as SC
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import Qty, graph_write

from cimbuilder.object_builder.generator.rotating_machine import RotatingMachineBuilder


class AsynchronousMachineBuilder(RotatingMachineBuilder):
    cim_class_name = "AsynchronousMachine"

    def add_electrical(
        self,
        machine: EL_BAL.AsynchronousMachine,
        *,
        ratedS: float | Qty | None = None,
        efficiency: float | None = None,
        asynchronousMachineType: str | None = None,
    ) -> EL_BAL.AsynchronousMachine:
        """Adds electrical_balanced.AsynchronousMachine's rating and kind.
        * ratedS: nameplate apparent power rating, float in VA or Qty('kVA'|'MVA')
        * efficiency: efficiency of the machine at nominal operation, in percent
        * asynchronousMachineType: generator|motor
        """
        super().add_electrical(machine, ratedS=ratedS)
        graph_write.set_attr(machine, EL_BAL, "efficiency", efficiency)
        graph_write.set_attr(
            machine,
            EL_BAL,
            "asynchronousMachineType",
            self._enum("AsynchronousMachineKind", asynchronousMachineType),
        )
        return machine

    def add_short_circuit(
        self,
        machine: SC.RotatingMachine,
        *,
        ratedU: float | Qty | None = None,
        ratedPowerFactor: float | None = None,

    ) -> SC.RotatingMachine:
        super().add_short_circuit(
            machine, ratedU=ratedU, ratedPowerFactor=ratedPowerFactor
        )
        return machine
