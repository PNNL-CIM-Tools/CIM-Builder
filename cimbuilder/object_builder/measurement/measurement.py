import uuid
from dataclasses import dataclass

import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.measurement as MEAS
from cimtables import graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str

# IEC 61850 WYE attribute of each phase. Split phases (s1, s2) have none.
WYE_ATTRIBUTE = {"A": "phsA", "B": "phsB", "C": "phsC"}

# Equipment classes whose per-phase children carry the phasing, as (class name, child list name)
PHASE_CHILDREN = [
    ("EnergyConsumer", "EnergyConsumerPhase"),
    ("PowerElectronicsConnection", "PowerElectronicsConnectionPhase"),
    ("ShuntCompensator", "ShuntCompensatorPhase"),
    ("ACLineSegment", "ACLineSegmentPhases"),
]


@dataclass(frozen=True)
class MeasurementKind:
    """
    One measured quantity, as mapped by IEC 62361-102 Tables 13-20
    * measurementType: IEC 61970-301 type string, e.g. PhaseToNeutralVoltage
    * logical_node: IEC 61850 logical node class, e.g. MMXU
    * data_object: IEC 61850 data object name, e.g. PNV
    * unitSymbol: CIM UnitSymbol of the value, e.g. V
    * wye: True if the data object is a WYE, with one phsA/phsB/phsC attribute per phase
    """

    measurementType: str
    logical_node: str
    data_object: str
    unitSymbol: str
    wye: bool = False

    def iec61850_name(self, phase: str | None) -> str:
        """e.g. MMXU.PNV.phsA, or XCBR.Pos for a quantity that is not a WYE"""
        name = f"{self.logical_node}.{self.data_object}"
        if self.wye and phase in WYE_ATTRIBUTE:
            name += f".{WYE_ATTRIBUTE[phase]}"
        return name


def single_phases(phase_code: str) -> list[str]:
    """The phases of a PhaseCode string, without neutral: ABCN -> [A, B, C], s12N -> [s1, s2]"""
    if phase_code == "none":
        return []
    letters = phase_code.replace("N", "")
    if letters.startswith("s"):
        return [f"s{number}" for number in letters[1:]]
    return list(letters)


class MeasurementBuilder(ObjectBuilder):
    """
    Base for the Analog and Discrete builders. Builder functions to be called in the following order:
    * create() - instantiate the Measurement; put the IEC 61850 name (e.g. MMXU.PNV.phsA) in description
    * add_measurement() - measured quantity, phases and the PowerSystemResource/Terminal measured
    The add_<equipment>_analogs()/add_<equipment>_discretes() methods of the subclasses do both for
    every standard measurement of one piece of equipment.
    """

    cim_class_name = "Measurement"

    def add_measurement(
        self,
        measurement: MEAS.Measurement,
        *,
        measurementType: str,
        PowerSystemResource: mRID,
        Terminal: mRID | None = None,
        phases: str | None = None,
        unitSymbol: str | None = None,
    ) -> MEAS.Measurement:
        """
        Adds the measurement profile layer
        * measurementType: IEC 61970-301 / IEC 62361-102 type string, e.g. PhaseToNeutralVoltage
        * PowerSystemResource: mRID of the measured equipment, tap changer or battery
        * Terminal: mRID of the Terminal at the sensing location, None if it has none (e.g. state of charge)
        * phases: phase-code string, e.g. A; None means ABC
        * unitSymbol: unit of the measured quantity, e.g. V, A, VA, none
        """
        meas: MEAS = self.cim  # type: ignore
        graph_write.set_attr(measurement, MEAS, "measurementType", measurementType)
        graph_write.set_attr(measurement, MEAS, "phases", self._enum("PhaseCode", phases))
        graph_write.set_attr(measurement, MEAS, "unitSymbol", self._enum("UnitSymbol", unitSymbol))
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=measurement,
            profile_part=MEAS,
            association_name="PowerSystemResource",
            target_class=meas.PowerSystemResource,
            target_mRID=PowerSystemResource,
        )
        if Terminal is not None:
            graph_write.set_assc_from_mrid(
                network=self.network,
                source_object=measurement,
                profile_part=MEAS,
                association_name="Terminal",
                target_class=meas.ACDCTerminal,
                target_mRID=Terminal,
            )
        return measurement

    # Shared pieces, used by the add_<equipment>_analogs()/add_<equipment>_discretes() methods

    def _measure(
        self,
        kind: MeasurementKind,
        resource: MEAS.PowerSystemResource,
        *,
        terminal: CN.Terminal | None = None,
        phase: str | None = None,
    ) -> MEAS.Measurement:
        """
        create() + add_measurement() for one quantity, with the IEC 61850 name as the description.
        The mRID is a UUID seeded from the resource mRID, type, terminal and phase, so rebuilding
        returns the existing measurement instead of a duplicate.
        """
        meas: MEAS = self.cim  # type: ignore
        suffix = kind.measurementType
        if terminal is not None:
            suffix += f"_{terminal.sequenceNumber}"
        if phase is not None:
            suffix += f"_{phase}"
        measurement_mRID = str(uuid.uuid5(uuid.NAMESPACE_OID, f"{resource.mRID}_{suffix}"))

        existing = graph_write.resolve(self.network, meas.Measurement, measurement_mRID)
        if existing is not None:
            return existing  # type: ignore

        measurement: MEAS.Measurement = self.create(
            mRID=measurement_mRID,
            name=f"{type(resource).__name__}_{resource.name}_{suffix}",
            description=kind.iec61850_name(phase),
        )  # type: ignore
        return self.add_measurement(
            measurement,
            measurementType=kind.measurementType,
            PowerSystemResource=resource.mRID,
            Terminal=terminal.mRID if terminal is not None else None,
            phases=phase,
            unitSymbol=kind.unitSymbol,
        )

    def _measure_phases(
        self, kind: MeasurementKind, equipment: CN.ConductingEquipment, terminal: CN.Terminal
    ) -> list[MEAS.Measurement]:
        """One measurement of kind per phase of the terminal"""
        return [
            self._measure(kind, equipment, terminal=terminal, phase=phase)
            for phase in self._phases(equipment, terminal)
        ]

    def _phases(self, equipment: CN.ConductingEquipment, terminal: CN.Terminal) -> list[str]:
        """Phases of a terminal, without neutral, or A, B, C - the CIM default for a terminal without phases"""
        return self._known_phases(equipment, terminal) or ["A", "B", "C"]

    def _known_phases(self, equipment: CN.ConductingEquipment, terminal: CN.Terminal) -> list[str]:
        """
        Phases of a terminal, without neutral, from the first of:
        * Terminal.phases, where CIM18 keeps the phasing
        * the TransformerPhaseEnds on a transformer end's Terminal, one per conductor
        * the equipment's per-phase children (SwitchPhase side, EnergyConsumerPhase, ...)
        Empty if none of them is set.
        """
        if terminal.phases is not None:
            return single_phases(terminal.phases.value)

        phases = []
        if isinstance(equipment, self.cim.PowerTransformer):
            phases = [
                end.phase.value
                for end in terminal.TransformerEnd
                if isinstance(end, self.cim.TransformerPhaseEnd)
            ]
        if isinstance(equipment, self.cim.Switch):
            side = f"phaseSide{terminal.sequenceNumber}"
            phases = [getattr(switch_phase, side).value for switch_phase in equipment.SwitchPhase]
        for class_name, children in PHASE_CHILDREN:
            if isinstance(equipment, getattr(self.cim, class_name)):
                phases = [child.phase.value for child in getattr(equipment, children)]

        return [phase for phase in phases if phase != "N"]
