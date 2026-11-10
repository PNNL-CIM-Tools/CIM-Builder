import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.measurement as MEAS

from cimbuilder.core.sort_terminals import sort_terminals_by_sequence
from cimbuilder.object_builder.measurement.measurement import (
    MeasurementBuilder,
    MeasurementKind,
)


def switch_position(logical_node: str) -> MeasurementKind:
    """IEC 62361-102 Table 18 SwitchPosition, replacing the GridAPPS-D Pos type"""
    return MeasurementKind("SwitchPosition", logical_node, "Pos", "none")


class DiscreteBuilder(MeasurementBuilder):
    """
    Builder for Discrete measurements. Either build one Discrete with create() + add_measurement(),
    or every standard Discrete of one piece of equipment with an add_<equipment>_discretes() method.
    Each of those returns the equipment and its Discretes, with the IEC 61850 name as description.
    Tap position is an Analog in IEC 62361-102 Table 18: see AnalogBuilder.add_tap_changer_analogs().
    """

    cim_class_name = "Discrete"

    def add_switch_discretes(self, switch: CN.Switch) -> tuple[CN.Switch, list[MEAS.Discrete]]:
        """
        Switch position per phase at terminal 1. Logical node per IEC 62361-102 Table 12:
        XFUS for a Fuse, XCBR for a Breaker or Recloser (short circuit breaking), else XSWI
        """
        if isinstance(switch, self.cim.Fuse):
            logical_node = "XFUS"
        elif isinstance(switch, (self.cim.Breaker, self.cim.Recloser)):
            logical_node = "XCBR"
        else:
            logical_node = "XSWI"
        terminal = sort_terminals_by_sequence(switch)[0]
        return switch, self._measure_phases(switch_position(logical_node), switch, terminal)

    def add_shunt_discretes(
        self, shunt: CN.ShuntCompensator
    ) -> tuple[CN.ShuntCompensator, list[MEAS.Discrete]]:
        """Position of the capacitor bank switch (XSWI) per phase of the capacitor terminal"""
        terminal = sort_terminals_by_sequence(shunt)[0]
        return shunt, self._measure_phases(switch_position("XSWI"), shunt, terminal)
