import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
import cimprofiles.cim18.cim18v17.short_circuit as SC
import cimprofiles.cim18.cim18v17.steady_state_hypothesis as SSH
from cimtables import Qty, graph_write

from cimbuilder.object_builder.generator.rotating_machine import RotatingMachineBuilder


class SynchronousMachineBuilder(RotatingMachineBuilder):
    cim_class_name = "SynchronousMachine"

    def add_electrical(
        self,
        machine: EL_BAL.RotatingMachine,
        *,
        ratedS: float | Qty | None = None,
        baseQ: float | Qty | None = None,
        minQ: float | Qty | None = None,
        maxQ: float | Qty | None = None,
        minU: float | Qty | None = None,
        maxU: float | Qty | None = None,
    ) -> EL_BAL.RotatingMachine:
        super().add_electrical(machine, ratedS=ratedS)
        graph_write.set_attr(machine, EL_BAL, "baseQ", baseQ)
        graph_write.set_attr(machine, EL_BAL, "minQ", minQ)
        graph_write.set_attr(machine, EL_BAL, "maxQ", maxQ)
        graph_write.set_attr(machine, EL_BAL, "minU", minU)
        graph_write.set_attr(machine, EL_BAL, "maxU", maxU)

        return machine

    def add_ssh(
        self,
        machine: SSH.RotatingMachine,
        *,
        p: float | Qty | None = None,
        q: float | Qty | None = None,
        operatingMode: str|None=None,
        inService: bool | None = None,
    ) -> SSH.RotatingMachine:
        super().add_ssh(machine, p=p, q=q, inService=inService)
        graph_write.set_attr(machine, SSH, "operatingMode", operatingMode)

        return machine

    def add_short_circuit(
        self,
        machine: SC.RotatingMachine,
        *,
        ratedU: float | Qty | None = None,
        ratedPowerFactor: float | None = None,
        r: float | Qty | None = None,
        r0: float | Qty | None = None,
        r2: float | Qty | None = None,
        x0: float | Qty | None = None,
        x2: float | Qty | None = None,
        earthing: bool | None = None,
        earthingStarPointR: float | Qty | None = None,
        earthingStarPointX: float | Qty | None = None,
    ) -> SC.RotatingMachine:
        super().add_short_circuit(
            machine, ratedU=ratedU, ratedPowerFactor=ratedPowerFactor
        )
        graph_write.set_attr(machine, SC, "r", r)
        graph_write.set_attr(machine, SC, "r0", r0)
        graph_write.set_attr(machine, SC, "r2", r2)
        graph_write.set_attr(machine, SC, "x0", x0)
        graph_write.set_attr(machine, SC, "x2", x2)
        graph_write.set_attr(machine, SC, "earthing", earthing)
        graph_write.set_attr(machine, SC, "earthingStarPointR", earthingStarPointR)
        graph_write.set_attr(machine, SC, "earthingStarPointX", earthingStarPointX)

        return machine

    def add_dynamics(self):
        pass
