import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.measurement as MEAS

from cimbuilder.core.sort_terminals import sort_terminals_by_sequence
from cimbuilder.object_builder.measurement.measurement import (
    MeasurementBuilder,
    MeasurementKind,
    single_phases,
)

# IEC 62361-102 Tables 14, 18 and 19. The old GridAPPS-D type each replaces is in the comment;
# the IEC 61850 data object (description) keeps that name where the two agree.
PHASE_VOLTAGE = MeasurementKind("PhaseToNeutralVoltage", "MMXU", "PNV", "V", wye=True)  # PNV
PHASE_CURRENT = MeasurementKind("PhaseCurrent", "MMXU", "A", "A", wye=True)  # A
# No per-phase power string is defined (Table 16 ApparentPower is MMXN.VolAmp, non-phase-related);
# ApparentPower with Measurement.phases set, and MMXU.VA.phsX as the 61850 name
PHASE_POWER = MeasurementKind("ApparentPower", "MMXU", "VA", "VA", wye=True)  # VA
STATE_OF_CHARGE = MeasurementKind("StateOfChargePct", "DSTO", "UseSocPct", "none")  # SoC
# Table 18 makes tap position an Analog, not a Discrete
TAP_POSITION = MeasurementKind("TapPosition", "ATCC", "TapPos", "none")  # Pos on a regulator


class AnalogBuilder(MeasurementBuilder):
    """
    Builder for Analog measurements. Either build one Analog with create() + add_measurement(),
    or every standard Analog of one piece of equipment with an add_<equipment>_analogs() method.
    Each of those returns the equipment and its Analogs, with the IEC 61850 name as description.
    Phase voltage: one-terminal equipment (load, capacitor, inverter, generator) always gets its own;
    lines, switches and transformers add one only where the node has none for that phase yet.
    """

    cim_class_name = "Analog"

    def add_load_analogs(
        self, load: CN.EnergyConsumer
    ) -> tuple[CN.EnergyConsumer, list[MEAS.Analog]]:
        """Phase voltage and power per phase of the load terminal"""
        return load, self._voltage_and_power(load)

    def add_shunt_analogs(
        self, shunt: CN.ShuntCompensator
    ) -> tuple[CN.ShuntCompensator, list[MEAS.Analog]]:
        """Phase voltage and power per phase of the capacitor terminal"""
        return shunt, self._voltage_and_power(shunt)

    def add_generator_analogs(
        self, generator: CN.RotatingMachine
    ) -> tuple[CN.RotatingMachine, list[MEAS.Analog]]:
        """Phase voltage and power per phase of the machine terminal"""
        return generator, self._voltage_and_power(generator)

    def add_inverter_analogs(
        self, inverter: CN.PowerElectronicsConnection
    ) -> tuple[CN.PowerElectronicsConnection, list[MEAS.Analog]]:
        """
        Phase voltage and power per phase of the inverter terminal, plus the state of charge of
        each BatteryUnit behind it (on the BatteryUnit, no Terminal - DSTO maps to BatteryUnit)
        """
        analogs = self._voltage_and_power(inverter)
        for unit in inverter.PowerElectronicsUnit:
            if isinstance(unit, self.cim.BatteryUnit):
                analogs.append(self._measure(STATE_OF_CHARGE, unit, phase="none"))
        return inverter, analogs

    def add_line_analogs(
        self, line: CN.ACLineSegment
    ) -> tuple[CN.ACLineSegment, list[MEAS.Analog]]:
        """Power per phase at terminal 1, and the node voltage there if not yet measured"""
        terminal = sort_terminals_by_sequence(line)[0]
        analogs = self._measure_phases(PHASE_POWER, line, terminal)
        analogs += self._node_voltage(line, terminal)
        return line, analogs

    def add_switch_analogs(self, switch: CN.Switch) -> tuple[CN.Switch, list[MEAS.Analog]]:
        """Current per phase at terminal 1, and the node voltage at both terminals if not yet measured"""
        terminals = sort_terminals_by_sequence(switch)
        analogs = self._measure_phases(PHASE_CURRENT, switch, terminals[0])
        for terminal in terminals:
            analogs += self._node_voltage(switch, terminal)
        return switch, analogs

    def add_transformer_analogs(
        self, transformer: CN.PowerTransformer | CN.AutoTransformer
    ) -> tuple[CN.PowerTransformer | CN.AutoTransformer, list[MEAS.Analog]]:
        """
        Power per phase at the Terminal of every end, and the node voltage there if not yet measured.
        Phases from Terminal.phases, else the TransformerPhaseEnds on the Terminal. Also takes a
        VoltageRegulator (an AutoTransformer).
        """
        analogs = []
        for terminal in sort_terminals_by_sequence(transformer):
            analogs += self._measure_phases(PHASE_POWER, transformer, terminal)
            analogs += self._node_voltage(transformer, terminal)
        return transformer, analogs

    def add_tap_changer_analogs(
        self, tap_changer: CN.TapChanger
    ) -> tuple[CN.TapChanger, list[MEAS.Analog]]:
        """
        One tap position on the tap changer (ATCC maps to TapChanger), at its end's Terminal.
        Phases of that Terminal (e.g. A for a single-phase regulator), else None - ABC.
        """
        terminal = tap_changer.TransformerEnd.Terminal
        phases = self._known_phases(terminal.ConductingEquipment, terminal)
        phase = "".join(phases) or None
        return tap_changer, [self._measure(TAP_POSITION, tap_changer, terminal=terminal, phase=phase)]

    def _voltage_and_power(self, equipment: CN.ConductingEquipment) -> list[MEAS.Analog]:
        """Phase voltage and power per phase of every terminal"""
        analogs = []
        for terminal in sort_terminals_by_sequence(equipment):
            analogs += self._measure_phases(PHASE_VOLTAGE, equipment, terminal)
            analogs += self._measure_phases(PHASE_POWER, equipment, terminal)
        return analogs

    def _node_voltage(
        self, equipment: CN.ConductingEquipment, terminal: CN.Terminal
    ) -> list[MEAS.Analog]:
        """Phase voltage per phase of the terminal that its node does not already measure"""
        measured = set()
        for node_terminal in terminal.ConnectivityNode.Terminals:
            for measurement in node_terminal.Measurements:
                if measurement.measurementType == PHASE_VOLTAGE.measurementType:
                    phases = measurement.phases.value if measurement.phases is not None else "ABC"
                    measured.update(single_phases(phases))
        return [
            self._measure(PHASE_VOLTAGE, equipment, terminal=terminal, phase=phase)
            for phase in self._phases(equipment, terminal)
            if phase not in measured
        ]
