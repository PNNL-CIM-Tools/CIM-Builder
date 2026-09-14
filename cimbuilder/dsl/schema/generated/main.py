# Auto generated from main.yaml by pythongen.py version: 0.0.1
# Generation date: 2026-09-14T12:12:04
# Schema: cimtbl
#
# id: https://github.com/AAndersn/CIM-Builder/cimtbl
# description: LinkML validation schema for the .cimtbl DSL (design: CIMTBL_DESIGN.md §2, §12.2). <Class>Row classes (classes/rows.yaml) compose the real cimhub_2026 CIMTool export with DSL-only mixins (classes/extensions.yaml) for connectivity, phases, and Template columns that aren't real CIM attributes. Column units live on the .cimtbl header (§3.2), not in this schema - float/int/str ranges here are the coerced value only; validate.py binds units into Qty afterward.
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Date, Datetime, Decimal, Float, Integer, String, Time
from linkml_runtime.utils.metamodelcore import Bool, Decimal, XSDDate, XSDDateTime, XSDTime

metamodel_version = "1.11.0"
version = None

# Namespaces
CIM = CurieNamespace('cim', 'http://cim.ucaiug.io/cim101/draft#')
CIMTBL = CurieNamespace('cimtbl', 'https://github.com/AAndersn/CIM-Builder/cimtbl/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = CIMTBL


# Types
class ActivePower(float):
    """ Product of RMS value of the voltage and the RMS value of the in-phase component of the current. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "ActivePower"
    type_model_uri = CIMTBL.ActivePower


class ActivePowerChangeRate(float):
    """ Rate of change of active power per time. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "ActivePowerChangeRate"
    type_model_uri = CIMTBL.ActivePowerChangeRate


class ActivePowerPerFrequency(float):
    """ Active power variation with frequency. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "ActivePowerPerFrequency"
    type_model_uri = CIMTBL.ActivePowerPerFrequency


class AngleDegrees(float):
    """ Measurement of angle in degrees. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "AngleDegrees"
    type_model_uri = CIMTBL.AngleDegrees


class AngleRadians(float):
    """ Phase angle in radians. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "AngleRadians"
    type_model_uri = CIMTBL.AngleRadians


class ApparentPower(float):
    """ Product of the RMS value of the voltage and the RMS value of the current. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "ApparentPower"
    type_model_uri = CIMTBL.ApparentPower


class Area(float):
    """ Area. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Area"
    type_model_uri = CIMTBL.Area


class Classification(int):
    """ Classification of level.  Specify as 1..n, with 1 being the most detailed, highest priority, etc as described on the attribute using this data type. """
    type_class_uri = XSD["integer"]
    type_class_curie = "xsd:integer"
    type_name = "Classification"
    type_model_uri = CIMTBL.Classification


class Conductance(float):
    """ Factor by which voltage must be multiplied to give corresponding power lost from a circuit. Real part of admittance. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Conductance"
    type_model_uri = CIMTBL.Conductance


class ConductancePerLength(float):
    """ Real part of admittance per unit of length. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "ConductancePerLength"
    type_model_uri = CIMTBL.ConductancePerLength


class CostPerHeatUnit(float):
    """ Cost, in units of currency, per quantity of heat generated. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "CostPerHeatUnit"
    type_model_uri = CIMTBL.CostPerHeatUnit


class CurrentFlow(float):
    """ Electrical current with sign convention: positive flow is out of the conducting equipment into the connectivity node. Can be both AC and DC. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "CurrentFlow"
    type_model_uri = CIMTBL.CurrentFlow


class Displacement(float):
    """ Unit of displacement relative to a reference position, hence can be negative. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Displacement"
    type_model_uri = CIMTBL.Displacement


class Force(float):
    """ Force in newtons. It shall be a positive value or zero. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Force"
    type_model_uri = CIMTBL.Force


class Frequency(float):
    """ Cycles per second. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Frequency"
    type_model_uri = CIMTBL.Frequency


class Impedance(float):
    """ Ratio of voltage to current. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Impedance"
    type_model_uri = CIMTBL.Impedance


class Inductance(float):
    """ Inductive part of reactance (imaginary part of impedance), at rated frequency. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Inductance"
    type_model_uri = CIMTBL.Inductance


class KiloActivePower(float):
    """ Active power in kilowatts. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "KiloActivePower"
    type_model_uri = CIMTBL.KiloActivePower


class Length(float):
    """ Unit of length. It shall be a positive value or zero. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Length"
    type_model_uri = CIMTBL.Length


class Money(Decimal):
    """ Amount of money. """
    type_class_uri = XSD["decimal"]
    type_class_curie = "xsd:decimal"
    type_name = "Money"
    type_model_uri = CIMTBL.Money


class PU(float):
    """ Per Unit - a positive or negative value referred to a defined base. Values typically range from -10 to +10. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "PU"
    type_model_uri = CIMTBL.PU


class PerCent(float):
    """ Percentage on a defined base. For example, specify as 100 to indicate at the defined base. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "PerCent"
    type_model_uri = CIMTBL.PerCent


class Pressure(float):
    """ Pressure in pascals. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Pressure"
    type_model_uri = CIMTBL.Pressure


class Reactance(float):
    """ Reactance (imaginary part of impedance), at rated frequency. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Reactance"
    type_model_uri = CIMTBL.Reactance


class ReactancePerLength(float):
    """ Reactance (imaginary part of impedance) per unit of length, at rated frequency. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "ReactancePerLength"
    type_model_uri = CIMTBL.ReactancePerLength


class ReactivePower(float):
    """ Product of RMS value of the voltage and the RMS value of the quadrature component of the current. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "ReactivePower"
    type_model_uri = CIMTBL.ReactivePower


class RealEnergy(float):
    """ Real electrical energy. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "RealEnergy"
    type_model_uri = CIMTBL.RealEnergy


class Resistance(float):
    """ Resistance (real part of impedance). """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Resistance"
    type_model_uri = CIMTBL.Resistance


class ResistancePerLength(float):
    """ Resistance (real part of impedance) per unit of length. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "ResistancePerLength"
    type_model_uri = CIMTBL.ResistancePerLength


class RotationSpeed(float):
    """ Number of revolutions per second. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "RotationSpeed"
    type_model_uri = CIMTBL.RotationSpeed


class Seconds(float):
    """ Time, in seconds. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Seconds"
    type_model_uri = CIMTBL.Seconds


class Susceptance(float):
    """ Imaginary part of admittance. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Susceptance"
    type_model_uri = CIMTBL.Susceptance


class SusceptancePerLength(float):
    """ Imaginary part of admittance per unit of length. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "SusceptancePerLength"
    type_model_uri = CIMTBL.SusceptancePerLength


class Temperature(float):
    """ Value of temperature in degrees Celsius. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Temperature"
    type_model_uri = CIMTBL.Temperature


class Voltage(float):
    """ Electrical voltage, can be both AC and DC. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "Voltage"
    type_model_uri = CIMTBL.Voltage


class VoltagePerReactivePower(float):
    """ Voltage variation with reactive power. """
    type_class_uri = XSD["float"]
    type_class_curie = "xsd:float"
    type_name = "VoltagePerReactivePower"
    type_model_uri = CIMTBL.VoltagePerReactivePower


# Class references



@dataclass(repr=False)
class BranchGroupTerminal(YAMLRoot):
    """
    A specific directed terminal flow for a branch group.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BranchGroupTerminal"]
    class_class_curie: ClassVar[str] = "cim:BranchGroupTerminal"
    class_name: ClassVar[str] = "BranchGroupTerminal"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BranchGroupTerminal

    positiveFlowIn: Optional[Union[bool, Bool]] = None
    BranchGroup: Optional[Union[dict, "BranchGroup"]] = None
    Terminal: Optional[Union[dict, "Terminal"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.positiveFlowIn is not None and not isinstance(self.positiveFlowIn, Bool):
            self.positiveFlowIn = Bool(self.positiveFlowIn)

        if self.BranchGroup is not None and not isinstance(self.BranchGroup, BranchGroup):
            self.BranchGroup = BranchGroup(**as_dict(self.BranchGroup))

        if self.Terminal is not None and not isinstance(self.Terminal, Terminal):
            self.Terminal = Terminal(**as_dict(self.Terminal))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CableArmorInfo(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["CableArmorInfo"]
    class_class_curie: ClassVar[str] = "cim:CableArmorInfo"
    class_name: ClassVar[str] = "CableArmorInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.CableArmorInfo

    diameterOverArmor: Optional[float] = None
    layLength: Optional[float] = None
    strandRadius: Optional[float] = None
    tapeLap: Optional[float] = None
    tapeThickness: Optional[float] = None
    TapeWidth: Optional[float] = None
    Thickness: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.diameterOverArmor is not None and not isinstance(self.diameterOverArmor, float):
            self.diameterOverArmor = float(self.diameterOverArmor)

        if self.layLength is not None and not isinstance(self.layLength, float):
            self.layLength = float(self.layLength)

        if self.strandRadius is not None and not isinstance(self.strandRadius, float):
            self.strandRadius = float(self.strandRadius)

        if self.tapeLap is not None and not isinstance(self.tapeLap, float):
            self.tapeLap = float(self.tapeLap)

        if self.tapeThickness is not None and not isinstance(self.tapeThickness, float):
            self.tapeThickness = float(self.tapeThickness)

        if self.TapeWidth is not None and not isinstance(self.TapeWidth, float):
            self.TapeWidth = float(self.TapeWidth)

        if self.Thickness is not None and not isinstance(self.Thickness, float):
            self.Thickness = float(self.Thickness)

        super().__post_init__(**kwargs)


class ChangeSetMember(YAMLRoot):
    """
    A CRUD-style data object.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ChangeSetMember"]
    class_class_curie: ClassVar[str] = "cim:ChangeSetMember"
    class_name: ClassVar[str] = "ChangeSetMember"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ChangeSetMember


@dataclass(repr=False)
class CurrentDroopOverride(YAMLRoot):
    """
    Current droop override uses the following logic:- When the current exceeds a threshold the device executes the
    following transitions: 1) When injecting an inductive voltage or in monitoring mode the device tends to inject a
    voltage proportional to the difference between the line current and the aforementioned threshold. 2) When
    injecting a capacitive voltage the device transitions to monitoring mode.- If the aforementioned proportional
    voltage is lower than the initial one, the voltage injection remains unchanged.Current droop override is not
    applied when the device operates in currentDroop mode.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["CurrentDroopOverride"]
    class_class_curie: ClassVar[str] = "cim:CurrentDroopOverride"
    class_name: ClassVar[str] = "CurrentDroopOverride"
    class_model_uri: ClassVar[URIRef] = CIMTBL.CurrentDroopOverride

    mRID: Optional[str] = None
    droopCapacitive: Optional[float] = None
    droopInductive: Optional[float] = None
    enabled: Optional[Union[bool, Bool]] = None
    offsetCapacitiveI: Optional[float] = None
    offsetInductiveI: Optional[float] = None
    targetValueCapacitiveI: Optional[float] = None
    targetValueInductiveI: Optional[float] = None
    SSSCController: Optional[Union[dict, "SSSCController"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.mRID is not None and not isinstance(self.mRID, str):
            self.mRID = str(self.mRID)

        if self.droopCapacitive is not None and not isinstance(self.droopCapacitive, float):
            self.droopCapacitive = float(self.droopCapacitive)

        if self.droopInductive is not None and not isinstance(self.droopInductive, float):
            self.droopInductive = float(self.droopInductive)

        if self.enabled is not None and not isinstance(self.enabled, Bool):
            self.enabled = Bool(self.enabled)

        if self.offsetCapacitiveI is not None and not isinstance(self.offsetCapacitiveI, float):
            self.offsetCapacitiveI = float(self.offsetCapacitiveI)

        if self.offsetInductiveI is not None and not isinstance(self.offsetInductiveI, float):
            self.offsetInductiveI = float(self.offsetInductiveI)

        if self.targetValueCapacitiveI is not None and not isinstance(self.targetValueCapacitiveI, float):
            self.targetValueCapacitiveI = float(self.targetValueCapacitiveI)

        if self.targetValueInductiveI is not None and not isinstance(self.targetValueInductiveI, float):
            self.targetValueInductiveI = float(self.targetValueInductiveI)

        if self.SSSCController is not None and not isinstance(self.SSSCController, SSSCController):
            self.SSSCController = SSSCController(**as_dict(self.SSSCController))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CurveData(YAMLRoot):
    """
    Multi-purpose data points for defining a curve. The use of this generic class is discouraged if a more specific
    class can be used to specify the X and Y axis values along with their specific data types.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["CurveData"]
    class_class_curie: ClassVar[str] = "cim:CurveData"
    class_name: ClassVar[str] = "CurveData"
    class_model_uri: ClassVar[URIRef] = CIMTBL.CurveData

    xvalue: Optional[float] = None
    y1value: Optional[float] = None
    y2value: Optional[float] = None
    y3value: Optional[float] = None
    Curve: Optional[Union[dict, "Curve"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.xvalue is not None and not isinstance(self.xvalue, float):
            self.xvalue = float(self.xvalue)

        if self.y1value is not None and not isinstance(self.y1value, float):
            self.y1value = float(self.y1value)

        if self.y2value is not None and not isinstance(self.y2value, float):
            self.y2value = float(self.y2value)

        if self.y3value is not None and not isinstance(self.y3value, float):
            self.y3value = float(self.y3value)

        if self.Curve is not None and not isinstance(self.Curve, Curve):
            self.Curve = Curve(**as_dict(self.Curve))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DateInterval(YAMLRoot):
    """
    Interval between two dates.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["DateInterval"]
    class_class_curie: ClassVar[str] = "cim:DateInterval"
    class_name: ClassVar[str] = "DateInterval"
    class_model_uri: ClassVar[URIRef] = CIMTBL.DateInterval

    end: Optional[Union[str, XSDDate]] = None
    start: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.end is not None and not isinstance(self.end, XSDDate):
            self.end = XSDDate(self.end)

        if self.start is not None and not isinstance(self.start, XSDDate):
            self.start = XSDDate(self.start)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DateTimeInterval(YAMLRoot):
    """
    rdfs:label : Date-time interval@enrdfs:comment : 'intervalo de fecha-hora' es una subclase de 'intervalo propio',
    definida utilizando el multi-elemento 'descripci�n de fecha-hora'.@es<http://www.w3.org/2004/02/skos/core#note> :
    'intervalo de fecha-hora' se puede utilizar s�lo para un intervalo cuyos l�mites coinciden con un elemento de
    fecha-hora alineados con el calendario y la zona horaria indicados. Por ejemplo, aunque ambos tienen una duraci�n
    de un d�a, el intervalo de 24 horas que empieza en la media noche del comienzo del 8 mayo en Europa Central se
    puede expresar como un 'intervalo de fecha-hora', el intervalo de 24 horas que empieza a las 1:30pm
    no.@esrdfs:label : intervalo de fecha-hora@es<http://www.w3.org/2004/02/skos/core#definition> : DateTimeInterval
    is a subclass of ProperInterval, defined using the multi-element DateTimeDescription.@enrdfs:comment :
    DateTimeInterval is a subclass of ProperInterval, defined using the multi-element
    DateTimeDescription.@en<http://www.w3.org/2004/02/skos/core#note> : :DateTimeInterval can only be used for an
    interval whose limits coincide with a date-time element aligned to the calendar and timezone indicated. For
    example, while both have a duration of one day, the 24-hour interval beginning at midnight at the beginning of 8
    May in Central Europe can be expressed as a :DateTimeInterval, but the 24-hour interval starting at 1:30pm
    cannot.@en<http://www.w3.org/2004/02/skos/core#definition> : 'intervalo de fecha-hora' es una subclase de
    'intervalo propio', definida utilizando el multi-elemento 'descripci�n de fecha-hora'.@es
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["DateTimeInterval"]
    class_class_curie: ClassVar[str] = "cim:DateTimeInterval"
    class_name: ClassVar[str] = "DateTimeInterval"
    class_model_uri: ClassVar[URIRef] = CIMTBL.DateTimeInterval

    end: Optional[Union[str, XSDDateTime]] = None
    start: Optional[Union[str, XSDDateTime]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.end is not None and not isinstance(self.end, XSDDateTime):
            self.end = XSDDateTime(self.end)

        if self.start is not None and not isinstance(self.start, XSDDateTime):
            self.start = XSDDateTime(self.start)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DecimalQuantity(YAMLRoot):
    """
    Quantity with decimal value and associated unit or currency information.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["DecimalQuantity"]
    class_class_curie: ClassVar[str] = "cim:DecimalQuantity"
    class_name: ClassVar[str] = "DecimalQuantity"
    class_model_uri: ClassVar[URIRef] = CIMTBL.DecimalQuantity

    currency: Optional[Union[str, "Currency"]] = None
    multiplier: Optional[Union[str, "UnitMultiplier"]] = None
    unit: Optional[Union[str, "UnitSymbol"]] = None
    value: Optional[Decimal] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.currency is not None and not isinstance(self.currency, Currency):
            self.currency = Currency(self.currency)

        if self.multiplier is not None and not isinstance(self.multiplier, UnitMultiplier):
            self.multiplier = UnitMultiplier(self.multiplier)

        if self.unit is not None and not isinstance(self.unit, UnitSymbol):
            self.unit = UnitSymbol(self.unit)

        if self.value is not None and not isinstance(self.value, Decimal):
            self.value = Decimal(self.value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FloatQuantity(YAMLRoot):
    """
    Quantity with float value and associated unit information.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["FloatQuantity"]
    class_class_curie: ClassVar[str] = "cim:FloatQuantity"
    class_name: ClassVar[str] = "FloatQuantity"
    class_model_uri: ClassVar[URIRef] = CIMTBL.FloatQuantity

    multiplier: Optional[Union[str, "UnitMultiplier"]] = None
    unit: Optional[Union[str, "UnitSymbol"]] = None
    value: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.multiplier is not None and not isinstance(self.multiplier, UnitMultiplier):
            self.multiplier = UnitMultiplier(self.multiplier)

        if self.unit is not None and not isinstance(self.unit, UnitSymbol):
            self.unit = UnitSymbol(self.unit)

        if self.value is not None and not isinstance(self.value, float):
            self.value = float(self.value)

        super().__post_init__(**kwargs)


class GeneralDateTimeDescription(YAMLRoot):
    """
    rdfs:label : descripci�n de fecha-hora generalizada@esrdfs:label : Generalized date-time
    description@en<http://www.w3.org/2004/02/skos/core#note> : Some combinations of properties are redundant - for
    example, within a specified :year if :dayOfYear is provided then :day and :month can be computed, and vice versa.
    Individual values should be consistent with each other and the calendar, indicated through the value of the
    :hasTRS property.^^xsd:stringrdfs:comment : Description of date and time structured with separate values for the
    various elements of a calendar-clock system@enrdfs:comment : Descripci�n de fecha y hora estructurada con valores
    separados para los distintos elementos de un sistema
    calendario-reloj.@es<http://www.w3.org/2004/02/skos/core#definition> : Description of date and time structured
    with separate values for the various elements of a calendar-clock
    system@en<http://www.w3.org/2004/02/skos/core#definition> : Descripci�n de fecha y hora estructurada con valores
    separados para los distintos elementos de un sistema
    calendario-reloj.^^xsd:string<http://www.w3.org/2004/02/skos/core#note> : Algunas combinaciones de propiedades son
    redundantes - por ejemplo, dentro de un 'a�o' especificado si se proporciona 'd�a del a�o' entonces 'd�a' y 'mes'
    se pueden computar, y viceversa. Los valores individuales deber�an ser consistentes entre ellos y con el
    calendario, indicado a trav�s del valor de la propiedad 'tiene TRS'.@es
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["GeneralDateTimeDescription"]
    class_class_curie: ClassVar[str] = "cim:GeneralDateTimeDescription"
    class_name: ClassVar[str] = "GeneralDateTimeDescription"
    class_model_uri: ClassVar[URIRef] = CIMTBL.GeneralDateTimeDescription


@dataclass(repr=False)
class IdentifiedObject(YAMLRoot):
    """
    This is a class that provides common identification for all classes needing identification and naming attributes.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["IdentifiedObject"]
    class_class_curie: ClassVar[str] = "cim:IdentifiedObject"
    class_name: ClassVar[str] = "IdentifiedObject"
    class_model_uri: ClassVar[URIRef] = CIMTBL.IdentifiedObject

    mRID: Optional[str] = None
    aliasName: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    InstanceSet: Optional[Union[dict, "InstanceSet"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.mRID is not None and not isinstance(self.mRID, str):
            self.mRID = str(self.mRID)

        if self.aliasName is not None and not isinstance(self.aliasName, str):
            self.aliasName = str(self.aliasName)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.InstanceSet is not None and not isinstance(self.InstanceSet, InstanceSet):
            self.InstanceSet = InstanceSet()

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ACDCTerminal(IdentifiedObject):
    """
    An electrical connection point (AC or DC) to a piece of conducting equipment. Terminals are connected at physical
    connection points called connectivity nodes.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ACDCTerminal"]
    class_class_curie: ClassVar[str] = "cim:ACDCTerminal"
    class_name: ClassVar[str] = "ACDCTerminal"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ACDCTerminal

    connected: Optional[Union[bool, Bool]] = None
    sequenceNumber: Optional[int] = None
    BusNameMarker: Optional[Union[dict, "BusNameMarker"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.connected is not None and not isinstance(self.connected, Bool):
            self.connected = Bool(self.connected)

        if self.sequenceNumber is not None and not isinstance(self.sequenceNumber, int):
            self.sequenceNumber = int(self.sequenceNumber)

        if self.BusNameMarker is not None and not isinstance(self.BusNameMarker, BusNameMarker):
            self.BusNameMarker = BusNameMarker(**as_dict(self.BusNameMarker))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ACPointOfCommonCoupling(IdentifiedObject):
    """
    Point of interconnection of the DC converter station to the adjacent AC system (IEC 60633).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ACPointOfCommonCoupling"]
    class_class_curie: ClassVar[str] = "cim:ACPointOfCommonCoupling"
    class_name: ClassVar[str] = "ACPointOfCommonCoupling"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ACPointOfCommonCoupling

    ConnectivityNode: Optional[Union[dict, "ConnectivityNode"]] = None
    DCConverterUnit: Optional[Union[dict, "DCConverterUnit"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.ConnectivityNode is not None and not isinstance(self.ConnectivityNode, ConnectivityNode):
            self.ConnectivityNode = ConnectivityNode(**as_dict(self.ConnectivityNode))

        if self.DCConverterUnit is not None and not isinstance(self.DCConverterUnit, DCConverterUnit):
            self.DCConverterUnit = DCConverterUnit(**as_dict(self.DCConverterUnit))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AltGeneratingUnitMeas(IdentifiedObject):
    """
    A prioritized measurement to be used for the generating unit in the control area specification.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["AltGeneratingUnitMeas"]
    class_class_curie: ClassVar[str] = "cim:AltGeneratingUnitMeas"
    class_name: ClassVar[str] = "AltGeneratingUnitMeas"
    class_model_uri: ClassVar[URIRef] = CIMTBL.AltGeneratingUnitMeas

    priority: Optional[int] = None
    AnalogValue: Optional[Union[dict, "AnalogValue"]] = None
    ControlAreaGeneratingUnit: Optional[Union[dict, "ControlAreaGeneratingUnit"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.priority is not None and not isinstance(self.priority, int):
            self.priority = int(self.priority)

        if self.AnalogValue is not None and not isinstance(self.AnalogValue, AnalogValue):
            self.AnalogValue = AnalogValue(**as_dict(self.AnalogValue))

        if self.ControlAreaGeneratingUnit is not None and not isinstance(self.ControlAreaGeneratingUnit, ControlAreaGeneratingUnit):
            self.ControlAreaGeneratingUnit = ControlAreaGeneratingUnit(**as_dict(self.ControlAreaGeneratingUnit))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AltTieMeas(IdentifiedObject):
    """
    A prioritized measurement to be used for the tie flow as part of the control area specification.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["AltTieMeas"]
    class_class_curie: ClassVar[str] = "cim:AltTieMeas"
    class_name: ClassVar[str] = "AltTieMeas"
    class_model_uri: ClassVar[URIRef] = CIMTBL.AltTieMeas

    priority: Optional[int] = None
    AnalogValue: Optional[Union[dict, "AnalogValue"]] = None
    TieFlow: Optional[Union[dict, "TieFlow"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.priority is not None and not isinstance(self.priority, int):
            self.priority = int(self.priority)

        if self.AnalogValue is not None and not isinstance(self.AnalogValue, AnalogValue):
            self.AnalogValue = AnalogValue(**as_dict(self.AnalogValue))

        if self.TieFlow is not None and not isinstance(self.TieFlow, TieFlow):
            self.TieFlow = TieFlow(**as_dict(self.TieFlow))

        super().__post_init__(**kwargs)


class Asset(IdentifiedObject):
    """
    Tangible resource of the utility, including power system equipment, various end devices, cabinets, buildings, etc.
    For electrical network equipment, the role of the asset is defined through PowerSystemResource and its subclasses,
    defined mainly in the Wires model (refer to IEC61970-301 and model package IEC61970::Wires). Asset description
    places emphasis on the physical characteristics of the equipment fulfilling that role.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Asset"]
    class_class_curie: ClassVar[str] = "cim:Asset"
    class_name: ClassVar[str] = "Asset"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Asset


@dataclass(repr=False)
class AssetInfo(IdentifiedObject):
    """
    Set of attributes of an asset, representing typical datasheet information of a physical device that can be
    instantiated and shared in different data exchange contexts:- as attributes of an asset instance (installed or in
    stock)- as attributes of an asset model (product by a manufacturer)- as attributes of a type asset (generic type
    of an asset as used in designs/extension planning).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["AssetInfo"]
    class_class_curie: ClassVar[str] = "cim:AssetInfo"
    class_name: ClassVar[str] = "AssetInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.AssetInfo

    CatalogAssetType: Optional[Union[dict, "CatalogAssetType"]] = None
    ProductAssetModel: Optional[Union[dict, "ProductAssetModel"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.CatalogAssetType is not None and not isinstance(self.CatalogAssetType, CatalogAssetType):
            self.CatalogAssetType = CatalogAssetType(**as_dict(self.CatalogAssetType))

        if self.ProductAssetModel is not None and not isinstance(self.ProductAssetModel, ProductAssetModel):
            self.ProductAssetModel = ProductAssetModel(**as_dict(self.ProductAssetModel))

        super().__post_init__(**kwargs)


class AsynchronousMachineDynamics(IdentifiedObject):
    """
    Asynchronous machine whose behaviour is described by reference to a standard model expressed in either time
    constant reactance form or equivalent circuit form <font color=#0f0f0f>or by definition of a user-defined
    model.</font>Parameter details:<ol> <li>Asynchronous machine parameters such as <i>Xl, Xs,</i> etc. are actually
    used as inductances in the model, but are commonly referred to as reactances since, at nominal frequency, the PU
    values are the same. However, some references use the symbol <i>L</i> instead of <i>X</i>.</li></ol>
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["AsynchronousMachineDynamics"]
    class_class_curie: ClassVar[str] = "cim:AsynchronousMachineDynamics"
    class_name: ClassVar[str] = "AsynchronousMachineDynamics"
    class_model_uri: ClassVar[URIRef] = CIMTBL.AsynchronousMachineDynamics


@dataclass(repr=False)
class BaseFrequency(IdentifiedObject):
    """
    The BaseFrequency class describes a base frequency for a power system network. In case of multiple power networks
    with different frequencies, e.g. 50 Hz or 60 Hz each network will have its own base frequency class. Hence it is
    assumed that power system objects having different base frequencies appear in separate documents where each
    document has a single base frequency instance.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BaseFrequency"]
    class_class_curie: ClassVar[str] = "cim:BaseFrequency"
    class_name: ClassVar[str] = "BaseFrequency"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BaseFrequency

    frequency: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.frequency is not None and not isinstance(self.frequency, float):
            self.frequency = float(self.frequency)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BasePower(IdentifiedObject):
    """
    The BasePower class defines the base power used in the per unit calculations.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BasePower"]
    class_class_curie: ClassVar[str] = "cim:BasePower"
    class_name: ClassVar[str] = "BasePower"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BasePower

    basePower: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.basePower is not None and not isinstance(self.basePower, float):
            self.basePower = float(self.basePower)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BaseVoltage(IdentifiedObject):
    """
    Defines a system base voltage which is referenced. This may be different than the rated voltage.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BaseVoltage"]
    class_class_curie: ClassVar[str] = "cim:BaseVoltage"
    class_name: ClassVar[str] = "BaseVoltage"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BaseVoltage

    nominalVoltage: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.nominalVoltage is not None and not isinstance(self.nominalVoltage, float):
            self.nominalVoltage = float(self.nominalVoltage)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BasicIntervalSchedule(IdentifiedObject):
    """
    Schedule of values at points in time.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BasicIntervalSchedule"]
    class_class_curie: ClassVar[str] = "cim:BasicIntervalSchedule"
    class_name: ClassVar[str] = "BasicIntervalSchedule"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BasicIntervalSchedule

    startTime: Optional[Union[str, XSDDateTime]] = None
    value1Description: Optional[str] = None
    value1Multiplier: Optional[Union[str, "UnitMultiplier"]] = None
    value1Unit: Optional[Union[str, "UnitSymbol"]] = None
    value2Description: Optional[str] = None
    value2Multiplier: Optional[Union[str, "UnitMultiplier"]] = None
    value2Unit: Optional[Union[str, "UnitSymbol"]] = None
    value3Description: Optional[str] = None
    value3Multiplier: Optional[Union[str, "UnitMultiplier"]] = None
    value3Unit: Optional[Union[str, "UnitSymbol"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.startTime is not None and not isinstance(self.startTime, XSDDateTime):
            self.startTime = XSDDateTime(self.startTime)

        if self.value1Description is not None and not isinstance(self.value1Description, str):
            self.value1Description = str(self.value1Description)

        if self.value1Multiplier is not None and not isinstance(self.value1Multiplier, UnitMultiplier):
            self.value1Multiplier = UnitMultiplier(self.value1Multiplier)

        if self.value1Unit is not None and not isinstance(self.value1Unit, UnitSymbol):
            self.value1Unit = UnitSymbol(self.value1Unit)

        if self.value2Description is not None and not isinstance(self.value2Description, str):
            self.value2Description = str(self.value2Description)

        if self.value2Multiplier is not None and not isinstance(self.value2Multiplier, UnitMultiplier):
            self.value2Multiplier = UnitMultiplier(self.value2Multiplier)

        if self.value2Unit is not None and not isinstance(self.value2Unit, UnitSymbol):
            self.value2Unit = UnitSymbol(self.value2Unit)

        if self.value3Description is not None and not isinstance(self.value3Description, str):
            self.value3Description = str(self.value3Description)

        if self.value3Multiplier is not None and not isinstance(self.value3Multiplier, UnitMultiplier):
            self.value3Multiplier = UnitMultiplier(self.value3Multiplier)

        if self.value3Unit is not None and not isinstance(self.value3Unit, UnitSymbol):
            self.value3Unit = UnitSymbol(self.value3Unit)

        super().__post_init__(**kwargs)


class BilateralExchangeActor(IdentifiedObject):
    """
    BilateralExchangeActor describes an actor that provides ICCP data, consumes ICCP data or both. The ICCP data
    provider lists the data it makes available to an ICCP data consumer. This data is described by
    ProvidedBilateralPoints. The relation between an ICCP data provider and a consumer is established by a
    BilateralExchangeAgreement. It is up to the ICCP data consumer to select what ProvidedBilateralPoints to use. The
    selection made is not described in this information model.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BilateralExchangeActor"]
    class_class_curie: ClassVar[str] = "cim:BilateralExchangeActor"
    class_name: ClassVar[str] = "BilateralExchangeActor"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BilateralExchangeActor


@dataclass(repr=False)
class BranchGroup(IdentifiedObject):
    """
    A group of branch terminals whose directed flow summation is to be monitored. A branch group need not form a
    cutset of the network.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BranchGroup"]
    class_class_curie: ClassVar[str] = "cim:BranchGroup"
    class_name: ClassVar[str] = "BranchGroup"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BranchGroup

    maximumActivePower: Optional[float] = None
    maximumReactivePower: Optional[float] = None
    minimumActivePower: Optional[float] = None
    minimumReactivePower: Optional[float] = None
    monitorActivePower: Optional[Union[bool, Bool]] = None
    monitorReactivePower: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.maximumActivePower is not None and not isinstance(self.maximumActivePower, float):
            self.maximumActivePower = float(self.maximumActivePower)

        if self.maximumReactivePower is not None and not isinstance(self.maximumReactivePower, float):
            self.maximumReactivePower = float(self.maximumReactivePower)

        if self.minimumActivePower is not None and not isinstance(self.minimumActivePower, float):
            self.minimumActivePower = float(self.minimumActivePower)

        if self.minimumReactivePower is not None and not isinstance(self.minimumReactivePower, float):
            self.minimumReactivePower = float(self.minimumReactivePower)

        if self.monitorActivePower is not None and not isinstance(self.monitorActivePower, Bool):
            self.monitorActivePower = Bool(self.monitorActivePower)

        if self.monitorReactivePower is not None and not isinstance(self.monitorReactivePower, Bool):
            self.monitorReactivePower = Bool(self.monitorReactivePower)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BundleConfiguration(AssetInfo):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BundleConfiguration"]
    class_class_curie: ClassVar[str] = "cim:BundleConfiguration"
    class_name: ClassVar[str] = "BundleConfiguration"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BundleConfiguration

    conductorCount: Optional[int] = None
    conductorSpacing: Optional[float] = None
    gmr: Optional[float] = None
    radius: Optional[float] = None
    WireInfo: Optional[Union[dict, "WireInfo"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.conductorCount is not None and not isinstance(self.conductorCount, int):
            self.conductorCount = int(self.conductorCount)

        if self.conductorSpacing is not None and not isinstance(self.conductorSpacing, float):
            self.conductorSpacing = float(self.conductorSpacing)

        if self.gmr is not None and not isinstance(self.gmr, float):
            self.gmr = float(self.gmr)

        if self.radius is not None and not isinstance(self.radius, float):
            self.radius = float(self.radius)

        if self.WireInfo is not None and not isinstance(self.WireInfo, WireInfo):
            self.WireInfo = WireInfo(**as_dict(self.WireInfo))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BusNameMarker(IdentifiedObject):
    """
    Used to apply user standard names to TopologicalNodes. Associated with one or more terminals that are normally
    connected with the bus name. The associated terminals are normally connected by non-retained switches. For a ring
    bus station configuration, all BusbarSection terminals in the ring are typically associated. For a breaker and a
    half scheme, both BusbarSections would normally be associated. For a ring bus, all BusbarSections would normally
    be associated. For a straight busbar configuration, normally only the main terminal at the BusbarSection would be
    associated.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BusNameMarker"]
    class_class_curie: ClassVar[str] = "cim:BusNameMarker"
    class_name: ClassVar[str] = "BusNameMarker"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BusNameMarker

    priority: Optional[int] = None
    ReportingGroup: Optional[Union[dict, "ReportingGroup"]] = None
    TopologicalNode: Optional[Union[dict, "TopologicalNode"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.priority is not None and not isinstance(self.priority, int):
            self.priority = int(self.priority)

        if self.ReportingGroup is not None and not isinstance(self.ReportingGroup, ReportingGroup):
            self.ReportingGroup = ReportingGroup(**as_dict(self.ReportingGroup))

        if self.TopologicalNode is not None and not isinstance(self.TopologicalNode, TopologicalNode):
            self.TopologicalNode = TopologicalNode(**as_dict(self.TopologicalNode))

        super().__post_init__(**kwargs)


class Bushing(Asset):
    """
    Bushing asset.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Bushing"]
    class_class_curie: ClassVar[str] = "cim:Bushing"
    class_name: ClassVar[str] = "Bushing"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Bushing


class CalculationMethodHierarchy(IdentifiedObject):
    """
    The hierarchy of calculation methods used to derive this measurement.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["CalculationMethodHierarchy"]
    class_class_curie: ClassVar[str] = "cim:CalculationMethodHierarchy"
    class_name: ClassVar[str] = "CalculationMethodHierarchy"
    class_model_uri: ClassVar[URIRef] = CIMTBL.CalculationMethodHierarchy


@dataclass(repr=False)
class CatalogAssetType(IdentifiedObject):
    """
    a Assets that may be used for planning, work or design purposes.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["CatalogAssetType"]
    class_class_curie: ClassVar[str] = "cim:CatalogAssetType"
    class_name: ClassVar[str] = "CatalogAssetType"
    class_model_uri: ClassVar[URIRef] = CIMTBL.CatalogAssetType

    estimatedUnitCost: Optional[Decimal] = None
    kind: Optional[Union[str, "AssetKind"]] = None
    stockItem: Optional[Union[bool, Bool]] = None
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.estimatedUnitCost is not None and not isinstance(self.estimatedUnitCost, Decimal):
            self.estimatedUnitCost = Decimal(self.estimatedUnitCost)

        if self.kind is not None and not isinstance(self.kind, AssetKind):
            self.kind = AssetKind(self.kind)

        if self.stockItem is not None and not isinstance(self.stockItem, Bool):
            self.stockItem = Bool(self.stockItem)

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)


class ChargingConnectorInfo(AssetInfo):
    """
    Datasheet for charging connectors used within a charging station and electric vehicles
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ChargingConnectorInfo"]
    class_class_curie: ClassVar[str] = "cim:ChargingConnectorInfo"
    class_name: ClassVar[str] = "ChargingConnectorInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ChargingConnectorInfo


@dataclass(repr=False)
class ChargingStation(Asset):
    """
    Physical equipment consisting of one or more EV supply equipment managing the energy transfer to and from EVs.
    [IEC 63382-1]
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ChargingStation"]
    class_class_curie: ClassVar[str] = "cim:ChargingStation"
    class_name: ClassVar[str] = "ChargingStation"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ChargingStation

    networkProvider: Optional[str] = None
    operatorName: Optional[str] = None
    paymentMethods: Optional[str] = None
    phoneSupport: Optional[str] = None
    weatherProtection: Optional[Union[bool, Bool]] = None
    ChargingConnector: Optional[Union[dict, ChargingConnectorInfo]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.networkProvider is not None and not isinstance(self.networkProvider, str):
            self.networkProvider = str(self.networkProvider)

        if self.operatorName is not None and not isinstance(self.operatorName, str):
            self.operatorName = str(self.operatorName)

        if self.paymentMethods is not None and not isinstance(self.paymentMethods, str):
            self.paymentMethods = str(self.paymentMethods)

        if self.phoneSupport is not None and not isinstance(self.phoneSupport, str):
            self.phoneSupport = str(self.phoneSupport)

        if self.weatherProtection is not None and not isinstance(self.weatherProtection, Bool):
            self.weatherProtection = Bool(self.weatherProtection)

        if self.ChargingConnector is not None and not isinstance(self.ChargingConnector, ChargingConnectorInfo):
            self.ChargingConnector = ChargingConnectorInfo(**as_dict(self.ChargingConnector))

        super().__post_init__(**kwargs)


class Company(IdentifiedObject):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Company"]
    class_class_curie: ClassVar[str] = "cim:Company"
    class_name: ClassVar[str] = "Company"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Company


@dataclass(repr=False)
class ConductingAssetInfo(AssetInfo):
    """
    Generic information for conducting asset
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ConductingAssetInfo"]
    class_class_curie: ClassVar[str] = "cim:ConductingAssetInfo"
    class_name: ClassVar[str] = "ConductingAssetInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConductingAssetInfo

    phaseCount: Optional[Union[str, "PhaseCountKind"]] = None
    ratedCurrent: Optional[float] = None
    ratedFrequency: Optional[float] = None
    ratedVoltage: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.phaseCount is not None and not isinstance(self.phaseCount, PhaseCountKind):
            self.phaseCount = PhaseCountKind(self.phaseCount)

        if self.ratedCurrent is not None and not isinstance(self.ratedCurrent, float):
            self.ratedCurrent = float(self.ratedCurrent)

        if self.ratedFrequency is not None and not isinstance(self.ratedFrequency, float):
            self.ratedFrequency = float(self.ratedFrequency)

        if self.ratedVoltage is not None and not isinstance(self.ratedVoltage, float):
            self.ratedVoltage = float(self.ratedVoltage)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ConductorDistance(AssetInfo):
    """
    Distance from
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ConductorDistance"]
    class_class_curie: ClassVar[str] = "cim:ConductorDistance"
    class_name: ClassVar[str] = "ConductorDistance"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConductorDistance

    distance: Optional[float] = None
    fromPhase: Optional[Union[str, "SinglePhaseKind"]] = None
    fromSequenceNumber: Optional[int] = None
    toPhase: Optional[Union[str, "SinglePhaseKind"]] = None
    toSequenceNumber: Optional[int] = None
    WireSpacing: Optional[Union[dict, "ConductorDistanceSpacing"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.distance is not None and not isinstance(self.distance, float):
            self.distance = float(self.distance)

        if self.fromPhase is not None and not isinstance(self.fromPhase, SinglePhaseKind):
            self.fromPhase = SinglePhaseKind(self.fromPhase)

        if self.fromSequenceNumber is not None and not isinstance(self.fromSequenceNumber, int):
            self.fromSequenceNumber = int(self.fromSequenceNumber)

        if self.toPhase is not None and not isinstance(self.toPhase, SinglePhaseKind):
            self.toPhase = SinglePhaseKind(self.toPhase)

        if self.toSequenceNumber is not None and not isinstance(self.toSequenceNumber, int):
            self.toSequenceNumber = int(self.toSequenceNumber)

        if self.WireSpacing is not None and not isinstance(self.WireSpacing, ConductorDistanceSpacing):
            self.WireSpacing = ConductorDistanceSpacing()

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ConductorInfo(ConductingAssetInfo):
    """
    Common class for rigid and flexible conductors.[IEC 826-14-06]: Conductive part intended to carry a specified
    electric current
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ConductorInfo"]
    class_class_curie: ClassVar[str] = "cim:ConductorInfo"
    class_name: ClassVar[str] = "ConductorInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConductorInfo

    crossSection: Optional[float] = None
    material: Optional[Union[str, "WireMaterialKind"]] = None
    purpose: Optional[str] = None
    rAC25: Optional[float] = None
    rAC50: Optional[float] = None
    rAC75: Optional[float] = None
    rDC20: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.crossSection is not None and not isinstance(self.crossSection, float):
            self.crossSection = float(self.crossSection)

        if self.material is not None and not isinstance(self.material, WireMaterialKind):
            self.material = WireMaterialKind(self.material)

        if self.purpose is not None and not isinstance(self.purpose, str):
            self.purpose = str(self.purpose)

        if self.rAC25 is not None and not isinstance(self.rAC25, float):
            self.rAC25 = float(self.rAC25)

        if self.rAC50 is not None and not isinstance(self.rAC50, float):
            self.rAC50 = float(self.rAC50)

        if self.rAC75 is not None and not isinstance(self.rAC75, float):
            self.rAC75 = float(self.rAC75)

        if self.rDC20 is not None and not isinstance(self.rDC20, float):
            self.rDC20 = float(self.rDC20)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AngleBusbarInfo(ConductorInfo):
    """
    L-shape bar with both legs of uniform thickness and same width
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["AngleBusbarInfo"]
    class_class_curie: ClassVar[str] = "cim:AngleBusbarInfo"
    class_name: ClassVar[str] = "AngleBusbarInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.AngleBusbarInfo

    crossSectionWidth: Optional[float] = None
    thickness: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.crossSectionWidth is not None and not isinstance(self.crossSectionWidth, float):
            self.crossSectionWidth = float(self.crossSectionWidth)

        if self.thickness is not None and not isinstance(self.thickness, float):
            self.thickness = float(self.thickness)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ConnectivityNode(IdentifiedObject):
    """
    Connectivity nodes are points where terminals of AC conducting equipment are connected together with zero
    impedance.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ConnectivityNode"]
    class_class_curie: ClassVar[str] = "cim:ConnectivityNode"
    class_name: ClassVar[str] = "ConnectivityNode"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConnectivityNode

    ACPointOfCommonCoupling: Optional[Union[dict, ACPointOfCommonCoupling]] = None
    BaseVoltage: Optional[Union[dict, BaseVoltage]] = None
    BoundaryPoint: Optional[Union[dict, "BoundaryPoint"]] = None
    ConnectivityNodeContainer: Optional[Union[dict, "ConnectivityNodeContainer"]] = None
    IndividualPnode: Optional[Union[dict, "IndividualPnode"]] = None
    TopologicalNode: Optional[Union[dict, "TopologicalNode"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.ACPointOfCommonCoupling is not None and not isinstance(self.ACPointOfCommonCoupling, ACPointOfCommonCoupling):
            self.ACPointOfCommonCoupling = ACPointOfCommonCoupling(**as_dict(self.ACPointOfCommonCoupling))

        if self.BaseVoltage is not None and not isinstance(self.BaseVoltage, BaseVoltage):
            self.BaseVoltage = BaseVoltage(**as_dict(self.BaseVoltage))

        if self.BoundaryPoint is not None and not isinstance(self.BoundaryPoint, BoundaryPoint):
            self.BoundaryPoint = BoundaryPoint(**as_dict(self.BoundaryPoint))

        if self.ConnectivityNodeContainer is not None and not isinstance(self.ConnectivityNodeContainer, ConnectivityNodeContainer):
            self.ConnectivityNodeContainer = ConnectivityNodeContainer(**as_dict(self.ConnectivityNodeContainer))

        if self.IndividualPnode is not None and not isinstance(self.IndividualPnode, IndividualPnode):
            self.IndividualPnode = IndividualPnode(**as_dict(self.IndividualPnode))

        if self.TopologicalNode is not None and not isinstance(self.TopologicalNode, TopologicalNode):
            self.TopologicalNode = TopologicalNode(**as_dict(self.TopologicalNode))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ControlAreaGeneratingUnit(IdentifiedObject):
    """
    A control area generating unit. This class is needed so that alternate control area definitions may include the
    same generating unit. It should be noted that only one instance within a control area should reference a specific
    generating unit.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ControlAreaGeneratingUnit"]
    class_class_curie: ClassVar[str] = "cim:ControlAreaGeneratingUnit"
    class_name: ClassVar[str] = "ControlAreaGeneratingUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ControlAreaGeneratingUnit

    ControlArea: Optional[Union[dict, "ControlArea"]] = None
    GeneratingUnit: Optional[Union[dict, "GeneratingUnit"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.ControlArea is not None and not isinstance(self.ControlArea, ControlArea):
            self.ControlArea = ControlArea(**as_dict(self.ControlArea))

        if self.GeneratingUnit is not None and not isinstance(self.GeneratingUnit, GeneratingUnit):
            self.GeneratingUnit = GeneratingUnit(**as_dict(self.GeneratingUnit))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ControlAreaPowerElectronicsUnit(IdentifiedObject):
    """
    A control area power electronics unit. This class is needed so that alternate control area definitions may include
    the same power electronics unit. It should be noted that only one instance within a control area should reference
    a specific power electronics unit.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ControlAreaPowerElectronicsUnit"]
    class_class_curie: ClassVar[str] = "cim:ControlAreaPowerElectronicsUnit"
    class_name: ClassVar[str] = "ControlAreaPowerElectronicsUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ControlAreaPowerElectronicsUnit

    ControlArea: Optional[Union[dict, "ControlArea"]] = None
    PowerElectronicsUnit: Optional[Union[dict, "PowerElectronicsUnit"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.ControlArea is not None and not isinstance(self.ControlArea, ControlArea):
            self.ControlArea = ControlArea(**as_dict(self.ControlArea))

        if self.PowerElectronicsUnit is not None and not isinstance(self.PowerElectronicsUnit, PowerElectronicsUnit):
            self.PowerElectronicsUnit = PowerElectronicsUnit(**as_dict(self.PowerElectronicsUnit))

        super().__post_init__(**kwargs)


class CoupledLineSegmentGroup(IdentifiedObject):
    """
    Aggregates a set of line segments that are on the same tower, or in the same right-of-way, close enough that
    mutual coupling impedances between the lines need to be included in network analysis.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["CoupledLineSegmentGroup"]
    class_class_curie: ClassVar[str] = "cim:CoupledLineSegmentGroup"
    class_name: ClassVar[str] = "CoupledLineSegmentGroup"
    class_model_uri: ClassVar[URIRef] = CIMTBL.CoupledLineSegmentGroup


@dataclass(repr=False)
class CurrentDroopControlFunction(IdentifiedObject):
    """
    Current droop control function is a function block that calculates the operating point of the controlled equipment
    to achieve the target current.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["CurrentDroopControlFunction"]
    class_class_curie: ClassVar[str] = "cim:CurrentDroopControlFunction"
    class_name: ClassVar[str] = "CurrentDroopControlFunction"
    class_model_uri: ClassVar[URIRef] = CIMTBL.CurrentDroopControlFunction

    droopCapacitive: Optional[float] = None
    droopInductive: Optional[float] = None
    offsetCapacitive: Optional[float] = None
    offsetInductive: Optional[float] = None
    targetValueCapacitive: Optional[float] = None
    targetValueInductive: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.droopCapacitive is not None and not isinstance(self.droopCapacitive, float):
            self.droopCapacitive = float(self.droopCapacitive)

        if self.droopInductive is not None and not isinstance(self.droopInductive, float):
            self.droopInductive = float(self.droopInductive)

        if self.offsetCapacitive is not None and not isinstance(self.offsetCapacitive, float):
            self.offsetCapacitive = float(self.offsetCapacitive)

        if self.offsetInductive is not None and not isinstance(self.offsetInductive, float):
            self.offsetInductive = float(self.offsetInductive)

        if self.targetValueCapacitive is not None and not isinstance(self.targetValueCapacitive, float):
            self.targetValueCapacitive = float(self.targetValueCapacitive)

        if self.targetValueInductive is not None and not isinstance(self.targetValueInductive, float):
            self.targetValueInductive = float(self.targetValueInductive)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Curve(IdentifiedObject):
    """
    A multi-purpose curve or functional relationship between an independent variable (X-axis) and dependent (Y-axis)
    variables.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Curve"]
    class_class_curie: ClassVar[str] = "cim:Curve"
    class_name: ClassVar[str] = "Curve"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Curve

    curveStyle: Optional[Union[str, "CurveStyle"]] = None
    xMultiplier: Optional[Union[str, "UnitMultiplier"]] = None
    xUnit: Optional[Union[str, "UnitSymbol"]] = None
    y1Multiplier: Optional[Union[str, "UnitMultiplier"]] = None
    y1Unit: Optional[Union[str, "UnitSymbol"]] = None
    y2Multiplier: Optional[Union[str, "UnitMultiplier"]] = None
    y2Unit: Optional[Union[str, "UnitSymbol"]] = None
    y3Multiplier: Optional[Union[str, "UnitMultiplier"]] = None
    y3Unit: Optional[Union[str, "UnitSymbol"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.curveStyle is not None and not isinstance(self.curveStyle, CurveStyle):
            self.curveStyle = CurveStyle(self.curveStyle)

        if self.xMultiplier is not None and not isinstance(self.xMultiplier, UnitMultiplier):
            self.xMultiplier = UnitMultiplier(self.xMultiplier)

        if self.xUnit is not None and not isinstance(self.xUnit, UnitSymbol):
            self.xUnit = UnitSymbol(self.xUnit)

        if self.y1Multiplier is not None and not isinstance(self.y1Multiplier, UnitMultiplier):
            self.y1Multiplier = UnitMultiplier(self.y1Multiplier)

        if self.y1Unit is not None and not isinstance(self.y1Unit, UnitSymbol):
            self.y1Unit = UnitSymbol(self.y1Unit)

        if self.y2Multiplier is not None and not isinstance(self.y2Multiplier, UnitMultiplier):
            self.y2Multiplier = UnitMultiplier(self.y2Multiplier)

        if self.y2Unit is not None and not isinstance(self.y2Unit, UnitSymbol):
            self.y2Unit = UnitSymbol(self.y2Unit)

        if self.y3Multiplier is not None and not isinstance(self.y3Multiplier, UnitMultiplier):
            self.y3Multiplier = UnitMultiplier(self.y3Multiplier)

        if self.y3Unit is not None and not isinstance(self.y3Unit, UnitSymbol):
            self.y3Unit = UnitSymbol(self.y3Unit)

        super().__post_init__(**kwargs)


class AmbientTemperatureDependencyCurve(Curve):
    """
    A curve or functional relationship between the ambient temperature independent variable (X-axis) and relative
    temperature dependent (Y-axis) variables.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["AmbientTemperatureDependencyCurve"]
    class_class_curie: ClassVar[str] = "cim:AmbientTemperatureDependencyCurve"
    class_name: ClassVar[str] = "AmbientTemperatureDependencyCurve"
    class_model_uri: ClassVar[URIRef] = CIMTBL.AmbientTemperatureDependencyCurve


class BaseOverloadLimitCurve(Curve):
    """
    A curve or functional relationship between- the relative loading - current loading over permanent loading (PATL)
    independent variable (X-axis), and- temporary overloading (TATL) limiting dependent (Y-axis) variables.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BaseOverloadLimitCurve"]
    class_class_curie: ClassVar[str] = "cim:BaseOverloadLimitCurve"
    class_name: ClassVar[str] = "BaseOverloadLimitCurve"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BaseOverloadLimitCurve


class ConductorCharacteristicCurve(Curve):
    """
    Class to associate damage curves to conductors or to their datasheets.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ConductorCharacteristicCurve"]
    class_class_curie: ClassVar[str] = "cim:ConductorCharacteristicCurve"
    class_name: ClassVar[str] = "ConductorCharacteristicCurve"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConductorCharacteristicCurve


class CutAction(IdentifiedObject):
    """
    Action on cut as a switching step.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["CutAction"]
    class_class_curie: ClassVar[str] = "cim:CutAction"
    class_name: ClassVar[str] = "CutAction"
    class_model_uri: ClassVar[URIRef] = CIMTBL.CutAction


class DCConductingAssetInfo(AssetInfo):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["DCConductingAssetInfo"]
    class_class_curie: ClassVar[str] = "cim:DCConductingAssetInfo"
    class_name: ClassVar[str] = "DCConductingAssetInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.DCConductingAssetInfo


@dataclass(repr=False)
class BatteryInfo(DCConductingAssetInfo):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BatteryInfo"]
    class_class_curie: ClassVar[str] = "cim:BatteryInfo"
    class_name: ClassVar[str] = "BatteryInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BatteryInfo

    batteryType: Optional[Union[str, "BatteryTypeKind"]] = None
    cellChemistry: Optional[str] = None
    numberOfCells: Optional[int] = None
    ratedCapacity: Optional[float] = None
    usableCapacity: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.batteryType is not None and not isinstance(self.batteryType, BatteryTypeKind):
            self.batteryType = BatteryTypeKind(self.batteryType)

        if self.cellChemistry is not None and not isinstance(self.cellChemistry, str):
            self.cellChemistry = str(self.cellChemistry)

        if self.numberOfCells is not None and not isinstance(self.numberOfCells, int):
            self.numberOfCells = int(self.numberOfCells)

        if self.ratedCapacity is not None and not isinstance(self.ratedCapacity, float):
            self.ratedCapacity = float(self.ratedCapacity)

        if self.usableCapacity is not None and not isinstance(self.usableCapacity, float):
            self.usableCapacity = float(self.usableCapacity)

        super().__post_init__(**kwargs)


class DCTerminal(ACDCTerminal):
    """
    An electrical connection point to generic DC conducting equipment.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["DCTerminal"]
    class_class_curie: ClassVar[str] = "cim:DCTerminal"
    class_name: ClassVar[str] = "DCTerminal"
    class_model_uri: ClassVar[URIRef] = CIMTBL.DCTerminal


class DCTopologicalNode(IdentifiedObject):
    """
    DC bus.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["DCTopologicalNode"]
    class_class_curie: ClassVar[str] = "cim:DCTopologicalNode"
    class_name: ClassVar[str] = "DCTopologicalNode"
    class_model_uri: ClassVar[URIRef] = CIMTBL.DCTopologicalNode


class DayType(IdentifiedObject):
    """
    Group of similar days.   For example it could be used to represent weekdays, weekend, or holidays.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["DayType"]
    class_class_curie: ClassVar[str] = "cim:DayType"
    class_name: ClassVar[str] = "DayType"
    class_model_uri: ClassVar[URIRef] = CIMTBL.DayType


class DesignElement(IdentifiedObject):
    """
    An element of a design that places a compatible unit or an asset at a specific design  location
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["DesignElement"]
    class_class_curie: ClassVar[str] = "cim:DesignElement"
    class_name: ClassVar[str] = "DesignElement"
    class_model_uri: ClassVar[URIRef] = CIMTBL.DesignElement


@dataclass(repr=False)
class DuctBank(Asset):
    """
    A duct contains individual wires in the layout as specified with associated wire spacing instances; number of them
    gives the number of conductors in this duct.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["DuctBank"]
    class_class_curie: ClassVar[str] = "cim:DuctBank"
    class_name: ClassVar[str] = "DuctBank"
    class_model_uri: ClassVar[URIRef] = CIMTBL.DuctBank

    circuitCount: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.circuitCount is not None and not isinstance(self.circuitCount, int):
            self.circuitCount = int(self.circuitCount)

        super().__post_init__(**kwargs)


class DurationOverloadLimitCurve(Curve):
    """
    A curve or functional relationship between- the overload duration independent variable (X-axis), and- temporary
    overloading (TATL) limiting dependent (Y-axis) variables.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["DurationOverloadLimitCurve"]
    class_class_curie: ClassVar[str] = "cim:DurationOverloadLimitCurve"
    class_name: ClassVar[str] = "DurationOverloadLimitCurve"
    class_model_uri: ClassVar[URIRef] = CIMTBL.DurationOverloadLimitCurve


@dataclass(repr=False)
class EarthResistivity(IdentifiedObject):
    """
    Resistance of earth (soil)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EarthResistivity"]
    class_class_curie: ClassVar[str] = "cim:EarthResistivity"
    class_name: ClassVar[str] = "EarthResistivity"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EarthResistivity

    earthModelType: Optional[Union[str, "EarthModelKind"]] = None
    earthReturnGMR: Optional[float] = None
    rho: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.earthModelType is not None and not isinstance(self.earthModelType, EarthModelKind):
            self.earthModelType = EarthModelKind(self.earthModelType)

        if self.earthReturnGMR is not None and not isinstance(self.earthReturnGMR, float):
            self.earthReturnGMR = float(self.earthReturnGMR)

        if self.rho is not None and not isinstance(self.rho, float):
            self.rho = float(self.rho)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EnergyArea(IdentifiedObject):
    """
    Describes an area having energy production or consumption. Specializations are intended to support the load
    allocation function as typically required in energy management systems or planning studies to allocate
    hypothesized load levels to individual load points for power flow analysis. Often the energy area can be linked to
    both measured and forecast load levels.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EnergyArea"]
    class_class_curie: ClassVar[str] = "cim:EnergyArea"
    class_name: ClassVar[str] = "EnergyArea"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EnergyArea

    ControlArea: Optional[Union[dict, "ControlArea"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.ControlArea is not None and not isinstance(self.ControlArea, ControlArea):
            self.ControlArea = ControlArea(**as_dict(self.ControlArea))

        super().__post_init__(**kwargs)


class EnergyConsumerAction(IdentifiedObject):
    """
    Action to connect or disconnect the Energy Consumer from its Terminal
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EnergyConsumerAction"]
    class_class_curie: ClassVar[str] = "cim:EnergyConsumerAction"
    class_name: ClassVar[str] = "EnergyConsumerAction"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EnergyConsumerAction


class EnergySchedulingType(IdentifiedObject):
    """
    Used to define the type of generation for scheduling purposes.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EnergySchedulingType"]
    class_class_curie: ClassVar[str] = "cim:EnergySchedulingType"
    class_name: ClassVar[str] = "EnergySchedulingType"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EnergySchedulingType


class EnergySourceAction(IdentifiedObject):
    """
    Action on energy source as a switching step.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EnergySourceAction"]
    class_class_curie: ClassVar[str] = "cim:EnergySourceAction"
    class_name: ClassVar[str] = "EnergySourceAction"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EnergySourceAction


class EnergySourceModification(IdentifiedObject):
    """
    Energy source action.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EnergySourceModification"]
    class_class_curie: ClassVar[str] = "cim:EnergySourceModification"
    class_name: ClassVar[str] = "EnergySourceModification"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EnergySourceModification


@dataclass(repr=False)
class FossilFuel(IdentifiedObject):
    """
    The fossil fuel consumed by the non-nuclear thermal generating unit. For example, coal, oil, gas, etc. These are
    the specific fuels that the generating unit can consume.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["FossilFuel"]
    class_class_curie: ClassVar[str] = "cim:FossilFuel"
    class_name: ClassVar[str] = "FossilFuel"
    class_model_uri: ClassVar[URIRef] = CIMTBL.FossilFuel

    fossilFuelType: Optional[Union[str, "FuelType"]] = None
    fuelCost: Optional[float] = None
    fuelDispatchCost: Optional[float] = None
    fuelEffFactor: Optional[float] = None
    fuelHandlingCost: Optional[float] = None
    fuelHeatContent: Optional[float] = None
    fuelMixture: Optional[float] = None
    fuelSulfur: Optional[float] = None
    highBreakpointP: Optional[float] = None
    lowBreakpointP: Optional[float] = None
    FuelStorage: Optional[Union[dict, "FuelStorage"]] = None
    ThermalGeneratingUnit: Optional[Union[dict, "ThermalGeneratingUnit"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.fossilFuelType is not None and not isinstance(self.fossilFuelType, FuelType):
            self.fossilFuelType = FuelType(self.fossilFuelType)

        if self.fuelCost is not None and not isinstance(self.fuelCost, float):
            self.fuelCost = float(self.fuelCost)

        if self.fuelDispatchCost is not None and not isinstance(self.fuelDispatchCost, float):
            self.fuelDispatchCost = float(self.fuelDispatchCost)

        if self.fuelEffFactor is not None and not isinstance(self.fuelEffFactor, float):
            self.fuelEffFactor = float(self.fuelEffFactor)

        if self.fuelHandlingCost is not None and not isinstance(self.fuelHandlingCost, float):
            self.fuelHandlingCost = float(self.fuelHandlingCost)

        if self.fuelHeatContent is not None and not isinstance(self.fuelHeatContent, float):
            self.fuelHeatContent = float(self.fuelHeatContent)

        if self.fuelMixture is not None and not isinstance(self.fuelMixture, float):
            self.fuelMixture = float(self.fuelMixture)

        if self.fuelSulfur is not None and not isinstance(self.fuelSulfur, float):
            self.fuelSulfur = float(self.fuelSulfur)

        if self.highBreakpointP is not None and not isinstance(self.highBreakpointP, float):
            self.highBreakpointP = float(self.highBreakpointP)

        if self.lowBreakpointP is not None and not isinstance(self.lowBreakpointP, float):
            self.lowBreakpointP = float(self.lowBreakpointP)

        if self.FuelStorage is not None and not isinstance(self.FuelStorage, FuelStorage):
            self.FuelStorage = FuelStorage(**as_dict(self.FuelStorage))

        if self.ThermalGeneratingUnit is not None and not isinstance(self.ThermalGeneratingUnit, ThermalGeneratingUnit):
            self.ThermalGeneratingUnit = ThermalGeneratingUnit(**as_dict(self.ThermalGeneratingUnit))

        super().__post_init__(**kwargs)


class FuseCharacteristicCurve(Curve):
    """
    This class represents the characteristic curve of fuse.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["FuseCharacteristicCurve"]
    class_class_curie: ClassVar[str] = "cim:FuseCharacteristicCurve"
    class_name: ClassVar[str] = "FuseCharacteristicCurve"
    class_model_uri: ClassVar[URIRef] = CIMTBL.FuseCharacteristicCurve


class GeographicalRegion(IdentifiedObject):
    """
    A geographical region of a power system network model.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["GeographicalRegion"]
    class_class_curie: ClassVar[str] = "cim:GeographicalRegion"
    class_name: ClassVar[str] = "GeographicalRegion"
    class_model_uri: ClassVar[URIRef] = CIMTBL.GeographicalRegion


@dataclass(repr=False)
class GridEdgeDeviceInfo(ConductingAssetInfo):
    """
    A Grid Edge Device is any device that is connected to the power grid with the ability to produce, store, and/or
    variably consume electricity. This include devices like local generation (solar photovoltaic and wind), storage
    (chemical or electrical batteries), flexible loads (heading, cooling, lighting systems), and electric vehicles
    (essentially a combination of storage and flexible load)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["GridEdgeDeviceInfo"]
    class_class_curie: ClassVar[str] = "cim:GridEdgeDeviceInfo"
    class_name: ClassVar[str] = "GridEdgeDeviceInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.GridEdgeDeviceInfo

    apparentPowerMaximum: Optional[float] = None
    ratedVoltageMax: Optional[float] = None
    ratedVoltageMin: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.apparentPowerMaximum is not None and not isinstance(self.apparentPowerMaximum, float):
            self.apparentPowerMaximum = float(self.apparentPowerMaximum)

        if self.ratedVoltageMax is not None and not isinstance(self.ratedVoltageMax, float):
            self.ratedVoltageMax = float(self.ratedVoltageMax)

        if self.ratedVoltageMin is not None and not isinstance(self.ratedVoltageMin, float):
            self.ratedVoltageMin = float(self.ratedVoltageMin)

        super().__post_init__(**kwargs)


class GroundAction(IdentifiedObject):
    """
    Action on ground as a switching step.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["GroundAction"]
    class_class_curie: ClassVar[str] = "cim:GroundAction"
    class_name: ClassVar[str] = "GroundAction"
    class_model_uri: ClassVar[URIRef] = CIMTBL.GroundAction


@dataclass(repr=False)
class IOPoint(IdentifiedObject):
    """
    The class describe a measurement or control value. The purpose is to enable having attributes and associations
    common for measurement and control.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["IOPoint"]
    class_class_curie: ClassVar[str] = "cim:IOPoint"
    class_name: ClassVar[str] = "IOPoint"
    class_model_uri: ClassVar[URIRef] = CIMTBL.IOPoint

    IOPointSource: Optional[Union[dict, "IOPointSource"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.IOPointSource is not None and not isinstance(self.IOPointSource, IOPointSource):
            self.IOPointSource = IOPointSource(**as_dict(self.IOPointSource))

        super().__post_init__(**kwargs)


class ImpedanceTapChangerTable(IdentifiedObject):
    """
    Describes a curve for how the power transformer end impedance varies with the tap step.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ImpedanceTapChangerTable"]
    class_class_curie: ClassVar[str] = "cim:ImpedanceTapChangerTable"
    class_name: ClassVar[str] = "ImpedanceTapChangerTable"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ImpedanceTapChangerTable


@dataclass(repr=False)
class ImpedanceTapChangerTablePoint(YAMLRoot):
    """
    Describes each tap step in the impedance tap changer tabular curve.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ImpedanceTapChangerTablePoint"]
    class_class_curie: ClassVar[str] = "cim:ImpedanceTapChangerTablePoint"
    class_name: ClassVar[str] = "ImpedanceTapChangerTablePoint"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ImpedanceTapChangerTablePoint

    angle: Optional[float] = None
    ratio: Optional[float] = None
    rEnd1: Optional[float] = None
    rEnd2: Optional[float] = None
    rEnd3: Optional[float] = None
    step: Optional[int] = None
    xEnd1: Optional[float] = None
    xEnd2: Optional[float] = None
    xEnd3: Optional[float] = None
    ImpedanceTapChangerTable: Optional[Union[dict, ImpedanceTapChangerTable]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.angle is not None and not isinstance(self.angle, float):
            self.angle = float(self.angle)

        if self.ratio is not None and not isinstance(self.ratio, float):
            self.ratio = float(self.ratio)

        if self.rEnd1 is not None and not isinstance(self.rEnd1, float):
            self.rEnd1 = float(self.rEnd1)

        if self.rEnd2 is not None and not isinstance(self.rEnd2, float):
            self.rEnd2 = float(self.rEnd2)

        if self.rEnd3 is not None and not isinstance(self.rEnd3, float):
            self.rEnd3 = float(self.rEnd3)

        if self.step is not None and not isinstance(self.step, int):
            self.step = int(self.step)

        if self.xEnd1 is not None and not isinstance(self.xEnd1, float):
            self.xEnd1 = float(self.xEnd1)

        if self.xEnd2 is not None and not isinstance(self.xEnd2, float):
            self.xEnd2 = float(self.xEnd2)

        if self.xEnd3 is not None and not isinstance(self.xEnd3, float):
            self.xEnd3 = float(self.xEnd3)

        if self.ImpedanceTapChangerTable is not None and not isinstance(self.ImpedanceTapChangerTable, ImpedanceTapChangerTable):
            self.ImpedanceTapChangerTable = ImpedanceTapChangerTable(**as_dict(self.ImpedanceTapChangerTable))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class IndividualPnode(IdentifiedObject):
    """
    Individual pricing node based on Pnode.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["IndividualPnode"]
    class_class_curie: ClassVar[str] = "cim:IndividualPnode"
    class_name: ClassVar[str] = "IndividualPnode"
    class_model_uri: ClassVar[URIRef] = CIMTBL.IndividualPnode

    ConnectivityNode: Optional[Union[dict, ConnectivityNode]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.ConnectivityNode is not None and not isinstance(self.ConnectivityNode, ConnectivityNode):
            self.ConnectivityNode = ConnectivityNode(**as_dict(self.ConnectivityNode))

        super().__post_init__(**kwargs)


class InstanceSet(YAMLRoot):
    """
    Instance of a version of a model part.   This corresponds to a payload of instance data.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["InstanceSet"]
    class_class_curie: ClassVar[str] = "cim:InstanceSet"
    class_name: ClassVar[str] = "InstanceSet"
    class_model_uri: ClassVar[URIRef] = CIMTBL.InstanceSet


@dataclass(repr=False)
class InsulationInfo(AssetInfo):
    """
    Wire data that can be specified per line segment phase, or for the line segment as a whole in case its phases all
    have the same wire characteristics.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["InsulationInfo"]
    class_class_curie: ClassVar[str] = "cim:InsulationInfo"
    class_name: ClassVar[str] = "InsulationInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.InsulationInfo

    insulated: Optional[Union[bool, Bool]] = None
    insulationMaterial: Optional[Union[str, "WireInsulationKind"]] = None
    insulationThickness: Optional[float] = None
    CableInfo: Optional[Union[dict, "CableInfo"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.insulated is not None and not isinstance(self.insulated, Bool):
            self.insulated = Bool(self.insulated)

        if self.insulationMaterial is not None and not isinstance(self.insulationMaterial, WireInsulationKind):
            self.insulationMaterial = WireInsulationKind(self.insulationMaterial)

        if self.insulationThickness is not None and not isinstance(self.insulationThickness, float):
            self.insulationThickness = float(self.insulationThickness)

        if self.CableInfo is not None and not isinstance(self.CableInfo, CableInfo):
            self.CableInfo = CableInfo(**as_dict(self.CableInfo))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class IntegerQuantity(YAMLRoot):
    """
    Quantity with integer value and associated unit information.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["IntegerQuantity"]
    class_class_curie: ClassVar[str] = "cim:IntegerQuantity"
    class_name: ClassVar[str] = "IntegerQuantity"
    class_model_uri: ClassVar[URIRef] = CIMTBL.IntegerQuantity

    multiplier: Optional[Union[str, "UnitMultiplier"]] = None
    unit: Optional[Union[str, "UnitSymbol"]] = None
    value: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.multiplier is not None and not isinstance(self.multiplier, UnitMultiplier):
            self.multiplier = UnitMultiplier(self.multiplier)

        if self.unit is not None and not isinstance(self.unit, UnitSymbol):
            self.unit = UnitSymbol(self.unit)

        if self.value is not None and not isinstance(self.value, int):
            self.value = int(self.value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class InverterCapabilities(YAMLRoot):
    """
    Based on IEEE 1547-2018 Table 28:<i>Supported control mode functions</i>Indication of support for each control
    mode function
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["InverterCapabilities"]
    class_class_curie: ClassVar[str] = "cim:InverterCapabilities"
    class_name: ClassVar[str] = "InverterCapabilities"
    class_model_uri: ClassVar[URIRef] = CIMTBL.InverterCapabilities

    isModeCapableActivePowerReactivePower: Optional[Union[bool, Bool]] = None
    isModeCapableConstantPowerFactor: Optional[Union[bool, Bool]] = None
    isModeCapableConstantReactivePower: Optional[Union[bool, Bool]] = None
    isModeCapableFrequencyActivePower: Optional[Union[bool, Bool]] = None
    isModeCapableVoltageActivePower: Optional[Union[bool, Bool]] = None
    isModeCapableVoltageReactivePower: Optional[Union[bool, Bool]] = None
    isProtectionCapableEnterServiceAfterTrip: Optional[Union[bool, Bool]] = None
    isProtectionCapableFrequencyTrip: Optional[Union[bool, Bool]] = None
    isProtectionCapableLimitActivePower: Optional[Union[bool, Bool]] = None
    isProtectionCapableMomentaryCessation: Optional[Union[bool, Bool]] = None
    isProtectionCapableVoltageTrip: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.isModeCapableActivePowerReactivePower is not None and not isinstance(self.isModeCapableActivePowerReactivePower, Bool):
            self.isModeCapableActivePowerReactivePower = Bool(self.isModeCapableActivePowerReactivePower)

        if self.isModeCapableConstantPowerFactor is not None and not isinstance(self.isModeCapableConstantPowerFactor, Bool):
            self.isModeCapableConstantPowerFactor = Bool(self.isModeCapableConstantPowerFactor)

        if self.isModeCapableConstantReactivePower is not None and not isinstance(self.isModeCapableConstantReactivePower, Bool):
            self.isModeCapableConstantReactivePower = Bool(self.isModeCapableConstantReactivePower)

        if self.isModeCapableFrequencyActivePower is not None and not isinstance(self.isModeCapableFrequencyActivePower, Bool):
            self.isModeCapableFrequencyActivePower = Bool(self.isModeCapableFrequencyActivePower)

        if self.isModeCapableVoltageActivePower is not None and not isinstance(self.isModeCapableVoltageActivePower, Bool):
            self.isModeCapableVoltageActivePower = Bool(self.isModeCapableVoltageActivePower)

        if self.isModeCapableVoltageReactivePower is not None and not isinstance(self.isModeCapableVoltageReactivePower, Bool):
            self.isModeCapableVoltageReactivePower = Bool(self.isModeCapableVoltageReactivePower)

        if self.isProtectionCapableEnterServiceAfterTrip is not None and not isinstance(self.isProtectionCapableEnterServiceAfterTrip, Bool):
            self.isProtectionCapableEnterServiceAfterTrip = Bool(self.isProtectionCapableEnterServiceAfterTrip)

        if self.isProtectionCapableFrequencyTrip is not None and not isinstance(self.isProtectionCapableFrequencyTrip, Bool):
            self.isProtectionCapableFrequencyTrip = Bool(self.isProtectionCapableFrequencyTrip)

        if self.isProtectionCapableLimitActivePower is not None and not isinstance(self.isProtectionCapableLimitActivePower, Bool):
            self.isProtectionCapableLimitActivePower = Bool(self.isProtectionCapableLimitActivePower)

        if self.isProtectionCapableMomentaryCessation is not None and not isinstance(self.isProtectionCapableMomentaryCessation, Bool):
            self.isProtectionCapableMomentaryCessation = Bool(self.isProtectionCapableMomentaryCessation)

        if self.isProtectionCapableVoltageTrip is not None and not isinstance(self.isProtectionCapableVoltageTrip, Bool):
            self.isProtectionCapableVoltageTrip = Bool(self.isProtectionCapableVoltageTrip)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class InverterInfo(GridEdgeDeviceInfo):
    """
    Inverter-based devices are a type of Grid Edge Device which convert DC sources (and/or sinks) into AC sources
    (and/or sinks) allowing for the power to be synchronized to the grid.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["InverterInfo"]
    class_class_curie: ClassVar[str] = "cim:InverterInfo"
    class_name: ClassVar[str] = "InverterInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.InverterInfo

    activePowerRatingOverExcited: Optional[float] = None
    activePowerRatingUnderExcited: Optional[float] = None
    activePowerRatingUnityPowerFactor: Optional[float] = None
    powerFactorOverExcited: Optional[float] = None
    powerFactorUnderExcited: Optional[float] = None
    reactivePowerAbsorbedMax: Optional[float] = None
    reactivePowerInjectedMax: Optional[float] = None
    susceptanceOffline: Optional[float] = None
    InverterCapabilites: Optional[Union[dict, InverterCapabilities]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.activePowerRatingOverExcited is not None and not isinstance(self.activePowerRatingOverExcited, float):
            self.activePowerRatingOverExcited = float(self.activePowerRatingOverExcited)

        if self.activePowerRatingUnderExcited is not None and not isinstance(self.activePowerRatingUnderExcited, float):
            self.activePowerRatingUnderExcited = float(self.activePowerRatingUnderExcited)

        if self.activePowerRatingUnityPowerFactor is not None and not isinstance(self.activePowerRatingUnityPowerFactor, float):
            self.activePowerRatingUnityPowerFactor = float(self.activePowerRatingUnityPowerFactor)

        if self.powerFactorOverExcited is not None and not isinstance(self.powerFactorOverExcited, float):
            self.powerFactorOverExcited = float(self.powerFactorOverExcited)

        if self.powerFactorUnderExcited is not None and not isinstance(self.powerFactorUnderExcited, float):
            self.powerFactorUnderExcited = float(self.powerFactorUnderExcited)

        if self.reactivePowerAbsorbedMax is not None and not isinstance(self.reactivePowerAbsorbedMax, float):
            self.reactivePowerAbsorbedMax = float(self.reactivePowerAbsorbedMax)

        if self.reactivePowerInjectedMax is not None and not isinstance(self.reactivePowerInjectedMax, float):
            self.reactivePowerInjectedMax = float(self.reactivePowerInjectedMax)

        if self.susceptanceOffline is not None and not isinstance(self.susceptanceOffline, float):
            self.susceptanceOffline = float(self.susceptanceOffline)

        if self.InverterCapabilites is not None and not isinstance(self.InverterCapabilites, InverterCapabilities):
            self.InverterCapabilites = InverterCapabilities(**as_dict(self.InverterCapabilites))

        super().__post_init__(**kwargs)


class IrregularIntervalSchedule(BasicIntervalSchedule):
    """
    The schedule has time points where the time between them varies.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["IrregularIntervalSchedule"]
    class_class_curie: ClassVar[str] = "cim:IrregularIntervalSchedule"
    class_name: ClassVar[str] = "IrregularIntervalSchedule"
    class_model_uri: ClassVar[URIRef] = CIMTBL.IrregularIntervalSchedule


@dataclass(repr=False)
class IrregularTimePoint(YAMLRoot):
    """
    TimePoints for a schedule where the time between the points varies.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["IrregularTimePoint"]
    class_class_curie: ClassVar[str] = "cim:IrregularTimePoint"
    class_name: ClassVar[str] = "IrregularTimePoint"
    class_model_uri: ClassVar[URIRef] = CIMTBL.IrregularTimePoint

    time: Optional[float] = None
    value1: Optional[float] = None
    value2: Optional[float] = None
    value3: Optional[float] = None
    IntervalSchedule: Optional[Union[dict, IrregularIntervalSchedule]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.time is not None and not isinstance(self.time, float):
            self.time = float(self.time)

        if self.value1 is not None and not isinstance(self.value1, float):
            self.value1 = float(self.value1)

        if self.value2 is not None and not isinstance(self.value2, float):
            self.value2 = float(self.value2)

        if self.value3 is not None and not isinstance(self.value3, float):
            self.value3 = float(self.value3)

        if self.IntervalSchedule is not None and not isinstance(self.IntervalSchedule, IrregularIntervalSchedule):
            self.IntervalSchedule = IrregularIntervalSchedule(**as_dict(self.IntervalSchedule))

        super().__post_init__(**kwargs)


class JumperAction(IdentifiedObject):
    """
    Action on jumper as a switching step.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["JumperAction"]
    class_class_curie: ClassVar[str] = "cim:JumperAction"
    class_name: ClassVar[str] = "JumperAction"
    class_model_uri: ClassVar[URIRef] = CIMTBL.JumperAction


@dataclass(repr=False)
class LineSegmentCoupling(IdentifiedObject):
    """
    Describes the relationship of a line in a coupled group to the reference line in the group. (Reference line has a
    coupledLineNumber = 1.)
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["LineSegmentCoupling"]
    class_class_curie: ClassVar[str] = "cim:LineSegmentCoupling"
    class_name: ClassVar[str] = "LineSegmentCoupling"
    class_model_uri: ClassVar[URIRef] = CIMTBL.LineSegmentCoupling

    coupledLineNumber: Optional[int] = None
    reverseFlow: Optional[Union[bool, Bool]] = None
    xOffset: Optional[float] = None
    ACLineSegment: Optional[Union[dict, "ACLineSegment"]] = None
    CoupledLineSegmentGroup: Optional[Union[dict, CoupledLineSegmentGroup]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.coupledLineNumber is not None and not isinstance(self.coupledLineNumber, int):
            self.coupledLineNumber = int(self.coupledLineNumber)

        if self.reverseFlow is not None and not isinstance(self.reverseFlow, Bool):
            self.reverseFlow = Bool(self.reverseFlow)

        if self.xOffset is not None and not isinstance(self.xOffset, float):
            self.xOffset = float(self.xOffset)

        if self.ACLineSegment is not None and not isinstance(self.ACLineSegment, ACLineSegment):
            self.ACLineSegment = ACLineSegment(**as_dict(self.ACLineSegment))

        if self.CoupledLineSegmentGroup is not None and not isinstance(self.CoupledLineSegmentGroup, CoupledLineSegmentGroup):
            self.CoupledLineSegmentGroup = CoupledLineSegmentGroup(**as_dict(self.CoupledLineSegmentGroup))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LoadArea(EnergyArea):
    """
    The class is the root or first level in a hierarchical structure for grouping of loads for the purpose of load
    flow load scaling.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["LoadArea"]
    class_class_curie: ClassVar[str] = "cim:LoadArea"
    class_name: ClassVar[str] = "LoadArea"
    class_model_uri: ClassVar[URIRef] = CIMTBL.LoadArea

    peakLoad: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.peakLoad is not None and not isinstance(self.peakLoad, float):
            self.peakLoad = float(self.peakLoad)

        super().__post_init__(**kwargs)


class LoadDynamics(IdentifiedObject):
    """
    Load whose behaviour is described by reference to a standard model <font color=#0f0f0f>or by definition of a
    user-defined model.</font>A standard feature of dynamic load behaviour modelling is the ability to associate the
    same behaviour to multiple energy consumers by means of a single load definition. The load model is always applied
    to individual bus loads (energy consumers).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["LoadDynamics"]
    class_class_curie: ClassVar[str] = "cim:LoadDynamics"
    class_name: ClassVar[str] = "LoadDynamics"
    class_model_uri: ClassVar[URIRef] = CIMTBL.LoadDynamics


@dataclass(repr=False)
class LoadGroup(IdentifiedObject):
    """
    The class is the third level in a hierarchical structure for grouping of loads for the purpose of load flow load
    scaling.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["LoadGroup"]
    class_class_curie: ClassVar[str] = "cim:LoadGroup"
    class_name: ClassVar[str] = "LoadGroup"
    class_model_uri: ClassVar[URIRef] = CIMTBL.LoadGroup

    SubLoadArea: Optional[Union[dict, "SubLoadArea"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.SubLoadArea is not None and not isinstance(self.SubLoadArea, SubLoadArea):
            self.SubLoadArea = SubLoadArea(**as_dict(self.SubLoadArea))

        super().__post_init__(**kwargs)


class ConformLoadGroup(LoadGroup):
    """
    A group of loads conforming to an allocation pattern.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ConformLoadGroup"]
    class_class_curie: ClassVar[str] = "cim:ConformLoadGroup"
    class_name: ClassVar[str] = "ConformLoadGroup"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConformLoadGroup


@dataclass(repr=False)
class LoadResponseCharacteristic(IdentifiedObject):
    """
    Models the characteristic response of the load demand due to changes in system conditions such as voltage and
    frequency. It is not related to demand response.If LoadResponseCharacteristic.exponentModel is True, the
    exponential voltage or frequency dependent models are specified and used as to calculate active and reactive power
    components of the load model.The equations to calculate active and reactive power components of the load model are
    internal to the power flow calculation, hence they use different quantities depending on the use case of the data
    exchange.The equations for exponential voltage dependent load model injected power are:pInjection= Pnominal*
    (Voltage/cim:BaseVoltage.nominalVoltage) ** cim:LoadResponseCharacteristic.pVoltageExponentqInjection= Qnominal*
    (Voltage/cim:BaseVoltage.nominalVoltage) ** cim:LoadResponseCharacteristic.qVoltageExponentpInjection = Pnominal*
    (Frequency/(Nominal frequency))**cim:LoadResponseCharacteristic.pFrequencyExponentqInjection = Qnominal*
    (Frequency/(Nominal frequency))**cim:LoadResponseCharacteristic.qFrequencyExponentNote that both voltage and
    frequency exponents could be used together so the full equation would be:pInjection = Pnominal*
    (Voltage/(cim:BaseVoltage.nominalVoltage))**cim:LoadResponseCharacteristic.pVoltageExponent * (Frequency/(base
    frequency))**cim:LoadResponseCharacteristic.pFrequencyExponentqInjection = Qnominal*
    (Voltage/(cim:BaseVoltage.nominalVoltage))**cim:LoadResponseCharacteristic.qVoltageExponent * (Frequency/(base
    frequency))**cim:LoadResponseCharacteristic.qFrequencyExponentThe voltage and frequency expressed in the equation
    are values obtained from solved power flow. Base voltage and base frequency are those derived from the
    connectivity of the static network model.Where:1) * means multiply and ** is raised to the power of;2) Pnominal
    and Qnominal represent the active power and reactive power at nominal voltage as any load described by the voltage
    exponential model shall be given at nominal voltage. This means that EnergyConsumer.p and EnergyConsumer.q are at
    nominal voltage.3) After power flow is solved:-pInjection and qInjection correspond to SvPowerflow.p and
    SvPowerflow.q respectively.- Voltage corresponds to SvVoltage.v at the TopologicalNode where the load is
    connected.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["LoadResponseCharacteristic"]
    class_class_curie: ClassVar[str] = "cim:LoadResponseCharacteristic"
    class_name: ClassVar[str] = "LoadResponseCharacteristic"
    class_model_uri: ClassVar[URIRef] = CIMTBL.LoadResponseCharacteristic

    exponentModel: Optional[Union[bool, Bool]] = None
    pConstantCurrent: Optional[float] = None
    pConstantImpedance: Optional[float] = None
    pConstantPower: Optional[float] = None
    pFrequencyExponent: Optional[float] = None
    pVoltageExponent: Optional[float] = None
    qConstantCurrent: Optional[float] = None
    qConstantImpedance: Optional[float] = None
    qConstantPower: Optional[float] = None
    qFrequencyExponent: Optional[float] = None
    qVoltageExponent: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.exponentModel is not None and not isinstance(self.exponentModel, Bool):
            self.exponentModel = Bool(self.exponentModel)

        if self.pConstantCurrent is not None and not isinstance(self.pConstantCurrent, float):
            self.pConstantCurrent = float(self.pConstantCurrent)

        if self.pConstantImpedance is not None and not isinstance(self.pConstantImpedance, float):
            self.pConstantImpedance = float(self.pConstantImpedance)

        if self.pConstantPower is not None and not isinstance(self.pConstantPower, float):
            self.pConstantPower = float(self.pConstantPower)

        if self.pFrequencyExponent is not None and not isinstance(self.pFrequencyExponent, float):
            self.pFrequencyExponent = float(self.pFrequencyExponent)

        if self.pVoltageExponent is not None and not isinstance(self.pVoltageExponent, float):
            self.pVoltageExponent = float(self.pVoltageExponent)

        if self.qConstantCurrent is not None and not isinstance(self.qConstantCurrent, float):
            self.qConstantCurrent = float(self.qConstantCurrent)

        if self.qConstantImpedance is not None and not isinstance(self.qConstantImpedance, float):
            self.qConstantImpedance = float(self.qConstantImpedance)

        if self.qConstantPower is not None and not isinstance(self.qConstantPower, float):
            self.qConstantPower = float(self.qConstantPower)

        if self.qFrequencyExponent is not None and not isinstance(self.qFrequencyExponent, float):
            self.qFrequencyExponent = float(self.qFrequencyExponent)

        if self.qVoltageExponent is not None and not isinstance(self.qVoltageExponent, float):
            self.qVoltageExponent = float(self.qVoltageExponent)

        super().__post_init__(**kwargs)


class Location(IdentifiedObject):
    """
    rdfs:isDefinedBy : http://www.w3.org/ns/prov-o#<http://www.w3.org/ns/prov#n> :
    http://www.w3.org/TR/2013/REC-prov-n-20130430/#expression-attribute^^xsd:anyURI<http://www.w3.org/ns/prov#category>
    : expanded^^xsd:stringrdfs:seeAlso : http://www.w3.org/ns/prov#atLocationrdfs:label :
    Location^^xsd:string<http://www.w3.org/ns/prov#dm> :
    http://www.w3.org/TR/2013/REC-prov-dm-20130430/#term-attribute-location^^xsd:anyURI<http://www.w3.org/ns/prov#definition>
    : A location can be an identifiable geographic place (ISO 19112), but it can also be a non-geographic place such
    as a directory, row, or column. As such, there are numerous ways in which location can be expressed, such as by a
    coordinate, address, landmark, and so forth.@en
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Location"]
    class_class_curie: ClassVar[str] = "cim:Location"
    class_name: ClassVar[str] = "Location"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Location


class ChargingSite(Location):
    """
    geographical area that encloses one or more charging stations with one operator[From : IEC 63110-1  and ISO]
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ChargingSite"]
    class_class_curie: ClassVar[str] = "cim:ChargingSite"
    class_name: ClassVar[str] = "ChargingSite"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ChargingSite


@dataclass(repr=False)
class LossCurve(Curve):
    """
    Represents the losses in the equipment due to operation position.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["LossCurve"]
    class_class_curie: ClassVar[str] = "cim:LossCurve"
    class_name: ClassVar[str] = "LossCurve"
    class_model_uri: ClassVar[URIRef] = CIMTBL.LossCurve

    FACTSEquipment: Optional[Union[dict, "FACTSEquipment"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.FACTSEquipment is not None and not isinstance(self.FACTSEquipment, FACTSEquipment):
            self.FACTSEquipment = FACTSEquipment(**as_dict(self.FACTSEquipment))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Measurement(IdentifiedObject):
    """
    A Measurement represents any measured, calculated or non-measured non-calculated quantity. Any piece of equipment
    may contain Measurements, e.g. a substation may have temperature measurements and door open indications, a
    transformer may have oil temperature and tank pressure measurements, a bay may contain a number of power flow
    measurements and a Breaker may contain a switch status measurement.The PSR - Measurement association is intended
    to capture this use of Measurement and is included in the naming hierarchy based on EquipmentContainer. The naming
    hierarchy typically has Measurements as leaves, e.g. Substation-VoltageLevel-Bay-Switch-Measurement.Some
    Measurements represent quantities related to a particular sensor location in the network, e.g. a voltage
    transformer (VT) or potential transformer (PT) at a busbar or a current transformer (CT) at the bar between a
    breaker and an isolator. The sensing position is not captured in the PSR - Measurement association. Instead it is
    captured by the Measurement - Terminal association that is used to define the sensing location in the network
    topology. The location is defined by the connection of the Terminal to ConductingEquipment.If both a Terminal and
    PSR are associated, and the PSR is of type ConductingEquipment, the associated Terminal should belong to that
    ConductingEquipment instance.When the sensor location is needed both Measurement-PSR and Measurement-Terminal are
    used. The Measurement-Terminal association is never used alone.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Measurement"]
    class_class_curie: ClassVar[str] = "cim:Measurement"
    class_name: ClassVar[str] = "Measurement"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Measurement

    measurementType: Optional[str] = None
    phases: Optional[Union[str, "PhaseCode"]] = None
    sourceType: Optional[Union[str, "MeasurementSourceKind"]] = None
    unitMultiplier: Optional[Union[str, "UnitMultiplier"]] = None
    unitSymbol: Optional[Union[str, "UnitSymbol"]] = None
    Asset: Optional[Union[dict, Asset]] = None
    CalculationMethodHierarchy: Optional[Union[dict, CalculationMethodHierarchy]] = None
    MeasurementAction: Optional[Union[dict, "MeasurementAction"]] = None
    MeasurementSystem: Optional[Union[dict, "MeasurementSystem"]] = None
    PowerSystemResource: Optional[Union[dict, "PowerSystemResource"]] = None
    Terminal: Optional[Union[dict, ACDCTerminal]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.measurementType is not None and not isinstance(self.measurementType, str):
            self.measurementType = str(self.measurementType)

        if self.phases is not None and not isinstance(self.phases, PhaseCode):
            self.phases = PhaseCode(self.phases)

        if self.sourceType is not None and not isinstance(self.sourceType, MeasurementSourceKind):
            self.sourceType = MeasurementSourceKind(self.sourceType)

        if self.unitMultiplier is not None and not isinstance(self.unitMultiplier, UnitMultiplier):
            self.unitMultiplier = UnitMultiplier(self.unitMultiplier)

        if self.unitSymbol is not None and not isinstance(self.unitSymbol, UnitSymbol):
            self.unitSymbol = UnitSymbol(self.unitSymbol)

        if self.Asset is not None and not isinstance(self.Asset, Asset):
            self.Asset = Asset(**as_dict(self.Asset))

        if self.CalculationMethodHierarchy is not None and not isinstance(self.CalculationMethodHierarchy, CalculationMethodHierarchy):
            self.CalculationMethodHierarchy = CalculationMethodHierarchy(**as_dict(self.CalculationMethodHierarchy))

        if self.MeasurementAction is not None and not isinstance(self.MeasurementAction, MeasurementAction):
            self.MeasurementAction = MeasurementAction(**as_dict(self.MeasurementAction))

        if self.MeasurementSystem is not None and not isinstance(self.MeasurementSystem, MeasurementSystem):
            self.MeasurementSystem = MeasurementSystem(**as_dict(self.MeasurementSystem))

        if self.PowerSystemResource is not None and not isinstance(self.PowerSystemResource, PowerSystemResource):
            self.PowerSystemResource = PowerSystemResource(**as_dict(self.PowerSystemResource))

        if self.Terminal is not None and not isinstance(self.Terminal, ACDCTerminal):
            self.Terminal = ACDCTerminal(**as_dict(self.Terminal))

        super().__post_init__(**kwargs)


class Analog(Measurement):
    """
    Analog represents an analog Measurement.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Analog"]
    class_class_curie: ClassVar[str] = "cim:Analog"
    class_name: ClassVar[str] = "Analog"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Analog


@dataclass(repr=False)
class Discrete(Measurement):
    """
    Discrete represents a discrete Measurement, i.e. a Measurement representing discrete values, e.g. a Breaker
    position.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Discrete"]
    class_class_curie: ClassVar[str] = "cim:Discrete"
    class_name: ClassVar[str] = "Discrete"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Discrete

    maxValue: Optional[int] = None
    minValue: Optional[int] = None
    normalValue: Optional[int] = None
    ValueAliasSet: Optional[Union[dict, "ValueAliasSet"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.maxValue is not None and not isinstance(self.maxValue, int):
            self.maxValue = int(self.maxValue)

        if self.minValue is not None and not isinstance(self.minValue, int):
            self.minValue = int(self.minValue)

        if self.normalValue is not None and not isinstance(self.normalValue, int):
            self.normalValue = int(self.normalValue)

        if self.ValueAliasSet is not None and not isinstance(self.ValueAliasSet, ValueAliasSet):
            self.ValueAliasSet = ValueAliasSet(**as_dict(self.ValueAliasSet))

        super().__post_init__(**kwargs)


class MeasurementAction(IdentifiedObject):
    """
    Measurement taken as a switching step.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["MeasurementAction"]
    class_class_curie: ClassVar[str] = "cim:MeasurementAction"
    class_name: ClassVar[str] = "MeasurementAction"
    class_model_uri: ClassVar[URIRef] = CIMTBL.MeasurementAction


@dataclass(repr=False)
class MeasurementValue(IOPoint):
    """
    The current state for a measurement. A state value is an instance of a measurement from a specific source.
    Measurements can be associated with many state values, each representing a different source for the measurement.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["MeasurementValue"]
    class_class_curie: ClassVar[str] = "cim:MeasurementValue"
    class_name: ClassVar[str] = "MeasurementValue"
    class_model_uri: ClassVar[URIRef] = CIMTBL.MeasurementValue

    sensorAccuracy: Optional[float] = None
    timeStamp: Optional[Union[str, XSDDateTime]] = None
    CalculationMethodHierarchy: Optional[Union[dict, CalculationMethodHierarchy]] = None
    ErpPerson: Optional[Union[dict, "OldPerson"]] = None
    MeasurementValueQuality: Optional[Union[dict, "MeasurementValueQuality"]] = None
    MeasurementValueSource: Optional[Union[dict, "MeasurementValueSource"]] = None
    RemoteSource: Optional[Union[dict, "RemoteSource"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.sensorAccuracy is not None and not isinstance(self.sensorAccuracy, float):
            self.sensorAccuracy = float(self.sensorAccuracy)

        if self.timeStamp is not None and not isinstance(self.timeStamp, XSDDateTime):
            self.timeStamp = XSDDateTime(self.timeStamp)

        if self.CalculationMethodHierarchy is not None and not isinstance(self.CalculationMethodHierarchy, CalculationMethodHierarchy):
            self.CalculationMethodHierarchy = CalculationMethodHierarchy(**as_dict(self.CalculationMethodHierarchy))

        if self.ErpPerson is not None and not isinstance(self.ErpPerson, OldPerson):
            self.ErpPerson = OldPerson(**as_dict(self.ErpPerson))

        if self.MeasurementValueQuality is not None and not isinstance(self.MeasurementValueQuality, MeasurementValueQuality):
            self.MeasurementValueQuality = MeasurementValueQuality(**as_dict(self.MeasurementValueQuality))

        if self.MeasurementValueSource is not None and not isinstance(self.MeasurementValueSource, MeasurementValueSource):
            self.MeasurementValueSource = MeasurementValueSource(**as_dict(self.MeasurementValueSource))

        if self.RemoteSource is not None and not isinstance(self.RemoteSource, RemoteSource):
            self.RemoteSource = RemoteSource(**as_dict(self.RemoteSource))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AnalogValue(MeasurementValue):
    """
    AnalogValue represents an analog MeasurementValue.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["AnalogValue"]
    class_class_curie: ClassVar[str] = "cim:AnalogValue"
    class_name: ClassVar[str] = "AnalogValue"
    class_model_uri: ClassVar[URIRef] = CIMTBL.AnalogValue

    value: Optional[float] = None
    Analog: Optional[Union[dict, Analog]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.value is not None and not isinstance(self.value, float):
            self.value = float(self.value)

        if self.Analog is not None and not isinstance(self.Analog, Analog):
            self.Analog = Analog(**as_dict(self.Analog))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MeasurementValueQuality(YAMLRoot):
    """
    Measurement quality flags. Bits 0-10 are defined for substation automation in IEC 61850-7-3. Bits 11-15 are
    reserved for future expansion by that document. Bits 16-31 are reserved for EMS applications.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["MeasurementValueQuality"]
    class_class_curie: ClassVar[str] = "cim:MeasurementValueQuality"
    class_name: ClassVar[str] = "MeasurementValueQuality"
    class_model_uri: ClassVar[URIRef] = CIMTBL.MeasurementValueQuality

    MeasurementValue: Optional[Union[dict, MeasurementValue]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.MeasurementValue is not None and not isinstance(self.MeasurementValue, MeasurementValue):
            self.MeasurementValue = MeasurementValue(**as_dict(self.MeasurementValue))

        super().__post_init__(**kwargs)


class MeasurementValueSource(IdentifiedObject):
    """
    MeasurementValueSource describes the alternative sources updating a MeasurementValue. User conventions for how to
    use the MeasurementValueSource attributes are defined in IEC 61970-301.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["MeasurementValueSource"]
    class_class_curie: ClassVar[str] = "cim:MeasurementValueSource"
    class_name: ClassVar[str] = "MeasurementValueSource"
    class_model_uri: ClassVar[URIRef] = CIMTBL.MeasurementValueSource


class IOPointSource(MeasurementValueSource):
    """
    Indicates the point source for an IO Point.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["IOPointSource"]
    class_class_curie: ClassVar[str] = "cim:IOPointSource"
    class_name: ClassVar[str] = "IOPointSource"
    class_model_uri: ClassVar[URIRef] = CIMTBL.IOPointSource


@dataclass(repr=False)
class MeasurementVector(MeasurementValue):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["MeasurementVector"]
    class_class_curie: ClassVar[str] = "cim:MeasurementVector"
    class_name: ClassVar[str] = "MeasurementVector"
    class_model_uri: ClassVar[URIRef] = CIMTBL.MeasurementVector

    angle: Optional[float] = None
    magnitude: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.angle is not None and not isinstance(self.angle, float):
            self.angle = float(self.angle)

        if self.magnitude is not None and not isinstance(self.magnitude, float):
            self.magnitude = float(self.magnitude)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MonthDayInterval(YAMLRoot):
    """
    Interval between two times specified as month and day.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["MonthDayInterval"]
    class_class_curie: ClassVar[str] = "cim:MonthDayInterval"
    class_name: ClassVar[str] = "MonthDayInterval"
    class_model_uri: ClassVar[URIRef] = CIMTBL.MonthDayInterval

    end: Optional[str] = None
    start: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.end is not None and not isinstance(self.end, str):
            self.end = str(self.end)

        if self.start is not None and not isinstance(self.start, str):
            self.start = str(self.start)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MutualCoupling(IdentifiedObject):
    """
    This class represents the zero sequence line mutual coupling.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["MutualCoupling"]
    class_class_curie: ClassVar[str] = "cim:MutualCoupling"
    class_name: ClassVar[str] = "MutualCoupling"
    class_model_uri: ClassVar[URIRef] = CIMTBL.MutualCoupling

    b0ch: Optional[float] = None
    distance11: Optional[float] = None
    distance12: Optional[float] = None
    distance21: Optional[float] = None
    distance22: Optional[float] = None
    g0ch: Optional[float] = None
    r0: Optional[float] = None
    x0: Optional[float] = None
    First_Terminal: Optional[Union[dict, "Terminal"]] = None
    Second_Terminal: Optional[Union[dict, "Terminal"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.b0ch is not None and not isinstance(self.b0ch, float):
            self.b0ch = float(self.b0ch)

        if self.distance11 is not None and not isinstance(self.distance11, float):
            self.distance11 = float(self.distance11)

        if self.distance12 is not None and not isinstance(self.distance12, float):
            self.distance12 = float(self.distance12)

        if self.distance21 is not None and not isinstance(self.distance21, float):
            self.distance21 = float(self.distance21)

        if self.distance22 is not None and not isinstance(self.distance22, float):
            self.distance22 = float(self.distance22)

        if self.g0ch is not None and not isinstance(self.g0ch, float):
            self.g0ch = float(self.g0ch)

        if self.r0 is not None and not isinstance(self.r0, float):
            self.r0 = float(self.r0)

        if self.x0 is not None and not isinstance(self.x0, float):
            self.x0 = float(self.x0)

        if self.First_Terminal is not None and not isinstance(self.First_Terminal, Terminal):
            self.First_Terminal = Terminal(**as_dict(self.First_Terminal))

        if self.Second_Terminal is not None and not isinstance(self.Second_Terminal, Terminal):
            self.Second_Terminal = Terminal(**as_dict(self.Second_Terminal))

        super().__post_init__(**kwargs)


class NonConformLoadGroup(LoadGroup):
    """
    Loads that do not follow a daily and seasonal load variation pattern.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["NonConformLoadGroup"]
    class_class_curie: ClassVar[str] = "cim:NonConformLoadGroup"
    class_name: ClassVar[str] = "NonConformLoadGroup"
    class_model_uri: ClassVar[URIRef] = CIMTBL.NonConformLoadGroup


@dataclass(repr=False)
class NonlinearShuntCompensatorPhasePoint(YAMLRoot):
    """
    A per phase non linear shunt compensator bank or section admittance value. The number of
    NonlinearShuntCompensatorPhasePoint instances associated with a NonlinearShuntCompensatorPhase shall be equal to
    ShuntCompensatorPhase.maximumSections. ShuntCompensator.sections shall only be set to one of the
    NonlinearShuntCompensatorPhasePoint.sectionNumber. There is no interpolation between
    NonlinearShuntCompensatorPhasePoint-s.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["NonlinearShuntCompensatorPhasePoint"]
    class_class_curie: ClassVar[str] = "cim:NonlinearShuntCompensatorPhasePoint"
    class_name: ClassVar[str] = "NonlinearShuntCompensatorPhasePoint"
    class_model_uri: ClassVar[URIRef] = CIMTBL.NonlinearShuntCompensatorPhasePoint

    bTotal: Optional[float] = None
    gTotal: Optional[float] = None
    sectionNumber: Optional[int] = None
    NonlinearShuntCompensatorPhase: Optional[Union[dict, "NonlinearShuntCompensatorPhase"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.bTotal is not None and not isinstance(self.bTotal, float):
            self.bTotal = float(self.bTotal)

        if self.gTotal is not None and not isinstance(self.gTotal, float):
            self.gTotal = float(self.gTotal)

        if self.sectionNumber is not None and not isinstance(self.sectionNumber, int):
            self.sectionNumber = int(self.sectionNumber)

        if self.NonlinearShuntCompensatorPhase is not None and not isinstance(self.NonlinearShuntCompensatorPhase, NonlinearShuntCompensatorPhase):
            self.NonlinearShuntCompensatorPhase = NonlinearShuntCompensatorPhase(**as_dict(self.NonlinearShuntCompensatorPhase))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class NonlinearShuntCompensatorPoint(YAMLRoot):
    """
    A non linear shunt compensator bank or section admittance value. The number of NonlinearShuntCompensatorPoint
    instances associated with a NonlinearShuntCompensator shall be equal to ShuntCompensator.maximumSections.
    ShuntCompensator.sections shall only be set to one of the NonlinearShuntCompensatorPoint.sectionNumber. There is
    no interpolation between NonlinearShuntCompensatorPoint-s.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["NonlinearShuntCompensatorPoint"]
    class_class_curie: ClassVar[str] = "cim:NonlinearShuntCompensatorPoint"
    class_name: ClassVar[str] = "NonlinearShuntCompensatorPoint"
    class_model_uri: ClassVar[URIRef] = CIMTBL.NonlinearShuntCompensatorPoint

    b0Total: Optional[float] = None
    bTotal: Optional[float] = None
    g0Total: Optional[float] = None
    gTotal: Optional[float] = None
    sectionNumber: Optional[int] = None
    NonlinearShuntCompensator: Optional[Union[dict, "NonlinearShuntCompensator"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.b0Total is not None and not isinstance(self.b0Total, float):
            self.b0Total = float(self.b0Total)

        if self.bTotal is not None and not isinstance(self.bTotal, float):
            self.bTotal = float(self.bTotal)

        if self.g0Total is not None and not isinstance(self.g0Total, float):
            self.g0Total = float(self.g0Total)

        if self.gTotal is not None and not isinstance(self.gTotal, float):
            self.gTotal = float(self.gTotal)

        if self.sectionNumber is not None and not isinstance(self.sectionNumber, int):
            self.sectionNumber = int(self.sectionNumber)

        if self.NonlinearShuntCompensator is not None and not isinstance(self.NonlinearShuntCompensator, NonlinearShuntCompensator):
            self.NonlinearShuntCompensator = NonlinearShuntCompensator(**as_dict(self.NonlinearShuntCompensator))

        super().__post_init__(**kwargs)


class ObjectType(YAMLRoot):
    """
    Identifies the specialised type of an object when the instance object is serialised using a generalised class. It
    may be useful when the object type is not otherwise included in the exchange. For example, a Meter may be
    serialised as an EndDevice in message exchanges and need to have the ObjectType.type be specified as 'Meter' to
    provide context to the message receiver.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ObjectType"]
    class_class_curie: ClassVar[str] = "cim:ObjectType"
    class_name: ClassVar[str] = "ObjectType"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ObjectType


class OldPerson(IdentifiedObject):
    """
    General purpose information for name and other information to contact people.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["OldPerson"]
    class_class_curie: ClassVar[str] = "cim:OldPerson"
    class_name: ClassVar[str] = "OldPerson"
    class_model_uri: ClassVar[URIRef] = CIMTBL.OldPerson


class OperationalAuthority(IdentifiedObject):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["OperationalAuthority"]
    class_class_curie: ClassVar[str] = "cim:OperationalAuthority"
    class_name: ClassVar[str] = "OperationalAuthority"
    class_model_uri: ClassVar[URIRef] = CIMTBL.OperationalAuthority


@dataclass(repr=False)
class OperationalLimit(IdentifiedObject):
    """
    A value and normal value associated with a specific kind of limit.The sub class value and normalValue attributes
    vary inversely to the associated OperationalLimitType.acceptableDuration (acceptableDuration for short).If a
    particular piece of equipment has multiple operational limits of the same kind (apparent power, current, etc.),
    the limit with the greatest acceptableDuration shall have the smallest limit value and the limit with the smallest
    acceptableDuration shall have the largest limit value. Note: A large current can only be allowed to flow through a
    piece of equipment for a short duration without causing damage, but a lesser current can be allowed to flow for a
    longer duration.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["OperationalLimit"]
    class_class_curie: ClassVar[str] = "cim:OperationalLimit"
    class_name: ClassVar[str] = "OperationalLimit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.OperationalLimit

    OperationalLimitSet: Optional[Union[dict, "OperationalLimitSet"]] = None
    OperationalLimitType: Optional[Union[dict, "OperationalLimitType"]] = None
    StepOperationalLimitTable: Optional[Union[dict, "StepOperationalLimitTable"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.OperationalLimitSet is not None and not isinstance(self.OperationalLimitSet, OperationalLimitSet):
            self.OperationalLimitSet = OperationalLimitSet(**as_dict(self.OperationalLimitSet))

        if self.OperationalLimitType is not None and not isinstance(self.OperationalLimitType, OperationalLimitType):
            self.OperationalLimitType = OperationalLimitType(**as_dict(self.OperationalLimitType))

        if self.StepOperationalLimitTable is not None and not isinstance(self.StepOperationalLimitTable, StepOperationalLimitTable):
            self.StepOperationalLimitTable = StepOperationalLimitTable(**as_dict(self.StepOperationalLimitTable))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ActivePowerLimit(OperationalLimit):
    """
    Limit on active power flow.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ActivePowerLimit"]
    class_class_curie: ClassVar[str] = "cim:ActivePowerLimit"
    class_name: ClassVar[str] = "ActivePowerLimit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ActivePowerLimit

    normalValue: Optional[float] = None
    value: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.normalValue is not None and not isinstance(self.normalValue, float):
            self.normalValue = float(self.normalValue)

        if self.value is not None and not isinstance(self.value, float):
            self.value = float(self.value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ApparentPowerLimit(OperationalLimit):
    """
    Apparent power limit.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ApparentPowerLimit"]
    class_class_curie: ClassVar[str] = "cim:ApparentPowerLimit"
    class_name: ClassVar[str] = "ApparentPowerLimit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ApparentPowerLimit

    normalValue: Optional[float] = None
    value: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.normalValue is not None and not isinstance(self.normalValue, float):
            self.normalValue = float(self.normalValue)

        if self.value is not None and not isinstance(self.value, float):
            self.value = float(self.value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CurrentLimit(OperationalLimit):
    """
    Operational limit on current.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["CurrentLimit"]
    class_class_curie: ClassVar[str] = "cim:CurrentLimit"
    class_name: ClassVar[str] = "CurrentLimit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.CurrentLimit

    normalValue: Optional[float] = None
    value: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.normalValue is not None and not isinstance(self.normalValue, float):
            self.normalValue = float(self.normalValue)

        if self.value is not None and not isinstance(self.value, float):
            self.value = float(self.value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OperationalLimitSet(IdentifiedObject):
    """
    A set of limits associated with equipment. Sets of limits might apply to a specific temperature, or season for
    example. A set of limits may contain different severities of limit levels that would apply to the same equipment.
    The set may contain limits of different types such as apparent power and current limits or high and low voltage
    limits that are logically applied together as a set.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["OperationalLimitSet"]
    class_class_curie: ClassVar[str] = "cim:OperationalLimitSet"
    class_name: ClassVar[str] = "OperationalLimitSet"
    class_model_uri: ClassVar[URIRef] = CIMTBL.OperationalLimitSet

    Equipment: Optional[Union[dict, "Equipment"]] = None
    PowerTransferCorridor: Optional[Union[dict, "PowerTransferCorridor"]] = None
    Terminal: Optional[Union[dict, ACDCTerminal]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.Equipment is not None and not isinstance(self.Equipment, Equipment):
            self.Equipment = Equipment(**as_dict(self.Equipment))

        if self.PowerTransferCorridor is not None and not isinstance(self.PowerTransferCorridor, PowerTransferCorridor):
            self.PowerTransferCorridor = PowerTransferCorridor(**as_dict(self.PowerTransferCorridor))

        if self.Terminal is not None and not isinstance(self.Terminal, ACDCTerminal):
            self.Terminal = ACDCTerminal(**as_dict(self.Terminal))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OperationalLimitType(IdentifiedObject):
    """
    The operational meaning of a category of limits.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["OperationalLimitType"]
    class_class_curie: ClassVar[str] = "cim:OperationalLimitType"
    class_name: ClassVar[str] = "OperationalLimitType"
    class_model_uri: ClassVar[URIRef] = CIMTBL.OperationalLimitType

    acceptableDuration: Optional[float] = None
    direction: Optional[Union[str, "OperationalLimitDirectionKind"]] = None
    isInfiniteDuration: Optional[Union[bool, Bool]] = None
    isMinimum: Optional[Union[bool, Bool]] = None
    kind: Optional[Union[str, "LimitKind"]] = None
    PermanentAmbientTemperatureDependencyCurve: Optional[Union[dict, AmbientTemperatureDependencyCurve]] = None
    PermanentSolarRadiationCurve: Optional[Union[dict, "SolarRadiationDependencyCurve"]] = None
    RecoveryOverloadLimitCurve: Optional[Union[dict, "RecoveryOverloadLimitCurve"]] = None
    TemporaryBaseOverloadLimitCurve: Optional[Union[dict, BaseOverloadLimitCurve]] = None
    TemporaryDurationOverloadLimitCurve: Optional[Union[dict, DurationOverloadLimitCurve]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.acceptableDuration is not None and not isinstance(self.acceptableDuration, float):
            self.acceptableDuration = float(self.acceptableDuration)

        if self.direction is not None and not isinstance(self.direction, OperationalLimitDirectionKind):
            self.direction = OperationalLimitDirectionKind(self.direction)

        if self.isInfiniteDuration is not None and not isinstance(self.isInfiniteDuration, Bool):
            self.isInfiniteDuration = Bool(self.isInfiniteDuration)

        if self.isMinimum is not None and not isinstance(self.isMinimum, Bool):
            self.isMinimum = Bool(self.isMinimum)

        if self.kind is not None and not isinstance(self.kind, LimitKind):
            self.kind = LimitKind(self.kind)

        if self.PermanentAmbientTemperatureDependencyCurve is not None and not isinstance(self.PermanentAmbientTemperatureDependencyCurve, AmbientTemperatureDependencyCurve):
            self.PermanentAmbientTemperatureDependencyCurve = AmbientTemperatureDependencyCurve(**as_dict(self.PermanentAmbientTemperatureDependencyCurve))

        if self.PermanentSolarRadiationCurve is not None and not isinstance(self.PermanentSolarRadiationCurve, SolarRadiationDependencyCurve):
            self.PermanentSolarRadiationCurve = SolarRadiationDependencyCurve(**as_dict(self.PermanentSolarRadiationCurve))

        if self.RecoveryOverloadLimitCurve is not None and not isinstance(self.RecoveryOverloadLimitCurve, RecoveryOverloadLimitCurve):
            self.RecoveryOverloadLimitCurve = RecoveryOverloadLimitCurve(**as_dict(self.RecoveryOverloadLimitCurve))

        if self.TemporaryBaseOverloadLimitCurve is not None and not isinstance(self.TemporaryBaseOverloadLimitCurve, BaseOverloadLimitCurve):
            self.TemporaryBaseOverloadLimitCurve = BaseOverloadLimitCurve(**as_dict(self.TemporaryBaseOverloadLimitCurve))

        if self.TemporaryDurationOverloadLimitCurve is not None and not isinstance(self.TemporaryDurationOverloadLimitCurve, DurationOverloadLimitCurve):
            self.TemporaryDurationOverloadLimitCurve = DurationOverloadLimitCurve(**as_dict(self.TemporaryDurationOverloadLimitCurve))

        super().__post_init__(**kwargs)


class Outage(IdentifiedObject):
    """
    Document describing details of an active or planned outage in a part of the electrical network.A non-planned
    outage may be created upon:- a breaker trip,- a fault indicator status change,- a meter event indicating customer
    outage,- a reception of one or more customer trouble calls, or- an operator command, reflecting information
    obtained from the field crew.Outage restoration may be performed using a switching plan which complements the
    outage information with detailed switching activities, including the relationship to the crew and work.A planned
    outage may be created upon:- a request for service, maintenance or construction work in the field, or- an
    operator-defined outage for what-if/contingency network analysis.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Outage"]
    class_class_curie: ClassVar[str] = "cim:Outage"
    class_name: ClassVar[str] = "Outage"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Outage


@dataclass(repr=False)
class PMUConfiguration(IdentifiedObject):
    """
    PMU Configuration Frame data from IEEE Std. C37.118
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PMUConfiguration"]
    class_class_curie: ClassVar[str] = "cim:PMUConfiguration"
    class_name: ClassVar[str] = "PMUConfiguration"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PMUConfiguration

    anNmr: Optional[int] = None
    anScale: Optional[str] = None
    cfgCnt: Optional[int] = None
    chNam: Optional[str] = None
    dfdtNmr: Optional[int] = None
    dfdtScale: Optional[str] = None
    format: Optional[str] = None
    frNmr: Optional[int] = None
    frScale: Optional[str] = None
    grpDly: Optional[Union[str, XSDTime]] = None
    phNmr: Optional[int] = None
    phScale: Optional[str] = None
    pmuDataRate: Optional[int] = None
    streamDataRate: Optional[int] = None
    waitTime: Optional[Union[str, XSDTime]] = None
    window: Optional[Union[str, XSDTime]] = None
    PhasorMeasurementUnit: Optional[Union[dict, "PhasorMeasurementUnit"]] = None
    PMUConfigurationFrame: Optional[Union[dict, "PMUConfigurationFrame"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.anNmr is not None and not isinstance(self.anNmr, int):
            self.anNmr = int(self.anNmr)

        if self.anScale is not None and not isinstance(self.anScale, str):
            self.anScale = str(self.anScale)

        if self.cfgCnt is not None and not isinstance(self.cfgCnt, int):
            self.cfgCnt = int(self.cfgCnt)

        if self.chNam is not None and not isinstance(self.chNam, str):
            self.chNam = str(self.chNam)

        if self.dfdtNmr is not None and not isinstance(self.dfdtNmr, int):
            self.dfdtNmr = int(self.dfdtNmr)

        if self.dfdtScale is not None and not isinstance(self.dfdtScale, str):
            self.dfdtScale = str(self.dfdtScale)

        if self.format is not None and not isinstance(self.format, str):
            self.format = str(self.format)

        if self.frNmr is not None and not isinstance(self.frNmr, int):
            self.frNmr = int(self.frNmr)

        if self.frScale is not None and not isinstance(self.frScale, str):
            self.frScale = str(self.frScale)

        if self.grpDly is not None and not isinstance(self.grpDly, XSDTime):
            self.grpDly = XSDTime(self.grpDly)

        if self.phNmr is not None and not isinstance(self.phNmr, int):
            self.phNmr = int(self.phNmr)

        if self.phScale is not None and not isinstance(self.phScale, str):
            self.phScale = str(self.phScale)

        if self.pmuDataRate is not None and not isinstance(self.pmuDataRate, int):
            self.pmuDataRate = int(self.pmuDataRate)

        if self.streamDataRate is not None and not isinstance(self.streamDataRate, int):
            self.streamDataRate = int(self.streamDataRate)

        if self.waitTime is not None and not isinstance(self.waitTime, XSDTime):
            self.waitTime = XSDTime(self.waitTime)

        if self.window is not None and not isinstance(self.window, XSDTime):
            self.window = XSDTime(self.window)

        if self.PhasorMeasurementUnit is not None and not isinstance(self.PhasorMeasurementUnit, PhasorMeasurementUnit):
            self.PhasorMeasurementUnit = PhasorMeasurementUnit(**as_dict(self.PhasorMeasurementUnit))

        if self.PMUConfigurationFrame is not None and not isinstance(self.PMUConfigurationFrame, PMUConfigurationFrame):
            self.PMUConfigurationFrame = PMUConfigurationFrame(**as_dict(self.PMUConfigurationFrame))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PMUStream(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PMUStream"]
    class_class_curie: ClassVar[str] = "cim:PMUStream"
    class_name: ClassVar[str] = "PMUStream"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PMUStream

    PMU: Optional[Union[dict, "PhasorMeasurementUnit"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.PMU is not None and not isinstance(self.PMU, PhasorMeasurementUnit):
            self.PMU = PhasorMeasurementUnit(**as_dict(self.PMU))

        super().__post_init__(**kwargs)


class PMUValueConcentration(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PMUValueConcentration"]
    class_class_curie: ClassVar[str] = "cim:PMUValueConcentration"
    class_name: ClassVar[str] = "PMUValueConcentration"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PMUValueConcentration


@dataclass(repr=False)
class PMUValueQuality(MeasurementValueQuality):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PMUValueQuality"]
    class_class_curie: ClassVar[str] = "cim:PMUValueQuality"
    class_name: ClassVar[str] = "PMUValueQuality"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PMUValueQuality

    dataBad: Optional[Union[bool, Bool]] = None
    dataError: Optional[Union[bool, Bool]] = None
    insertedData: Optional[Union[bool, Bool]] = None
    localTimeStamp: Optional[Union[bool, Bool]] = None
    pmuSync: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.dataBad is not None and not isinstance(self.dataBad, Bool):
            self.dataBad = Bool(self.dataBad)

        if self.dataError is not None and not isinstance(self.dataError, Bool):
            self.dataError = Bool(self.dataError)

        if self.insertedData is not None and not isinstance(self.insertedData, Bool):
            self.insertedData = Bool(self.insertedData)

        if self.localTimeStamp is not None and not isinstance(self.localTimeStamp, Bool):
            self.localTimeStamp = Bool(self.localTimeStamp)

        if self.pmuSync is not None and not isinstance(self.pmuSync, Bool):
            self.pmuSync = Bool(self.pmuSync)

        super().__post_init__(**kwargs)


class PSRType(IdentifiedObject):
    """
    Classifying instances of the same class, e.g. overhead and underground ACLineSegments. This classification
    mechanism is intended to provide flexibility outside the scope of this document, i.e. provide customisation that
    is non standard.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PSRType"]
    class_class_curie: ClassVar[str] = "cim:PSRType"
    class_name: ClassVar[str] = "PSRType"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PSRType


@dataclass(repr=False)
class PerLengthLineParameter(IdentifiedObject):
    """
    Common type for per-length electrical line parameters.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PerLengthLineParameter"]
    class_class_curie: ClassVar[str] = "cim:PerLengthLineParameter"
    class_name: ClassVar[str] = "PerLengthLineParameter"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PerLengthLineParameter

    WireAssemblyInfo: Optional[Union[dict, "WireAssemblyInfo"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.WireAssemblyInfo is not None and not isinstance(self.WireAssemblyInfo, WireAssemblyInfo):
            self.WireAssemblyInfo = WireAssemblyInfo(**as_dict(self.WireAssemblyInfo))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PerLengthImpedance(PerLengthLineParameter):
    """
    Frequency in which impedances have been calculated at.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PerLengthImpedance"]
    class_class_curie: ClassVar[str] = "cim:PerLengthImpedance"
    class_name: ClassVar[str] = "PerLengthImpedance"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PerLengthImpedance

    calculatedFrequency: Optional[float] = None
    calculatedTemperature: Optional[float] = None
    isUserDefined: Optional[Union[bool, Bool]] = None
    rg: Optional[float] = None
    xg: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.calculatedFrequency is not None and not isinstance(self.calculatedFrequency, float):
            self.calculatedFrequency = float(self.calculatedFrequency)

        if self.calculatedTemperature is not None and not isinstance(self.calculatedTemperature, float):
            self.calculatedTemperature = float(self.calculatedTemperature)

        if self.isUserDefined is not None and not isinstance(self.isUserDefined, Bool):
            self.isUserDefined = Bool(self.isUserDefined)

        if self.rg is not None and not isinstance(self.rg, float):
            self.rg = float(self.rg)

        if self.xg is not None and not isinstance(self.xg, float):
            self.xg = float(self.xg)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PerLengthPhaseImpedance(PerLengthImpedance):
    """
    The per length phase impedance matrix expresses impedance and admittance parameters per unit length for
    n-conductor unbalanced line segments. A phase impedance matrix contains both self impedances for each phase and
    mutual impedances between pairs of phases. The matrix is stored in symmetric lower triangular format where the
    diagonal entries represent self-impedances (and have the same value in row and column) and the off diagonal
    entries represent phase-to-phase impedances (and have different row and column values).The matrix can be use to
    express impedances for both non-coupled and coupled line segments. Coupled line segments share a single per length
    phase impedance matrix whose entries reflect the self and mutual impedances of all the phases of all the wires.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PerLengthPhaseImpedance"]
    class_class_curie: ClassVar[str] = "cim:PerLengthPhaseImpedance"
    class_name: ClassVar[str] = "PerLengthPhaseImpedance"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PerLengthPhaseImpedance

    conductorCount: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.conductorCount is not None and not isinstance(self.conductorCount, int):
            self.conductorCount = int(self.conductorCount)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PerLengthSequenceImpedance(PerLengthImpedance):
    """
    Sequence impedance and admittance parameters per unit length, for transposed line segments of 1, 2, or 3 phases.
    For 1-phase line segments, define x = x0 = xself. For 2-phase line segments, define x = xself - xmutual and x0 =
    xself + xmutual.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PerLengthSequenceImpedance"]
    class_class_curie: ClassVar[str] = "cim:PerLengthSequenceImpedance"
    class_name: ClassVar[str] = "PerLengthSequenceImpedance"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PerLengthSequenceImpedance

    b0ch: Optional[float] = None
    bch: Optional[float] = None
    g0ch: Optional[float] = None
    gch: Optional[float] = None
    r: Optional[float] = None
    r0: Optional[float] = None
    x: Optional[float] = None
    x0: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.b0ch is not None and not isinstance(self.b0ch, float):
            self.b0ch = float(self.b0ch)

        if self.bch is not None and not isinstance(self.bch, float):
            self.bch = float(self.bch)

        if self.g0ch is not None and not isinstance(self.g0ch, float):
            self.g0ch = float(self.g0ch)

        if self.gch is not None and not isinstance(self.gch, float):
            self.gch = float(self.gch)

        if self.r is not None and not isinstance(self.r, float):
            self.r = float(self.r)

        if self.r0 is not None and not isinstance(self.r0, float):
            self.r0 = float(self.r0)

        if self.x is not None and not isinstance(self.x, float):
            self.x = float(self.x)

        if self.x0 is not None and not isinstance(self.x0, float):
            self.x0 = float(self.x0)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PhaseImpedanceData(IdentifiedObject):
    """
    Per length phase impedance matrix entry describes impedance and conductance matrix element values for a specific
    row and column of the matrix.The phases to which each entry applies can be determined by means of the row and
    column attributes which bind to a sequence number provided in either ACLineSegmentPhase or WirePosition (which
    also specify phase). Due to physical symmetry that is reflected in the matrix, only the lower triangle of the
    matrix is populated with the row and column method. That is, the column attribute is always less than or equal to
    the row attribute.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PhaseImpedanceData"]
    class_class_curie: ClassVar[str] = "cim:PhaseImpedanceData"
    class_name: ClassVar[str] = "PhaseImpedanceData"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhaseImpedanceData

    b: Optional[float] = None
    column: Optional[int] = None
    fromPhase: Optional[Union[str, "SinglePhaseKind"]] = None
    g: Optional[float] = None
    r: Optional[float] = None
    row: Optional[int] = None
    toPhase: Optional[Union[str, "SinglePhaseKind"]] = None
    x: Optional[float] = None
    PhaseImpedance: Optional[Union[dict, PerLengthPhaseImpedance]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.b is not None and not isinstance(self.b, float):
            self.b = float(self.b)

        if self.column is not None and not isinstance(self.column, int):
            self.column = int(self.column)

        if self.fromPhase is not None and not isinstance(self.fromPhase, SinglePhaseKind):
            self.fromPhase = SinglePhaseKind(self.fromPhase)

        if self.g is not None and not isinstance(self.g, float):
            self.g = float(self.g)

        if self.r is not None and not isinstance(self.r, float):
            self.r = float(self.r)

        if self.row is not None and not isinstance(self.row, int):
            self.row = int(self.row)

        if self.toPhase is not None and not isinstance(self.toPhase, SinglePhaseKind):
            self.toPhase = SinglePhaseKind(self.toPhase)

        if self.x is not None and not isinstance(self.x, float):
            self.x = float(self.x)

        if self.PhaseImpedance is not None and not isinstance(self.PhaseImpedance, PerLengthPhaseImpedance):
            self.PhaseImpedance = PerLengthPhaseImpedance(**as_dict(self.PhaseImpedance))

        super().__post_init__(**kwargs)


class PhaseTapChangerTable(IdentifiedObject):
    """
    Describes a tabular curve for how the phase angle difference and impedance varies with the tap step.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PhaseTapChangerTable"]
    class_class_curie: ClassVar[str] = "cim:PhaseTapChangerTable"
    class_name: ClassVar[str] = "PhaseTapChangerTable"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhaseTapChangerTable


@dataclass(repr=False)
class ConnectionAngleTapChangerTable(PhaseTapChangerTable):
    """
    Describes a tabular curve for how the connection angle varies with the tap step. This table is used when its
    winding connection angle matches the operating angle of the tap changer. There must be an instance of this table
    for each winding connection angle that can be used.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ConnectionAngleTapChangerTable"]
    class_class_curie: ClassVar[str] = "cim:ConnectionAngleTapChangerTable"
    class_name: ClassVar[str] = "ConnectionAngleTapChangerTable"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConnectionAngleTapChangerTable

    windingConnectionAngle: Optional[float] = None
    ConnectionAngleTapChanger: Optional[Union[dict, "ConnectionAngleTapChanger"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.windingConnectionAngle is not None and not isinstance(self.windingConnectionAngle, float):
            self.windingConnectionAngle = float(self.windingConnectionAngle)

        if self.ConnectionAngleTapChanger is not None and not isinstance(self.ConnectionAngleTapChanger, ConnectionAngleTapChanger):
            self.ConnectionAngleTapChanger = ConnectionAngleTapChanger(**as_dict(self.ConnectionAngleTapChanger))

        super().__post_init__(**kwargs)


class PhasorMeasurementValue(MeasurementVector):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PhasorMeasurementValue"]
    class_class_curie: ClassVar[str] = "cim:PhasorMeasurementValue"
    class_name: ClassVar[str] = "PhasorMeasurementValue"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhasorMeasurementValue


@dataclass(repr=False)
class PositionPoint(YAMLRoot):
    """
    Set of spatial coordinates that determine a point, defined in the coordinate system specified in
    'Location.CoordinateSystem'. Use a single position point instance to describe a point-oriented location. Use a
    sequence of position points to describe a line-oriented object (physical location of non-point oriented objects
    like cables or lines), or area of an object (like a substation or a geographical zone - in this case, have first
    and last position point with the same values).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PositionPoint"]
    class_class_curie: ClassVar[str] = "cim:PositionPoint"
    class_name: ClassVar[str] = "PositionPoint"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PositionPoint

    sequenceNumber: Optional[int] = None
    xPosition: Optional[str] = None
    yPosition: Optional[str] = None
    zPosition: Optional[str] = None
    Location: Optional[Union[dict, Location]] = None
    RelativeHeight: Optional[Union[dict, "RelativeHeight"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.sequenceNumber is not None and not isinstance(self.sequenceNumber, int):
            self.sequenceNumber = int(self.sequenceNumber)

        if self.xPosition is not None and not isinstance(self.xPosition, str):
            self.xPosition = str(self.xPosition)

        if self.yPosition is not None and not isinstance(self.yPosition, str):
            self.yPosition = str(self.yPosition)

        if self.zPosition is not None and not isinstance(self.zPosition, str):
            self.zPosition = str(self.zPosition)

        if self.Location is not None and not isinstance(self.Location, Location):
            self.Location = Location(**as_dict(self.Location))

        if self.RelativeHeight is not None and not isinstance(self.RelativeHeight, RelativeHeight):
            self.RelativeHeight = RelativeHeight()

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PowerSystemResource(IdentifiedObject):
    """
    A power system resource (PSR) can be an item of equipment such as a switch, an equipment container containing many
    individual items of equipment such as a substation, or an organisational entity such as sub-control area. Power
    system resources can have measurements associated.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PowerSystemResource"]
    class_class_curie: ClassVar[str] = "cim:PowerSystemResource"
    class_name: ClassVar[str] = "PowerSystemResource"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerSystemResource

    AssetDatasheet: Optional[Union[dict, AssetInfo]] = None
    DesignElement: Optional[Union[dict, DesignElement]] = None
    Location: Optional[Union[dict, Location]] = None
    OperatedByCompany: Optional[Union[dict, Company]] = None
    PSRType: Optional[Union[dict, PSRType]] = None
    ResourceContainer: Optional[Union[dict, "ResourceContainer"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.AssetDatasheet is not None and not isinstance(self.AssetDatasheet, AssetInfo):
            self.AssetDatasheet = AssetInfo(**as_dict(self.AssetDatasheet))

        if self.DesignElement is not None and not isinstance(self.DesignElement, DesignElement):
            self.DesignElement = DesignElement(**as_dict(self.DesignElement))

        if self.Location is not None and not isinstance(self.Location, Location):
            self.Location = Location(**as_dict(self.Location))

        if self.OperatedByCompany is not None and not isinstance(self.OperatedByCompany, Company):
            self.OperatedByCompany = Company(**as_dict(self.OperatedByCompany))

        if self.PSRType is not None and not isinstance(self.PSRType, PSRType):
            self.PSRType = PSRType(**as_dict(self.PSRType))

        if self.ResourceContainer is not None and not isinstance(self.ResourceContainer, ResourceContainer):
            self.ResourceContainer = ResourceContainer()

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ACLineSegmentPhase(PowerSystemResource):
    """
    A line segment phase represents one phase (or optionally the neutral) of an alternating current line segment.Under
    most circumstances there is not a line segment phase for the neutral. However, if a wire assembly is being used
    and it does not specify phase, a line segment phase must exist for each position in the assembly (including the
    neutral).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ACLineSegmentPhase"]
    class_class_curie: ClassVar[str] = "cim:ACLineSegmentPhase"
    class_name: ClassVar[str] = "ACLineSegmentPhase"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ACLineSegmentPhase

    phase: Optional[Union[str, "SinglePhaseKind"]] = None
    sequenceNumber: Optional[int] = None
    ACLineSegment: Optional[Union[dict, "ACLineSegment"]] = None
    WireInfo: Optional[Union[dict, "WireInfo"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.phase is not None and not isinstance(self.phase, SinglePhaseKind):
            self.phase = SinglePhaseKind(self.phase)

        if self.sequenceNumber is not None and not isinstance(self.sequenceNumber, int):
            self.sequenceNumber = int(self.sequenceNumber)

        if self.ACLineSegment is not None and not isinstance(self.ACLineSegment, ACLineSegment):
            self.ACLineSegment = ACLineSegment(**as_dict(self.ACLineSegment))

        if self.WireInfo is not None and not isinstance(self.WireInfo, WireInfo):
            self.WireInfo = WireInfo(**as_dict(self.WireInfo))

        super().__post_init__(**kwargs)


class AreaDispatchableUnit(PowerSystemResource):
    """
    Allocates a given producing or consuming unit, including direct current corridor and collection of units, to a
    given control area (through the scheduling area) for supporting the control of the given area through dispatch
    instruction.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["AreaDispatchableUnit"]
    class_class_curie: ClassVar[str] = "cim:AreaDispatchableUnit"
    class_name: ClassVar[str] = "AreaDispatchableUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.AreaDispatchableUnit


@dataclass(repr=False)
class AreaInterchangeController(PowerSystemResource):
    """
    Area interchange control is set to control active power of an area.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["AreaInterchangeController"]
    class_class_curie: ClassVar[str] = "cim:AreaInterchangeController"
    class_name: ClassVar[str] = "AreaInterchangeController"
    class_model_uri: ClassVar[URIRef] = CIMTBL.AreaInterchangeController

    pTolerance: Optional[float] = None
    ControlArea: Optional[Union[dict, "ControlArea"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.pTolerance is not None and not isinstance(self.pTolerance, float):
            self.pTolerance = float(self.pTolerance)

        if self.ControlArea is not None and not isinstance(self.ControlArea, ControlArea):
            self.ControlArea = ControlArea(**as_dict(self.ControlArea))

        super().__post_init__(**kwargs)


class BoundaryPoint(PowerSystemResource):
    """
    Designates a connection point at which one or more model authority sets shall connect to. The location of the
    connection point as well as other properties are agreed between organisations responsible for the interconnection,
    hence all attributes of the class represent this agreement. It is primarily used in a boundary model authority set
    which can contain one or many BoundaryPoint-s among other Equipment-s and their connections.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BoundaryPoint"]
    class_class_curie: ClassVar[str] = "cim:BoundaryPoint"
    class_name: ClassVar[str] = "BoundaryPoint"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BoundaryPoint


@dataclass(repr=False)
class CommunicationLink(PowerSystemResource):
    """
    The connection to remote units is through one or more communication links. Reduntant links may exist. The
    CommunicationLink class inherits PowerSystemResource. The intention is to allow CommunicationLinks to have
    Measurements. These Measurements can be used to model link status as operational, out of service, unit failure
    etc.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["CommunicationLink"]
    class_class_curie: ClassVar[str] = "cim:CommunicationLink"
    class_name: ClassVar[str] = "CommunicationLink"
    class_model_uri: ClassVar[URIRef] = CIMTBL.CommunicationLink

    communicationMediumKind: Optional[Union[str, "CommunicationMediumKind"]] = None
    communicationProtocolType: Optional[Union[str, "CommunicationProtocolKind"]] = None
    BilateralExchangeActor: Optional[Union[dict, BilateralExchangeActor]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.communicationMediumKind is not None and not isinstance(self.communicationMediumKind, CommunicationMediumKind):
            self.communicationMediumKind = CommunicationMediumKind(self.communicationMediumKind)

        if self.communicationProtocolType is not None and not isinstance(self.communicationProtocolType, CommunicationProtocolKind):
            self.communicationProtocolType = CommunicationProtocolKind(self.communicationProtocolType)

        if self.BilateralExchangeActor is not None and not isinstance(self.BilateralExchangeActor, BilateralExchangeActor):
            self.BilateralExchangeActor = BilateralExchangeActor(**as_dict(self.BilateralExchangeActor))

        super().__post_init__(**kwargs)


class ConnectivityNodeContainer(PowerSystemResource):
    """
    A base class for all objects that may contain connectivity nodes or topological nodes.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ConnectivityNodeContainer"]
    class_class_curie: ClassVar[str] = "cim:ConnectivityNodeContainer"
    class_name: ClassVar[str] = "ConnectivityNodeContainer"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConnectivityNodeContainer


@dataclass(repr=False)
class ControlArea(PowerSystemResource):
    """
    A control area is a grouping of generating units and/or loads and a cutset of tie lines (as terminals) which may
    be used for a variety of purposes including automatic generation control, power flow solution area interchange
    control specification, and input to load forecasting. All generation and load within the area defined by the
    terminals on the border are considered in the area interchange control. Note that any number of overlapping
    control area specifications may be superimposed on the physical model. The following general principles apply to
    ControlArea:1. The control area orientation for net interchange is positive for an import, negative for an
    export.2. The control area net interchange is determined by summing flows in Terminals. The Terminals are
    identified by creating a set of TieFlow objects associated with a ControlArea object. Each TieFlow object
    identifies one Terminal.3. In a single network model, a tie between two control areas must be modelled in both
    control area specifications, such that the two representations of the tie flow sum to zero.4. The normal
    orientation of Terminal flow is positive for flow into the conducting equipment that owns the Terminal. (i.e. flow
    from a bus into a device is positive.) However, the orientation of each flow in the control area specification
    must align with the control area convention, i.e. import is positive. If the orientation of the Terminal flow
    referenced by a TieFlow is positive into the control area, then this is confirmed by setting
    TieFlow.positiveFlowIn flag TRUE. If not, the orientation must be reversed by setting the TieFlow.positiveFlowIn
    flag FALSE.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ControlArea"]
    class_class_curie: ClassVar[str] = "cim:ControlArea"
    class_name: ClassVar[str] = "ControlArea"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ControlArea

    netInterchange: Optional[float] = None
    pTolerance: Optional[float] = None
    type: Optional[Union[str, "ControlAreaTypeKind"]] = None
    AreaInterchangeController: Optional[Union[dict, AreaInterchangeController]] = None
    EnergyArea: Optional[Union[dict, EnergyArea]] = None
    OutageCoordinationRegion: Optional[Union[dict, "OutageCoordinationRegion"]] = None
    PowerFrequencyController: Optional[Union[dict, "PowerFrequencyController"]] = None
    SystemOperator: Optional[Union[dict, "SystemOperator"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.netInterchange is not None and not isinstance(self.netInterchange, float):
            self.netInterchange = float(self.netInterchange)

        if self.pTolerance is not None and not isinstance(self.pTolerance, float):
            self.pTolerance = float(self.pTolerance)

        if self.type is not None and not isinstance(self.type, ControlAreaTypeKind):
            self.type = ControlAreaTypeKind(self.type)

        if self.AreaInterchangeController is not None and not isinstance(self.AreaInterchangeController, AreaInterchangeController):
            self.AreaInterchangeController = AreaInterchangeController(**as_dict(self.AreaInterchangeController))

        if self.EnergyArea is not None and not isinstance(self.EnergyArea, EnergyArea):
            self.EnergyArea = EnergyArea(**as_dict(self.EnergyArea))

        if self.OutageCoordinationRegion is not None and not isinstance(self.OutageCoordinationRegion, OutageCoordinationRegion):
            self.OutageCoordinationRegion = OutageCoordinationRegion(**as_dict(self.OutageCoordinationRegion))

        if self.PowerFrequencyController is not None and not isinstance(self.PowerFrequencyController, PowerFrequencyController):
            self.PowerFrequencyController = PowerFrequencyController(**as_dict(self.PowerFrequencyController))

        if self.SystemOperator is not None and not isinstance(self.SystemOperator, SystemOperator):
            self.SystemOperator = SystemOperator()

        super().__post_init__(**kwargs)


class BalancingControlArea(ControlArea):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BalancingControlArea"]
    class_class_curie: ClassVar[str] = "cim:BalancingControlArea"
    class_name: ClassVar[str] = "BalancingControlArea"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BalancingControlArea


class DistributionControlArea(ControlArea):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["DistributionControlArea"]
    class_class_curie: ClassVar[str] = "cim:DistributionControlArea"
    class_name: ClassVar[str] = "DistributionControlArea"
    class_model_uri: ClassVar[URIRef] = CIMTBL.DistributionControlArea


@dataclass(repr=False)
class EnergyConsumerPhase(PowerSystemResource):
    """
    A single phase of an energy consumer.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EnergyConsumerPhase"]
    class_class_curie: ClassVar[str] = "cim:EnergyConsumerPhase"
    class_name: ClassVar[str] = "EnergyConsumerPhase"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EnergyConsumerPhase

    p: Optional[float] = None
    pfixed: Optional[float] = None
    pfixedPct: Optional[float] = None
    phase: Optional[Union[str, "SinglePhaseKind"]] = None
    q: Optional[float] = None
    qfixed: Optional[float] = None
    qfixedPct: Optional[float] = None
    EnergyConsumer: Optional[Union[dict, "EnergyConsumer"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.p is not None and not isinstance(self.p, float):
            self.p = float(self.p)

        if self.pfixed is not None and not isinstance(self.pfixed, float):
            self.pfixed = float(self.pfixed)

        if self.pfixedPct is not None and not isinstance(self.pfixedPct, float):
            self.pfixedPct = float(self.pfixedPct)

        if self.phase is not None and not isinstance(self.phase, SinglePhaseKind):
            self.phase = SinglePhaseKind(self.phase)

        if self.q is not None and not isinstance(self.q, float):
            self.q = float(self.q)

        if self.qfixed is not None and not isinstance(self.qfixed, float):
            self.qfixed = float(self.qfixed)

        if self.qfixedPct is not None and not isinstance(self.qfixedPct, float):
            self.qfixedPct = float(self.qfixedPct)

        if self.EnergyConsumer is not None and not isinstance(self.EnergyConsumer, EnergyConsumer):
            self.EnergyConsumer = EnergyConsumer(**as_dict(self.EnergyConsumer))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EnergySourcePhase(PowerSystemResource):
    """
    Represents the single phase information of an unbalanced energy source.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EnergySourcePhase"]
    class_class_curie: ClassVar[str] = "cim:EnergySourcePhase"
    class_name: ClassVar[str] = "EnergySourcePhase"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EnergySourcePhase

    phase: Optional[Union[str, "SinglePhaseKind"]] = None
    EnergySource: Optional[Union[dict, "EnergySource"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.phase is not None and not isinstance(self.phase, SinglePhaseKind):
            self.phase = SinglePhaseKind(self.phase)

        if self.EnergySource is not None and not isinstance(self.EnergySource, EnergySource):
            self.EnergySource = EnergySource(**as_dict(self.EnergySource))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Equipment(PowerSystemResource):
    """
    The parts of a power system that are physical devices, electronic or mechanical.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Equipment"]
    class_class_curie: ClassVar[str] = "cim:Equipment"
    class_name: ClassVar[str] = "Equipment"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Equipment

    aggregate: Optional[Union[bool, Bool]] = None
    inService: Optional[Union[bool, Bool]] = None
    networkAnalysisEnabled: Optional[Union[bool, Bool]] = None
    normallyInService: Optional[Union[bool, Bool]] = None
    AdditionalEquipmentContainer: Optional[Union[Union[dict, "EquipmentContainer"], list[Union[dict, "EquipmentContainer"]]]] = empty_list()
    EquipmentContainer: Optional[Union[dict, "EquipmentContainer"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.aggregate is not None and not isinstance(self.aggregate, Bool):
            self.aggregate = Bool(self.aggregate)

        if self.inService is not None and not isinstance(self.inService, Bool):
            self.inService = Bool(self.inService)

        if self.networkAnalysisEnabled is not None and not isinstance(self.networkAnalysisEnabled, Bool):
            self.networkAnalysisEnabled = Bool(self.networkAnalysisEnabled)

        if self.normallyInService is not None and not isinstance(self.normallyInService, Bool):
            self.normallyInService = Bool(self.normallyInService)

        if not isinstance(self.AdditionalEquipmentContainer, list):
            self.AdditionalEquipmentContainer = [self.AdditionalEquipmentContainer] if self.AdditionalEquipmentContainer is not None else []
        self.AdditionalEquipmentContainer = [v if isinstance(v, EquipmentContainer) else EquipmentContainer(**as_dict(v)) for v in self.AdditionalEquipmentContainer]

        if self.EquipmentContainer is not None and not isinstance(self.EquipmentContainer, EquipmentContainer):
            self.EquipmentContainer = EquipmentContainer(**as_dict(self.EquipmentContainer))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CompositeSwitch(Equipment):
    """
    A model of a set of individual Switches normally enclosed within the same cabinet and possibly with interlocks
    that restrict the combination of switch positions. These are typically found in medium voltage distribution
    networks.A CompositeSwitch could represent a Ring-Main-Unit (RMU), or pad-mounted switchgear, with primitive
    internal devices such as an internal bus-bar plus 3 or 4 internal switches each of which may individually be open
    or closed. A CompositeSwitch and a set of contained Switches can also be used to represent a multi-position switch
    e.g. a switch that can connect a circuit to Ground, Open or Busbar.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["CompositeSwitch"]
    class_class_curie: ClassVar[str] = "cim:CompositeSwitch"
    class_name: ClassVar[str] = "CompositeSwitch"
    class_model_uri: ClassVar[URIRef] = CIMTBL.CompositeSwitch

    compositeSwitchType: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.compositeSwitchType is not None and not isinstance(self.compositeSwitchType, str):
            self.compositeSwitchType = str(self.compositeSwitchType)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ConductingEquipment(Equipment):
    """
    The parts of the AC power system that are designed to carry current or that are conductively connected through
    terminals.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ConductingEquipment"]
    class_class_curie: ClassVar[str] = "cim:ConductingEquipment"
    class_name: ClassVar[str] = "ConductingEquipment"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConductingEquipment

    BaseVoltage: Optional[Union[dict, BaseVoltage]] = None
    GroundingAction: Optional[Union[dict, GroundAction]] = None
    JumpingAction: Optional[Union[dict, JumperAction]] = None
    Outage: Optional[Union[dict, Outage]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.BaseVoltage is not None and not isinstance(self.BaseVoltage, BaseVoltage):
            self.BaseVoltage = BaseVoltage(**as_dict(self.BaseVoltage))

        if self.GroundingAction is not None and not isinstance(self.GroundingAction, GroundAction):
            self.GroundingAction = GroundAction(**as_dict(self.GroundingAction))

        if self.JumpingAction is not None and not isinstance(self.JumpingAction, JumperAction):
            self.JumpingAction = JumperAction(**as_dict(self.JumpingAction))

        if self.Outage is not None and not isinstance(self.Outage, Outage):
            self.Outage = Outage(**as_dict(self.Outage))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Clamp(ConductingEquipment):
    """
    A Clamp is a galvanic connection at a line segment where other equipment is connected. A Clamp does not cut the
    line segment.A Clamp is ConductingEquipment and has one Terminal with an associated ConnectivityNode. Any other
    ConductingEquipment can be connected to the Clamp ConnectivityNode.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Clamp"]
    class_class_curie: ClassVar[str] = "cim:Clamp"
    class_name: ClassVar[str] = "Clamp"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Clamp

    lengthFromTerminal1: Optional[float] = None
    ACLineSegment: Optional[Union[dict, "ACLineSegment"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.lengthFromTerminal1 is not None and not isinstance(self.lengthFromTerminal1, float):
            self.lengthFromTerminal1 = float(self.lengthFromTerminal1)

        if self.ACLineSegment is not None and not isinstance(self.ACLineSegment, ACLineSegment):
            self.ACLineSegment = ACLineSegment(**as_dict(self.ACLineSegment))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Conductor(ConductingEquipment):
    """
    Combination of conducting material with consistent electrical characteristics, building a single electrical
    system, used to carry current between points in the power system.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Conductor"]
    class_class_curie: ClassVar[str] = "cim:Conductor"
    class_name: ClassVar[str] = "Conductor"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Conductor

    length: Optional[float] = None
    DamageCurve: Optional[Union[dict, ConductorCharacteristicCurve]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.length is not None and not isinstance(self.length, float):
            self.length = float(self.length)

        if self.DamageCurve is not None and not isinstance(self.DamageCurve, ConductorCharacteristicCurve):
            self.DamageCurve = ConductorCharacteristicCurve(**as_dict(self.DamageCurve))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ACLineSegment(Conductor):
    """
    A line segment is a conductor or combination of conductors, with consistent electrical characteristics along its
    length, building a single electrical system that carries alternating current between two points in the power
    system.The BaseVoltage at the two ends of a line segment shall have the same BaseVoltage.nominalVoltage. However,
    boundary lines may have slightly different BaseVoltage.nominalVoltages and variation is allowed. Larger voltage
    difference in general requires use of an equivalent branch.Line segment impedances can be either directly
    described in electrical terms or physical line detail can be provided from which impedances can be
    calculated.<b>Directly described impedances</b>For symmetrical, transposed three phase line segments, it is
    sufficient to use attributes of the line segment, which describe impedances and admittances for the entire length
    of the line segment. Additionally, line segment impedances can be computed by using line segment length and
    associated per length impedances.Unbalanced modeling of impedances is supported by the per length phase impedance
    matrix (PerLengthPhaseImpedance) in conjunction with phase-to-sequence number mapping supplied by either
    ACLineSegmentPhase or WirePosition. The sequence numbers are referenced by the row and column attributes of the
    per length phase impedance matrix. This method enables single-phase and two-phase line segments, and
    transpositions of phases, to be described using the same per length phase impedance matrix. The length of the line
    segment is used in the computation of total impedance values for the line segment.<b>Line detail
    characteristics</b>There are three approaches to providing line detail and all use WireAssembly to supply line
    positions:<ul> <li>Option 1 - WireAssembly supplies only line positions. ACLineSegmentPhase points to wire type
    and intraphase spacing and supplies the phase-to-sequence number mapping.</li> <li>Option 2 - WireAssembly
    supplies line position and, for each position, also supplies wire type and intraphase spacing. ACLineSegmentPhase
    supplies the phase-to-sequence number mapping.</li> <li>Option 3 - WireAssembly supplies line position and, for
    each position, also supplies wire type and intraphase spacing and phase. WireAssembly therefore supplies the
    phase-to-sequence number mapping and ACLineSegmentPhase is not needed.</li></ul>
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ACLineSegment"]
    class_class_curie: ClassVar[str] = "cim:ACLineSegment"
    class_name: ClassVar[str] = "ACLineSegment"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ACLineSegment

    b0ch: Optional[float] = None
    bch: Optional[float] = None
    circuitNumber: Optional[int] = None
    g0ch: Optional[float] = None
    gch: Optional[float] = None
    isUnderground: Optional[Union[bool, Bool]] = None
    r: Optional[float] = None
    r0: Optional[float] = None
    shortCircuitEndTemperature: Optional[float] = None
    x: Optional[float] = None
    x0: Optional[float] = None
    EarthResistivity: Optional[Union[dict, EarthResistivity]] = None
    PerLengthImpedance: Optional[Union[dict, PerLengthImpedance]] = None
    WireSpacing: Optional[Union[dict, "WireSpacing"]] = None
    WireSpacingInfo: Optional[Union[dict, "WireSpacingInfo"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.b0ch is not None and not isinstance(self.b0ch, float):
            self.b0ch = float(self.b0ch)

        if self.bch is not None and not isinstance(self.bch, float):
            self.bch = float(self.bch)

        if self.circuitNumber is not None and not isinstance(self.circuitNumber, int):
            self.circuitNumber = int(self.circuitNumber)

        if self.g0ch is not None and not isinstance(self.g0ch, float):
            self.g0ch = float(self.g0ch)

        if self.gch is not None and not isinstance(self.gch, float):
            self.gch = float(self.gch)

        if self.isUnderground is not None and not isinstance(self.isUnderground, Bool):
            self.isUnderground = Bool(self.isUnderground)

        if self.r is not None and not isinstance(self.r, float):
            self.r = float(self.r)

        if self.r0 is not None and not isinstance(self.r0, float):
            self.r0 = float(self.r0)

        if self.shortCircuitEndTemperature is not None and not isinstance(self.shortCircuitEndTemperature, float):
            self.shortCircuitEndTemperature = float(self.shortCircuitEndTemperature)

        if self.x is not None and not isinstance(self.x, float):
            self.x = float(self.x)

        if self.x0 is not None and not isinstance(self.x0, float):
            self.x0 = float(self.x0)

        if self.EarthResistivity is not None and not isinstance(self.EarthResistivity, EarthResistivity):
            self.EarthResistivity = EarthResistivity(**as_dict(self.EarthResistivity))

        if self.PerLengthImpedance is not None and not isinstance(self.PerLengthImpedance, PerLengthImpedance):
            self.PerLengthImpedance = PerLengthImpedance(**as_dict(self.PerLengthImpedance))

        if self.WireSpacing is not None and not isinstance(self.WireSpacing, WireSpacing):
            self.WireSpacing = WireSpacing()

        if self.WireSpacingInfo is not None and not isinstance(self.WireSpacingInfo, WireSpacingInfo):
            self.WireSpacingInfo = WireSpacingInfo(**as_dict(self.WireSpacingInfo))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BusSegment(Conductor):
    """
    A two terminal and power conducting device of negligible impedance and length represented as zero impedance device
    that can be used to represent the conductor between connection points to substation conducting equipment on a
    substation bus.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BusSegment"]
    class_class_curie: ClassVar[str] = "cim:BusSegment"
    class_name: ClassVar[str] = "BusSegment"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BusSegment

    Retain: Optional[Union[bool, Bool]] = None
    retained: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.Retain is not None and not isinstance(self.Retain, Bool):
            self.Retain = Bool(self.Retain)

        if self.retained is not None and not isinstance(self.retained, Bool):
            self.retained = Bool(self.retained)

        super().__post_init__(**kwargs)


class Connector(ConductingEquipment):
    """
    A conductor, or group of conductors, with negligible impedance, that serve to connect other conducting equipment
    within a single substation and are modelled with a single logical terminal.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Connector"]
    class_class_curie: ClassVar[str] = "cim:Connector"
    class_name: ClassVar[str] = "Connector"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Connector


@dataclass(repr=False)
class BusbarSection(Connector):
    """
    A conductor, or group of conductors, with negligible impedance, that serve to connect other conducting equipment
    within a single substation. The BusbarSection class is intended to represent physical parts of bus bars no matter
    how that bus bar is constructed.Voltage measurements are typically obtained from voltage transformers that are
    connected to busbar sections. A bus bar section may have many physical terminals but for analysis is modelled with
    exactly one logical terminal.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BusbarSection"]
    class_class_curie: ClassVar[str] = "cim:BusbarSection"
    class_name: ClassVar[str] = "BusbarSection"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BusbarSection

    ipMax: Optional[float] = None
    VoltageControlZone: Optional[Union[dict, "VoltageControlZone"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.ipMax is not None and not isinstance(self.ipMax, float):
            self.ipMax = float(self.ipMax)

        if self.VoltageControlZone is not None and not isinstance(self.VoltageControlZone, VoltageControlZone):
            self.VoltageControlZone = VoltageControlZone(**as_dict(self.VoltageControlZone))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CurrentTransformer(Equipment):
    """
    Instrument transformer used to measure electrical qualities of the circuit that is being protected and/or
    monitored. Typically used as current transducer for the purpose of metering or protection. A typical secondary
    current rating would be 5A.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["CurrentTransformer"]
    class_class_curie: ClassVar[str] = "cim:CurrentTransformer"
    class_name: ClassVar[str] = "CurrentTransformer"
    class_model_uri: ClassVar[URIRef] = CIMTBL.CurrentTransformer

    accuracyLimit: Optional[float] = None
    coreBurden: Optional[float] = None
    usage: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.accuracyLimit is not None and not isinstance(self.accuracyLimit, float):
            self.accuracyLimit = float(self.accuracyLimit)

        if self.coreBurden is not None and not isinstance(self.coreBurden, float):
            self.coreBurden = float(self.coreBurden)

        if self.usage is not None and not isinstance(self.usage, str):
            self.usage = str(self.usage)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EarthFaultCompensator(ConductingEquipment):
    """
    A conducting equipment used to represent a connection to ground which is typically used to compensate earth
    faults. An earth fault compensator device modelled with a single terminal implies a second terminal solidly
    connected to ground. If two terminals are modelled, the ground is not assumed and normal connection rules apply.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EarthFaultCompensator"]
    class_class_curie: ClassVar[str] = "cim:EarthFaultCompensator"
    class_name: ClassVar[str] = "EarthFaultCompensator"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EarthFaultCompensator

    r: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.r is not None and not isinstance(self.r, float):
            self.r = float(self.r)

        super().__post_init__(**kwargs)


class EnergyConnection(ConductingEquipment):
    """
    A connection of energy generation or consumption on the power system model.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EnergyConnection"]
    class_class_curie: ClassVar[str] = "cim:EnergyConnection"
    class_name: ClassVar[str] = "EnergyConnection"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EnergyConnection


@dataclass(repr=False)
class EnergyConsumer(EnergyConnection):
    """
    Generic user of energy - a point of consumption on the power system model.EnergyConsumer.pfixed, .qfixed,
    .pfixedPct and .qfixedPct have meaning only if there is no LoadResponseCharacteristic associated with
    EnergyConsumer or if LoadResponseCharacteristic.exponentModel is set to False.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EnergyConsumer"]
    class_class_curie: ClassVar[str] = "cim:EnergyConsumer"
    class_name: ClassVar[str] = "EnergyConsumer"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EnergyConsumer

    customerCount: Optional[int] = None
    grounded: Optional[Union[bool, Bool]] = None
    p: Optional[float] = None
    pfixed: Optional[float] = None
    pfixedPct: Optional[float] = None
    phaseConnection: Optional[Union[str, "PhaseShuntConnectionKind"]] = None
    q: Optional[float] = None
    qfixed: Optional[float] = None
    qfixedPct: Optional[float] = None
    AreaDispatchableUnit: Optional[Union[dict, AreaDispatchableUnit]] = None
    EnergyConsumerAction: Optional[Union[dict, EnergyConsumerAction]] = None
    LoadDynamics: Optional[Union[dict, LoadDynamics]] = None
    LoadResponse: Optional[Union[dict, LoadResponseCharacteristic]] = None
    PowerCutZone: Optional[Union[dict, "PowerCutZone"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.customerCount is not None and not isinstance(self.customerCount, int):
            self.customerCount = int(self.customerCount)

        if self.grounded is not None and not isinstance(self.grounded, Bool):
            self.grounded = Bool(self.grounded)

        if self.p is not None and not isinstance(self.p, float):
            self.p = float(self.p)

        if self.pfixed is not None and not isinstance(self.pfixed, float):
            self.pfixed = float(self.pfixed)

        if self.pfixedPct is not None and not isinstance(self.pfixedPct, float):
            self.pfixedPct = float(self.pfixedPct)

        if self.phaseConnection is not None and not isinstance(self.phaseConnection, PhaseShuntConnectionKind):
            self.phaseConnection = PhaseShuntConnectionKind(self.phaseConnection)

        if self.q is not None and not isinstance(self.q, float):
            self.q = float(self.q)

        if self.qfixed is not None and not isinstance(self.qfixed, float):
            self.qfixed = float(self.qfixed)

        if self.qfixedPct is not None and not isinstance(self.qfixedPct, float):
            self.qfixedPct = float(self.qfixedPct)

        if self.AreaDispatchableUnit is not None and not isinstance(self.AreaDispatchableUnit, AreaDispatchableUnit):
            self.AreaDispatchableUnit = AreaDispatchableUnit(**as_dict(self.AreaDispatchableUnit))

        if self.EnergyConsumerAction is not None and not isinstance(self.EnergyConsumerAction, EnergyConsumerAction):
            self.EnergyConsumerAction = EnergyConsumerAction(**as_dict(self.EnergyConsumerAction))

        if self.LoadDynamics is not None and not isinstance(self.LoadDynamics, LoadDynamics):
            self.LoadDynamics = LoadDynamics(**as_dict(self.LoadDynamics))

        if self.LoadResponse is not None and not isinstance(self.LoadResponse, LoadResponseCharacteristic):
            self.LoadResponse = LoadResponseCharacteristic(**as_dict(self.LoadResponse))

        if self.PowerCutZone is not None and not isinstance(self.PowerCutZone, PowerCutZone):
            self.PowerCutZone = PowerCutZone(**as_dict(self.PowerCutZone))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ConformLoad(EnergyConsumer):
    """
    ConformLoad represents loads that follow a daily load change pattern where the pattern can be used to scale the
    load with a system load.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ConformLoad"]
    class_class_curie: ClassVar[str] = "cim:ConformLoad"
    class_name: ClassVar[str] = "ConformLoad"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConformLoad

    LoadGroup: Optional[Union[dict, ConformLoadGroup]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.LoadGroup is not None and not isinstance(self.LoadGroup, ConformLoadGroup):
            self.LoadGroup = ConformLoadGroup(**as_dict(self.LoadGroup))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EnergySource(EnergyConnection):
    """
    A generic equivalent for an energy supplier on a transmission or distribution voltage level.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EnergySource"]
    class_class_curie: ClassVar[str] = "cim:EnergySource"
    class_name: ClassVar[str] = "EnergySource"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EnergySource

    activePower: Optional[float] = None
    grounded: Optional[Union[bool, Bool]] = None
    nominalVoltage: Optional[float] = None
    pMax: Optional[float] = None
    pMin: Optional[float] = None
    r: Optional[float] = None
    r0: Optional[float] = None
    r2: Optional[float] = None
    reactivePower: Optional[float] = None
    voltageAngle: Optional[float] = None
    voltageMagnitude: Optional[float] = None
    x: Optional[float] = None
    x0: Optional[float] = None
    x2: Optional[float] = None
    EnergySchedulingType: Optional[Union[dict, EnergySchedulingType]] = None
    EnergySourceAction: Optional[Union[dict, EnergySourceModification]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.activePower is not None and not isinstance(self.activePower, float):
            self.activePower = float(self.activePower)

        if self.grounded is not None and not isinstance(self.grounded, Bool):
            self.grounded = Bool(self.grounded)

        if self.nominalVoltage is not None and not isinstance(self.nominalVoltage, float):
            self.nominalVoltage = float(self.nominalVoltage)

        if self.pMax is not None and not isinstance(self.pMax, float):
            self.pMax = float(self.pMax)

        if self.pMin is not None and not isinstance(self.pMin, float):
            self.pMin = float(self.pMin)

        if self.r is not None and not isinstance(self.r, float):
            self.r = float(self.r)

        if self.r0 is not None and not isinstance(self.r0, float):
            self.r0 = float(self.r0)

        if self.r2 is not None and not isinstance(self.r2, float):
            self.r2 = float(self.r2)

        if self.reactivePower is not None and not isinstance(self.reactivePower, float):
            self.reactivePower = float(self.reactivePower)

        if self.voltageAngle is not None and not isinstance(self.voltageAngle, float):
            self.voltageAngle = float(self.voltageAngle)

        if self.voltageMagnitude is not None and not isinstance(self.voltageMagnitude, float):
            self.voltageMagnitude = float(self.voltageMagnitude)

        if self.x is not None and not isinstance(self.x, float):
            self.x = float(self.x)

        if self.x0 is not None and not isinstance(self.x0, float):
            self.x0 = float(self.x0)

        if self.x2 is not None and not isinstance(self.x2, float):
            self.x2 = float(self.x2)

        if self.EnergySchedulingType is not None and not isinstance(self.EnergySchedulingType, EnergySchedulingType):
            self.EnergySchedulingType = EnergySchedulingType(**as_dict(self.EnergySchedulingType))

        if self.EnergySourceAction is not None and not isinstance(self.EnergySourceAction, EnergySourceModification):
            self.EnergySourceAction = EnergySourceModification(**as_dict(self.EnergySourceAction))

        super().__post_init__(**kwargs)


class EquipmentContainer(ConnectivityNodeContainer):
    """
    A modelling construct to provide a root class for containing equipment.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EquipmentContainer"]
    class_class_curie: ClassVar[str] = "cim:EquipmentContainer"
    class_name: ClassVar[str] = "EquipmentContainer"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EquipmentContainer


@dataclass(repr=False)
class Bay(EquipmentContainer):
    """
    A collection of power system resources (within a given substation) including conducting equipment, protection
    relays, measurements, and telemetry. A bay typically represents a physical grouping related to modularization of
    equipment.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Bay"]
    class_class_curie: ClassVar[str] = "cim:Bay"
    class_name: ClassVar[str] = "Bay"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Bay

    bayEnergyMeasFlag: Optional[Union[bool, Bool]] = None
    bayPowerMeasFlag: Optional[Union[bool, Bool]] = None
    breakerConfiguration: Optional[Union[str, "BreakerConfiguration"]] = None
    busBarConfiguration: Optional[Union[str, "BusbarConfiguration"]] = None
    Substation: Optional[Union[dict, "Substation"]] = None
    VoltageLevel: Optional[Union[dict, "VoltageLevel"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.bayEnergyMeasFlag is not None and not isinstance(self.bayEnergyMeasFlag, Bool):
            self.bayEnergyMeasFlag = Bool(self.bayEnergyMeasFlag)

        if self.bayPowerMeasFlag is not None and not isinstance(self.bayPowerMeasFlag, Bool):
            self.bayPowerMeasFlag = Bool(self.bayPowerMeasFlag)

        if self.breakerConfiguration is not None and not isinstance(self.breakerConfiguration, BreakerConfiguration):
            self.breakerConfiguration = BreakerConfiguration(self.breakerConfiguration)

        if self.busBarConfiguration is not None and not isinstance(self.busBarConfiguration, BusbarConfiguration):
            self.busBarConfiguration = BusbarConfiguration(self.busBarConfiguration)

        if self.Substation is not None and not isinstance(self.Substation, Substation):
            self.Substation = Substation(**as_dict(self.Substation))

        if self.VoltageLevel is not None and not isinstance(self.VoltageLevel, VoltageLevel):
            self.VoltageLevel = VoltageLevel(**as_dict(self.VoltageLevel))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ConnectivityArea(EquipmentContainer):
    """
    A persistent connectivity-based containment of Equipment with clearly defined electrical boundaries based on
    terminals of boundary equipment in a transmission or distribution network.In a transmission context, this class
    provides a persistent superset grouping of equipment across multiple substations to describe an operating area of
    responsibility or bounded area for simulation studies.In a distribution context, this class differs from Feeder
    (which is largely for naming purposes) by providing groupings of equipment on the basis of connectivity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ConnectivityArea"]
    class_class_curie: ClassVar[str] = "cim:ConnectivityArea"
    class_name: ClassVar[str] = "ConnectivityArea"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConnectivityArea

    areaType: Optional[Union[str, "ConnectivityAreaKind"]] = None
    AdjacentArea: Optional[Union[dict, "ConnectivityArea"]] = None
    ContainedWithin: Optional[Union[dict, "ConnectivityArea"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.areaType is not None and not isinstance(self.areaType, ConnectivityAreaKind):
            self.areaType = ConnectivityAreaKind(self.areaType)

        if self.AdjacentArea is not None and not isinstance(self.AdjacentArea, ConnectivityArea):
            self.AdjacentArea = ConnectivityArea(**as_dict(self.AdjacentArea))

        if self.ContainedWithin is not None and not isinstance(self.ContainedWithin, ConnectivityArea):
            self.ContainedWithin = ConnectivityArea(**as_dict(self.ContainedWithin))

        super().__post_init__(**kwargs)


class DCConverterUnit(EquipmentContainer):
    """
    Indivisible operative unit comprising all equipment between the point of common coupling on the AC side and the
    point of common coupling � DC side, essentially one or more converters, together with one or more converter
    transformers, converter control equipment, essential protective and switching devices and auxiliaries, if any,
    used for conversion.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["DCConverterUnit"]
    class_class_curie: ClassVar[str] = "cim:DCConverterUnit"
    class_name: ClassVar[str] = "DCConverterUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.DCConverterUnit


class EquipmentController(PowerSystemResource):
    """
    Equipment controller is an automation function that can control one or multiple equipment function to achieve all
    the targets inside the given tolerance.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EquipmentController"]
    class_class_curie: ClassVar[str] = "cim:EquipmentController"
    class_name: ClassVar[str] = "EquipmentController"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EquipmentController


class ExtendedWardEquivalent(ConductingEquipment):
    """
    An extended ward equivalent is a combination of an impedance load, a PQ load and as voltage source with an
    internal impedance.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ExtendedWardEquivalent"]
    class_class_curie: ClassVar[str] = "cim:ExtendedWardEquivalent"
    class_name: ClassVar[str] = "ExtendedWardEquivalent"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ExtendedWardEquivalent


@dataclass(repr=False)
class Feeder(EquipmentContainer):
    """
    A collection of equipment for organizational purposes, used for grouping distribution resources.The organization a
    feeder does not necessarily reflect connectivity or current operation state.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Feeder"]
    class_class_curie: ClassVar[str] = "cim:Feeder"
    class_name: ClassVar[str] = "Feeder"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Feeder

    NormalEnergizingSubstation: Optional[Union[dict, "Substation"]] = None
    SubSchedulingArea: Optional[Union[dict, "SubSchedulingArea"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.NormalEnergizingSubstation is not None and not isinstance(self.NormalEnergizingSubstation, Substation):
            self.NormalEnergizingSubstation = Substation(**as_dict(self.NormalEnergizingSubstation))

        if self.SubSchedulingArea is not None and not isinstance(self.SubSchedulingArea, SubSchedulingArea):
            self.SubSchedulingArea = SubSchedulingArea(**as_dict(self.SubSchedulingArea))

        super().__post_init__(**kwargs)


class FuelStorage(PowerSystemResource):
    """
    Fuel storage. e.g. pile of coal that can be shared between multiple thermal generating units.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["FuelStorage"]
    class_class_curie: ClassVar[str] = "cim:FuelStorage"
    class_name: ClassVar[str] = "FuelStorage"
    class_model_uri: ClassVar[URIRef] = CIMTBL.FuelStorage


@dataclass(repr=False)
class GeneratingUnit(Equipment):
    """
    A single or set of synchronous machines for converting mechanical power into alternating-current power. For
    example, individual machines within a set may be defined for scheduling purposes while a single control signal is
    derived for the set. In this case there would be a GeneratingUnit for each member of the set and an additional
    GeneratingUnit corresponding to the set.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["GeneratingUnit"]
    class_class_curie: ClassVar[str] = "cim:GeneratingUnit"
    class_name: ClassVar[str] = "GeneratingUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.GeneratingUnit

    allocSpinResP: Optional[float] = None
    autoCntrlMarginP: Optional[float] = None
    baseP: Optional[float] = None
    controlDeadband: Optional[float] = None
    controlPulseHigh: Optional[float] = None
    controlPulseLow: Optional[float] = None
    controlResponseRate: Optional[float] = None
    efficiency: Optional[float] = None
    genControlMode: Optional[Union[str, "GeneratorControlMode"]] = None
    genControlSource: Optional[Union[str, "GeneratorControlSource"]] = None
    governorMPL: Optional[float] = None
    governorSCD: Optional[float] = None
    highControlLimit: Optional[float] = None
    initialP: Optional[float] = None
    longPF: Optional[float] = None
    lowControlLimit: Optional[float] = None
    lowerRampRate: Optional[float] = None
    maxEconomicP: Optional[float] = None
    maximumAllowableSpinningReserve: Optional[float] = None
    maxOperatingP: Optional[float] = None
    minEconomicP: Optional[float] = None
    minimumOffTime: Optional[float] = None
    minOperatingP: Optional[float] = None
    modelDetail: Optional[int] = None
    nominalP: Optional[float] = None
    normalPF: Optional[float] = None
    penaltyFactor: Optional[float] = None
    raiseRampRate: Optional[float] = None
    ratedGrossMaxP: Optional[float] = None
    ratedGrossMinP: Optional[float] = None
    ratedNetMaxP: Optional[float] = None
    shortPF: Optional[float] = None
    startupCost: Optional[Decimal] = None
    startupTime: Optional[float] = None
    tieLinePF: Optional[float] = None
    totalEfficiency: Optional[float] = None
    variableCost: Optional[Decimal] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.allocSpinResP is not None and not isinstance(self.allocSpinResP, float):
            self.allocSpinResP = float(self.allocSpinResP)

        if self.autoCntrlMarginP is not None and not isinstance(self.autoCntrlMarginP, float):
            self.autoCntrlMarginP = float(self.autoCntrlMarginP)

        if self.baseP is not None and not isinstance(self.baseP, float):
            self.baseP = float(self.baseP)

        if self.controlDeadband is not None and not isinstance(self.controlDeadband, float):
            self.controlDeadband = float(self.controlDeadband)

        if self.controlPulseHigh is not None and not isinstance(self.controlPulseHigh, float):
            self.controlPulseHigh = float(self.controlPulseHigh)

        if self.controlPulseLow is not None and not isinstance(self.controlPulseLow, float):
            self.controlPulseLow = float(self.controlPulseLow)

        if self.controlResponseRate is not None and not isinstance(self.controlResponseRate, float):
            self.controlResponseRate = float(self.controlResponseRate)

        if self.efficiency is not None and not isinstance(self.efficiency, float):
            self.efficiency = float(self.efficiency)

        if self.genControlMode is not None and not isinstance(self.genControlMode, GeneratorControlMode):
            self.genControlMode = GeneratorControlMode(self.genControlMode)

        if self.genControlSource is not None and not isinstance(self.genControlSource, GeneratorControlSource):
            self.genControlSource = GeneratorControlSource(self.genControlSource)

        if self.governorMPL is not None and not isinstance(self.governorMPL, float):
            self.governorMPL = float(self.governorMPL)

        if self.governorSCD is not None and not isinstance(self.governorSCD, float):
            self.governorSCD = float(self.governorSCD)

        if self.highControlLimit is not None and not isinstance(self.highControlLimit, float):
            self.highControlLimit = float(self.highControlLimit)

        if self.initialP is not None and not isinstance(self.initialP, float):
            self.initialP = float(self.initialP)

        if self.longPF is not None and not isinstance(self.longPF, float):
            self.longPF = float(self.longPF)

        if self.lowControlLimit is not None and not isinstance(self.lowControlLimit, float):
            self.lowControlLimit = float(self.lowControlLimit)

        if self.lowerRampRate is not None and not isinstance(self.lowerRampRate, float):
            self.lowerRampRate = float(self.lowerRampRate)

        if self.maxEconomicP is not None and not isinstance(self.maxEconomicP, float):
            self.maxEconomicP = float(self.maxEconomicP)

        if self.maximumAllowableSpinningReserve is not None and not isinstance(self.maximumAllowableSpinningReserve, float):
            self.maximumAllowableSpinningReserve = float(self.maximumAllowableSpinningReserve)

        if self.maxOperatingP is not None and not isinstance(self.maxOperatingP, float):
            self.maxOperatingP = float(self.maxOperatingP)

        if self.minEconomicP is not None and not isinstance(self.minEconomicP, float):
            self.minEconomicP = float(self.minEconomicP)

        if self.minimumOffTime is not None and not isinstance(self.minimumOffTime, float):
            self.minimumOffTime = float(self.minimumOffTime)

        if self.minOperatingP is not None and not isinstance(self.minOperatingP, float):
            self.minOperatingP = float(self.minOperatingP)

        if self.modelDetail is not None and not isinstance(self.modelDetail, int):
            self.modelDetail = int(self.modelDetail)

        if self.nominalP is not None and not isinstance(self.nominalP, float):
            self.nominalP = float(self.nominalP)

        if self.normalPF is not None and not isinstance(self.normalPF, float):
            self.normalPF = float(self.normalPF)

        if self.penaltyFactor is not None and not isinstance(self.penaltyFactor, float):
            self.penaltyFactor = float(self.penaltyFactor)

        if self.raiseRampRate is not None and not isinstance(self.raiseRampRate, float):
            self.raiseRampRate = float(self.raiseRampRate)

        if self.ratedGrossMaxP is not None and not isinstance(self.ratedGrossMaxP, float):
            self.ratedGrossMaxP = float(self.ratedGrossMaxP)

        if self.ratedGrossMinP is not None and not isinstance(self.ratedGrossMinP, float):
            self.ratedGrossMinP = float(self.ratedGrossMinP)

        if self.ratedNetMaxP is not None and not isinstance(self.ratedNetMaxP, float):
            self.ratedNetMaxP = float(self.ratedNetMaxP)

        if self.shortPF is not None and not isinstance(self.shortPF, float):
            self.shortPF = float(self.shortPF)

        if self.startupCost is not None and not isinstance(self.startupCost, Decimal):
            self.startupCost = Decimal(self.startupCost)

        if self.startupTime is not None and not isinstance(self.startupTime, float):
            self.startupTime = float(self.startupTime)

        if self.tieLinePF is not None and not isinstance(self.tieLinePF, float):
            self.tieLinePF = float(self.tieLinePF)

        if self.totalEfficiency is not None and not isinstance(self.totalEfficiency, float):
            self.totalEfficiency = float(self.totalEfficiency)

        if self.variableCost is not None and not isinstance(self.variableCost, Decimal):
            self.variableCost = Decimal(self.variableCost)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Ground(ConductingEquipment):
    """
    A point where the system is grounded used for connecting conducting equipment to ground. The power system model
    can have any number of grounds.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Ground"]
    class_class_curie: ClassVar[str] = "cim:Ground"
    class_name: ClassVar[str] = "Ground"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Ground

    GroundAction: Optional[Union[dict, GroundAction]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.GroundAction is not None and not isinstance(self.GroundAction, GroundAction):
            self.GroundAction = GroundAction(**as_dict(self.GroundAction))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GroundingImpedance(EarthFaultCompensator):
    """
    A fixed impedance device used for grounding.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["GroundingImpedance"]
    class_class_curie: ClassVar[str] = "cim:GroundingImpedance"
    class_name: ClassVar[str] = "GroundingImpedance"
    class_model_uri: ClassVar[URIRef] = CIMTBL.GroundingImpedance

    x: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.x is not None and not isinstance(self.x, float):
            self.x = float(self.x)

        super().__post_init__(**kwargs)


class HydroPump(Equipment):
    """
    A synchronous motor-driven pump, typically associated with a pumped storage plant.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["HydroPump"]
    class_class_curie: ClassVar[str] = "cim:HydroPump"
    class_name: ClassVar[str] = "HydroPump"
    class_model_uri: ClassVar[URIRef] = CIMTBL.HydroPump


class Junction(Connector):
    """
    A point where one or more conducting equipments are connected with zero resistance.The Junction class is intended
    to provide a place to associate additional information to a connectivity node which connects two or more equipment
    terminals. Examples include a tee-point or the connection point between two switches.The Junction class is
    intended to provide a method to associate additional information, for instance Location, to a ConnectivityNode.
    Examples include a T-point or the connection point between two switches. Typically, BusbarSection objects and
    Junction objects are represented by different symbols on diagrams.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Junction"]
    class_class_curie: ClassVar[str] = "cim:Junction"
    class_name: ClassVar[str] = "Junction"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Junction


@dataclass(repr=False)
class Line(EquipmentContainer):
    """
    Contains equipment beyond a substation belonging to a power transmission line.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Line"]
    class_class_curie: ClassVar[str] = "cim:Line"
    class_name: ClassVar[str] = "Line"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Line

    ACTieCorridor: Optional[Union[dict, "ACTieCorridor"]] = None
    Region: Optional[Union[dict, "SubGeographicalRegion"]] = None
    SchedulingArea: Optional[Union[dict, "SchedulingArea"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.ACTieCorridor is not None and not isinstance(self.ACTieCorridor, ACTieCorridor):
            self.ACTieCorridor = ACTieCorridor(**as_dict(self.ACTieCorridor))

        if self.Region is not None and not isinstance(self.Region, SubGeographicalRegion):
            self.Region = SubGeographicalRegion(**as_dict(self.Region))

        if self.SchedulingArea is not None and not isinstance(self.SchedulingArea, SchedulingArea):
            self.SchedulingArea = SchedulingArea(**as_dict(self.SchedulingArea))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MeasurementSystem(PowerSystemResource):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["MeasurementSystem"]
    class_class_curie: ClassVar[str] = "cim:MeasurementSystem"
    class_name: ClassVar[str] = "MeasurementSystem"
    class_model_uri: ClassVar[URIRef] = CIMTBL.MeasurementSystem

    reportingRate: Optional[float] = None
    CommunicationLink: Optional[Union[dict, CommunicationLink]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.reportingRate is not None and not isinstance(self.reportingRate, float):
            self.reportingRate = float(self.reportingRate)

        if self.CommunicationLink is not None and not isinstance(self.CommunicationLink, CommunicationLink):
            self.CommunicationLink = CommunicationLink(**as_dict(self.CommunicationLink))

        super().__post_init__(**kwargs)


class DigitalFaultRecorder(MeasurementSystem):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["DigitalFaultRecorder"]
    class_class_curie: ClassVar[str] = "cim:DigitalFaultRecorder"
    class_name: ClassVar[str] = "DigitalFaultRecorder"
    class_model_uri: ClassVar[URIRef] = CIMTBL.DigitalFaultRecorder


class MergingUnit(MeasurementSystem):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["MergingUnit"]
    class_class_curie: ClassVar[str] = "cim:MergingUnit"
    class_name: ClassVar[str] = "MergingUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.MergingUnit


@dataclass(repr=False)
class NonConformLoad(EnergyConsumer):
    """
    NonConformLoad represents loads that do not follow a daily load change pattern and whose changes are not
    correlated with the daily load change pattern.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["NonConformLoad"]
    class_class_curie: ClassVar[str] = "cim:NonConformLoad"
    class_name: ClassVar[str] = "NonConformLoad"
    class_model_uri: ClassVar[URIRef] = CIMTBL.NonConformLoad

    LoadGroup: Optional[Union[dict, NonConformLoadGroup]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.LoadGroup is not None and not isinstance(self.LoadGroup, NonConformLoadGroup):
            self.LoadGroup = NonConformLoadGroup(**as_dict(self.LoadGroup))

        super().__post_init__(**kwargs)


class OutageCoordinationRegion(PowerSystemResource):
    """
    A region that has a common organisation or service responsible for outage planning and coordination and its impact
    on grid operation.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["OutageCoordinationRegion"]
    class_class_curie: ClassVar[str] = "cim:OutageCoordinationRegion"
    class_name: ClassVar[str] = "OutageCoordinationRegion"
    class_model_uri: ClassVar[URIRef] = CIMTBL.OutageCoordinationRegion


@dataclass(repr=False)
class PetersenCoil(EarthFaultCompensator):
    """
    A variable impedance device normally used to offset line charging during single line faults in an ungrounded
    section of network.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PetersenCoil"]
    class_class_curie: ClassVar[str] = "cim:PetersenCoil"
    class_name: ClassVar[str] = "PetersenCoil"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PetersenCoil

    mode: Optional[Union[str, "PetersenCoilModeKind"]] = None
    nominalU: Optional[float] = None
    offsetCurrent: Optional[float] = None
    positionCurrent: Optional[float] = None
    xGroundMax: Optional[float] = None
    xGroundMin: Optional[float] = None
    xGroundNominal: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.mode is not None and not isinstance(self.mode, PetersenCoilModeKind):
            self.mode = PetersenCoilModeKind(self.mode)

        if self.nominalU is not None and not isinstance(self.nominalU, float):
            self.nominalU = float(self.nominalU)

        if self.offsetCurrent is not None and not isinstance(self.offsetCurrent, float):
            self.offsetCurrent = float(self.offsetCurrent)

        if self.positionCurrent is not None and not isinstance(self.positionCurrent, float):
            self.positionCurrent = float(self.positionCurrent)

        if self.xGroundMax is not None and not isinstance(self.xGroundMax, float):
            self.xGroundMax = float(self.xGroundMax)

        if self.xGroundMin is not None and not isinstance(self.xGroundMin, float):
            self.xGroundMin = float(self.xGroundMin)

        if self.xGroundNominal is not None and not isinstance(self.xGroundNominal, float):
            self.xGroundNominal = float(self.xGroundNominal)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PhasorDataConcentrator(PowerSystemResource):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PhasorDataConcentrator"]
    class_class_curie: ClassVar[str] = "cim:PhasorDataConcentrator"
    class_name: ClassVar[str] = "PhasorDataConcentrator"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhasorDataConcentrator

    CentralPDC: Optional[Union[dict, "PhasorDataConcentrator"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.CentralPDC is not None and not isinstance(self.CentralPDC, PhasorDataConcentrator):
            self.CentralPDC = PhasorDataConcentrator(**as_dict(self.CentralPDC))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PhasorMeasurementUnit(MeasurementSystem):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PhasorMeasurementUnit"]
    class_class_curie: ClassVar[str] = "cim:PhasorMeasurementUnit"
    class_name: ClassVar[str] = "PhasorMeasurementUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhasorMeasurementUnit

    timeSourceType: Optional[Union[str, "TimeSourceKind"]] = None
    PhasorDataConcentrator: Optional[Union[dict, PhasorDataConcentrator]] = None
    PMUConfiguration: Optional[Union[dict, PMUConfiguration]] = None
    PMUStream: Optional[Union[dict, PMUStream]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.timeSourceType is not None and not isinstance(self.timeSourceType, TimeSourceKind):
            self.timeSourceType = TimeSourceKind(self.timeSourceType)

        if self.PhasorDataConcentrator is not None and not isinstance(self.PhasorDataConcentrator, PhasorDataConcentrator):
            self.PhasorDataConcentrator = PhasorDataConcentrator(**as_dict(self.PhasorDataConcentrator))

        if self.PMUConfiguration is not None and not isinstance(self.PMUConfiguration, PMUConfiguration):
            self.PMUConfiguration = PMUConfiguration(**as_dict(self.PMUConfiguration))

        if self.PMUStream is not None and not isinstance(self.PMUStream, PMUStream):
            self.PMUStream = PMUStream(**as_dict(self.PMUStream))

        super().__post_init__(**kwargs)


class DisturbanceRecorder(PhasorMeasurementUnit):
    """
    PMU that is also capable of collecting point-on-wave data
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["DisturbanceRecorder"]
    class_class_curie: ClassVar[str] = "cim:DisturbanceRecorder"
    class_name: ClassVar[str] = "DisturbanceRecorder"
    class_model_uri: ClassVar[URIRef] = CIMTBL.DisturbanceRecorder


class Plant(EquipmentContainer):
    """
    A Plant is a collection of equipment for purposes of generation.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Plant"]
    class_class_curie: ClassVar[str] = "cim:Plant"
    class_name: ClassVar[str] = "Plant"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Plant


class PointOnWaveSensor(MeasurementSystem):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PointOnWaveSensor"]
    class_class_curie: ClassVar[str] = "cim:PointOnWaveSensor"
    class_name: ClassVar[str] = "PointOnWaveSensor"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PointOnWaveSensor


@dataclass(repr=False)
class PotentialTransformer(Equipment):
    """
    Instrument transformer (also known as Voltage Transformer) used to measure electrical qualities of the circuit
    that is being protected and/or monitored. Typically used as voltage transducer for the purpose of metering,
    protection, or sometimes auxiliary substation supply. A typical secondary voltage rating would be 120V.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PotentialTransformer"]
    class_class_curie: ClassVar[str] = "cim:PotentialTransformer"
    class_name: ClassVar[str] = "PotentialTransformer"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PotentialTransformer

    nominalRatio: Optional[float] = None
    type: Optional[Union[str, "PotentialTransformerKind"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.nominalRatio is not None and not isinstance(self.nominalRatio, float):
            self.nominalRatio = float(self.nominalRatio)

        if self.type is not None and not isinstance(self.type, PotentialTransformerKind):
            self.type = PotentialTransformerKind(self.type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PowerCutZone(PowerSystemResource):
    """
    An area or zone of the power system which is used for load shedding purposes.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PowerCutZone"]
    class_class_curie: ClassVar[str] = "cim:PowerCutZone"
    class_name: ClassVar[str] = "PowerCutZone"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerCutZone

    cutLevel1: Optional[float] = None
    cutLevel2: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.cutLevel1 is not None and not isinstance(self.cutLevel1, float):
            self.cutLevel1 = float(self.cutLevel1)

        if self.cutLevel2 is not None and not isinstance(self.cutLevel2, float):
            self.cutLevel2 = float(self.cutLevel2)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PowerElectronicsConnectionPhase(PowerSystemResource):
    """
    A single phase of a power electronics connection.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PowerElectronicsConnectionPhase"]
    class_class_curie: ClassVar[str] = "cim:PowerElectronicsConnectionPhase"
    class_name: ClassVar[str] = "PowerElectronicsConnectionPhase"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerElectronicsConnectionPhase

    p: Optional[float] = None
    phase: Optional[Union[str, "SinglePhaseKind"]] = None
    q: Optional[float] = None
    PowerElectronicsConnection: Optional[Union[dict, "PowerElectronicsConnection"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.p is not None and not isinstance(self.p, float):
            self.p = float(self.p)

        if self.phase is not None and not isinstance(self.phase, SinglePhaseKind):
            self.phase = SinglePhaseKind(self.phase)

        if self.q is not None and not isinstance(self.q, float):
            self.q = float(self.q)

        if self.PowerElectronicsConnection is not None and not isinstance(self.PowerElectronicsConnection, PowerElectronicsConnection):
            self.PowerElectronicsConnection = PowerElectronicsConnection(**as_dict(self.PowerElectronicsConnection))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PowerElectronicsUnit(Equipment):
    """
    A generating unit or battery or aggregation that connects to the AC network using power electronics rather than
    rotating machines.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PowerElectronicsUnit"]
    class_class_curie: ClassVar[str] = "cim:PowerElectronicsUnit"
    class_name: ClassVar[str] = "PowerElectronicsUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerElectronicsUnit

    maxP: Optional[float] = None
    minP: Optional[float] = None
    PowerElectronicsConnection: Optional[Union[dict, "PowerElectronicsConnection"]] = None
    PowerElectronicsUnitController: Optional[Union[dict, "PowerElectronicsUnitController"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.maxP is not None and not isinstance(self.maxP, float):
            self.maxP = float(self.maxP)

        if self.minP is not None and not isinstance(self.minP, float):
            self.minP = float(self.minP)

        if self.PowerElectronicsConnection is not None and not isinstance(self.PowerElectronicsConnection, PowerElectronicsConnection):
            self.PowerElectronicsConnection = PowerElectronicsConnection(**as_dict(self.PowerElectronicsConnection))

        if self.PowerElectronicsUnitController is not None and not isinstance(self.PowerElectronicsUnitController, PowerElectronicsUnitController):
            self.PowerElectronicsUnitController = PowerElectronicsUnitController(**as_dict(self.PowerElectronicsUnitController))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BatteryUnit(PowerElectronicsUnit):
    """
    An electrochemical energy storage device.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BatteryUnit"]
    class_class_curie: ClassVar[str] = "cim:BatteryUnit"
    class_name: ClassVar[str] = "BatteryUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BatteryUnit

    batteryState: Optional[Union[str, "BatteryStateKind"]] = None
    chargingEfficiency: Optional[float] = None
    dischargingEfficiency: Optional[float] = None
    idlingP: Optional[float] = None
    idlingQ: Optional[float] = None
    minimumE: Optional[float] = None
    ratedE: Optional[float] = None
    storedE: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.batteryState is not None and not isinstance(self.batteryState, BatteryStateKind):
            self.batteryState = BatteryStateKind(self.batteryState)

        if self.chargingEfficiency is not None and not isinstance(self.chargingEfficiency, float):
            self.chargingEfficiency = float(self.chargingEfficiency)

        if self.dischargingEfficiency is not None and not isinstance(self.dischargingEfficiency, float):
            self.dischargingEfficiency = float(self.dischargingEfficiency)

        if self.idlingP is not None and not isinstance(self.idlingP, float):
            self.idlingP = float(self.idlingP)

        if self.idlingQ is not None and not isinstance(self.idlingQ, float):
            self.idlingQ = float(self.idlingQ)

        if self.minimumE is not None and not isinstance(self.minimumE, float):
            self.minimumE = float(self.minimumE)

        if self.ratedE is not None and not isinstance(self.ratedE, float):
            self.ratedE = float(self.ratedE)

        if self.storedE is not None and not isinstance(self.storedE, float):
            self.storedE = float(self.storedE)

        super().__post_init__(**kwargs)


class ChargingUnit(PowerElectronicsUnit):
    """
    A unit that supplies electrical power for charging electrical non-stationary entities, e.g. electrical vehicle,
    trucks, buses, ferries, boats and airplanes. The characteristic is that the energy consumption is highly schedule
    dependent.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ChargingUnit"]
    class_class_curie: ClassVar[str] = "cim:ChargingUnit"
    class_name: ClassVar[str] = "ChargingUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ChargingUnit


@dataclass(repr=False)
class MobileElectricalUnit(BatteryUnit):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["MobileElectricalUnit"]
    class_class_curie: ClassVar[str] = "cim:MobileElectricalUnit"
    class_name: ClassVar[str] = "MobileElectricalUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.MobileElectricalUnit

    ChargingUnit: Optional[Union[dict, ChargingUnit]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.ChargingUnit is not None and not isinstance(self.ChargingUnit, ChargingUnit):
            self.ChargingUnit = ChargingUnit(**as_dict(self.ChargingUnit))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ElectricalVehicleUnit(MobileElectricalUnit):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ElectricalVehicleUnit"]
    class_class_curie: ClassVar[str] = "cim:ElectricalVehicleUnit"
    class_name: ClassVar[str] = "ElectricalVehicleUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ElectricalVehicleUnit

    v2gCapable: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.v2gCapable is not None and not isinstance(self.v2gCapable, Bool):
            self.v2gCapable = Bool(self.v2gCapable)

        super().__post_init__(**kwargs)


class PhotoVoltaicUnit(PowerElectronicsUnit):
    """
    A photovoltaic device or an aggregation of such devices.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PhotoVoltaicUnit"]
    class_class_curie: ClassVar[str] = "cim:PhotoVoltaicUnit"
    class_name: ClassVar[str] = "PhotoVoltaicUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhotoVoltaicUnit


@dataclass(repr=False)
class PowerElectricalChemicalUnit(PowerElectronicsUnit):
    """
    A unit capable of either generating electrical energy from chemical reactions or using electrical energy to cause
    chemical reactions.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PowerElectricalChemicalUnit"]
    class_class_curie: ClassVar[str] = "cim:PowerElectricalChemicalUnit"
    class_name: ClassVar[str] = "PowerElectricalChemicalUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerElectricalChemicalUnit

    kind: Optional[Union[str, "PowerElectricalChemicalUnitKind"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.kind is not None and not isinstance(self.kind, PowerElectricalChemicalUnitKind):
            self.kind = PowerElectricalChemicalUnitKind(self.kind)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PowerElectronicsMarineUnit(PowerElectronicsUnit):
    """
    A unit that capture energy from marine sources, e.g. waves, for generating electrical power.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PowerElectronicsMarineUnit"]
    class_class_curie: ClassVar[str] = "cim:PowerElectronicsMarineUnit"
    class_name: ClassVar[str] = "PowerElectronicsMarineUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerElectronicsMarineUnit

    kind: Optional[Union[str, "MarineUnitKind"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.kind is not None and not isinstance(self.kind, MarineUnitKind):
            self.kind = MarineUnitKind(self.kind)

        super().__post_init__(**kwargs)


class PowerElectronicsThermalUnit(PowerElectronicsUnit):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PowerElectronicsThermalUnit"]
    class_class_curie: ClassVar[str] = "cim:PowerElectronicsThermalUnit"
    class_name: ClassVar[str] = "PowerElectronicsThermalUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerElectronicsThermalUnit


class PowerElectronicsUnitController(EquipmentController):
    """
    Power electronics unit controller is controlling the equipment to optimize the power electronics unit.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PowerElectronicsUnitController"]
    class_class_curie: ClassVar[str] = "cim:PowerElectronicsUnitController"
    class_name: ClassVar[str] = "PowerElectronicsUnitController"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerElectronicsUnitController


class PowerElectronicsWindUnit(PowerElectronicsUnit):
    """
    A wind generating unit that connects to the AC network with power electronics rather than rotating machines or an
    aggregation of such units.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PowerElectronicsWindUnit"]
    class_class_curie: ClassVar[str] = "cim:PowerElectronicsWindUnit"
    class_name: ClassVar[str] = "PowerElectronicsWindUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerElectronicsWindUnit


class PowerFrequencyController(PowerSystemResource):
    """
    Power frequency controller is controlling the active power balance as typically done by the secondary control. If
    an unbalance between the scheduled active power values of each generation unit and the loads plus losses occurs,
    primary control will adapt (increase/decrease) the active power production of each unit (depending on the power
    shift key strategy), leading to an over- or under-frequency situation. The secondary frequency controller will
    then control the frequency back to its nominal value, re- establishing a cost-efficient generation delivered by
    each unit.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PowerFrequencyController"]
    class_class_curie: ClassVar[str] = "cim:PowerFrequencyController"
    class_name: ClassVar[str] = "PowerFrequencyController"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerFrequencyController


class PowerTransferCorridor(PowerSystemResource):
    """
    A power transfer corridor is defined as a set of circuits (transmission lines or transformers) separating two
    portions of the power system, or a subset of circuits exposed to a substantial portion of the transmission
    exchange between two parts of the system.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PowerTransferCorridor"]
    class_class_curie: ClassVar[str] = "cim:PowerTransferCorridor"
    class_name: ClassVar[str] = "PowerTransferCorridor"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerTransferCorridor


@dataclass(repr=False)
class PowerTransformer(ConductingEquipment):
    """
    An electrical device consisting of two or more coupled windings, with or without a magnetic core, for introducing
    mutual coupling between electric circuits. Transformers can be used to control voltage and phase shift (active
    power flow).A power transformer may be composed of separate transformer tanks that need not be identical.A power
    transformer can be modelled with or without tanks and is intended for use in both balanced and unbalanced
    representations. A power transformer typically has two terminals, but may have one (grounding), three or more
    terminals.The inherited association ConductingEquipment.BaseVoltage should not be used. The association from
    TransformerEnd to BaseVoltage should be used instead.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PowerTransformer"]
    class_class_curie: ClassVar[str] = "cim:PowerTransformer"
    class_name: ClassVar[str] = "PowerTransformer"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerTransformer

    beforeShCircuitHighestOperatingCurrent: Optional[float] = None
    beforeShCircuitHighestOperatingVoltage: Optional[float] = None
    beforeShortCircuitAnglePf: Optional[float] = None
    highSideMinOperatingU: Optional[float] = None
    isPartOfGeneratorUnit: Optional[Union[bool, Bool]] = None
    operationalValuesConsidered: Optional[Union[bool, Bool]] = None
    vectorGroup: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.beforeShCircuitHighestOperatingCurrent is not None and not isinstance(self.beforeShCircuitHighestOperatingCurrent, float):
            self.beforeShCircuitHighestOperatingCurrent = float(self.beforeShCircuitHighestOperatingCurrent)

        if self.beforeShCircuitHighestOperatingVoltage is not None and not isinstance(self.beforeShCircuitHighestOperatingVoltage, float):
            self.beforeShCircuitHighestOperatingVoltage = float(self.beforeShCircuitHighestOperatingVoltage)

        if self.beforeShortCircuitAnglePf is not None and not isinstance(self.beforeShortCircuitAnglePf, float):
            self.beforeShortCircuitAnglePf = float(self.beforeShortCircuitAnglePf)

        if self.highSideMinOperatingU is not None and not isinstance(self.highSideMinOperatingU, float):
            self.highSideMinOperatingU = float(self.highSideMinOperatingU)

        if self.isPartOfGeneratorUnit is not None and not isinstance(self.isPartOfGeneratorUnit, Bool):
            self.isPartOfGeneratorUnit = Bool(self.isPartOfGeneratorUnit)

        if self.operationalValuesConsidered is not None and not isinstance(self.operationalValuesConsidered, Bool):
            self.operationalValuesConsidered = Bool(self.operationalValuesConsidered)

        if self.vectorGroup is not None and not isinstance(self.vectorGroup, str):
            self.vectorGroup = str(self.vectorGroup)

        super().__post_init__(**kwargs)


class PowerTransformerInfo(AssetInfo):
    """
    Set of power transformer data, from an equipment library.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PowerTransformerInfo"]
    class_class_curie: ClassVar[str] = "cim:PowerTransformerInfo"
    class_name: ClassVar[str] = "PowerTransformerInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerTransformerInfo


class ProductAssetModel(IdentifiedObject):
    """
    Asset model by a specific manufacturer.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ProductAssetModel"]
    class_class_curie: ClassVar[str] = "cim:ProductAssetModel"
    class_name: ClassVar[str] = "ProductAssetModel"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ProductAssetModel


class RatioTapChangerTable(IdentifiedObject):
    """
    Describes a curve for how the voltage magnitude and impedance varies with the tap step.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["RatioTapChangerTable"]
    class_class_curie: ClassVar[str] = "cim:RatioTapChangerTable"
    class_name: ClassVar[str] = "RatioTapChangerTable"
    class_model_uri: ClassVar[URIRef] = CIMTBL.RatioTapChangerTable


@dataclass(repr=False)
class ReactiveCapabilityCurve(Curve):
    """
    Reactive power rating envelope versus the synchronous machine's active power, in both the generating and motoring
    modes. For each active power value there is a corresponding high and low reactive power limit value. Typically
    there will be a separate curve for each coolant condition, such as hydrogen pressure. The Y1 axis values represent
    reactive minimum and the Y2 axis values represent reactive maximum.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ReactiveCapabilityCurve"]
    class_class_curie: ClassVar[str] = "cim:ReactiveCapabilityCurve"
    class_name: ClassVar[str] = "ReactiveCapabilityCurve"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ReactiveCapabilityCurve

    coolantTemperature: Optional[float] = None
    hydrogenPressure: Optional[float] = None
    referenceVoltage: Optional[float] = None
    ExtendedWardEquivalent: Optional[Union[dict, ExtendedWardEquivalent]] = None
    SynchronousMachine: Optional[Union[dict, "SynchronousMachine"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.coolantTemperature is not None and not isinstance(self.coolantTemperature, float):
            self.coolantTemperature = float(self.coolantTemperature)

        if self.hydrogenPressure is not None and not isinstance(self.hydrogenPressure, float):
            self.hydrogenPressure = float(self.hydrogenPressure)

        if self.referenceVoltage is not None and not isinstance(self.referenceVoltage, float):
            self.referenceVoltage = float(self.referenceVoltage)

        if self.ExtendedWardEquivalent is not None and not isinstance(self.ExtendedWardEquivalent, ExtendedWardEquivalent):
            self.ExtendedWardEquivalent = ExtendedWardEquivalent(**as_dict(self.ExtendedWardEquivalent))

        if self.SynchronousMachine is not None and not isinstance(self.SynchronousMachine, SynchronousMachine):
            self.SynchronousMachine = SynchronousMachine(**as_dict(self.SynchronousMachine))

        super().__post_init__(**kwargs)


class RecoveryOverloadLimitCurve(Curve):
    """
    The relation between the recovery time and an overload limit.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["RecoveryOverloadLimitCurve"]
    class_class_curie: ClassVar[str] = "cim:RecoveryOverloadLimitCurve"
    class_name: ClassVar[str] = "RecoveryOverloadLimitCurve"
    class_model_uri: ClassVar[URIRef] = CIMTBL.RecoveryOverloadLimitCurve


@dataclass(repr=False)
class RegularIntervalSchedule(BasicIntervalSchedule):
    """
    The schedule has time points where the time between them is constant.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["RegularIntervalSchedule"]
    class_class_curie: ClassVar[str] = "cim:RegularIntervalSchedule"
    class_name: ClassVar[str] = "RegularIntervalSchedule"
    class_model_uri: ClassVar[URIRef] = CIMTBL.RegularIntervalSchedule

    endTime: Optional[Union[str, XSDDateTime]] = None
    timeStep: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.endTime is not None and not isinstance(self.endTime, XSDDateTime):
            self.endTime = XSDDateTime(self.endTime)

        if self.timeStep is not None and not isinstance(self.timeStep, float):
            self.timeStep = float(self.timeStep)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PointOnWaveValue(RegularIntervalSchedule):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PointOnWaveValue"]
    class_class_curie: ClassVar[str] = "cim:PointOnWaveValue"
    class_name: ClassVar[str] = "PointOnWaveValue"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PointOnWaveValue

    Analog: Optional[Union[dict, Analog]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.Analog is not None and not isinstance(self.Analog, Analog):
            self.Analog = Analog(**as_dict(self.Analog))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RegularTimePoint(YAMLRoot):
    """
    Time point for a schedule where the time between the consecutive points is constant.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["RegularTimePoint"]
    class_class_curie: ClassVar[str] = "cim:RegularTimePoint"
    class_name: ClassVar[str] = "RegularTimePoint"
    class_model_uri: ClassVar[URIRef] = CIMTBL.RegularTimePoint

    sequenceNumber: Optional[int] = None
    value1: Optional[float] = None
    value2: Optional[float] = None
    value3: Optional[float] = None
    IntervalSchedule: Optional[Union[dict, RegularIntervalSchedule]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.sequenceNumber is not None and not isinstance(self.sequenceNumber, int):
            self.sequenceNumber = int(self.sequenceNumber)

        if self.value1 is not None and not isinstance(self.value1, float):
            self.value1 = float(self.value1)

        if self.value2 is not None and not isinstance(self.value2, float):
            self.value2 = float(self.value2)

        if self.value3 is not None and not isinstance(self.value3, float):
            self.value3 = float(self.value3)

        if self.IntervalSchedule is not None and not isinstance(self.IntervalSchedule, RegularIntervalSchedule):
            self.IntervalSchedule = RegularIntervalSchedule(**as_dict(self.IntervalSchedule))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RegulatingCondEq(EnergyConnection):
    """
    A type of conducting equipment that can regulate a quantity (i.e. voltage or flow) at a specific point in the
    network.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["RegulatingCondEq"]
    class_class_curie: ClassVar[str] = "cim:RegulatingCondEq"
    class_name: ClassVar[str] = "RegulatingCondEq"
    class_model_uri: ClassVar[URIRef] = CIMTBL.RegulatingCondEq

    controlEnabled: Optional[Union[bool, Bool]] = None
    EquipmentController: Optional[Union[dict, EquipmentController]] = None
    RegulatingControl: Optional[Union[dict, "RegulatingControl"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.controlEnabled is not None and not isinstance(self.controlEnabled, Bool):
            self.controlEnabled = Bool(self.controlEnabled)

        if self.EquipmentController is not None and not isinstance(self.EquipmentController, EquipmentController):
            self.EquipmentController = EquipmentController(**as_dict(self.EquipmentController))

        if self.RegulatingControl is not None and not isinstance(self.RegulatingControl, RegulatingControl):
            self.RegulatingControl = RegulatingControl(**as_dict(self.RegulatingControl))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ExternalNetworkInjection(RegulatingCondEq):
    """
    This class represents the external network for use in power flow and short-circuit calculations.In the power flow
    domain the external network is modelled as a power injection with power limits and a power-frequency bias. For
    short-circuit calculations the external network is modelled as the �network feeders� element defined in section
    6.2 of IEC60909-0:2016. Boolean flag ikSecond allows short-circuit calculations using the superposition method to
    detect that the maximum and minimum initial symmetrical short-circuit currents have to be corrected for the fact
    that they were calculated according the IEC60909-0 method.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ExternalNetworkInjection"]
    class_class_curie: ClassVar[str] = "cim:ExternalNetworkInjection"
    class_name: ClassVar[str] = "ExternalNetworkInjection"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ExternalNetworkInjection

    governorSCD: Optional[float] = None
    ikSecond: Optional[Union[bool, Bool]] = None
    maxInitialSymShCCurrent: Optional[float] = None
    maxP: Optional[float] = None
    maxQ: Optional[float] = None
    maxR0ToX0Ratio: Optional[float] = None
    maxR1ToX1Ratio: Optional[float] = None
    maxZ0ToZ1Ratio: Optional[float] = None
    minInitialSymShCCurrent: Optional[float] = None
    minP: Optional[float] = None
    minQ: Optional[float] = None
    minR0ToX0Ratio: Optional[float] = None
    minR1ToX1Ratio: Optional[float] = None
    minZ0ToZ1Ratio: Optional[float] = None
    p: Optional[float] = None
    q: Optional[float] = None
    referencePriority: Optional[int] = None
    voltageFactor: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.governorSCD is not None and not isinstance(self.governorSCD, float):
            self.governorSCD = float(self.governorSCD)

        if self.ikSecond is not None and not isinstance(self.ikSecond, Bool):
            self.ikSecond = Bool(self.ikSecond)

        if self.maxInitialSymShCCurrent is not None and not isinstance(self.maxInitialSymShCCurrent, float):
            self.maxInitialSymShCCurrent = float(self.maxInitialSymShCCurrent)

        if self.maxP is not None and not isinstance(self.maxP, float):
            self.maxP = float(self.maxP)

        if self.maxQ is not None and not isinstance(self.maxQ, float):
            self.maxQ = float(self.maxQ)

        if self.maxR0ToX0Ratio is not None and not isinstance(self.maxR0ToX0Ratio, float):
            self.maxR0ToX0Ratio = float(self.maxR0ToX0Ratio)

        if self.maxR1ToX1Ratio is not None and not isinstance(self.maxR1ToX1Ratio, float):
            self.maxR1ToX1Ratio = float(self.maxR1ToX1Ratio)

        if self.maxZ0ToZ1Ratio is not None and not isinstance(self.maxZ0ToZ1Ratio, float):
            self.maxZ0ToZ1Ratio = float(self.maxZ0ToZ1Ratio)

        if self.minInitialSymShCCurrent is not None and not isinstance(self.minInitialSymShCCurrent, float):
            self.minInitialSymShCCurrent = float(self.minInitialSymShCCurrent)

        if self.minP is not None and not isinstance(self.minP, float):
            self.minP = float(self.minP)

        if self.minQ is not None and not isinstance(self.minQ, float):
            self.minQ = float(self.minQ)

        if self.minR0ToX0Ratio is not None and not isinstance(self.minR0ToX0Ratio, float):
            self.minR0ToX0Ratio = float(self.minR0ToX0Ratio)

        if self.minR1ToX1Ratio is not None and not isinstance(self.minR1ToX1Ratio, float):
            self.minR1ToX1Ratio = float(self.minR1ToX1Ratio)

        if self.minZ0ToZ1Ratio is not None and not isinstance(self.minZ0ToZ1Ratio, float):
            self.minZ0ToZ1Ratio = float(self.minZ0ToZ1Ratio)

        if self.p is not None and not isinstance(self.p, float):
            self.p = float(self.p)

        if self.q is not None and not isinstance(self.q, float):
            self.q = float(self.q)

        if self.referencePriority is not None and not isinstance(self.referencePriority, int):
            self.referencePriority = int(self.referencePriority)

        if self.voltageFactor is not None and not isinstance(self.voltageFactor, float):
            self.voltageFactor = float(self.voltageFactor)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FACTSEquipment(RegulatingCondEq):
    """
    Flexible Alternating Current Transmission System regulating equipment.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["FACTSEquipment"]
    class_class_curie: ClassVar[str] = "cim:FACTSEquipment"
    class_name: ClassVar[str] = "FACTSEquipment"
    class_model_uri: ClassVar[URIRef] = CIMTBL.FACTSEquipment

    maxC: Optional[float] = None
    maxL: Optional[float] = None
    minC: Optional[float] = None
    minL: Optional[float] = None
    q: Optional[float] = None
    ratedC: Optional[float] = None
    ratedI: Optional[float] = None
    ratedL: Optional[float] = None
    ratedU: Optional[float] = None
    slope: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.maxC is not None and not isinstance(self.maxC, float):
            self.maxC = float(self.maxC)

        if self.maxL is not None and not isinstance(self.maxL, float):
            self.maxL = float(self.maxL)

        if self.minC is not None and not isinstance(self.minC, float):
            self.minC = float(self.minC)

        if self.minL is not None and not isinstance(self.minL, float):
            self.minL = float(self.minL)

        if self.q is not None and not isinstance(self.q, float):
            self.q = float(self.q)

        if self.ratedC is not None and not isinstance(self.ratedC, float):
            self.ratedC = float(self.ratedC)

        if self.ratedI is not None and not isinstance(self.ratedI, float):
            self.ratedI = float(self.ratedI)

        if self.ratedL is not None and not isinstance(self.ratedL, float):
            self.ratedL = float(self.ratedL)

        if self.ratedU is not None and not isinstance(self.ratedU, float):
            self.ratedU = float(self.ratedU)

        if self.slope is not None and not isinstance(self.slope, float):
            self.slope = float(self.slope)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FrequencyConverter(RegulatingCondEq):
    """
    A device to convert from one frequency to another (e.g., frequency F1 to F2) comprises a pair of
    FrequencyConverter instances. One converts from F1 to DC, the other converts the DC to F2.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["FrequencyConverter"]
    class_class_curie: ClassVar[str] = "cim:FrequencyConverter"
    class_name: ClassVar[str] = "FrequencyConverter"
    class_model_uri: ClassVar[URIRef] = CIMTBL.FrequencyConverter

    frequency: Optional[float] = None
    maxP: Optional[float] = None
    maxU: Optional[float] = None
    minP: Optional[float] = None
    minU: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.frequency is not None and not isinstance(self.frequency, float):
            self.frequency = float(self.frequency)

        if self.maxP is not None and not isinstance(self.maxP, float):
            self.maxP = float(self.maxP)

        if self.maxU is not None and not isinstance(self.maxU, float):
            self.maxU = float(self.maxU)

        if self.minP is not None and not isinstance(self.minP, float):
            self.minP = float(self.minP)

        if self.minU is not None and not isinstance(self.minU, float):
            self.minU = float(self.minU)

        super().__post_init__(**kwargs)


class ModularStaticSynchronousSeriesCompensator(FACTSEquipment):
    """
    Modular static synchronous series compensator (MSSSC) is a type of flexible AC transmission system regulating
    equipment which consists of solid-state voltage source inverter connected in series with a transmission line. This
    is similar to static synchronous series compensator (SSSC), but without injection transformer. This enables the
    MSSSC to be truly modular with the ability to simply install a number of equipment in series to provide a desired
    maximum level of impedance. MSSSC can be dispersed into multiple location in a circuit working collectively under
    the same controller scheme.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ModularStaticSynchronousSeriesCompensator"]
    class_class_curie: ClassVar[str] = "cim:ModularStaticSynchronousSeriesCompensator"
    class_name: ClassVar[str] = "ModularStaticSynchronousSeriesCompensator"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ModularStaticSynchronousSeriesCompensator


@dataclass(repr=False)
class PowerElectronicsConnection(RegulatingCondEq):
    """
    A connection to the AC network for energy production or consumption that uses power electronics rather than
    rotating machines.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PowerElectronicsConnection"]
    class_class_curie: ClassVar[str] = "cim:PowerElectronicsConnection"
    class_name: ClassVar[str] = "PowerElectronicsConnection"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerElectronicsConnection

    inSafeMode: Optional[Union[bool, Bool]] = None
    isGridForming: Optional[Union[bool, Bool]] = None
    maxIFault: Optional[float] = None
    maxQ: Optional[float] = None
    minQ: Optional[float] = None
    p: Optional[float] = None
    q: Optional[float] = None
    ratedS: Optional[float] = None
    ratedU: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.inSafeMode is not None and not isinstance(self.inSafeMode, Bool):
            self.inSafeMode = Bool(self.inSafeMode)

        if self.isGridForming is not None and not isinstance(self.isGridForming, Bool):
            self.isGridForming = Bool(self.isGridForming)

        if self.maxIFault is not None and not isinstance(self.maxIFault, float):
            self.maxIFault = float(self.maxIFault)

        if self.maxQ is not None and not isinstance(self.maxQ, float):
            self.maxQ = float(self.maxQ)

        if self.minQ is not None and not isinstance(self.minQ, float):
            self.minQ = float(self.minQ)

        if self.p is not None and not isinstance(self.p, float):
            self.p = float(self.p)

        if self.q is not None and not isinstance(self.q, float):
            self.q = float(self.q)

        if self.ratedS is not None and not isinstance(self.ratedS, float):
            self.ratedS = float(self.ratedS)

        if self.ratedU is not None and not isinstance(self.ratedU, float):
            self.ratedU = float(self.ratedU)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EVSE(PowerElectronicsConnection):
    """
    Equipment or a combination of equipment, providing dedicated functions to supply electric energy from a fixed
    electrical installation or supply network to an EV for the purpose of charging and discharging [SOURCE: IEC
    61851-1:2017, 3.1.1, modifiedElectric Vehicle Supply Equipment (EVSE) is a power conversion and interface device
    that enables electric vehicles to connect to the power system for charging or, when supported, discharging (V2G).
    An EVSE controls the flow of power between the grid (or local DER/microgrid resources) and the connected vehicle
    battery, ensuring safety, interoperability, and adherence to communication standards.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EVSE"]
    class_class_curie: ClassVar[str] = "cim:EVSE"
    class_name: ClassVar[str] = "EVSE"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EVSE

    chargingModeType: Optional[Union[str, "ChargingModeKind"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.chargingModeType is not None and not isinstance(self.chargingModeType, ChargingModeKind):
            self.chargingModeType = ChargingModeKind(self.chargingModeType)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RegulatingControl(EquipmentController):
    """
    Specifies a set of equipment that works together to control a power system quantity such as voltage or flow.Remote
    bus voltage control is possible by specifying the controlled terminal located at some place remote from the
    controlling equipment.The specified terminal shall be associated with the connectivity node of the controlled
    point. The most specific subtype of RegulatingControl shall be used in case such equipment participate in the
    control, e.g. TapChangerControl for tap changers.For flow control, load sign convention is used, i.e. positive
    sign means flow out from a TopologicalNode (bus) into the conducting equipment.The attribute minAllowedTargetValue
    and maxAllowedTargetValue are required in the following cases:- For a power generating module operated in power
    factor control mode to specify maximum and minimum power factor values;- Whenever it is necessary to have an off
    center target voltage for the tap changer regulator. For instance, due to long cables to off shore wind farms and
    the need to have a simpler setup at the off shore transformer platform, the voltage is controlled from the land at
    the connection point for the off shore wind farm. Since there usually is a voltage rise along the cable, there is
    typical and overvoltage of up 3 to 4 kV compared to the on shore station. Thus in normal operation the tap changer
    on the on shore station is operated with a target set point, which is in the lower parts of the dead band.The
    attributes minAllowedTargetValue and maxAllowedTargetValue are not related to the attribute targetDeadband and
    thus they are not treated as an alternative of the targetDeadband. They are needed due to limitations in the local
    substation controller. The attribute targetDeadband is used to prevent the power flow from moving the tap position
    in circles (hunting) that is to be used regardless of the attributes minAllowedTargetValue and
    maxAllowedTargetValue.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["RegulatingControl"]
    class_class_curie: ClassVar[str] = "cim:RegulatingControl"
    class_name: ClassVar[str] = "RegulatingControl"
    class_model_uri: ClassVar[URIRef] = CIMTBL.RegulatingControl

    ctRatio: Optional[float] = None
    discrete: Optional[Union[bool, Bool]] = None
    enabled: Optional[Union[bool, Bool]] = None
    maxAllowedTargetValue: Optional[float] = None
    minAllowedTargetValue: Optional[float] = None
    mode: Optional[Union[str, "RegulatingControlModeKind"]] = None
    monitoredPhase: Optional[Union[str, "PhaseCode"]] = None
    ptRatio: Optional[float] = None
    reverseTargetDeadband: Optional[float] = None
    reverseTargetValue: Optional[float] = None
    targetDeadband: Optional[float] = None
    targetValue: Optional[float] = None
    targetValueUnitMultiplier: Optional[Union[str, "UnitMultiplier"]] = None
    Terminal: Optional[Union[dict, "Terminal"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.ctRatio is not None and not isinstance(self.ctRatio, float):
            self.ctRatio = float(self.ctRatio)

        if self.discrete is not None and not isinstance(self.discrete, Bool):
            self.discrete = Bool(self.discrete)

        if self.enabled is not None and not isinstance(self.enabled, Bool):
            self.enabled = Bool(self.enabled)

        if self.maxAllowedTargetValue is not None and not isinstance(self.maxAllowedTargetValue, float):
            self.maxAllowedTargetValue = float(self.maxAllowedTargetValue)

        if self.minAllowedTargetValue is not None and not isinstance(self.minAllowedTargetValue, float):
            self.minAllowedTargetValue = float(self.minAllowedTargetValue)

        if self.mode is not None and not isinstance(self.mode, RegulatingControlModeKind):
            self.mode = RegulatingControlModeKind(self.mode)

        if self.monitoredPhase is not None and not isinstance(self.monitoredPhase, PhaseCode):
            self.monitoredPhase = PhaseCode(self.monitoredPhase)

        if self.ptRatio is not None and not isinstance(self.ptRatio, float):
            self.ptRatio = float(self.ptRatio)

        if self.reverseTargetDeadband is not None and not isinstance(self.reverseTargetDeadband, float):
            self.reverseTargetDeadband = float(self.reverseTargetDeadband)

        if self.reverseTargetValue is not None and not isinstance(self.reverseTargetValue, float):
            self.reverseTargetValue = float(self.reverseTargetValue)

        if self.targetDeadband is not None and not isinstance(self.targetDeadband, float):
            self.targetDeadband = float(self.targetDeadband)

        if self.targetValue is not None and not isinstance(self.targetValue, float):
            self.targetValue = float(self.targetValue)

        if self.targetValueUnitMultiplier is not None and not isinstance(self.targetValueUnitMultiplier, UnitMultiplier):
            self.targetValueUnitMultiplier = UnitMultiplier(self.targetValueUnitMultiplier)

        if self.Terminal is not None and not isinstance(self.Terminal, Terminal):
            self.Terminal = Terminal(**as_dict(self.Terminal))

        super().__post_init__(**kwargs)


class RelativeHeight(YAMLRoot):
    """
    Used to specify the height of a physical object relative to a specified reference. The X, Y, and Z positions for a
    given point describe the position of a point in space expressed in appropriate coordinate system units. In
    general, the Z-position will represent the ground-level altitude above sea level for the point. At times it is
    beneficial to know the height above ground level at which a particular piece of equipment is installed. For
    example, the location of a pole-mounted weather station may be specified as �10 meters above ground level� by
    specifying a vertical offset of �10 meters� and a vertical offset reference of �Ground Level�. Alternately, it
    could be specified as �1 meter below the top of the pole� using a vertical offset of �-1 meter� and vertical
    offset reference of �Pole Top�.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["RelativeHeight"]
    class_class_curie: ClassVar[str] = "cim:RelativeHeight"
    class_name: ClassVar[str] = "RelativeHeight"
    class_model_uri: ClassVar[URIRef] = CIMTBL.RelativeHeight


class RemoteSource(IdentifiedObject):
    """
    Remote sources are state variables that are telemetered or calculated within the remote unit.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["RemoteSource"]
    class_class_curie: ClassVar[str] = "cim:RemoteSource"
    class_name: ClassVar[str] = "RemoteSource"
    class_model_uri: ClassVar[URIRef] = CIMTBL.RemoteSource


class ReportingGroup(IdentifiedObject):
    """
    A reporting group is used for various ad-hoc groupings used for reporting.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ReportingGroup"]
    class_class_curie: ClassVar[str] = "cim:ReportingGroup"
    class_name: ClassVar[str] = "ReportingGroup"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ReportingGroup


class ResourceContainer(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ResourceContainer"]
    class_class_curie: ClassVar[str] = "cim:ResourceContainer"
    class_name: ClassVar[str] = "ResourceContainer"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ResourceContainer


@dataclass(repr=False)
class RotatingMachine(RegulatingCondEq):
    """
    A rotating machine which may be used as a generator or motor.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["RotatingMachine"]
    class_class_curie: ClassVar[str] = "cim:RotatingMachine"
    class_name: ClassVar[str] = "RotatingMachine"
    class_model_uri: ClassVar[URIRef] = CIMTBL.RotatingMachine

    p: Optional[float] = None
    q: Optional[float] = None
    ratedPowerFactor: Optional[float] = None
    ratedS: Optional[float] = None
    ratedU: Optional[float] = None
    GeneratingUnit: Optional[Union[dict, GeneratingUnit]] = None
    HydroPump: Optional[Union[dict, HydroPump]] = None
    RotatingMachinePhase: Optional[Union[dict, "RotatingMachinePhase"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.p is not None and not isinstance(self.p, float):
            self.p = float(self.p)

        if self.q is not None and not isinstance(self.q, float):
            self.q = float(self.q)

        if self.ratedPowerFactor is not None and not isinstance(self.ratedPowerFactor, float):
            self.ratedPowerFactor = float(self.ratedPowerFactor)

        if self.ratedS is not None and not isinstance(self.ratedS, float):
            self.ratedS = float(self.ratedS)

        if self.ratedU is not None and not isinstance(self.ratedU, float):
            self.ratedU = float(self.ratedU)

        if self.GeneratingUnit is not None and not isinstance(self.GeneratingUnit, GeneratingUnit):
            self.GeneratingUnit = GeneratingUnit(**as_dict(self.GeneratingUnit))

        if self.HydroPump is not None and not isinstance(self.HydroPump, HydroPump):
            self.HydroPump = HydroPump(**as_dict(self.HydroPump))

        if self.RotatingMachinePhase is not None and not isinstance(self.RotatingMachinePhase, RotatingMachinePhase):
            self.RotatingMachinePhase = RotatingMachinePhase(**as_dict(self.RotatingMachinePhase))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AsynchronousMachine(RotatingMachine):
    """
    A rotating machine whose shaft rotates asynchronously with the electrical field. Also known as an induction
    machine with no external connection to the rotor windings, e.g. squirrel-cage induction machine.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["AsynchronousMachine"]
    class_class_curie: ClassVar[str] = "cim:AsynchronousMachine"
    class_name: ClassVar[str] = "AsynchronousMachine"
    class_model_uri: ClassVar[URIRef] = CIMTBL.AsynchronousMachine

    asynchronousMachineType: Optional[Union[str, "AsynchronousMachineKind"]] = None
    converterFedDrive: Optional[Union[bool, Bool]] = None
    efficiency: Optional[float] = None
    iaIrRatio: Optional[float] = None
    nominalFrequency: Optional[float] = None
    nominalSpeed: Optional[float] = None
    polePairNumber: Optional[int] = None
    ratedMechanicalPower: Optional[float] = None
    reversible: Optional[Union[bool, Bool]] = None
    rr1: Optional[float] = None
    rr2: Optional[float] = None
    rxLockedRotorRatio: Optional[float] = None
    tpo: Optional[float] = None
    tppo: Optional[float] = None
    xlr1: Optional[float] = None
    xlr2: Optional[float] = None
    xm: Optional[float] = None
    xp: Optional[float] = None
    xpp: Optional[float] = None
    xs: Optional[float] = None
    AsynchronousMachineDynamics: Optional[Union[dict, AsynchronousMachineDynamics]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.asynchronousMachineType is not None and not isinstance(self.asynchronousMachineType, AsynchronousMachineKind):
            self.asynchronousMachineType = AsynchronousMachineKind(self.asynchronousMachineType)

        if self.converterFedDrive is not None and not isinstance(self.converterFedDrive, Bool):
            self.converterFedDrive = Bool(self.converterFedDrive)

        if self.efficiency is not None and not isinstance(self.efficiency, float):
            self.efficiency = float(self.efficiency)

        if self.iaIrRatio is not None and not isinstance(self.iaIrRatio, float):
            self.iaIrRatio = float(self.iaIrRatio)

        if self.nominalFrequency is not None and not isinstance(self.nominalFrequency, float):
            self.nominalFrequency = float(self.nominalFrequency)

        if self.nominalSpeed is not None and not isinstance(self.nominalSpeed, float):
            self.nominalSpeed = float(self.nominalSpeed)

        if self.polePairNumber is not None and not isinstance(self.polePairNumber, int):
            self.polePairNumber = int(self.polePairNumber)

        if self.ratedMechanicalPower is not None and not isinstance(self.ratedMechanicalPower, float):
            self.ratedMechanicalPower = float(self.ratedMechanicalPower)

        if self.reversible is not None and not isinstance(self.reversible, Bool):
            self.reversible = Bool(self.reversible)

        if self.rr1 is not None and not isinstance(self.rr1, float):
            self.rr1 = float(self.rr1)

        if self.rr2 is not None and not isinstance(self.rr2, float):
            self.rr2 = float(self.rr2)

        if self.rxLockedRotorRatio is not None and not isinstance(self.rxLockedRotorRatio, float):
            self.rxLockedRotorRatio = float(self.rxLockedRotorRatio)

        if self.tpo is not None and not isinstance(self.tpo, float):
            self.tpo = float(self.tpo)

        if self.tppo is not None and not isinstance(self.tppo, float):
            self.tppo = float(self.tppo)

        if self.xlr1 is not None and not isinstance(self.xlr1, float):
            self.xlr1 = float(self.xlr1)

        if self.xlr2 is not None and not isinstance(self.xlr2, float):
            self.xlr2 = float(self.xlr2)

        if self.xm is not None and not isinstance(self.xm, float):
            self.xm = float(self.xm)

        if self.xp is not None and not isinstance(self.xp, float):
            self.xp = float(self.xp)

        if self.xpp is not None and not isinstance(self.xpp, float):
            self.xpp = float(self.xpp)

        if self.xs is not None and not isinstance(self.xs, float):
            self.xs = float(self.xs)

        if self.AsynchronousMachineDynamics is not None and not isinstance(self.AsynchronousMachineDynamics, AsynchronousMachineDynamics):
            self.AsynchronousMachineDynamics = AsynchronousMachineDynamics(**as_dict(self.AsynchronousMachineDynamics))

        super().__post_init__(**kwargs)


class RotatingMachinePhase(PowerSystemResource):
    """
    Represents a single-phase motor or generator. The specifics of the RotatingMachinePhase (e.g. type) are determined
    by the associated asynchronous or synchronous machine along with the specific generating unit associated to the
    rotating machine.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["RotatingMachinePhase"]
    class_class_curie: ClassVar[str] = "cim:RotatingMachinePhase"
    class_name: ClassVar[str] = "RotatingMachinePhase"
    class_model_uri: ClassVar[URIRef] = CIMTBL.RotatingMachinePhase


@dataclass(repr=False)
class SSSCController(EquipmentController):
    """
    The controller of a Static synchronous series compensator (SSSC).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SSSCController"]
    class_class_curie: ClassVar[str] = "cim:SSSCController"
    class_name: ClassVar[str] = "SSSCController"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SSSCController

    maxInjectionU: Optional[float] = None
    maxLimitI: Optional[float] = None
    minInjectionU: Optional[float] = None
    minLimitI: Optional[float] = None
    mode: Optional[Union[str, "SSSCControlModeKind"]] = None
    CurrentDroopOverride: Optional[Union[dict, CurrentDroopOverride]] = None
    SSSCSimulationSettings: Optional[Union[dict, "SSSCSimulationSettings"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.maxInjectionU is not None and not isinstance(self.maxInjectionU, float):
            self.maxInjectionU = float(self.maxInjectionU)

        if self.maxLimitI is not None and not isinstance(self.maxLimitI, float):
            self.maxLimitI = float(self.maxLimitI)

        if self.minInjectionU is not None and not isinstance(self.minInjectionU, float):
            self.minInjectionU = float(self.minInjectionU)

        if self.minLimitI is not None and not isinstance(self.minLimitI, float):
            self.minLimitI = float(self.minLimitI)

        if self.mode is not None and not isinstance(self.mode, SSSCControlModeKind):
            self.mode = SSSCControlModeKind(self.mode)

        if self.CurrentDroopOverride is not None and not isinstance(self.CurrentDroopOverride, CurrentDroopOverride):
            self.CurrentDroopOverride = CurrentDroopOverride(**as_dict(self.CurrentDroopOverride))

        if self.SSSCSimulationSettings is not None and not isinstance(self.SSSCSimulationSettings, SSSCSimulationSettings):
            self.SSSCSimulationSettings = SSSCSimulationSettings(**as_dict(self.SSSCSimulationSettings))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SSSCSimulationSettings(YAMLRoot):
    """
    SSSC control simulation settings used by the algorithm for power flow calculations.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SSSCSimulationSettings"]
    class_class_curie: ClassVar[str] = "cim:SSSCSimulationSettings"
    class_name: ClassVar[str] = "SSSCSimulationSettings"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SSSCSimulationSettings

    mRID: Optional[str] = None
    deltaX: Optional[float] = None
    isEstimateDLDVSensitive: Optional[Union[bool, Bool]] = None
    maxCorrectionX: Optional[float] = None
    maxIterations: Optional[int] = None
    maxMismatch: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.mRID is not None and not isinstance(self.mRID, str):
            self.mRID = str(self.mRID)

        if self.deltaX is not None and not isinstance(self.deltaX, float):
            self.deltaX = float(self.deltaX)

        if self.isEstimateDLDVSensitive is not None and not isinstance(self.isEstimateDLDVSensitive, Bool):
            self.isEstimateDLDVSensitive = Bool(self.isEstimateDLDVSensitive)

        if self.maxCorrectionX is not None and not isinstance(self.maxCorrectionX, float):
            self.maxCorrectionX = float(self.maxCorrectionX)

        if self.maxIterations is not None and not isinstance(self.maxIterations, int):
            self.maxIterations = int(self.maxIterations)

        if self.maxMismatch is not None and not isinstance(self.maxMismatch, float):
            self.maxMismatch = float(self.maxMismatch)

        super().__post_init__(**kwargs)


class SchedulingArea(PowerSystemResource):
    """
    An area where production and/or consumption of energy can be forecasted, scheduled and measured. The area is
    operated by only one system operator, typically a Transmission System Operator (TSO). The area can consist of a
    sub area, which has the same definition as the main area, but it can be operated by another system operator
    (typically Distributed System Operator (DSO) or a Closed Distributed System Operator (CDSO)). This includes
    microgrid concept. A substation is the smallest grouping that can be included in the area. The area size should be
    considered in terms of the possibility of accumulated reading (settlement metering) and the capability of
    operating as an island.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SchedulingArea"]
    class_class_curie: ClassVar[str] = "cim:SchedulingArea"
    class_name: ClassVar[str] = "SchedulingArea"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SchedulingArea


@dataclass(repr=False)
class Season(IdentifiedObject):
    """
    A specified time period of the year.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Season"]
    class_class_curie: ClassVar[str] = "cim:Season"
    class_name: ClassVar[str] = "Season"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Season

    endDate: Optional[str] = None
    startDate: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.endDate is not None and not isinstance(self.endDate, str):
            self.endDate = str(self.endDate)

        if self.startDate is not None and not isinstance(self.startDate, str):
            self.startDate = str(self.startDate)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SeasonDayTypeSchedule(RegularIntervalSchedule):
    """
    A time schedule covering a 24 hour period, with curve data for a specific type of season and day.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SeasonDayTypeSchedule"]
    class_class_curie: ClassVar[str] = "cim:SeasonDayTypeSchedule"
    class_name: ClassVar[str] = "SeasonDayTypeSchedule"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SeasonDayTypeSchedule

    DayType: Optional[Union[dict, DayType]] = None
    Season: Optional[Union[dict, Season]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.DayType is not None and not isinstance(self.DayType, DayType):
            self.DayType = DayType(**as_dict(self.DayType))

        if self.Season is not None and not isinstance(self.Season, Season):
            self.Season = Season(**as_dict(self.Season))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ConformLoadSchedule(SeasonDayTypeSchedule):
    """
    A curve of load versus time (X-axis) showing the active power values (Y1-axis) and reactive power (Y2-axis) for
    each unit of the period covered. This curve represents a typical pattern of load over the time period for a given
    day type and season.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ConformLoadSchedule"]
    class_class_curie: ClassVar[str] = "cim:ConformLoadSchedule"
    class_name: ClassVar[str] = "ConformLoadSchedule"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConformLoadSchedule

    ConformLoadGroup: Optional[Union[dict, ConformLoadGroup]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.ConformLoadGroup is not None and not isinstance(self.ConformLoadGroup, ConformLoadGroup):
            self.ConformLoadGroup = ConformLoadGroup(**as_dict(self.ConformLoadGroup))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class NonConformLoadSchedule(SeasonDayTypeSchedule):
    """
    An active power (Y1-axis) and reactive power (Y2-axis) schedule (curves) versus time (X-axis) for non-conforming
    loads, e.g., large industrial load or power station service (where modelled).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["NonConformLoadSchedule"]
    class_class_curie: ClassVar[str] = "cim:NonConformLoadSchedule"
    class_name: ClassVar[str] = "NonConformLoadSchedule"
    class_model_uri: ClassVar[URIRef] = CIMTBL.NonConformLoadSchedule

    NonConformLoadGroup: Optional[Union[dict, NonConformLoadGroup]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.NonConformLoadGroup is not None and not isinstance(self.NonConformLoadGroup, NonConformLoadGroup):
            self.NonConformLoadGroup = NonConformLoadGroup(**as_dict(self.NonConformLoadGroup))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RegulationSchedule(SeasonDayTypeSchedule):
    """
    A pre-established pattern over time for a controlled variable, e.g., busbar voltage.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["RegulationSchedule"]
    class_class_curie: ClassVar[str] = "cim:RegulationSchedule"
    class_name: ClassVar[str] = "RegulationSchedule"
    class_model_uri: ClassVar[URIRef] = CIMTBL.RegulationSchedule

    RegulatingControl: Optional[Union[dict, RegulatingControl]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.RegulatingControl is not None and not isinstance(self.RegulatingControl, RegulatingControl):
            self.RegulatingControl = RegulatingControl(**as_dict(self.RegulatingControl))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SeriesCompensator(ConductingEquipment):
    """
    A Series Compensator is a series capacitor or reactor or an AC transmission line without charging susceptance. It
    is a two terminal device.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SeriesCompensator"]
    class_class_curie: ClassVar[str] = "cim:SeriesCompensator"
    class_name: ClassVar[str] = "SeriesCompensator"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SeriesCompensator

    r: Optional[float] = None
    r0: Optional[float] = None
    varistorPresent: Optional[Union[bool, Bool]] = None
    varistorRatedCurrent: Optional[float] = None
    varistorVoltageThreshold: Optional[float] = None
    x: Optional[float] = None
    x0: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.r is not None and not isinstance(self.r, float):
            self.r = float(self.r)

        if self.r0 is not None and not isinstance(self.r0, float):
            self.r0 = float(self.r0)

        if self.varistorPresent is not None and not isinstance(self.varistorPresent, Bool):
            self.varistorPresent = Bool(self.varistorPresent)

        if self.varistorRatedCurrent is not None and not isinstance(self.varistorRatedCurrent, float):
            self.varistorRatedCurrent = float(self.varistorRatedCurrent)

        if self.varistorVoltageThreshold is not None and not isinstance(self.varistorVoltageThreshold, float):
            self.varistorVoltageThreshold = float(self.varistorVoltageThreshold)

        if self.x is not None and not isinstance(self.x, float):
            self.x = float(self.x)

        if self.x0 is not None and not isinstance(self.x0, float):
            self.x0 = float(self.x0)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ShuntCompensator(RegulatingCondEq):
    """
    A shunt capacitor or reactor or switchable bank of shunt capacitors or reactors. A section of a shunt compensator
    is an individual capacitor or reactor. A negative value for bPerSection indicates that the compensator is a
    reactor. ShuntCompensator is a single terminal device. Ground is implied.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ShuntCompensator"]
    class_class_curie: ClassVar[str] = "cim:ShuntCompensator"
    class_name: ClassVar[str] = "ShuntCompensator"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ShuntCompensator

    aVRDelay: Optional[float] = None
    grounded: Optional[Union[bool, Bool]] = None
    maximumSections: Optional[int] = None
    nomU: Optional[float] = None
    normalSections: Optional[int] = None
    phaseConnection: Optional[Union[str, "PhaseShuntConnectionKind"]] = None
    sections: Optional[float] = None
    voltageSensitivity: Optional[float] = None
    ShuntCompensatorAction: Optional[Union[dict, "ShuntCompensatorAction"]] = None
    ShuntCompensatorDynamics: Optional[Union[dict, "ShuntCompensatorDynamics"]] = None
    StaticVarCompensatorSystemDynamics: Optional[Union[dict, "StaticVarCompensatorSystemDynamics"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.aVRDelay is not None and not isinstance(self.aVRDelay, float):
            self.aVRDelay = float(self.aVRDelay)

        if self.grounded is not None and not isinstance(self.grounded, Bool):
            self.grounded = Bool(self.grounded)

        if self.maximumSections is not None and not isinstance(self.maximumSections, int):
            self.maximumSections = int(self.maximumSections)

        if self.nomU is not None and not isinstance(self.nomU, float):
            self.nomU = float(self.nomU)

        if self.normalSections is not None and not isinstance(self.normalSections, int):
            self.normalSections = int(self.normalSections)

        if self.phaseConnection is not None and not isinstance(self.phaseConnection, PhaseShuntConnectionKind):
            self.phaseConnection = PhaseShuntConnectionKind(self.phaseConnection)

        if self.sections is not None and not isinstance(self.sections, float):
            self.sections = float(self.sections)

        if self.voltageSensitivity is not None and not isinstance(self.voltageSensitivity, float):
            self.voltageSensitivity = float(self.voltageSensitivity)

        if self.ShuntCompensatorAction is not None and not isinstance(self.ShuntCompensatorAction, ShuntCompensatorAction):
            self.ShuntCompensatorAction = ShuntCompensatorAction(**as_dict(self.ShuntCompensatorAction))

        if self.ShuntCompensatorDynamics is not None and not isinstance(self.ShuntCompensatorDynamics, ShuntCompensatorDynamics):
            self.ShuntCompensatorDynamics = ShuntCompensatorDynamics(**as_dict(self.ShuntCompensatorDynamics))

        if self.StaticVarCompensatorSystemDynamics is not None and not isinstance(self.StaticVarCompensatorSystemDynamics, StaticVarCompensatorSystemDynamics):
            self.StaticVarCompensatorSystemDynamics = StaticVarCompensatorSystemDynamics(**as_dict(self.StaticVarCompensatorSystemDynamics))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LinearShuntCompensator(ShuntCompensator):
    """
    A linear shunt compensator has banks or sections with equal admittance values.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["LinearShuntCompensator"]
    class_class_curie: ClassVar[str] = "cim:LinearShuntCompensator"
    class_name: ClassVar[str] = "LinearShuntCompensator"
    class_model_uri: ClassVar[URIRef] = CIMTBL.LinearShuntCompensator

    b0PerSection: Optional[float] = None
    bPerSection: Optional[float] = None
    g0PerSection: Optional[float] = None
    gPerSection: Optional[float] = None
    rPerSection: Optional[float] = None
    xPerSection: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.b0PerSection is not None and not isinstance(self.b0PerSection, float):
            self.b0PerSection = float(self.b0PerSection)

        if self.bPerSection is not None and not isinstance(self.bPerSection, float):
            self.bPerSection = float(self.bPerSection)

        if self.g0PerSection is not None and not isinstance(self.g0PerSection, float):
            self.g0PerSection = float(self.g0PerSection)

        if self.gPerSection is not None and not isinstance(self.gPerSection, float):
            self.gPerSection = float(self.gPerSection)

        if self.rPerSection is not None and not isinstance(self.rPerSection, float):
            self.rPerSection = float(self.rPerSection)

        if self.xPerSection is not None and not isinstance(self.xPerSection, float):
            self.xPerSection = float(self.xPerSection)

        super().__post_init__(**kwargs)


class NonlinearShuntCompensator(ShuntCompensator):
    """
    A non linear shunt compensator has bank or section admittance values that differ. The attributes gTotal, bTotal,
    g0Total and b0Total of the associated NonlinearShuntCompensatorPoint describe the total conductance and admittance
    of a NonlinearShuntCompensatorPoint at a section number specified by NonlinearShuntCompensatorPoint.sectionNumber.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["NonlinearShuntCompensator"]
    class_class_curie: ClassVar[str] = "cim:NonlinearShuntCompensator"
    class_name: ClassVar[str] = "NonlinearShuntCompensator"
    class_model_uri: ClassVar[URIRef] = CIMTBL.NonlinearShuntCompensator


class ShuntCompensatorAction(IdentifiedObject):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ShuntCompensatorAction"]
    class_class_curie: ClassVar[str] = "cim:ShuntCompensatorAction"
    class_name: ClassVar[str] = "ShuntCompensatorAction"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ShuntCompensatorAction


class ShuntCompensatorDynamics(IdentifiedObject):
    """
    Shunt compensator whose behaviour is described by reference to a standard model <font color=#0f0f0f>or by
    definition of a user-defined model.</font>
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ShuntCompensatorDynamics"]
    class_class_curie: ClassVar[str] = "cim:ShuntCompensatorDynamics"
    class_name: ClassVar[str] = "ShuntCompensatorDynamics"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ShuntCompensatorDynamics


class ShuntCompensatorModification(IdentifiedObject):
    """
    Shunt compensator action.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ShuntCompensatorModification"]
    class_class_curie: ClassVar[str] = "cim:ShuntCompensatorModification"
    class_name: ClassVar[str] = "ShuntCompensatorModification"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ShuntCompensatorModification


@dataclass(repr=False)
class ShuntCompensatorPhase(PowerSystemResource):
    """
    Single phase of a multi-phase shunt compensator when its attributes might be different per phase.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ShuntCompensatorPhase"]
    class_class_curie: ClassVar[str] = "cim:ShuntCompensatorPhase"
    class_name: ClassVar[str] = "ShuntCompensatorPhase"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ShuntCompensatorPhase

    maximumSections: Optional[int] = None
    normalSections: Optional[int] = None
    phase: Optional[Union[str, "SinglePhaseKind"]] = None
    sections: Optional[float] = None
    ShuntCompensator: Optional[Union[dict, ShuntCompensator]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.maximumSections is not None and not isinstance(self.maximumSections, int):
            self.maximumSections = int(self.maximumSections)

        if self.normalSections is not None and not isinstance(self.normalSections, int):
            self.normalSections = int(self.normalSections)

        if self.phase is not None and not isinstance(self.phase, SinglePhaseKind):
            self.phase = SinglePhaseKind(self.phase)

        if self.sections is not None and not isinstance(self.sections, float):
            self.sections = float(self.sections)

        if self.ShuntCompensator is not None and not isinstance(self.ShuntCompensator, ShuntCompensator):
            self.ShuntCompensator = ShuntCompensator(**as_dict(self.ShuntCompensator))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LinearShuntCompensatorPhase(ShuntCompensatorPhase):
    """
    A per phase linear shunt compensator has banks or sections with equal admittance values.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["LinearShuntCompensatorPhase"]
    class_class_curie: ClassVar[str] = "cim:LinearShuntCompensatorPhase"
    class_name: ClassVar[str] = "LinearShuntCompensatorPhase"
    class_model_uri: ClassVar[URIRef] = CIMTBL.LinearShuntCompensatorPhase

    bPerSection: Optional[float] = None
    gPerSection: Optional[float] = None
    rPerSection: Optional[float] = None
    strayInductancePerSection: Optional[float] = None
    xPerSection: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.bPerSection is not None and not isinstance(self.bPerSection, float):
            self.bPerSection = float(self.bPerSection)

        if self.gPerSection is not None and not isinstance(self.gPerSection, float):
            self.gPerSection = float(self.gPerSection)

        if self.rPerSection is not None and not isinstance(self.rPerSection, float):
            self.rPerSection = float(self.rPerSection)

        if self.strayInductancePerSection is not None and not isinstance(self.strayInductancePerSection, float):
            self.strayInductancePerSection = float(self.strayInductancePerSection)

        if self.xPerSection is not None and not isinstance(self.xPerSection, float):
            self.xPerSection = float(self.xPerSection)

        super().__post_init__(**kwargs)


class NonlinearShuntCompensatorPhase(ShuntCompensatorPhase):
    """
    A per phase non linear shunt compensator has bank or section admittance values that differ. The attributes gTotal
    and bTotal of the associated NonlinearShuntCompensatorPhasePoint describe the total conductance and admittance of
    a NonlinearShuntCompensatorPhasePoint at a section number specified by
    NonlinearShuntCompensatorPhasePoint.sectionNumber.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["NonlinearShuntCompensatorPhase"]
    class_class_curie: ClassVar[str] = "cim:NonlinearShuntCompensatorPhase"
    class_name: ClassVar[str] = "NonlinearShuntCompensatorPhase"
    class_model_uri: ClassVar[URIRef] = CIMTBL.NonlinearShuntCompensatorPhase


@dataclass(repr=False)
class SolarGeneratingUnit(GeneratingUnit):
    """
    A solar thermal generating unit, connected to the grid by means of a rotating machine. This class does not
    represent photovoltaic (PV) generation.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SolarGeneratingUnit"]
    class_class_curie: ClassVar[str] = "cim:SolarGeneratingUnit"
    class_name: ClassVar[str] = "SolarGeneratingUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SolarGeneratingUnit

    SolarPowerPlant: Optional[Union[dict, "SolarPowerPlant"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.SolarPowerPlant is not None and not isinstance(self.SolarPowerPlant, SolarPowerPlant):
            self.SolarPowerPlant = SolarPowerPlant(**as_dict(self.SolarPowerPlant))

        super().__post_init__(**kwargs)


class SolarPowerPlant(PowerSystemResource):
    """
    Solar power plant.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SolarPowerPlant"]
    class_class_curie: ClassVar[str] = "cim:SolarPowerPlant"
    class_name: ClassVar[str] = "SolarPowerPlant"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SolarPowerPlant


class SolarRadiationDependencyCurve(Curve):
    """
    A curve or functional relationship between- the solar radiation independent variable (X-axis), and- relative
    dependent (Y-axis) variables.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SolarRadiationDependencyCurve"]
    class_class_curie: ClassVar[str] = "cim:SolarRadiationDependencyCurve"
    class_name: ClassVar[str] = "SolarRadiationDependencyCurve"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SolarRadiationDependencyCurve


class StatcomDynamics(IdentifiedObject):
    """
    STATCOM whose behaviour is described by reference to a standard model <font color=#0f0f0f>or by definition of a
    user-defined model.</font>
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["StatcomDynamics"]
    class_class_curie: ClassVar[str] = "cim:StatcomDynamics"
    class_name: ClassVar[str] = "StatcomDynamics"
    class_model_uri: ClassVar[URIRef] = CIMTBL.StatcomDynamics


class StateShortCircuitResult(IdentifiedObject):
    """
    Short-circuit result calculated on a power system state.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["StateShortCircuitResult"]
    class_class_curie: ClassVar[str] = "cim:StateShortCircuitResult"
    class_name: ClassVar[str] = "StateShortCircuitResult"
    class_model_uri: ClassVar[URIRef] = CIMTBL.StateShortCircuitResult


class StateVariable(YAMLRoot):
    """
    An abstract class for state variables.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["StateVariable"]
    class_class_curie: ClassVar[str] = "cim:StateVariable"
    class_name: ClassVar[str] = "StateVariable"
    class_model_uri: ClassVar[URIRef] = CIMTBL.StateVariable


class StaticSynchronousCompensator(FACTSEquipment):
    """
    Static synchronous compensator (STATCOM), also known as a static synchronous condenser (STATCON), is a type of
    flexible AC transmission system regulating equipment used on alternating current electricity transmission
    networks. It is based on a power electronics voltage-source converter and can act as either a source or sink of
    reactive AC power to an electricity network. If connected to a source of power it can also provide active AC
    power.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["StaticSynchronousCompensator"]
    class_class_curie: ClassVar[str] = "cim:StaticSynchronousCompensator"
    class_name: ClassVar[str] = "StaticSynchronousCompensator"
    class_model_uri: ClassVar[URIRef] = CIMTBL.StaticSynchronousCompensator


@dataclass(repr=False)
class StaticVarCompensator(FACTSEquipment):
    """
    A facility for providing variable and controllable shunt reactive power. The SVC typically consists of a stepdown
    transformer, filter, thyristor-controlled reactor, and thyristor-switched capacitor arms.The SVC may operate in
    fixed MVar output mode or in voltage control mode. When in voltage control mode, the output of the SVC will be
    proportional to the deviation of voltage at the controlled bus from the voltage setpoint. The SVC characteristic
    slope defines the proportion. If the voltage at the controlled bus is equal to the voltage setpoint, the SVC MVar
    output is zero.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["StaticVarCompensator"]
    class_class_curie: ClassVar[str] = "cim:StaticVarCompensator"
    class_name: ClassVar[str] = "StaticVarCompensator"
    class_model_uri: ClassVar[URIRef] = CIMTBL.StaticVarCompensator

    capacitiveRating: Optional[float] = None
    inductiveRating: Optional[float] = None
    q: Optional[float] = None
    slope: Optional[float] = None
    sVCControlMode: Optional[Union[str, "SVCControlMode"]] = None
    voltageSetPoint: Optional[float] = None
    StaticVarCompensatorDynamics: Optional[Union[dict, "StaticVarCompensatorDynamics"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.capacitiveRating is not None and not isinstance(self.capacitiveRating, float):
            self.capacitiveRating = float(self.capacitiveRating)

        if self.inductiveRating is not None and not isinstance(self.inductiveRating, float):
            self.inductiveRating = float(self.inductiveRating)

        if self.q is not None and not isinstance(self.q, float):
            self.q = float(self.q)

        if self.slope is not None and not isinstance(self.slope, float):
            self.slope = float(self.slope)

        if self.sVCControlMode is not None and not isinstance(self.sVCControlMode, SVCControlMode):
            self.sVCControlMode = SVCControlMode(self.sVCControlMode)

        if self.voltageSetPoint is not None and not isinstance(self.voltageSetPoint, float):
            self.voltageSetPoint = float(self.voltageSetPoint)

        if self.StaticVarCompensatorDynamics is not None and not isinstance(self.StaticVarCompensatorDynamics, StaticVarCompensatorDynamics):
            self.StaticVarCompensatorDynamics = StaticVarCompensatorDynamics(**as_dict(self.StaticVarCompensatorDynamics))

        super().__post_init__(**kwargs)


class StaticVarCompensatorDynamics(IdentifiedObject):
    """
    Static var compensator whose behaviour is described by reference to a standard model <font color=#0f0f0f>or by
    definition of a user-defined model.</font>
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["StaticVarCompensatorDynamics"]
    class_class_curie: ClassVar[str] = "cim:StaticVarCompensatorDynamics"
    class_name: ClassVar[str] = "StaticVarCompensatorDynamics"
    class_model_uri: ClassVar[URIRef] = CIMTBL.StaticVarCompensatorDynamics


class StaticVarCompensatorSystemDynamics(StaticVarCompensatorDynamics):
    """
    Static var compensator system whose behaviour is described by reference to a standard model <font color=#0f0f0f>or
    by definition of a user-defined model.</font>
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["StaticVarCompensatorSystemDynamics"]
    class_class_curie: ClassVar[str] = "cim:StaticVarCompensatorSystemDynamics"
    class_name: ClassVar[str] = "StaticVarCompensatorSystemDynamics"
    class_model_uri: ClassVar[URIRef] = CIMTBL.StaticVarCompensatorSystemDynamics


class SVSMO4(StaticVarCompensatorSystemDynamics):
    """
    Hybrid STATCOM type SVSMO4 static var system, which has at most only one TSC and one TSR. It also has voltage
    source converter (VSC). Note this model is not final hence some changes are expected in the next editions of the
    standard.Reference: WECC Hybrid STATCOM.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SVSMO4"]
    class_class_curie: ClassVar[str] = "cim:SVSMO4"
    class_name: ClassVar[str] = "SVSMO4"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SVSMO4


class StationSupply(EnergyConsumer):
    """
    Station supply with load derived from the station output.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["StationSupply"]
    class_class_curie: ClassVar[str] = "cim:StationSupply"
    class_name: ClassVar[str] = "StationSupply"
    class_model_uri: ClassVar[URIRef] = CIMTBL.StationSupply


@dataclass(repr=False)
class StepLimitTablePoint(YAMLRoot):
    """
    Describes each limit per step in the operational limit curve.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["StepLimitTablePoint"]
    class_class_curie: ClassVar[str] = "cim:StepLimitTablePoint"
    class_name: ClassVar[str] = "StepLimitTablePoint"
    class_model_uri: ClassVar[URIRef] = CIMTBL.StepLimitTablePoint

    factor: Optional[float] = None
    step: Optional[int] = None
    StepOperationalLimitTable: Optional[Union[dict, "StepOperationalLimitTable"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.factor is not None and not isinstance(self.factor, float):
            self.factor = float(self.factor)

        if self.step is not None and not isinstance(self.step, int):
            self.step = int(self.step)

        if self.StepOperationalLimitTable is not None and not isinstance(self.StepOperationalLimitTable, StepOperationalLimitTable):
            self.StepOperationalLimitTable = StepOperationalLimitTable(**as_dict(self.StepOperationalLimitTable))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class StepOperationalLimitTable(IdentifiedObject):
    """
    Describes a tabular curve for how the operational limit varies with the tap step.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["StepOperationalLimitTable"]
    class_class_curie: ClassVar[str] = "cim:StepOperationalLimitTable"
    class_name: ClassVar[str] = "StepOperationalLimitTable"
    class_model_uri: ClassVar[URIRef] = CIMTBL.StepOperationalLimitTable

    TapChanger: Optional[Union[dict, "TapChanger"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.TapChanger is not None and not isinstance(self.TapChanger, TapChanger):
            self.TapChanger = TapChanger(**as_dict(self.TapChanger))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class StringQuantity(YAMLRoot):
    """
    Quantity with string value (when it is not important whether it is an integral or a floating point number) and
    associated unit information.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["StringQuantity"]
    class_class_curie: ClassVar[str] = "cim:StringQuantity"
    class_name: ClassVar[str] = "StringQuantity"
    class_model_uri: ClassVar[URIRef] = CIMTBL.StringQuantity

    multiplier: Optional[Union[str, "UnitMultiplier"]] = None
    unit: Optional[Union[str, "UnitSymbol"]] = None
    value: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.multiplier is not None and not isinstance(self.multiplier, UnitMultiplier):
            self.multiplier = UnitMultiplier(self.multiplier)

        if self.unit is not None and not isinstance(self.unit, UnitSymbol):
            self.unit = UnitSymbol(self.unit)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SubGeographicalRegion(IdentifiedObject):
    """
    A subset of a geographical region of a power system network model.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SubGeographicalRegion"]
    class_class_curie: ClassVar[str] = "cim:SubGeographicalRegion"
    class_name: ClassVar[str] = "SubGeographicalRegion"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SubGeographicalRegion

    Region: Optional[Union[dict, GeographicalRegion]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.Region is not None and not isinstance(self.Region, GeographicalRegion):
            self.Region = GeographicalRegion(**as_dict(self.Region))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SubLoadArea(EnergyArea):
    """
    The class is the second level in a hierarchical structure for grouping of loads for the purpose of load flow load
    scaling.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SubLoadArea"]
    class_class_curie: ClassVar[str] = "cim:SubLoadArea"
    class_name: ClassVar[str] = "SubLoadArea"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SubLoadArea

    LoadArea: Optional[Union[dict, LoadArea]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.LoadArea is not None and not isinstance(self.LoadArea, LoadArea):
            self.LoadArea = LoadArea(**as_dict(self.LoadArea))

        super().__post_init__(**kwargs)


class SubSchedulingArea(SchedulingArea):
    """
    An area that is a part of another scheduling area. Typically part of a Transmission System Operator (TSO)
    scheduling area operated by a Distributed System Operator (DSO) or a Close Distributed System Operator (CDSO).
    This includes microgrid concept. A sub scheduling area can contain other sub areas. A sub scheduling area leaf
    will form the smallest entity of any given energy area.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SubSchedulingArea"]
    class_class_curie: ClassVar[str] = "cim:SubSchedulingArea"
    class_name: ClassVar[str] = "SubSchedulingArea"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SubSchedulingArea


@dataclass(repr=False)
class Substation(EquipmentContainer):
    """
    A collection of equipment for purposes other than generation or utilization, through which electric energy in bulk
    is passed for the purposes of switching or modifying its characteristics.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Substation"]
    class_class_curie: ClassVar[str] = "cim:Substation"
    class_name: ClassVar[str] = "Substation"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Substation

    NamingFeeder: Optional[Union[dict, Feeder]] = None
    Region: Optional[Union[dict, SubGeographicalRegion]] = None
    SchedulingArea: Optional[Union[dict, SchedulingArea]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.NamingFeeder is not None and not isinstance(self.NamingFeeder, Feeder):
            self.NamingFeeder = Feeder(**as_dict(self.NamingFeeder))

        if self.Region is not None and not isinstance(self.Region, SubGeographicalRegion):
            self.Region = SubGeographicalRegion(**as_dict(self.Region))

        if self.SchedulingArea is not None and not isinstance(self.SchedulingArea, SchedulingArea):
            self.SchedulingArea = SchedulingArea(**as_dict(self.SchedulingArea))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SvDCPowerFlow(StateVariable):
    """
    State variable for power flow. Load convention is used for flow direction. This means flow out from the
    DCTopologicalNode into the equipment is positive.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SvDCPowerFlow"]
    class_class_curie: ClassVar[str] = "cim:SvDCPowerFlow"
    class_name: ClassVar[str] = "SvDCPowerFlow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SvDCPowerFlow

    p: Optional[float] = None
    DCTerminal: Optional[Union[dict, DCTerminal]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.p is not None and not isinstance(self.p, float):
            self.p = float(self.p)

        if self.DCTerminal is not None and not isinstance(self.DCTerminal, DCTerminal):
            self.DCTerminal = DCTerminal(**as_dict(self.DCTerminal))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SvDCVoltage(StateVariable):
    """
    State variable for direct current voltage.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SvDCVoltage"]
    class_class_curie: ClassVar[str] = "cim:SvDCVoltage"
    class_name: ClassVar[str] = "SvDCVoltage"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SvDCVoltage

    v: Optional[float] = None
    DCTopologicalNode: Optional[Union[dict, DCTopologicalNode]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.v is not None and not isinstance(self.v, float):
            self.v = float(self.v)

        if self.DCTopologicalNode is not None and not isinstance(self.DCTopologicalNode, DCTopologicalNode):
            self.DCTopologicalNode = DCTopologicalNode(**as_dict(self.DCTopologicalNode))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SvInjection(StateVariable):
    """
    The SvInjection reports the calculated bus injection minus the sum of the terminal flows. The terminal flow is
    positive out from the bus (load sign convention) and bus injection has positive flow into the bus. SvInjection may
    have the remainder after state estimation or slack after power flow calculation.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SvInjection"]
    class_class_curie: ClassVar[str] = "cim:SvInjection"
    class_name: ClassVar[str] = "SvInjection"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SvInjection

    phase: Optional[Union[str, "SinglePhaseKind"]] = None
    pInjection: Optional[float] = None
    qInjection: Optional[float] = None
    TopologicalNode: Optional[Union[dict, "TopologicalNode"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.phase is not None and not isinstance(self.phase, SinglePhaseKind):
            self.phase = SinglePhaseKind(self.phase)

        if self.pInjection is not None and not isinstance(self.pInjection, float):
            self.pInjection = float(self.pInjection)

        if self.qInjection is not None and not isinstance(self.qInjection, float):
            self.qInjection = float(self.qInjection)

        if self.TopologicalNode is not None and not isinstance(self.TopologicalNode, TopologicalNode):
            self.TopologicalNode = TopologicalNode(**as_dict(self.TopologicalNode))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SvPowerFlow(StateVariable):
    """
    State variable for power flow. Load convention is used for flow direction. This means flow out from the
    TopologicalNode into the equipment is positive.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SvPowerFlow"]
    class_class_curie: ClassVar[str] = "cim:SvPowerFlow"
    class_name: ClassVar[str] = "SvPowerFlow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SvPowerFlow

    p: Optional[float] = None
    phase: Optional[Union[str, "SinglePhaseKind"]] = None
    q: Optional[float] = None
    Terminal: Optional[Union[dict, "Terminal"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.p is not None and not isinstance(self.p, float):
            self.p = float(self.p)

        if self.phase is not None and not isinstance(self.phase, SinglePhaseKind):
            self.phase = SinglePhaseKind(self.phase)

        if self.q is not None and not isinstance(self.q, float):
            self.q = float(self.q)

        if self.Terminal is not None and not isinstance(self.Terminal, Terminal):
            self.Terminal = Terminal(**as_dict(self.Terminal))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SvShuntCompensatorSections(StateVariable):
    """
    State variable for the number of sections in service for a shunt compensator.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SvShuntCompensatorSections"]
    class_class_curie: ClassVar[str] = "cim:SvShuntCompensatorSections"
    class_name: ClassVar[str] = "SvShuntCompensatorSections"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SvShuntCompensatorSections

    phase: Optional[Union[str, "SinglePhaseKind"]] = None
    sections: Optional[float] = None
    ShuntCompensator: Optional[Union[dict, ShuntCompensator]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.phase is not None and not isinstance(self.phase, SinglePhaseKind):
            self.phase = SinglePhaseKind(self.phase)

        if self.sections is not None and not isinstance(self.sections, float):
            self.sections = float(self.sections)

        if self.ShuntCompensator is not None and not isinstance(self.ShuntCompensator, ShuntCompensator):
            self.ShuntCompensator = ShuntCompensator(**as_dict(self.ShuntCompensator))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SvStatus(StateVariable):
    """
    State variable for status.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SvStatus"]
    class_class_curie: ClassVar[str] = "cim:SvStatus"
    class_name: ClassVar[str] = "SvStatus"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SvStatus

    inService: Optional[Union[bool, Bool]] = None
    phase: Optional[Union[str, "SinglePhaseKind"]] = None
    ConductingEquipment: Optional[Union[dict, ConductingEquipment]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.inService is not None and not isinstance(self.inService, Bool):
            self.inService = Bool(self.inService)

        if self.phase is not None and not isinstance(self.phase, SinglePhaseKind):
            self.phase = SinglePhaseKind(self.phase)

        if self.ConductingEquipment is not None and not isinstance(self.ConductingEquipment, ConductingEquipment):
            self.ConductingEquipment = ConductingEquipment(**as_dict(self.ConductingEquipment))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SvSwitch(StateVariable):
    """
    State variable for switch.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SvSwitch"]
    class_class_curie: ClassVar[str] = "cim:SvSwitch"
    class_name: ClassVar[str] = "SvSwitch"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SvSwitch

    open: Optional[Union[bool, Bool]] = None
    phase: Optional[Union[str, "SinglePhaseKind"]] = None
    Switch: Optional[Union[dict, "Switch"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.open is not None and not isinstance(self.open, Bool):
            self.open = Bool(self.open)

        if self.phase is not None and not isinstance(self.phase, SinglePhaseKind):
            self.phase = SinglePhaseKind(self.phase)

        if self.Switch is not None and not isinstance(self.Switch, Switch):
            self.Switch = Switch(**as_dict(self.Switch))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SvTapStep(StateVariable):
    """
    State variable for transformer tap step.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SvTapStep"]
    class_class_curie: ClassVar[str] = "cim:SvTapStep"
    class_name: ClassVar[str] = "SvTapStep"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SvTapStep

    position: Optional[float] = None
    TapChanger: Optional[Union[dict, "TapChanger"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.position is not None and not isinstance(self.position, float):
            self.position = float(self.position)

        if self.TapChanger is not None and not isinstance(self.TapChanger, TapChanger):
            self.TapChanger = TapChanger(**as_dict(self.TapChanger))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SvVoltage(StateVariable):
    """
    State variable for voltage.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SvVoltage"]
    class_class_curie: ClassVar[str] = "cim:SvVoltage"
    class_name: ClassVar[str] = "SvVoltage"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SvVoltage

    angle: Optional[float] = None
    phase: Optional[Union[str, "SinglePhaseKind"]] = None
    v: Optional[float] = None
    TopologicalNode: Optional[Union[dict, "TopologicalNode"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.angle is not None and not isinstance(self.angle, float):
            self.angle = float(self.angle)

        if self.phase is not None and not isinstance(self.phase, SinglePhaseKind):
            self.phase = SinglePhaseKind(self.phase)

        if self.v is not None and not isinstance(self.v, float):
            self.v = float(self.v)

        if self.TopologicalNode is not None and not isinstance(self.TopologicalNode, TopologicalNode):
            self.TopologicalNode = TopologicalNode(**as_dict(self.TopologicalNode))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Switch(ConductingEquipment):
    """
    A generic device designed to close, or open, or both, one or more electric circuits. All switches are two terminal
    devices including grounding switches. The ACDCTerminal.connected at the two sides of the switch shall not be
    considered for assessing switch connectivity, i.e. only Switch.open, .normalOpen and .locked are relevant.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Switch"]
    class_class_curie: ClassVar[str] = "cim:Switch"
    class_name: ClassVar[str] = "Switch"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Switch

    locked: Optional[Union[bool, Bool]] = None
    normalOpen: Optional[Union[bool, Bool]] = None
    open: Optional[Union[bool, Bool]] = None
    ratedCurrent: Optional[float] = None
    retained: Optional[Union[bool, Bool]] = None
    topologicalUsageType: Optional[Union[str, "TopologicalUsageKind"]] = None
    CompositeSwitch: Optional[Union[dict, CompositeSwitch]] = None
    SwitchAction: Optional[Union[dict, "SwitchAction"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.locked is not None and not isinstance(self.locked, Bool):
            self.locked = Bool(self.locked)

        if self.normalOpen is not None and not isinstance(self.normalOpen, Bool):
            self.normalOpen = Bool(self.normalOpen)

        if self.open is not None and not isinstance(self.open, Bool):
            self.open = Bool(self.open)

        if self.ratedCurrent is not None and not isinstance(self.ratedCurrent, float):
            self.ratedCurrent = float(self.ratedCurrent)

        if self.retained is not None and not isinstance(self.retained, Bool):
            self.retained = Bool(self.retained)

        if self.topologicalUsageType is not None and not isinstance(self.topologicalUsageType, TopologicalUsageKind):
            self.topologicalUsageType = TopologicalUsageKind(self.topologicalUsageType)

        if self.CompositeSwitch is not None and not isinstance(self.CompositeSwitch, CompositeSwitch):
            self.CompositeSwitch = CompositeSwitch(**as_dict(self.CompositeSwitch))

        if self.SwitchAction is not None and not isinstance(self.SwitchAction, SwitchAction):
            self.SwitchAction = SwitchAction(**as_dict(self.SwitchAction))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Cut(Switch):
    """
    A cut separates a line segment into two parts. The cut appears as a switch inserted between these two parts and
    connects them together. As the cut is normally open there is no galvanic connection between the two line segment
    parts. But it is possible to close the cut to get galvanic connection.The cut terminals are oriented towards the
    line segment terminals with the same sequence number. Hence the cut terminal with sequence number equal to 1 is
    oriented to the line segment's terminal with sequence number equal to 1.The cut terminals also act as connection
    points for jumpers and other equipment, e.g. a mobile generator. To enable this, connectivity nodes are placed at
    the cut terminals. Once the connectivity nodes are in place any conducting equipment can be connected at them.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Cut"]
    class_class_curie: ClassVar[str] = "cim:Cut"
    class_name: ClassVar[str] = "Cut"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Cut

    lengthFromTerminal1: Optional[float] = None
    ACLineSegment: Optional[Union[dict, ACLineSegment]] = None
    CutAction: Optional[Union[dict, CutAction]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.lengthFromTerminal1 is not None and not isinstance(self.lengthFromTerminal1, float):
            self.lengthFromTerminal1 = float(self.lengthFromTerminal1)

        if self.ACLineSegment is not None and not isinstance(self.ACLineSegment, ACLineSegment):
            self.ACLineSegment = ACLineSegment(**as_dict(self.ACLineSegment))

        if self.CutAction is not None and not isinstance(self.CutAction, CutAction):
            self.CutAction = CutAction(**as_dict(self.CutAction))

        super().__post_init__(**kwargs)


class Disconnector(Switch):
    """
    A mechanical switching device which provides, in the open position, an isolating distance in accordance with
    specified requirements.A disconnector is capable of opening and closing a circuit when either negligible current
    is broken or made, or when no significant change in the voltage across the terminals of each of the poles of the
    disconnector occurs. It is also capable of carrying currents under normal circuit conditions and carrying for a
    specified time currents under abnormal conditions such as those of short circuit.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Disconnector"]
    class_class_curie: ClassVar[str] = "cim:Disconnector"
    class_name: ClassVar[str] = "Disconnector"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Disconnector


class EarthingSwitch(Switch):
    """
    A mechanical switching device for earthing parts of a circuit, capable of withstanding for a specified time
    currents under abnormal conditions such as those of short circuit, but not required to carry current under normal
    conditions of the circuit.An earthing switch may have a short-circuit making capacity.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EarthingSwitch"]
    class_class_curie: ClassVar[str] = "cim:EarthingSwitch"
    class_name: ClassVar[str] = "EarthingSwitch"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EarthingSwitch


@dataclass(repr=False)
class Fuse(Switch):
    """
    An overcurrent protective device with a circuit opening fusible part that is heated and severed by the passage of
    overcurrent through it. A fuse is considered a switching device because it breaks current.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Fuse"]
    class_class_curie: ClassVar[str] = "cim:Fuse"
    class_name: ClassVar[str] = "Fuse"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Fuse

    MiinimumMeltCurve: Optional[Union[dict, FuseCharacteristicCurve]] = None
    TotalClearingTimeCurve: Optional[Union[dict, FuseCharacteristicCurve]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.MiinimumMeltCurve is not None and not isinstance(self.MiinimumMeltCurve, FuseCharacteristicCurve):
            self.MiinimumMeltCurve = FuseCharacteristicCurve(**as_dict(self.MiinimumMeltCurve))

        if self.TotalClearingTimeCurve is not None and not isinstance(self.TotalClearingTimeCurve, FuseCharacteristicCurve):
            self.TotalClearingTimeCurve = FuseCharacteristicCurve(**as_dict(self.TotalClearingTimeCurve))

        super().__post_init__(**kwargs)


class GroundDisconnector(Switch):
    """
    A manually operated or motor operated mechanical switching device used for isolating a circuit or equipment from
    ground.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["GroundDisconnector"]
    class_class_curie: ClassVar[str] = "cim:GroundDisconnector"
    class_name: ClassVar[str] = "GroundDisconnector"
    class_model_uri: ClassVar[URIRef] = CIMTBL.GroundDisconnector


@dataclass(repr=False)
class Jumper(Switch):
    """
    A short section of conductor with negligible impedance which can be manually removed and replaced if the circuit
    is de-energized. Note that zero-impedance branches can potentially be modelled by other equipment types.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Jumper"]
    class_class_curie: ClassVar[str] = "cim:Jumper"
    class_name: ClassVar[str] = "Jumper"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Jumper

    JumperAction: Optional[Union[dict, JumperAction]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.JumperAction is not None and not isinstance(self.JumperAction, JumperAction):
            self.JumperAction = JumperAction(**as_dict(self.JumperAction))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProtectedSwitch(Switch):
    """
    A ProtectedSwitch is a switching device that can be operated by ProtectionEquipment.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ProtectedSwitch"]
    class_class_curie: ClassVar[str] = "cim:ProtectedSwitch"
    class_name: ClassVar[str] = "ProtectedSwitch"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ProtectedSwitch

    breakingCapacity: Optional[float] = None
    makingCapacity: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.breakingCapacity is not None and not isinstance(self.breakingCapacity, float):
            self.breakingCapacity = float(self.breakingCapacity)

        if self.makingCapacity is not None and not isinstance(self.makingCapacity, float):
            self.makingCapacity = float(self.makingCapacity)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Breaker(ProtectedSwitch):
    """
    A mechanical switching device capable of making, carrying, and breaking currents under normal circuit conditions
    and also making, carrying for a specified time, and breaking currents under specified abnormal circuit conditions
    e.g. those of short circuit.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Breaker"]
    class_class_curie: ClassVar[str] = "cim:Breaker"
    class_name: ClassVar[str] = "Breaker"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Breaker

    inTransitTime: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.inTransitTime is not None and not isinstance(self.inTransitTime, float):
            self.inTransitTime = float(self.inTransitTime)

        super().__post_init__(**kwargs)


class DisconnectingCircuitBreaker(Breaker):
    """
    A circuit breaking device including disconnecting function, eliminating the need for separate disconnectors.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["DisconnectingCircuitBreaker"]
    class_class_curie: ClassVar[str] = "cim:DisconnectingCircuitBreaker"
    class_name: ClassVar[str] = "DisconnectingCircuitBreaker"
    class_model_uri: ClassVar[URIRef] = CIMTBL.DisconnectingCircuitBreaker


class LoadBreakSwitch(ProtectedSwitch):
    """
    A mechanical switching device capable of making, carrying, and breaking currents under normal operating conditions.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["LoadBreakSwitch"]
    class_class_curie: ClassVar[str] = "cim:LoadBreakSwitch"
    class_name: ClassVar[str] = "LoadBreakSwitch"
    class_model_uri: ClassVar[URIRef] = CIMTBL.LoadBreakSwitch


class Recloser(ProtectedSwitch):
    """
    Pole-mounted fault interrupter with built-in phase and ground relays, current transformer (CT), and supplemental
    controls.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Recloser"]
    class_class_curie: ClassVar[str] = "cim:Recloser"
    class_name: ClassVar[str] = "Recloser"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Recloser


class Sectionaliser(Switch):
    """
    Automatic switch that will lock open to isolate a faulted section. It may, or may not, have load breaking
    capability. Its primary purpose is to provide fault sectionalising at locations where the fault current is either
    too high, or too low, for proper coordination of fuses.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Sectionaliser"]
    class_class_curie: ClassVar[str] = "cim:Sectionaliser"
    class_name: ClassVar[str] = "Sectionaliser"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Sectionaliser


class SwitchAction(IdentifiedObject):
    """
    Action on switch as a switching step.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SwitchAction"]
    class_class_curie: ClassVar[str] = "cim:SwitchAction"
    class_name: ClassVar[str] = "SwitchAction"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SwitchAction


@dataclass(repr=False)
class SwitchPhase(PowerSystemResource):
    """
    Single phase of a multi-phase switch when its attributes might be different per phase.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SwitchPhase"]
    class_class_curie: ClassVar[str] = "cim:SwitchPhase"
    class_name: ClassVar[str] = "SwitchPhase"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SwitchPhase

    closed: Optional[Union[bool, Bool]] = None
    normalOpen: Optional[Union[bool, Bool]] = None
    open: Optional[Union[bool, Bool]] = None
    phaseSide1: Optional[Union[str, "SinglePhaseKind"]] = None
    phaseSide2: Optional[Union[str, "SinglePhaseKind"]] = None
    ratedCurrent: Optional[float] = None
    Switch: Optional[Union[dict, Switch]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.closed is not None and not isinstance(self.closed, Bool):
            self.closed = Bool(self.closed)

        if self.normalOpen is not None and not isinstance(self.normalOpen, Bool):
            self.normalOpen = Bool(self.normalOpen)

        if self.open is not None and not isinstance(self.open, Bool):
            self.open = Bool(self.open)

        if self.phaseSide1 is not None and not isinstance(self.phaseSide1, SinglePhaseKind):
            self.phaseSide1 = SinglePhaseKind(self.phaseSide1)

        if self.phaseSide2 is not None and not isinstance(self.phaseSide2, SinglePhaseKind):
            self.phaseSide2 = SinglePhaseKind(self.phaseSide2)

        if self.ratedCurrent is not None and not isinstance(self.ratedCurrent, float):
            self.ratedCurrent = float(self.ratedCurrent)

        if self.Switch is not None and not isinstance(self.Switch, Switch):
            self.Switch = Switch(**as_dict(self.Switch))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SwitchSchedule(SeasonDayTypeSchedule):
    """
    Schedule for switch.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SwitchSchedule"]
    class_class_curie: ClassVar[str] = "cim:SwitchSchedule"
    class_name: ClassVar[str] = "SwitchSchedule"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SwitchSchedule

    Switch: Optional[Union[dict, Switch]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.Switch is not None and not isinstance(self.Switch, Switch):
            self.Switch = Switch(**as_dict(self.Switch))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SynchronousMachine(RotatingMachine):
    """
    An electromechanical device that operates with shaft rotating synchronously with the network. It is a single
    machine operating either as a generator or synchronous condenser or pump.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SynchronousMachine"]
    class_class_curie: ClassVar[str] = "cim:SynchronousMachine"
    class_name: ClassVar[str] = "SynchronousMachine"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SynchronousMachine

    aVRToManualLag: Optional[float] = None
    aVRToManualLead: Optional[float] = None
    baseQ: Optional[float] = None
    condenserP: Optional[float] = None
    coolantCondition: Optional[float] = None
    coolantType: Optional[Union[str, "CoolantType"]] = None
    earthing: Optional[Union[bool, Bool]] = None
    earthingStarPointR: Optional[float] = None
    earthingStarPointX: Optional[float] = None
    ikk: Optional[float] = None
    manualToAVR: Optional[float] = None
    maxQ: Optional[float] = None
    maxU: Optional[float] = None
    minQ: Optional[float] = None
    minU: Optional[float] = None
    mu: Optional[float] = None
    operatingMode: Optional[Union[str, "SynchronousMachineOperatingMode"]] = None
    qPercent: Optional[float] = None
    r: Optional[float] = None
    r0: Optional[float] = None
    r2: Optional[float] = None
    referencePriority: Optional[int] = None
    satDirectSubtransX: Optional[float] = None
    satDirectSyncX: Optional[float] = None
    satDirectTransX: Optional[float] = None
    shortCircuitRotorType: Optional[Union[str, "ShortCircuitRotorKind"]] = None
    type: Optional[Union[str, "SynchronousMachineKind"]] = None
    voltageRegulationRange: Optional[float] = None
    x0: Optional[float] = None
    x2: Optional[float] = None
    InitialReactiveCapabilityCurve: Optional[Union[dict, ReactiveCapabilityCurve]] = None
    SynchronousMachineDynamics: Optional[Union[dict, "SynchronousMachineDynamics"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.aVRToManualLag is not None and not isinstance(self.aVRToManualLag, float):
            self.aVRToManualLag = float(self.aVRToManualLag)

        if self.aVRToManualLead is not None and not isinstance(self.aVRToManualLead, float):
            self.aVRToManualLead = float(self.aVRToManualLead)

        if self.baseQ is not None and not isinstance(self.baseQ, float):
            self.baseQ = float(self.baseQ)

        if self.condenserP is not None and not isinstance(self.condenserP, float):
            self.condenserP = float(self.condenserP)

        if self.coolantCondition is not None and not isinstance(self.coolantCondition, float):
            self.coolantCondition = float(self.coolantCondition)

        if self.coolantType is not None and not isinstance(self.coolantType, CoolantType):
            self.coolantType = CoolantType(self.coolantType)

        if self.earthing is not None and not isinstance(self.earthing, Bool):
            self.earthing = Bool(self.earthing)

        if self.earthingStarPointR is not None and not isinstance(self.earthingStarPointR, float):
            self.earthingStarPointR = float(self.earthingStarPointR)

        if self.earthingStarPointX is not None and not isinstance(self.earthingStarPointX, float):
            self.earthingStarPointX = float(self.earthingStarPointX)

        if self.ikk is not None and not isinstance(self.ikk, float):
            self.ikk = float(self.ikk)

        if self.manualToAVR is not None and not isinstance(self.manualToAVR, float):
            self.manualToAVR = float(self.manualToAVR)

        if self.maxQ is not None and not isinstance(self.maxQ, float):
            self.maxQ = float(self.maxQ)

        if self.maxU is not None and not isinstance(self.maxU, float):
            self.maxU = float(self.maxU)

        if self.minQ is not None and not isinstance(self.minQ, float):
            self.minQ = float(self.minQ)

        if self.minU is not None and not isinstance(self.minU, float):
            self.minU = float(self.minU)

        if self.mu is not None and not isinstance(self.mu, float):
            self.mu = float(self.mu)

        if self.operatingMode is not None and not isinstance(self.operatingMode, SynchronousMachineOperatingMode):
            self.operatingMode = SynchronousMachineOperatingMode(self.operatingMode)

        if self.qPercent is not None and not isinstance(self.qPercent, float):
            self.qPercent = float(self.qPercent)

        if self.r is not None and not isinstance(self.r, float):
            self.r = float(self.r)

        if self.r0 is not None and not isinstance(self.r0, float):
            self.r0 = float(self.r0)

        if self.r2 is not None and not isinstance(self.r2, float):
            self.r2 = float(self.r2)

        if self.referencePriority is not None and not isinstance(self.referencePriority, int):
            self.referencePriority = int(self.referencePriority)

        if self.satDirectSubtransX is not None and not isinstance(self.satDirectSubtransX, float):
            self.satDirectSubtransX = float(self.satDirectSubtransX)

        if self.satDirectSyncX is not None and not isinstance(self.satDirectSyncX, float):
            self.satDirectSyncX = float(self.satDirectSyncX)

        if self.satDirectTransX is not None and not isinstance(self.satDirectTransX, float):
            self.satDirectTransX = float(self.satDirectTransX)

        if self.shortCircuitRotorType is not None and not isinstance(self.shortCircuitRotorType, ShortCircuitRotorKind):
            self.shortCircuitRotorType = ShortCircuitRotorKind(self.shortCircuitRotorType)

        if self.type is not None and not isinstance(self.type, SynchronousMachineKind):
            self.type = SynchronousMachineKind(self.type)

        if self.voltageRegulationRange is not None and not isinstance(self.voltageRegulationRange, float):
            self.voltageRegulationRange = float(self.voltageRegulationRange)

        if self.x0 is not None and not isinstance(self.x0, float):
            self.x0 = float(self.x0)

        if self.x2 is not None and not isinstance(self.x2, float):
            self.x2 = float(self.x2)

        if self.InitialReactiveCapabilityCurve is not None and not isinstance(self.InitialReactiveCapabilityCurve, ReactiveCapabilityCurve):
            self.InitialReactiveCapabilityCurve = ReactiveCapabilityCurve(**as_dict(self.InitialReactiveCapabilityCurve))

        if self.SynchronousMachineDynamics is not None and not isinstance(self.SynchronousMachineDynamics, SynchronousMachineDynamics):
            self.SynchronousMachineDynamics = SynchronousMachineDynamics(**as_dict(self.SynchronousMachineDynamics))

        super().__post_init__(**kwargs)


class SynchronousMachineDynamics(IdentifiedObject):
    """
    Synchronous machine whose behaviour is described by reference to a standard model expressed in one of the
    following forms:- simplified (or classical), where a group of generators or motors is not modelled in detail;-
    detailed, in equivalent circuit form;- detailed, in time constant reactance form; or<font color=#0f0f0f>- by
    definition of a user-defined model.</font><font color=#0f0f0f>It is a common practice to represent small
    generators by a negative load rather than by a dynamic generator model when performing dynamics simulations. In
    this case, a SynchronousMachine in the static model is not represented by anything in the dynamics model, instead
    it is treated as an ordinary load.</font><font color=#0f0f0f>Parameter details:</font><ol> <li><font
    color=#0f0f0f>Synchronous machine parameters such as <i>Xl, Xd, Xp</i> etc. are actually used as inductances in
    the models,</font> but are commonly referred to as reactances since, at nominal frequency, the PU values are the
    same. However, some references use the symbol <i>L</i> instead of <i>X</i>.</li></ol>
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SynchronousMachineDynamics"]
    class_class_curie: ClassVar[str] = "cim:SynchronousMachineDynamics"
    class_name: ClassVar[str] = "SynchronousMachineDynamics"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SynchronousMachineDynamics


@dataclass(repr=False)
class SynchrophaserFrame(IdentifiedObject):
    """
    Two-byte frame synchronization word following series of bits defined in Table 1 of IEEE c37.118-2024
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SynchrophaserFrame"]
    class_class_curie: ClassVar[str] = "cim:SynchrophaserFrame"
    class_name: ClassVar[str] = "SynchrophaserFrame"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SynchrophaserFrame

    chk: Optional[int] = None
    fracsec: Optional[int] = None
    framesize: Optional[int] = None
    leapByte: Optional[float] = None
    soc: Optional[Union[str, XSDTime]] = None
    streamId: Optional[int] = None
    sync: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.chk is not None and not isinstance(self.chk, int):
            self.chk = int(self.chk)

        if self.fracsec is not None and not isinstance(self.fracsec, int):
            self.fracsec = int(self.fracsec)

        if self.framesize is not None and not isinstance(self.framesize, int):
            self.framesize = int(self.framesize)

        if self.leapByte is not None and not isinstance(self.leapByte, float):
            self.leapByte = float(self.leapByte)

        if self.soc is not None and not isinstance(self.soc, XSDTime):
            self.soc = XSDTime(self.soc)

        if self.streamId is not None and not isinstance(self.streamId, int):
            self.streamId = int(self.streamId)

        if self.sync is not None and not isinstance(self.sync, str):
            self.sync = str(self.sync)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PMUConfigurationFrame(SynchrophaserFrame):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PMUConfigurationFrame"]
    class_class_curie: ClassVar[str] = "cim:PMUConfigurationFrame"
    class_name: ClassVar[str] = "PMUConfigurationFrame"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PMUConfigurationFrame

    dataRate: Optional[int] = None
    numPMU: Optional[int] = None
    pmuConfig: Optional[int] = None
    timeBase: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.dataRate is not None and not isinstance(self.dataRate, int):
            self.dataRate = int(self.dataRate)

        if self.numPMU is not None and not isinstance(self.numPMU, int):
            self.numPMU = int(self.numPMU)

        if self.pmuConfig is not None and not isinstance(self.pmuConfig, int):
            self.pmuConfig = int(self.pmuConfig)

        if self.timeBase is not None and not isinstance(self.timeBase, int):
            self.timeBase = int(self.timeBase)

        super().__post_init__(**kwargs)


class SystemOperator(YAMLRoot):
    """
    System operator.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["SystemOperator"]
    class_class_curie: ClassVar[str] = "cim:SystemOperator"
    class_name: ClassVar[str] = "SystemOperator"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SystemOperator


@dataclass(repr=False)
class TCSCCompensationPoint(YAMLRoot):
    """
    Compensation point of a TCSC compensator.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TCSCCompensationPoint"]
    class_class_curie: ClassVar[str] = "cim:TCSCCompensationPoint"
    class_name: ClassVar[str] = "TCSCCompensationPoint"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TCSCCompensationPoint

    mRID: Optional[str] = None
    compensationZ: Optional[float] = None
    section: Optional[int] = None
    ThyristorControlledSeriesCompensator: Optional[Union[dict, "ThyristorControlledSeriesCompensator"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.mRID is not None and not isinstance(self.mRID, str):
            self.mRID = str(self.mRID)

        if self.compensationZ is not None and not isinstance(self.compensationZ, float):
            self.compensationZ = float(self.compensationZ)

        if self.section is not None and not isinstance(self.section, int):
            self.section = int(self.section)

        if self.ThyristorControlledSeriesCompensator is not None and not isinstance(self.ThyristorControlledSeriesCompensator, ThyristorControlledSeriesCompensator):
            self.ThyristorControlledSeriesCompensator = ThyristorControlledSeriesCompensator(**as_dict(self.ThyristorControlledSeriesCompensator))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TapChanger(PowerSystemResource):
    """
    Mechanism for changing transformer winding tap positions.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TapChanger"]
    class_class_curie: ClassVar[str] = "cim:TapChanger"
    class_name: ClassVar[str] = "TapChanger"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TapChanger

    controlEnabled: Optional[Union[bool, Bool]] = None
    ctRating: Optional[float] = None
    ctRatio: Optional[float] = None
    highStep: Optional[int] = None
    initialDelay: Optional[float] = None
    lowStep: Optional[int] = None
    ltcFlag: Optional[Union[bool, Bool]] = None
    neutralStep: Optional[int] = None
    neutralU: Optional[float] = None
    normalStep: Optional[int] = None
    ptPhase: Optional[Union[str, "PhaseCode"]] = None
    ptRatio: Optional[float] = None
    step: Optional[float] = None
    subsequentDelay: Optional[float] = None
    SvTapStep: Optional[Union[dict, SvTapStep]] = None
    TapChangeController: Optional[Union[dict, "TapChangerController"]] = None
    TapChangerControl: Optional[Union[dict, "TapChangerControl"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.controlEnabled is not None and not isinstance(self.controlEnabled, Bool):
            self.controlEnabled = Bool(self.controlEnabled)

        if self.ctRating is not None and not isinstance(self.ctRating, float):
            self.ctRating = float(self.ctRating)

        if self.ctRatio is not None and not isinstance(self.ctRatio, float):
            self.ctRatio = float(self.ctRatio)

        if self.highStep is not None and not isinstance(self.highStep, int):
            self.highStep = int(self.highStep)

        if self.initialDelay is not None and not isinstance(self.initialDelay, float):
            self.initialDelay = float(self.initialDelay)

        if self.lowStep is not None and not isinstance(self.lowStep, int):
            self.lowStep = int(self.lowStep)

        if self.ltcFlag is not None and not isinstance(self.ltcFlag, Bool):
            self.ltcFlag = Bool(self.ltcFlag)

        if self.neutralStep is not None and not isinstance(self.neutralStep, int):
            self.neutralStep = int(self.neutralStep)

        if self.neutralU is not None and not isinstance(self.neutralU, float):
            self.neutralU = float(self.neutralU)

        if self.normalStep is not None and not isinstance(self.normalStep, int):
            self.normalStep = int(self.normalStep)

        if self.ptPhase is not None and not isinstance(self.ptPhase, PhaseCode):
            self.ptPhase = PhaseCode(self.ptPhase)

        if self.ptRatio is not None and not isinstance(self.ptRatio, float):
            self.ptRatio = float(self.ptRatio)

        if self.step is not None and not isinstance(self.step, float):
            self.step = float(self.step)

        if self.subsequentDelay is not None and not isinstance(self.subsequentDelay, float):
            self.subsequentDelay = float(self.subsequentDelay)

        if self.SvTapStep is not None and not isinstance(self.SvTapStep, SvTapStep):
            self.SvTapStep = SvTapStep(**as_dict(self.SvTapStep))

        if self.TapChangeController is not None and not isinstance(self.TapChangeController, TapChangerController):
            self.TapChangeController = TapChangerController(**as_dict(self.TapChangeController))

        if self.TapChangerControl is not None and not isinstance(self.TapChangerControl, TapChangerControl):
            self.TapChangerControl = TapChangerControl(**as_dict(self.TapChangerControl))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ImpedanceTapChangerTabular(TapChanger):
    """
    Describes a tap changer with a table defining the relation between the tap step and the impedance difference
    across the windings of a three winding transformer.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ImpedanceTapChangerTabular"]
    class_class_curie: ClassVar[str] = "cim:ImpedanceTapChangerTabular"
    class_name: ClassVar[str] = "ImpedanceTapChangerTabular"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ImpedanceTapChangerTabular

    ImpedanceTapChangerTable: Optional[Union[dict, ImpedanceTapChangerTable]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.ImpedanceTapChangerTable is not None and not isinstance(self.ImpedanceTapChangerTable, ImpedanceTapChangerTable):
            self.ImpedanceTapChangerTable = ImpedanceTapChangerTable(**as_dict(self.ImpedanceTapChangerTable))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PhaseTapChanger(TapChanger):
    """
    A transformer phase shifting tap model that controls the phase angle difference across the power transformer and
    potentially the active power flow through the power transformer. This phase tap model may also impact the voltage
    magnitude.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PhaseTapChanger"]
    class_class_curie: ClassVar[str] = "cim:PhaseTapChanger"
    class_name: ClassVar[str] = "PhaseTapChanger"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhaseTapChanger

    TransformerEnd: Optional[Union[dict, "TransformerEnd"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.TransformerEnd is not None and not isinstance(self.TransformerEnd, TransformerEnd):
            self.TransformerEnd = TransformerEnd(**as_dict(self.TransformerEnd))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PhaseTapChangerLinear(PhaseTapChanger):
    """
    Describes a tap changer with a linear relation between the tap step and the phase angle difference across the
    transformer. This is a mathematical model that is an approximation of a real phase tap changer.The phase angle is
    computed as stepPhaseShiftIncrement times the tap position.The voltage magnitude of both sides is the same.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PhaseTapChangerLinear"]
    class_class_curie: ClassVar[str] = "cim:PhaseTapChangerLinear"
    class_name: ClassVar[str] = "PhaseTapChangerLinear"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhaseTapChangerLinear

    stepPhaseShiftIncrement: Optional[float] = None
    xMax: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.stepPhaseShiftIncrement is not None and not isinstance(self.stepPhaseShiftIncrement, float):
            self.stepPhaseShiftIncrement = float(self.stepPhaseShiftIncrement)

        if self.xMax is not None and not isinstance(self.xMax, float):
            self.xMax = float(self.xMax)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PhaseTapChangerNonLinear(PhaseTapChanger):
    """
    The non-linear phase tap changer describes the non-linear behaviour of a phase tap changer. This is a base class
    for the symmetrical and asymmetrical phase tap changer models. The details of these models can be found in IEC
    61970-301.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PhaseTapChangerNonLinear"]
    class_class_curie: ClassVar[str] = "cim:PhaseTapChangerNonLinear"
    class_name: ClassVar[str] = "PhaseTapChangerNonLinear"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhaseTapChangerNonLinear

    voltageStepIncrement: Optional[float] = None
    xMax: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.voltageStepIncrement is not None and not isinstance(self.voltageStepIncrement, float):
            self.voltageStepIncrement = float(self.voltageStepIncrement)

        if self.xMax is not None and not isinstance(self.xMax, float):
            self.xMax = float(self.xMax)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ConnectionAngleTapChanger(PhaseTapChangerNonLinear):
    """
    Describes the tap model for an asymmetrical phase shifting transformer in which the difference voltage vector adds
    to the in-phase winding. The out-of-phase winding is the transformer end where the tap changer is located. The
    angle between the in-phase and out-of-phase windings is named the winding connection angle. The phase shift
    depends on both the difference voltage magnitude and the winding connection angle. The winding connection angle
    can be changed for different operating conditions while energized.The following options are supported:<ol>
    <li>Modelling of tap changer using ConnectionAngleTapChanger without ConnectionAngleTapChangerTable. Equations for
    asymmetrical transformer defined in IEC 61970-301 are used. The supported winding connection angle range is
    defined by the maximum winding connection angle and the minimum winding connection angle. The connection angle
    step size is used to define the allowed winding connection angles for the tap changer.</li> <li>Modelling of tap
    changer using ConnectionAngleTapChanger with ConnectionAngleTapChangerTable. There shall be different tables that
    relate to different winding connection angles that are supported by the tap changer. There is no need to provide
    information on winding connection angle range and connection angle step size as the allowed winding connection
    angles are defined by the table. The usage of the table is recommended in cases where the equations for
    asymmetrical transformer defined in IEC 61970-301 cannot fully describe the tap changer or in cases where it is
    exchange the data for different tap steps in an explicit way as a table.</li></ol>
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ConnectionAngleTapChanger"]
    class_class_curie: ClassVar[str] = "cim:ConnectionAngleTapChanger"
    class_name: ClassVar[str] = "ConnectionAngleTapChanger"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConnectionAngleTapChanger

    connectionAngleStepSize: Optional[float] = None
    maxWindingConnectionAngle: Optional[float] = None
    minWindingConnectionAngle: Optional[float] = None
    normalWindingConnectionAngle: Optional[float] = None
    windingConnectionAngle: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.connectionAngleStepSize is not None and not isinstance(self.connectionAngleStepSize, float):
            self.connectionAngleStepSize = float(self.connectionAngleStepSize)

        if self.maxWindingConnectionAngle is not None and not isinstance(self.maxWindingConnectionAngle, float):
            self.maxWindingConnectionAngle = float(self.maxWindingConnectionAngle)

        if self.minWindingConnectionAngle is not None and not isinstance(self.minWindingConnectionAngle, float):
            self.minWindingConnectionAngle = float(self.minWindingConnectionAngle)

        if self.normalWindingConnectionAngle is not None and not isinstance(self.normalWindingConnectionAngle, float):
            self.normalWindingConnectionAngle = float(self.normalWindingConnectionAngle)

        if self.windingConnectionAngle is not None and not isinstance(self.windingConnectionAngle, float):
            self.windingConnectionAngle = float(self.windingConnectionAngle)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PhaseTapChangerAsymmetrical(PhaseTapChangerNonLinear):
    """
    Describes the tap model for an asymmetrical phase shifting transformer in which the difference voltage vector adds
    to the in-phase winding. The out-of-phase winding is the transformer end where the tap changer is located. The
    angle between the in-phase and out-of-phase windings is named the winding connection angle. The phase shift
    depends on both the difference voltage magnitude and the winding connection angle.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PhaseTapChangerAsymmetrical"]
    class_class_curie: ClassVar[str] = "cim:PhaseTapChangerAsymmetrical"
    class_name: ClassVar[str] = "PhaseTapChangerAsymmetrical"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhaseTapChangerAsymmetrical

    windingConnectionAngle: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.windingConnectionAngle is not None and not isinstance(self.windingConnectionAngle, float):
            self.windingConnectionAngle = float(self.windingConnectionAngle)

        super().__post_init__(**kwargs)


class PhaseTapChangerSymmetrical(PhaseTapChangerNonLinear):
    """
    Describes a symmetrical phase shifting transformer tap model in which the voltage magnitude of both sides is the
    same. The difference voltage magnitude is the base in an equal-sided triangle where the sides corresponds to the
    primary and secondary voltages. The phase angle difference corresponds to the top angle and can be expressed as
    twice the arctangent of half the total difference voltage.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PhaseTapChangerSymmetrical"]
    class_class_curie: ClassVar[str] = "cim:PhaseTapChangerSymmetrical"
    class_name: ClassVar[str] = "PhaseTapChangerSymmetrical"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhaseTapChangerSymmetrical


@dataclass(repr=False)
class PhaseTapChangerTabular(PhaseTapChanger):
    """
    Describes a tap changer with a table defining the relation between the tap step and the phase angle difference
    across the transformer.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PhaseTapChangerTabular"]
    class_class_curie: ClassVar[str] = "cim:PhaseTapChangerTabular"
    class_name: ClassVar[str] = "PhaseTapChangerTabular"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhaseTapChangerTabular

    PhaseTapChangerTable: Optional[Union[dict, PhaseTapChangerTable]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.PhaseTapChangerTable is not None and not isinstance(self.PhaseTapChangerTable, PhaseTapChangerTable):
            self.PhaseTapChangerTable = PhaseTapChangerTable(**as_dict(self.PhaseTapChangerTable))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RatioTapChanger(TapChanger):
    """
    A tap changer that changes the voltage ratio impacting the voltage magnitude but not the phase angle across the
    transformer.Angle sign convention (general): Positive value indicates a positive phase shift from the winding
    where the tap is located to the other winding (for a two-winding transformer).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["RatioTapChanger"]
    class_class_curie: ClassVar[str] = "cim:RatioTapChanger"
    class_name: ClassVar[str] = "RatioTapChanger"
    class_model_uri: ClassVar[URIRef] = CIMTBL.RatioTapChanger

    stepVoltageIncrement: Optional[float] = None
    RatioTapChangerTable: Optional[Union[dict, RatioTapChangerTable]] = None
    TransformerEnd: Optional[Union[dict, "TransformerEnd"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.stepVoltageIncrement is not None and not isinstance(self.stepVoltageIncrement, float):
            self.stepVoltageIncrement = float(self.stepVoltageIncrement)

        if self.RatioTapChangerTable is not None and not isinstance(self.RatioTapChangerTable, RatioTapChangerTable):
            self.RatioTapChangerTable = RatioTapChangerTable(**as_dict(self.RatioTapChangerTable))

        if self.TransformerEnd is not None and not isinstance(self.TransformerEnd, TransformerEnd):
            self.TransformerEnd = TransformerEnd(**as_dict(self.TransformerEnd))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TapChangerControl(RegulatingControl):
    """
    Describes behaviour specific to tap changers, e.g. how the voltage at the end of a line varies with the load level
    and compensation of the voltage drop by tap adjustment. When TapChanger.ctRatio and .ptRatio are present,
    RegulatingControl.targetVoltage RegulatingControl.targetDeadband, RegulatingControl.maxAllowedTargetValue,
    RegulatingControl.minAllowedTargetValue as well as TapChangerControl.maxLimitVoltage and
    TapChangerControl.minLimitVoltage shall be expressed in terms of secondary CT currents and PT voltages.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TapChangerControl"]
    class_class_curie: ClassVar[str] = "cim:TapChangerControl"
    class_name: ClassVar[str] = "TapChangerControl"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TapChangerControl

    lineDropCompensation: Optional[Union[bool, Bool]] = None
    lineDropR: Optional[float] = None
    lineDropX: Optional[float] = None
    maxLimitVoltage: Optional[float] = None
    minLimitVoltage: Optional[float] = None
    reverseLineDropR: Optional[float] = None
    reverseLineDropX: Optional[float] = None
    reverseToNeutral: Optional[Union[bool, Bool]] = None
    reversible: Optional[Union[bool, Bool]] = None
    reversingDelay: Optional[float] = None
    reversingPowerThreshold: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.lineDropCompensation is not None and not isinstance(self.lineDropCompensation, Bool):
            self.lineDropCompensation = Bool(self.lineDropCompensation)

        if self.lineDropR is not None and not isinstance(self.lineDropR, float):
            self.lineDropR = float(self.lineDropR)

        if self.lineDropX is not None and not isinstance(self.lineDropX, float):
            self.lineDropX = float(self.lineDropX)

        if self.maxLimitVoltage is not None and not isinstance(self.maxLimitVoltage, float):
            self.maxLimitVoltage = float(self.maxLimitVoltage)

        if self.minLimitVoltage is not None and not isinstance(self.minLimitVoltage, float):
            self.minLimitVoltage = float(self.minLimitVoltage)

        if self.reverseLineDropR is not None and not isinstance(self.reverseLineDropR, float):
            self.reverseLineDropR = float(self.reverseLineDropR)

        if self.reverseLineDropX is not None and not isinstance(self.reverseLineDropX, float):
            self.reverseLineDropX = float(self.reverseLineDropX)

        if self.reverseToNeutral is not None and not isinstance(self.reverseToNeutral, Bool):
            self.reverseToNeutral = Bool(self.reverseToNeutral)

        if self.reversible is not None and not isinstance(self.reversible, Bool):
            self.reversible = Bool(self.reversible)

        if self.reversingDelay is not None and not isinstance(self.reversingDelay, float):
            self.reversingDelay = float(self.reversingDelay)

        if self.reversingPowerThreshold is not None and not isinstance(self.reversingPowerThreshold, float):
            self.reversingPowerThreshold = float(self.reversingPowerThreshold)

        super().__post_init__(**kwargs)


class TapChangerController(EquipmentController):
    """
    Tap changer controller is an equipment controller that controls a tap changer, e.g. how the voltage at the end of
    a line varies with the load level and compensation of the voltage drop by tap adjustment.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TapChangerController"]
    class_class_curie: ClassVar[str] = "cim:TapChangerController"
    class_name: ClassVar[str] = "TapChangerController"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TapChangerController


@dataclass(repr=False)
class TapChangerInfo(ConductingAssetInfo):
    """
    Tap changer data.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TapChangerInfo"]
    class_class_curie: ClassVar[str] = "cim:TapChangerInfo"
    class_name: ClassVar[str] = "TapChangerInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TapChangerInfo

    bil: Optional[float] = None
    ctRating: Optional[float] = None
    ctRatio: Optional[float] = None
    frequency: Optional[float] = None
    highStep: Optional[int] = None
    isTcul: Optional[Union[bool, Bool]] = None
    lowStep: Optional[int] = None
    neutralStep: Optional[int] = None
    neutralU: Optional[float] = None
    ptRatio: Optional[float] = None
    ratedApparentPower: Optional[float] = None
    stepPhaseIncrement: Optional[float] = None
    stepReactiveIncrement: Optional[float] = None
    stepVoltageIncrement: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.bil is not None and not isinstance(self.bil, float):
            self.bil = float(self.bil)

        if self.ctRating is not None and not isinstance(self.ctRating, float):
            self.ctRating = float(self.ctRating)

        if self.ctRatio is not None and not isinstance(self.ctRatio, float):
            self.ctRatio = float(self.ctRatio)

        if self.frequency is not None and not isinstance(self.frequency, float):
            self.frequency = float(self.frequency)

        if self.highStep is not None and not isinstance(self.highStep, int):
            self.highStep = int(self.highStep)

        if self.isTcul is not None and not isinstance(self.isTcul, Bool):
            self.isTcul = Bool(self.isTcul)

        if self.lowStep is not None and not isinstance(self.lowStep, int):
            self.lowStep = int(self.lowStep)

        if self.neutralStep is not None and not isinstance(self.neutralStep, int):
            self.neutralStep = int(self.neutralStep)

        if self.neutralU is not None and not isinstance(self.neutralU, float):
            self.neutralU = float(self.neutralU)

        if self.ptRatio is not None and not isinstance(self.ptRatio, float):
            self.ptRatio = float(self.ptRatio)

        if self.ratedApparentPower is not None and not isinstance(self.ratedApparentPower, float):
            self.ratedApparentPower = float(self.ratedApparentPower)

        if self.stepPhaseIncrement is not None and not isinstance(self.stepPhaseIncrement, float):
            self.stepPhaseIncrement = float(self.stepPhaseIncrement)

        if self.stepReactiveIncrement is not None and not isinstance(self.stepReactiveIncrement, float):
            self.stepReactiveIncrement = float(self.stepReactiveIncrement)

        if self.stepVoltageIncrement is not None and not isinstance(self.stepVoltageIncrement, float):
            self.stepVoltageIncrement = float(self.stepVoltageIncrement)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TapChangerTablePoint(YAMLRoot):
    """
    Describes each tap step in the tabular curve. Note that the upper boundary is not constrained to 100 percent.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TapChangerTablePoint"]
    class_class_curie: ClassVar[str] = "cim:TapChangerTablePoint"
    class_name: ClassVar[str] = "TapChangerTablePoint"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TapChangerTablePoint

    b: Optional[float] = None
    g: Optional[float] = None
    r: Optional[float] = None
    ratio: Optional[float] = None
    step: Optional[int] = None
    x: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.b is not None and not isinstance(self.b, float):
            self.b = float(self.b)

        if self.g is not None and not isinstance(self.g, float):
            self.g = float(self.g)

        if self.r is not None and not isinstance(self.r, float):
            self.r = float(self.r)

        if self.ratio is not None and not isinstance(self.ratio, float):
            self.ratio = float(self.ratio)

        if self.step is not None and not isinstance(self.step, int):
            self.step = int(self.step)

        if self.x is not None and not isinstance(self.x, float):
            self.x = float(self.x)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PhaseTapChangerTablePoint(TapChangerTablePoint):
    """
    Describes each tap step in the phase tap changer tabular curve.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PhaseTapChangerTablePoint"]
    class_class_curie: ClassVar[str] = "cim:PhaseTapChangerTablePoint"
    class_name: ClassVar[str] = "PhaseTapChangerTablePoint"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhaseTapChangerTablePoint

    angle: Optional[float] = None
    PhaseTapChangerTable: Optional[Union[dict, PhaseTapChangerTable]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.angle is not None and not isinstance(self.angle, float):
            self.angle = float(self.angle)

        if self.PhaseTapChangerTable is not None and not isinstance(self.PhaseTapChangerTable, PhaseTapChangerTable):
            self.PhaseTapChangerTable = PhaseTapChangerTable(**as_dict(self.PhaseTapChangerTable))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class RatioTapChangerTablePoint(TapChangerTablePoint):
    """
    Describes each tap step in the ratio tap changer tabular curve.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["RatioTapChangerTablePoint"]
    class_class_curie: ClassVar[str] = "cim:RatioTapChangerTablePoint"
    class_name: ClassVar[str] = "RatioTapChangerTablePoint"
    class_model_uri: ClassVar[URIRef] = CIMTBL.RatioTapChangerTablePoint

    RatioTapChangerTable: Optional[Union[dict, RatioTapChangerTable]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.RatioTapChangerTable is not None and not isinstance(self.RatioTapChangerTable, RatioTapChangerTable):
            self.RatioTapChangerTable = RatioTapChangerTable(**as_dict(self.RatioTapChangerTable))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TapSchedule(SeasonDayTypeSchedule):
    """
    A pre-established pattern over time for a tap step.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TapSchedule"]
    class_class_curie: ClassVar[str] = "cim:TapSchedule"
    class_name: ClassVar[str] = "TapSchedule"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TapSchedule

    TapChanger: Optional[Union[dict, TapChanger]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.TapChanger is not None and not isinstance(self.TapChanger, TapChanger):
            self.TapChanger = TapChanger(**as_dict(self.TapChanger))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Terminal(ACDCTerminal):
    """
    An AC electrical connection point to a piece of conducting equipment. Terminals are connected at physical
    connection points called connectivity nodes.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["Terminal"]
    class_class_curie: ClassVar[str] = "cim:Terminal"
    class_name: ClassVar[str] = "Terminal"
    class_model_uri: ClassVar[URIRef] = CIMTBL.Terminal

    phases: Optional[Union[str, "PhaseCode"]] = None
    BoundedConnectivityArea: Optional[Union[dict, ConnectivityArea]] = None
    BoundedContainer: Optional[Union[dict, ResourceContainer]] = None
    Bushing: Optional[Union[dict, Bushing]] = None
    ConductingEquipment: Optional[Union[dict, ConductingEquipment]] = None
    ConnectivityNode: Optional[Union[dict, ConnectivityNode]] = None
    NormalHeadFeeder: Optional[Union[dict, Feeder]] = None
    StateShortCircuitResult: Optional[Union[dict, StateShortCircuitResult]] = None
    TopologicalNode: Optional[Union[dict, "TopologicalNode"]] = None
    UsagePoint: Optional[Union[dict, "UsagePoint"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.phases is not None and not isinstance(self.phases, PhaseCode):
            self.phases = PhaseCode(self.phases)

        if self.BoundedConnectivityArea is not None and not isinstance(self.BoundedConnectivityArea, ConnectivityArea):
            self.BoundedConnectivityArea = ConnectivityArea(**as_dict(self.BoundedConnectivityArea))

        if self.BoundedContainer is not None and not isinstance(self.BoundedContainer, ResourceContainer):
            self.BoundedContainer = ResourceContainer()

        if self.Bushing is not None and not isinstance(self.Bushing, Bushing):
            self.Bushing = Bushing(**as_dict(self.Bushing))

        if self.ConductingEquipment is not None and not isinstance(self.ConductingEquipment, ConductingEquipment):
            self.ConductingEquipment = ConductingEquipment(**as_dict(self.ConductingEquipment))

        if self.ConnectivityNode is not None and not isinstance(self.ConnectivityNode, ConnectivityNode):
            self.ConnectivityNode = ConnectivityNode(**as_dict(self.ConnectivityNode))

        if self.NormalHeadFeeder is not None and not isinstance(self.NormalHeadFeeder, Feeder):
            self.NormalHeadFeeder = Feeder(**as_dict(self.NormalHeadFeeder))

        if self.StateShortCircuitResult is not None and not isinstance(self.StateShortCircuitResult, StateShortCircuitResult):
            self.StateShortCircuitResult = StateShortCircuitResult(**as_dict(self.StateShortCircuitResult))

        if self.TopologicalNode is not None and not isinstance(self.TopologicalNode, TopologicalNode):
            self.TopologicalNode = TopologicalNode(**as_dict(self.TopologicalNode))

        if self.UsagePoint is not None and not isinstance(self.UsagePoint, UsagePoint):
            self.UsagePoint = UsagePoint(**as_dict(self.UsagePoint))

        super().__post_init__(**kwargs)


class ThermalGeneratingUnit(GeneratingUnit):
    """
    A generating unit whose prime mover could be a steam turbine, combustion turbine, or diesel engine.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ThermalGeneratingUnit"]
    class_class_curie: ClassVar[str] = "cim:ThermalGeneratingUnit"
    class_name: ClassVar[str] = "ThermalGeneratingUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ThermalGeneratingUnit


@dataclass(repr=False)
class ThyristorControlledSeriesCompensator(FACTSEquipment):
    """
    Thyristor-controlled series capacitors (TCSC) is a type of flexible AC transmission system regulating equipment
    that is configured with controlled reactors in parallel with sections of a capacitor bank. This combination allows
    smooth control of the fundamental frequency capacitive reactance over a wide range. The thyristor valve contains a
    string of series connected high power thyristors. TCSC can control power flows in order to achieve eliminating of
    line overloads, reducing loop flows and minimising system losses.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ThyristorControlledSeriesCompensator"]
    class_class_curie: ClassVar[str] = "cim:ThyristorControlledSeriesCompensator"
    class_name: ClassVar[str] = "ThyristorControlledSeriesCompensator"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ThyristorControlledSeriesCompensator

    compensationZ: Optional[float] = None
    flexibleCapacitiveZ: Optional[float] = None
    flexibleInductiveZ: Optional[float] = None
    minI: Optional[float] = None
    reconnectionI: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.compensationZ is not None and not isinstance(self.compensationZ, float):
            self.compensationZ = float(self.compensationZ)

        if self.flexibleCapacitiveZ is not None and not isinstance(self.flexibleCapacitiveZ, float):
            self.flexibleCapacitiveZ = float(self.flexibleCapacitiveZ)

        if self.flexibleInductiveZ is not None and not isinstance(self.flexibleInductiveZ, float):
            self.flexibleInductiveZ = float(self.flexibleInductiveZ)

        if self.minI is not None and not isinstance(self.minI, float):
            self.minI = float(self.minI)

        if self.reconnectionI is not None and not isinstance(self.reconnectionI, float):
            self.reconnectionI = float(self.reconnectionI)

        super().__post_init__(**kwargs)


class TieCorridor(PowerSystemResource):
    """
    A collection of one or more tie-lines or direct current poles that connect two different control areas.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TieCorridor"]
    class_class_curie: ClassVar[str] = "cim:TieCorridor"
    class_name: ClassVar[str] = "TieCorridor"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TieCorridor


class ACTieCorridor(TieCorridor):
    """
    A collection of one or more AC tie lines that connect two different control areas.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ACTieCorridor"]
    class_class_curie: ClassVar[str] = "cim:ACTieCorridor"
    class_name: ClassVar[str] = "ACTieCorridor"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ACTieCorridor


@dataclass(repr=False)
class TieFlow(IdentifiedObject):
    """
    Defines the structure (in terms of location and direction) of the net interchange constraint for a control area.
    This constraint may be used by either AGC or power flow.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TieFlow"]
    class_class_curie: ClassVar[str] = "cim:TieFlow"
    class_name: ClassVar[str] = "TieFlow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TieFlow

    positiveFlowIn: Optional[Union[bool, Bool]] = None
    ControlArea: Optional[Union[dict, ControlArea]] = None
    Terminal: Optional[Union[dict, Terminal]] = None
    TieCorridor: Optional[Union[dict, TieCorridor]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.positiveFlowIn is not None and not isinstance(self.positiveFlowIn, Bool):
            self.positiveFlowIn = Bool(self.positiveFlowIn)

        if self.ControlArea is not None and not isinstance(self.ControlArea, ControlArea):
            self.ControlArea = ControlArea(**as_dict(self.ControlArea))

        if self.Terminal is not None and not isinstance(self.Terminal, Terminal):
            self.Terminal = Terminal(**as_dict(self.Terminal))

        if self.TieCorridor is not None and not isinstance(self.TieCorridor, TieCorridor):
            self.TieCorridor = TieCorridor(**as_dict(self.TieCorridor))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TimeInterval(YAMLRoot):
    """
    Interval between two times.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TimeInterval"]
    class_class_curie: ClassVar[str] = "cim:TimeInterval"
    class_name: ClassVar[str] = "TimeInterval"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TimeInterval

    end: Optional[Union[str, XSDTime]] = None
    start: Optional[Union[str, XSDTime]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.end is not None and not isinstance(self.end, XSDTime):
            self.end = XSDTime(self.end)

        if self.start is not None and not isinstance(self.start, XSDTime):
            self.start = XSDTime(self.start)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TopologicalArea(IdentifiedObject):
    """
    Topological grouping of connectivity areas based on current status of switch positions
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TopologicalArea"]
    class_class_curie: ClassVar[str] = "cim:TopologicalArea"
    class_name: ClassVar[str] = "TopologicalArea"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TopologicalArea

    topologyType: Optional[Union[str, "TopologicalAreaKind"]] = None
    TopologicalIsland: Optional[Union[dict, "TopologicalIsland"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.topologyType is not None and not isinstance(self.topologyType, TopologicalAreaKind):
            self.topologyType = TopologicalAreaKind(self.topologyType)

        if self.TopologicalIsland is not None and not isinstance(self.TopologicalIsland, TopologicalIsland):
            self.TopologicalIsland = TopologicalIsland(**as_dict(self.TopologicalIsland))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TopologicalIsland(IdentifiedObject):
    """
    An electrically connected subset of the network. Topological islands can change as the current network state
    changes, e.g. due to:- disconnect switches or breakers changing state in a SCADA/EMS.- manual creation, change or
    deletion of topological nodes in a planning tool.Only energised TopologicalNode-s shall be part of the topological
    island.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TopologicalIsland"]
    class_class_curie: ClassVar[str] = "cim:TopologicalIsland"
    class_name: ClassVar[str] = "TopologicalIsland"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TopologicalIsland

    AngleRefTopologicalNode: Optional[Union[dict, "TopologicalNode"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.AngleRefTopologicalNode is not None and not isinstance(self.AngleRefTopologicalNode, TopologicalNode):
            self.AngleRefTopologicalNode = TopologicalNode(**as_dict(self.AngleRefTopologicalNode))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TopologicalNode(IdentifiedObject):
    """
    For a detailed substation model a topological node is a set of connectivity nodes that, in the current network
    state, are connected together through any type of closed switches, including jumpers. Topological nodes change as
    the current network state changes (i.e., switches, breakers, etc. change state).For a planning model, switch
    statuses are not used to form topological nodes. Instead they are manually created or deleted in a model builder
    tool. Topological nodes maintained this way are also called busses.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TopologicalNode"]
    class_class_curie: ClassVar[str] = "cim:TopologicalNode"
    class_name: ClassVar[str] = "TopologicalNode"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TopologicalNode

    busName: Optional[str] = None
    busNumber: Optional[int] = None
    pInjection: Optional[float] = None
    qInjection: Optional[float] = None
    AngleRefTopologicalIsland: Optional[Union[dict, TopologicalIsland]] = None
    BaseVoltage: Optional[Union[dict, BaseVoltage]] = None
    ConnectivityNodeContainer: Optional[Union[dict, ConnectivityNodeContainer]] = None
    ReportingGroup: Optional[Union[dict, ReportingGroup]] = None
    StateShortCircuitResult: Optional[Union[dict, StateShortCircuitResult]] = None
    TopologicalIsland: Optional[Union[dict, TopologicalIsland]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.busName is not None and not isinstance(self.busName, str):
            self.busName = str(self.busName)

        if self.busNumber is not None and not isinstance(self.busNumber, int):
            self.busNumber = int(self.busNumber)

        if self.pInjection is not None and not isinstance(self.pInjection, float):
            self.pInjection = float(self.pInjection)

        if self.qInjection is not None and not isinstance(self.qInjection, float):
            self.qInjection = float(self.qInjection)

        if self.AngleRefTopologicalIsland is not None and not isinstance(self.AngleRefTopologicalIsland, TopologicalIsland):
            self.AngleRefTopologicalIsland = TopologicalIsland(**as_dict(self.AngleRefTopologicalIsland))

        if self.BaseVoltage is not None and not isinstance(self.BaseVoltage, BaseVoltage):
            self.BaseVoltage = BaseVoltage(**as_dict(self.BaseVoltage))

        if self.ConnectivityNodeContainer is not None and not isinstance(self.ConnectivityNodeContainer, ConnectivityNodeContainer):
            self.ConnectivityNodeContainer = ConnectivityNodeContainer(**as_dict(self.ConnectivityNodeContainer))

        if self.ReportingGroup is not None and not isinstance(self.ReportingGroup, ReportingGroup):
            self.ReportingGroup = ReportingGroup(**as_dict(self.ReportingGroup))

        if self.StateShortCircuitResult is not None and not isinstance(self.StateShortCircuitResult, StateShortCircuitResult):
            self.StateShortCircuitResult = StateShortCircuitResult(**as_dict(self.StateShortCircuitResult))

        if self.TopologicalIsland is not None and not isinstance(self.TopologicalIsland, TopologicalIsland):
            self.TopologicalIsland = TopologicalIsland(**as_dict(self.TopologicalIsland))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TransformerCoreAdmittance(IdentifiedObject):
    """
    The transformer core admittance. Used to specify the core admittance of a transformer in a manner that can be
    shared among power transformers.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TransformerCoreAdmittance"]
    class_class_curie: ClassVar[str] = "cim:TransformerCoreAdmittance"
    class_name: ClassVar[str] = "TransformerCoreAdmittance"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TransformerCoreAdmittance

    b: Optional[float] = None
    b0: Optional[float] = None
    g: Optional[float] = None
    g0: Optional[float] = None
    TransformerEndInfo: Optional[Union[dict, "TransformerEndInfo"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.b is not None and not isinstance(self.b, float):
            self.b = float(self.b)

        if self.b0 is not None and not isinstance(self.b0, float):
            self.b0 = float(self.b0)

        if self.g is not None and not isinstance(self.g, float):
            self.g = float(self.g)

        if self.g0 is not None and not isinstance(self.g0, float):
            self.g0 = float(self.g0)

        if self.TransformerEndInfo is not None and not isinstance(self.TransformerEndInfo, TransformerEndInfo):
            self.TransformerEndInfo = TransformerEndInfo(**as_dict(self.TransformerEndInfo))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TransformerEnd(IdentifiedObject):
    """
    A conducting connection point of a power transformer. It corresponds to a physical transformer winding terminal.
    In earlier CIM versions, the TransformerWinding class served a similar purpose, but this class is more flexible
    because it associates to terminal but is not a specialization of ConductingEquipment.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TransformerEnd"]
    class_class_curie: ClassVar[str] = "cim:TransformerEnd"
    class_name: ClassVar[str] = "TransformerEnd"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TransformerEnd

    bmagSat: Optional[float] = None
    endNumber: Optional[int] = None
    grounded: Optional[Union[bool, Bool]] = None
    magBaseU: Optional[float] = None
    magSatFlux: Optional[float] = None
    rground: Optional[float] = None
    xground: Optional[float] = None
    AdditionalRatioTapChanger: Optional[Union[dict, RatioTapChanger]] = None
    BaseVoltage: Optional[Union[dict, BaseVoltage]] = None
    CoreAdmittance: Optional[Union[dict, TransformerCoreAdmittance]] = None
    PhaseTapChanger: Optional[Union[dict, PhaseTapChanger]] = None
    RatioTapChanger: Optional[Union[dict, RatioTapChanger]] = None
    StarImpedance: Optional[Union[dict, "TransformerStarImpedance"]] = None
    Terminal: Optional[Union[dict, Terminal]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.bmagSat is not None and not isinstance(self.bmagSat, float):
            self.bmagSat = float(self.bmagSat)

        if self.endNumber is not None and not isinstance(self.endNumber, int):
            self.endNumber = int(self.endNumber)

        if self.grounded is not None and not isinstance(self.grounded, Bool):
            self.grounded = Bool(self.grounded)

        if self.magBaseU is not None and not isinstance(self.magBaseU, float):
            self.magBaseU = float(self.magBaseU)

        if self.magSatFlux is not None and not isinstance(self.magSatFlux, float):
            self.magSatFlux = float(self.magSatFlux)

        if self.rground is not None and not isinstance(self.rground, float):
            self.rground = float(self.rground)

        if self.xground is not None and not isinstance(self.xground, float):
            self.xground = float(self.xground)

        if self.AdditionalRatioTapChanger is not None and not isinstance(self.AdditionalRatioTapChanger, RatioTapChanger):
            self.AdditionalRatioTapChanger = RatioTapChanger(**as_dict(self.AdditionalRatioTapChanger))

        if self.BaseVoltage is not None and not isinstance(self.BaseVoltage, BaseVoltage):
            self.BaseVoltage = BaseVoltage(**as_dict(self.BaseVoltage))

        if self.CoreAdmittance is not None and not isinstance(self.CoreAdmittance, TransformerCoreAdmittance):
            self.CoreAdmittance = TransformerCoreAdmittance(**as_dict(self.CoreAdmittance))

        if self.PhaseTapChanger is not None and not isinstance(self.PhaseTapChanger, PhaseTapChanger):
            self.PhaseTapChanger = PhaseTapChanger(**as_dict(self.PhaseTapChanger))

        if self.RatioTapChanger is not None and not isinstance(self.RatioTapChanger, RatioTapChanger):
            self.RatioTapChanger = RatioTapChanger(**as_dict(self.RatioTapChanger))

        if self.StarImpedance is not None and not isinstance(self.StarImpedance, TransformerStarImpedance):
            self.StarImpedance = TransformerStarImpedance(**as_dict(self.StarImpedance))

        if self.Terminal is not None and not isinstance(self.Terminal, Terminal):
            self.Terminal = Terminal(**as_dict(self.Terminal))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PowerTransformerEnd(TransformerEnd):
    """
    A PowerTransformerEnd is associated with each Terminal of a PowerTransformer.The impedance values r, r0, x, and x0
    of a PowerTransformerEnd represents a star equivalent as follows.1) two PowerTransformerEnd-s shall be defined for
    a two Terminal PowerTransformer even if the two PowerTransformerEnd-s have the same rated voltage. The high
    voltage PowerTransformerEnd (TransformerEnd.endNumber=1) is the one used to exchange resistances (r, r0) and
    reactances (x, x0) of the PowerTransformer while the low voltage PowerTransformerEnd (TransformerEnd.endNumber=2)
    shall have zero impedance values.2) for a three Terminal PowerTransformer the three PowerTransformerEnds represent
    a star equivalent with each leg in the star represented by r, r0, x, and x0 values.3) For a three Terminal
    transformer each PowerTransformerEnd shall have g, g0, b and b0 values corresponding to the no load losses
    distributed on the three PowerTransformerEnds. The total no load loss shunt impedances may also be placed at one
    of the PowerTransformerEnds, preferably the end numbered 1, having the shunt values on end 1. This is the
    preferred way.4) for a PowerTransformer with more than three Terminals the PowerTransformerEnd impedance values
    cannot be used. Instead use the TransformerMeshImpedance or split the transformer into multiple
    PowerTransformers.Each PowerTransformerEnd must be contained by a PowerTransformer. Because a PowerTransformerEnd
    (or any other object) can not be contained by more than one parent, a PowerTransformerEnd can not have an
    association to an EquipmentContainer (Substation, VoltageLevel, etc).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["PowerTransformerEnd"]
    class_class_curie: ClassVar[str] = "cim:PowerTransformerEnd"
    class_name: ClassVar[str] = "PowerTransformerEnd"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerTransformerEnd

    b: Optional[float] = None
    b0: Optional[float] = None
    connectionKind: Optional[Union[str, "WindingConnection"]] = None
    g: Optional[float] = None
    g0: Optional[float] = None
    phaseAngleClock: Optional[int] = None
    r: Optional[float] = None
    r0: Optional[float] = None
    ratedS: Optional[float] = None
    ratedU: Optional[float] = None
    x: Optional[float] = None
    x0: Optional[float] = None
    PowerTransformer: Optional[Union[dict, PowerTransformer]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.b is not None and not isinstance(self.b, float):
            self.b = float(self.b)

        if self.b0 is not None and not isinstance(self.b0, float):
            self.b0 = float(self.b0)

        if self.connectionKind is not None and not isinstance(self.connectionKind, WindingConnection):
            self.connectionKind = WindingConnection(self.connectionKind)

        if self.g is not None and not isinstance(self.g, float):
            self.g = float(self.g)

        if self.g0 is not None and not isinstance(self.g0, float):
            self.g0 = float(self.g0)

        if self.phaseAngleClock is not None and not isinstance(self.phaseAngleClock, int):
            self.phaseAngleClock = int(self.phaseAngleClock)

        if self.r is not None and not isinstance(self.r, float):
            self.r = float(self.r)

        if self.r0 is not None and not isinstance(self.r0, float):
            self.r0 = float(self.r0)

        if self.ratedS is not None and not isinstance(self.ratedS, float):
            self.ratedS = float(self.ratedS)

        if self.ratedU is not None and not isinstance(self.ratedU, float):
            self.ratedU = float(self.ratedU)

        if self.x is not None and not isinstance(self.x, float):
            self.x = float(self.x)

        if self.x0 is not None and not isinstance(self.x0, float):
            self.x0 = float(self.x0)

        if self.PowerTransformer is not None and not isinstance(self.PowerTransformer, PowerTransformer):
            self.PowerTransformer = PowerTransformer(**as_dict(self.PowerTransformer))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TransformerEndInfo(ConductingAssetInfo):
    """
    Transformer end data.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TransformerEndInfo"]
    class_class_curie: ClassVar[str] = "cim:TransformerEndInfo"
    class_name: ClassVar[str] = "TransformerEndInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TransformerEndInfo

    connectionKind: Optional[Union[str, "WindingConnection"]] = None
    emergencyS: Optional[float] = None
    endNumber: Optional[int] = None
    insulationU: Optional[float] = None
    phaseAngleClock: Optional[int] = None
    r: Optional[float] = None
    ratedS: Optional[float] = None
    shortTermS: Optional[float] = None
    CoreAdmittance: Optional[Union[dict, TransformerCoreAdmittance]] = None
    TransformerStarImpedance: Optional[Union[dict, "TransformerStarImpedance"]] = None
    TransformerTankInfo: Optional[Union[dict, "TransformerTankInfo"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.connectionKind is not None and not isinstance(self.connectionKind, WindingConnection):
            self.connectionKind = WindingConnection(self.connectionKind)

        if self.emergencyS is not None and not isinstance(self.emergencyS, float):
            self.emergencyS = float(self.emergencyS)

        if self.endNumber is not None and not isinstance(self.endNumber, int):
            self.endNumber = int(self.endNumber)

        if self.insulationU is not None and not isinstance(self.insulationU, float):
            self.insulationU = float(self.insulationU)

        if self.phaseAngleClock is not None and not isinstance(self.phaseAngleClock, int):
            self.phaseAngleClock = int(self.phaseAngleClock)

        if self.r is not None and not isinstance(self.r, float):
            self.r = float(self.r)

        if self.ratedS is not None and not isinstance(self.ratedS, float):
            self.ratedS = float(self.ratedS)

        if self.shortTermS is not None and not isinstance(self.shortTermS, float):
            self.shortTermS = float(self.shortTermS)

        if self.CoreAdmittance is not None and not isinstance(self.CoreAdmittance, TransformerCoreAdmittance):
            self.CoreAdmittance = TransformerCoreAdmittance(**as_dict(self.CoreAdmittance))

        if self.TransformerStarImpedance is not None and not isinstance(self.TransformerStarImpedance, TransformerStarImpedance):
            self.TransformerStarImpedance = TransformerStarImpedance(**as_dict(self.TransformerStarImpedance))

        if self.TransformerTankInfo is not None and not isinstance(self.TransformerTankInfo, TransformerTankInfo):
            self.TransformerTankInfo = TransformerTankInfo(**as_dict(self.TransformerTankInfo))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TransformerMeshImpedance(IdentifiedObject):
    """
    Transformer mesh impedance (Delta-model) between transformer ends.The typical case is that this class describes
    the impedance between two transformer ends pair-wise, i.e. the cardinalities at both transformer end associations
    are 1. However, in cases where two or more transformer ends are modelled the cardinalities are larger than 1.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TransformerMeshImpedance"]
    class_class_curie: ClassVar[str] = "cim:TransformerMeshImpedance"
    class_name: ClassVar[str] = "TransformerMeshImpedance"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TransformerMeshImpedance

    r: Optional[float] = None
    r0: Optional[float] = None
    x: Optional[float] = None
    x0: Optional[float] = None
    FromTransformerEnd: Optional[Union[dict, TransformerEnd]] = None
    FromTransformerEndInfo: Optional[Union[dict, TransformerEndInfo]] = None
    ToTransformerEnd: Optional[Union[Union[dict, TransformerEnd], list[Union[dict, TransformerEnd]]]] = empty_list()
    ToTransformerEndInfos: Optional[Union[Union[dict, TransformerEndInfo], list[Union[dict, TransformerEndInfo]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.r is not None and not isinstance(self.r, float):
            self.r = float(self.r)

        if self.r0 is not None and not isinstance(self.r0, float):
            self.r0 = float(self.r0)

        if self.x is not None and not isinstance(self.x, float):
            self.x = float(self.x)

        if self.x0 is not None and not isinstance(self.x0, float):
            self.x0 = float(self.x0)

        if self.FromTransformerEnd is not None and not isinstance(self.FromTransformerEnd, TransformerEnd):
            self.FromTransformerEnd = TransformerEnd(**as_dict(self.FromTransformerEnd))

        if self.FromTransformerEndInfo is not None and not isinstance(self.FromTransformerEndInfo, TransformerEndInfo):
            self.FromTransformerEndInfo = TransformerEndInfo(**as_dict(self.FromTransformerEndInfo))

        if not isinstance(self.ToTransformerEnd, list):
            self.ToTransformerEnd = [self.ToTransformerEnd] if self.ToTransformerEnd is not None else []
        self.ToTransformerEnd = [v if isinstance(v, TransformerEnd) else TransformerEnd(**as_dict(v)) for v in self.ToTransformerEnd]

        if not isinstance(self.ToTransformerEndInfos, list):
            self.ToTransformerEndInfos = [self.ToTransformerEndInfos] if self.ToTransformerEndInfos is not None else []
        self.ToTransformerEndInfos = [v if isinstance(v, TransformerEndInfo) else TransformerEndInfo(**as_dict(v)) for v in self.ToTransformerEndInfos]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TransformerStarImpedance(IdentifiedObject):
    """
    Transformer star impedance (Pi-model) that accurately reflects impedance for transformers with 2 or 3 windings.
    For transformers with 4 or more windings, TransformerMeshImpedance class shall be used.For transmission networks
    use PowerTransformerEnd impedances (r, r0, x, x0, b, b0, g and g0).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TransformerStarImpedance"]
    class_class_curie: ClassVar[str] = "cim:TransformerStarImpedance"
    class_name: ClassVar[str] = "TransformerStarImpedance"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TransformerStarImpedance

    r: Optional[float] = None
    r0: Optional[float] = None
    x: Optional[float] = None
    x0: Optional[float] = None
    TransformerEndInfo: Optional[Union[dict, TransformerEndInfo]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.r is not None and not isinstance(self.r, float):
            self.r = float(self.r)

        if self.r0 is not None and not isinstance(self.r0, float):
            self.r0 = float(self.r0)

        if self.x is not None and not isinstance(self.x, float):
            self.x = float(self.x)

        if self.x0 is not None and not isinstance(self.x0, float):
            self.x0 = float(self.x0)

        if self.TransformerEndInfo is not None and not isinstance(self.TransformerEndInfo, TransformerEndInfo):
            self.TransformerEndInfo = TransformerEndInfo(**as_dict(self.TransformerEndInfo))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TransformerTank(Equipment):
    """
    An assembly of two or more coupled windings that transform electrical power between voltage levels. These windings
    are bound on a common core and placed in the same tank. Transformer tank can be used to model both single-phase
    and 3-phase transformers.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TransformerTank"]
    class_class_curie: ClassVar[str] = "cim:TransformerTank"
    class_name: ClassVar[str] = "TransformerTank"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TransformerTank

    PowerTransformer: Optional[Union[dict, PowerTransformer]] = None
    TransformerTankInfo: Optional[Union[dict, "TransformerTankInfo"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.PowerTransformer is not None and not isinstance(self.PowerTransformer, PowerTransformer):
            self.PowerTransformer = PowerTransformer(**as_dict(self.PowerTransformer))

        if self.TransformerTankInfo is not None and not isinstance(self.TransformerTankInfo, TransformerTankInfo):
            self.TransformerTankInfo = TransformerTankInfo(**as_dict(self.TransformerTankInfo))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TransformerTankEnd(TransformerEnd):
    """
    Transformer tank end represents an individual winding for unbalanced models or for transformer tanks connected
    into a bank (and bank is modelled with the PowerTransformer).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TransformerTankEnd"]
    class_class_curie: ClassVar[str] = "cim:TransformerTankEnd"
    class_name: ClassVar[str] = "TransformerTankEnd"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TransformerTankEnd

    phases: Optional[Union[str, "PhaseCode"]] = None
    TransformerTank: Optional[Union[dict, TransformerTank]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.phases is not None and not isinstance(self.phases, PhaseCode):
            self.phases = PhaseCode(self.phases)

        if self.TransformerTank is not None and not isinstance(self.TransformerTank, TransformerTank):
            self.TransformerTank = TransformerTank(**as_dict(self.TransformerTank))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TransformerTankInfo(AssetInfo):
    """
    Set of transformer tank data, from an equipment library.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TransformerTankInfo"]
    class_class_curie: ClassVar[str] = "cim:TransformerTankInfo"
    class_name: ClassVar[str] = "TransformerTankInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TransformerTankInfo

    PowerTransformerInfo: Optional[Union[dict, PowerTransformerInfo]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.PowerTransformerInfo is not None and not isinstance(self.PowerTransformerInfo, PowerTransformerInfo):
            self.PowerTransformerInfo = PowerTransformerInfo(**as_dict(self.PowerTransformerInfo))

        super().__post_init__(**kwargs)


class TransformerTest(IdentifiedObject):
    """
    Test result for transformer ends, such as short-circuit, open-circuit (excitation) or no-load test.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TransformerTest"]
    class_class_curie: ClassVar[str] = "cim:TransformerTest"
    class_name: ClassVar[str] = "TransformerTest"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TransformerTest


@dataclass(repr=False)
class NoLoadTest(TransformerTest):
    """
    No-load test results determine core admittance parameters. They include exciting current and core loss
    measurements from applying voltage to one winding. The excitation may be positive sequence or zero sequence. The
    test may be repeated at different voltages to measure saturation.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["NoLoadTest"]
    class_class_curie: ClassVar[str] = "cim:NoLoadTest"
    class_name: ClassVar[str] = "NoLoadTest"
    class_model_uri: ClassVar[URIRef] = CIMTBL.NoLoadTest

    energisedEndVoltage: Optional[float] = None
    excitingCurrent: Optional[float] = None
    excitingCurrentZero: Optional[float] = None
    loss: Optional[float] = None
    lossZero: Optional[float] = None
    EnergisedEnd: Optional[Union[dict, TransformerEndInfo]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.energisedEndVoltage is not None and not isinstance(self.energisedEndVoltage, float):
            self.energisedEndVoltage = float(self.energisedEndVoltage)

        if self.excitingCurrent is not None and not isinstance(self.excitingCurrent, float):
            self.excitingCurrent = float(self.excitingCurrent)

        if self.excitingCurrentZero is not None and not isinstance(self.excitingCurrentZero, float):
            self.excitingCurrentZero = float(self.excitingCurrentZero)

        if self.loss is not None and not isinstance(self.loss, float):
            self.loss = float(self.loss)

        if self.lossZero is not None and not isinstance(self.lossZero, float):
            self.lossZero = float(self.lossZero)

        if self.EnergisedEnd is not None and not isinstance(self.EnergisedEnd, TransformerEndInfo):
            self.EnergisedEnd = TransformerEndInfo(**as_dict(self.EnergisedEnd))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OpenCircuitTest(TransformerTest):
    """
    Open-circuit test results verify winding turn ratios and phase shifts. They include induced voltage and phase
    shift measurements on open-circuit windings, with voltage applied to the energised end. For three-phase windings,
    the excitation can be a positive sequence (the default) or a zero sequence.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["OpenCircuitTest"]
    class_class_curie: ClassVar[str] = "cim:OpenCircuitTest"
    class_name: ClassVar[str] = "OpenCircuitTest"
    class_model_uri: ClassVar[URIRef] = CIMTBL.OpenCircuitTest

    energisedEndStep: Optional[int] = None
    energisedEndVoltage: Optional[float] = None
    openEndStep: Optional[int] = None
    openEndVoltage: Optional[float] = None
    phaseShift: Optional[float] = None
    EnergisedEnd: Optional[Union[dict, TransformerEndInfo]] = None
    OpenEnd: Optional[Union[dict, TransformerEndInfo]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.energisedEndStep is not None and not isinstance(self.energisedEndStep, int):
            self.energisedEndStep = int(self.energisedEndStep)

        if self.energisedEndVoltage is not None and not isinstance(self.energisedEndVoltage, float):
            self.energisedEndVoltage = float(self.energisedEndVoltage)

        if self.openEndStep is not None and not isinstance(self.openEndStep, int):
            self.openEndStep = int(self.openEndStep)

        if self.openEndVoltage is not None and not isinstance(self.openEndVoltage, float):
            self.openEndVoltage = float(self.openEndVoltage)

        if self.phaseShift is not None and not isinstance(self.phaseShift, float):
            self.phaseShift = float(self.phaseShift)

        if self.EnergisedEnd is not None and not isinstance(self.EnergisedEnd, TransformerEndInfo):
            self.EnergisedEnd = TransformerEndInfo(**as_dict(self.EnergisedEnd))

        if self.OpenEnd is not None and not isinstance(self.OpenEnd, TransformerEndInfo):
            self.OpenEnd = TransformerEndInfo(**as_dict(self.OpenEnd))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ShortCircuitTest(TransformerTest):
    """
    Short-circuit test results determine mesh impedance parameters. They include load losses and leakage impedances.
    For three-phase windings, the excitation can be a positive sequence (the default) or a zero sequence. There shall
    be at least one grounded winding.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ShortCircuitTest"]
    class_class_curie: ClassVar[str] = "cim:ShortCircuitTest"
    class_name: ClassVar[str] = "ShortCircuitTest"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ShortCircuitTest

    current: Optional[float] = None
    energisedEndStep: Optional[int] = None
    groundedEndStep: Optional[int] = None
    leakageImpedance: Optional[float] = None
    leakageImpedanceZero: Optional[float] = None
    loss: Optional[float] = None
    lossZero: Optional[float] = None
    power: Optional[float] = None
    voltage: Optional[float] = None
    EnergisedEnd: Optional[Union[dict, TransformerEndInfo]] = None
    GroundedEnds: Optional[Union[Union[dict, TransformerEndInfo], list[Union[dict, TransformerEndInfo]]]] = empty_list()

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.current is not None and not isinstance(self.current, float):
            self.current = float(self.current)

        if self.energisedEndStep is not None and not isinstance(self.energisedEndStep, int):
            self.energisedEndStep = int(self.energisedEndStep)

        if self.groundedEndStep is not None and not isinstance(self.groundedEndStep, int):
            self.groundedEndStep = int(self.groundedEndStep)

        if self.leakageImpedance is not None and not isinstance(self.leakageImpedance, float):
            self.leakageImpedance = float(self.leakageImpedance)

        if self.leakageImpedanceZero is not None and not isinstance(self.leakageImpedanceZero, float):
            self.leakageImpedanceZero = float(self.leakageImpedanceZero)

        if self.loss is not None and not isinstance(self.loss, float):
            self.loss = float(self.loss)

        if self.lossZero is not None and not isinstance(self.lossZero, float):
            self.lossZero = float(self.lossZero)

        if self.power is not None and not isinstance(self.power, float):
            self.power = float(self.power)

        if self.voltage is not None and not isinstance(self.voltage, float):
            self.voltage = float(self.voltage)

        if self.EnergisedEnd is not None and not isinstance(self.EnergisedEnd, TransformerEndInfo):
            self.EnergisedEnd = TransformerEndInfo(**as_dict(self.EnergisedEnd))

        if not isinstance(self.GroundedEnds, list):
            self.GroundedEnds = [self.GroundedEnds] if self.GroundedEnds is not None else []
        self.GroundedEnds = [v if isinstance(v, TransformerEndInfo) else TransformerEndInfo(**as_dict(v)) for v in self.GroundedEnds]

        super().__post_init__(**kwargs)


class TransmissionControlArea(ControlArea):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TransmissionControlArea"]
    class_class_curie: ClassVar[str] = "cim:TransmissionControlArea"
    class_name: ClassVar[str] = "TransmissionControlArea"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TransmissionControlArea


class UsagePoint(IdentifiedObject):
    """
    Logical or physical point in the network to which readings or events may be attributed. Used at the place where a
    physical or virtual meter may be located; however, it is not required that a meter be present.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["UsagePoint"]
    class_class_curie: ClassVar[str] = "cim:UsagePoint"
    class_name: ClassVar[str] = "UsagePoint"
    class_model_uri: ClassVar[URIRef] = CIMTBL.UsagePoint


class ValueAliasSet(IdentifiedObject):
    """
    Describes the translation of a set of values into a name and is intendend to facilitate custom translations. Each
    ValueAliasSet has a name, description etc. A specific Measurement may represent a discrete state like Open,
    Closed, Intermediate etc. This requires a translation from the MeasurementValue.value number to a string, e.g.
    0-&gt;Invalid, 1-&gt;Open, 2-&gt;Closed, 3-&gt;Intermediate. Each ValueToAlias member in ValueAliasSet.Value
    describe a mapping for one particular value to a name.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ValueAliasSet"]
    class_class_curie: ClassVar[str] = "cim:ValueAliasSet"
    class_name: ClassVar[str] = "ValueAliasSet"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ValueAliasSet


class VariableShuntCompensator(NonlinearShuntCompensator):
    """
    A variable shunt compensator (VSR) is an oil-filled reactor with discrete on-line regulation of reactive power.
    The regulation range typically varies between 30% and 100% of the rated reactive power. When energized VSR cannot
    have a reactive output of 0 Mvar, so minimal valid section number is 1 with reactive power output at either 100%
    or at minimal reactive power output. Note that reactive power can increase or decrease with increasing of the
    section number (NonlinearShuntCompensatorPoint.sectionNumber).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["VariableShuntCompensator"]
    class_class_curie: ClassVar[str] = "cim:VariableShuntCompensator"
    class_name: ClassVar[str] = "VariableShuntCompensator"
    class_model_uri: ClassVar[URIRef] = CIMTBL.VariableShuntCompensator


@dataclass(repr=False)
class VehicleInfo(AssetInfo):
    """
    Type of vehicle needed to perform certain type of work.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["VehicleInfo"]
    class_class_curie: ClassVar[str] = "cim:VehicleInfo"
    class_name: ClassVar[str] = "VehicleInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.VehicleInfo

    make: Optional[str] = None
    model: Optional[str] = None
    vehicleType: Optional[str] = None
    year: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.make is not None and not isinstance(self.make, str):
            self.make = str(self.make)

        if self.model is not None and not isinstance(self.model, str):
            self.model = str(self.model)

        if self.vehicleType is not None and not isinstance(self.vehicleType, str):
            self.vehicleType = str(self.vehicleType)

        if self.year is not None and not isinstance(self.year, str):
            self.year = str(self.year)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ElectricVehicleInfo(VehicleInfo):
    """
    The ElectricVehicleInfo class associates the vehicle with its physical and operational characteristics (make,
    model, year, battery, connectors) and its state of charge (SOC) dynamics.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ElectricVehicleInfo"]
    class_class_curie: ClassVar[str] = "cim:ElectricVehicleInfo"
    class_name: ClassVar[str] = "ElectricVehicleInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ElectricVehicleInfo

    batteryCapacity: Optional[float] = None
    evType: Optional[Union[str, "EVTypeKind"]] = None
    maxChargingRate: Optional[float] = None
    v2gCapable: Optional[Union[bool, Bool]] = None
    BatteryInfo: Optional[Union[dict, BatteryInfo]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.batteryCapacity is not None and not isinstance(self.batteryCapacity, float):
            self.batteryCapacity = float(self.batteryCapacity)

        if self.evType is not None and not isinstance(self.evType, EVTypeKind):
            self.evType = EVTypeKind(self.evType)

        if self.maxChargingRate is not None and not isinstance(self.maxChargingRate, float):
            self.maxChargingRate = float(self.maxChargingRate)

        if self.v2gCapable is not None and not isinstance(self.v2gCapable, Bool):
            self.v2gCapable = Bool(self.v2gCapable)

        if self.BatteryInfo is not None and not isinstance(self.BatteryInfo, BatteryInfo):
            self.BatteryInfo = BatteryInfo(**as_dict(self.BatteryInfo))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class VoltageAngleLimit(OperationalLimit):
    """
    Voltage angle limit between two terminals. The association end OperationalLimitSet.Terminal defines one end and
    the host of the limit. The association end VoltageAngleLimit.AngleReferenceTerminal defines the reference
    terminal.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["VoltageAngleLimit"]
    class_class_curie: ClassVar[str] = "cim:VoltageAngleLimit"
    class_name: ClassVar[str] = "VoltageAngleLimit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.VoltageAngleLimit

    isFlowToRefTerminal: Optional[Union[bool, Bool]] = None
    normalValue: Optional[float] = None
    value: Optional[float] = None
    AngleReferenceTerminal: Optional[Union[dict, Terminal]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.isFlowToRefTerminal is not None and not isinstance(self.isFlowToRefTerminal, Bool):
            self.isFlowToRefTerminal = Bool(self.isFlowToRefTerminal)

        if self.normalValue is not None and not isinstance(self.normalValue, float):
            self.normalValue = float(self.normalValue)

        if self.value is not None and not isinstance(self.value, float):
            self.value = float(self.value)

        if self.AngleReferenceTerminal is not None and not isinstance(self.AngleReferenceTerminal, Terminal):
            self.AngleReferenceTerminal = Terminal(**as_dict(self.AngleReferenceTerminal))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class VoltageControlZone(PowerSystemResource):
    """
    An area of the power system network which is defined for secondary voltage control purposes. A voltage control
    zone consists of a collection of substations with a designated bus bar section whose voltage will be controlled.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["VoltageControlZone"]
    class_class_curie: ClassVar[str] = "cim:VoltageControlZone"
    class_name: ClassVar[str] = "VoltageControlZone"
    class_model_uri: ClassVar[URIRef] = CIMTBL.VoltageControlZone

    BusbarSection: Optional[Union[dict, BusbarSection]] = None
    RegulationSchedule: Optional[Union[dict, RegulationSchedule]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.BusbarSection is not None and not isinstance(self.BusbarSection, BusbarSection):
            self.BusbarSection = BusbarSection(**as_dict(self.BusbarSection))

        if self.RegulationSchedule is not None and not isinstance(self.RegulationSchedule, RegulationSchedule):
            self.RegulationSchedule = RegulationSchedule(**as_dict(self.RegulationSchedule))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class VoltageInjectionControlFunction(IdentifiedObject):
    """
    Voltage injection control function is a function block that calculates the operating point of the controlled
    equipment to achieve the target voltage injection. The controlled point is the Terminal with sequenceNumber =1.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["VoltageInjectionControlFunction"]
    class_class_curie: ClassVar[str] = "cim:VoltageInjectionControlFunction"
    class_name: ClassVar[str] = "VoltageInjectionControlFunction"
    class_model_uri: ClassVar[URIRef] = CIMTBL.VoltageInjectionControlFunction

    targetValue: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.targetValue is not None and not isinstance(self.targetValue, float):
            self.targetValue = float(self.targetValue)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class VoltageLevel(EquipmentContainer):
    """
    A collection of equipment at one common system voltage forming a switchgear. The equipment typically consists of
    breakers, busbars, instrumentation, control, regulation and protection devices as well as assemblies of all these.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["VoltageLevel"]
    class_class_curie: ClassVar[str] = "cim:VoltageLevel"
    class_name: ClassVar[str] = "VoltageLevel"
    class_model_uri: ClassVar[URIRef] = CIMTBL.VoltageLevel

    highVoltageLimit: Optional[float] = None
    lowVoltageLimit: Optional[float] = None
    BaseVoltage: Optional[Union[dict, BaseVoltage]] = None
    Substation: Optional[Union[dict, Substation]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.highVoltageLimit is not None and not isinstance(self.highVoltageLimit, float):
            self.highVoltageLimit = float(self.highVoltageLimit)

        if self.lowVoltageLimit is not None and not isinstance(self.lowVoltageLimit, float):
            self.lowVoltageLimit = float(self.lowVoltageLimit)

        if self.BaseVoltage is not None and not isinstance(self.BaseVoltage, BaseVoltage):
            self.BaseVoltage = BaseVoltage(**as_dict(self.BaseVoltage))

        if self.Substation is not None and not isinstance(self.Substation, Substation):
            self.Substation = Substation(**as_dict(self.Substation))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class VoltageLimit(OperationalLimit):
    """
    Operational limit applied to voltage.The use of operational VoltageLimit is preferred instead of limits defined at
    VoltageLevel. The operational VoltageLimits are used, if present.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["VoltageLimit"]
    class_class_curie: ClassVar[str] = "cim:VoltageLimit"
    class_name: ClassVar[str] = "VoltageLimit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.VoltageLimit

    normalValue: Optional[float] = None
    value: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.normalValue is not None and not isinstance(self.normalValue, float):
            self.normalValue = float(self.normalValue)

        if self.value is not None and not isinstance(self.value, float):
            self.value = float(self.value)

        super().__post_init__(**kwargs)


class WeccREPCC(IdentifiedObject):
    """
    WECC Plant controller model (REPC_C).Reference: WECC REMWG, Proposal for new features for the renewable energy
    system generic models, 2021.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["WeccREPCC"]
    class_class_curie: ClassVar[str] = "cim:WeccREPCC"
    class_name: ClassVar[str] = "WeccREPCC"
    class_model_uri: ClassVar[URIRef] = CIMTBL.WeccREPCC


class WeccWTGIBFFRA(IdentifiedObject):
    """
    WECC WTGIBFFR_A model. Auxiliary control model representing the so-called inertial-based fast-frequency response
    (IBFFR) controls.Reference: WECC REMWG, Proposal for new features for the renewable energy system generic models,
    2021.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["WeccWTGIBFFRA"]
    class_class_curie: ClassVar[str] = "cim:WeccWTGIBFFRA"
    class_name: ClassVar[str] = "WeccWTGIBFFRA"
    class_model_uri: ClassVar[URIRef] = CIMTBL.WeccWTGIBFFRA


@dataclass(repr=False)
class WindGeneratingUnit(GeneratingUnit):
    """
    A wind driven generating unit, connected to the grid by means of a rotating machine. May be used to represent a
    single turbine or an aggregation.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["WindGeneratingUnit"]
    class_class_curie: ClassVar[str] = "cim:WindGeneratingUnit"
    class_name: ClassVar[str] = "WindGeneratingUnit"
    class_model_uri: ClassVar[URIRef] = CIMTBL.WindGeneratingUnit

    windGenUnitType: Optional[Union[str, "WindGenUnitKind"]] = None
    WindPowerPlant: Optional[Union[dict, "WindPowerPlant"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.windGenUnitType is not None and not isinstance(self.windGenUnitType, WindGenUnitKind):
            self.windGenUnitType = WindGenUnitKind(self.windGenUnitType)

        if self.WindPowerPlant is not None and not isinstance(self.WindPowerPlant, WindPowerPlant):
            self.WindPowerPlant = WindPowerPlant(**as_dict(self.WindPowerPlant))

        super().__post_init__(**kwargs)


class WindPlantDynamics(IdentifiedObject):
    """
    Parent class supporting relationships to wind turbines type 3 and type 4 and wind plant IEC and user-defined wind
    plants including their control models.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["WindPlantDynamics"]
    class_class_curie: ClassVar[str] = "cim:WindPlantDynamics"
    class_name: ClassVar[str] = "WindPlantDynamics"
    class_model_uri: ClassVar[URIRef] = CIMTBL.WindPlantDynamics


class WindPowerPlant(PowerSystemResource):
    """
    Wind power plant.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["WindPowerPlant"]
    class_class_curie: ClassVar[str] = "cim:WindPowerPlant"
    class_name: ClassVar[str] = "WindPowerPlant"
    class_model_uri: ClassVar[URIRef] = CIMTBL.WindPowerPlant


class WindTurbineType3or4Dynamics(IdentifiedObject):
    """
    Parent class supporting relationships to wind turbines type 3 and type 4 and wind plant including their control
    models.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["WindTurbineType3or4Dynamics"]
    class_class_curie: ClassVar[str] = "cim:WindTurbineType3or4Dynamics"
    class_name: ClassVar[str] = "WindTurbineType3or4Dynamics"
    class_model_uri: ClassVar[URIRef] = CIMTBL.WindTurbineType3or4Dynamics


class WireAssemblyInfo(AssetInfo):
    """
    Describes the construction of a multi-conductor wire.<-NOTE: period missing.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["WireAssemblyInfo"]
    class_class_curie: ClassVar[str] = "cim:WireAssemblyInfo"
    class_name: ClassVar[str] = "WireAssemblyInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.WireAssemblyInfo


@dataclass(repr=False)
class WireInfo(ConductorInfo):
    """
    Wire data that can be specified per line segment phase, or for the line segment as a whole in case its phases all
    have the same wire characteristics.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["WireInfo"]
    class_class_curie: ClassVar[str] = "cim:WireInfo"
    class_name: ClassVar[str] = "WireInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.WireInfo

    constructionKind: Optional[Union[str, "WireMaterialKind"]] = None
    coreRadius: Optional[float] = None
    coreStrandCount: Optional[int] = None
    coreStrandRadius: Optional[float] = None
    gmr: Optional[float] = None
    insulated: Optional[Union[bool, Bool]] = None
    insulationMaterial: Optional[Union[str, "WireInsulationKind"]] = None
    insulationThickness: Optional[float] = None
    radius: Optional[float] = None
    ratedStrength: Optional[float] = None
    sizeDescription: Optional[str] = None
    strandCount: Optional[int] = None
    strandRadius: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.constructionKind is not None and not isinstance(self.constructionKind, WireMaterialKind):
            self.constructionKind = WireMaterialKind(self.constructionKind)

        if self.coreRadius is not None and not isinstance(self.coreRadius, float):
            self.coreRadius = float(self.coreRadius)

        if self.coreStrandCount is not None and not isinstance(self.coreStrandCount, int):
            self.coreStrandCount = int(self.coreStrandCount)

        if self.coreStrandRadius is not None and not isinstance(self.coreStrandRadius, float):
            self.coreStrandRadius = float(self.coreStrandRadius)

        if self.gmr is not None and not isinstance(self.gmr, float):
            self.gmr = float(self.gmr)

        if self.insulated is not None and not isinstance(self.insulated, Bool):
            self.insulated = Bool(self.insulated)

        if self.insulationMaterial is not None and not isinstance(self.insulationMaterial, WireInsulationKind):
            self.insulationMaterial = WireInsulationKind(self.insulationMaterial)

        if self.insulationThickness is not None and not isinstance(self.insulationThickness, float):
            self.insulationThickness = float(self.insulationThickness)

        if self.radius is not None and not isinstance(self.radius, float):
            self.radius = float(self.radius)

        if self.ratedStrength is not None and not isinstance(self.ratedStrength, float):
            self.ratedStrength = float(self.ratedStrength)

        if self.sizeDescription is not None and not isinstance(self.sizeDescription, str):
            self.sizeDescription = str(self.sizeDescription)

        if self.strandCount is not None and not isinstance(self.strandCount, int):
            self.strandCount = int(self.strandCount)

        if self.strandRadius is not None and not isinstance(self.strandRadius, float):
            self.strandRadius = float(self.strandRadius)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class BareWireInfo(WireInfo):
    """
    Bare wire data.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["BareWireInfo"]
    class_class_curie: ClassVar[str] = "cim:BareWireInfo"
    class_name: ClassVar[str] = "BareWireInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BareWireInfo

    wireConstructionKind: Optional[Union[str, "WireConstructionKind"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.wireConstructionKind is not None and not isinstance(self.wireConstructionKind, WireConstructionKind):
            self.wireConstructionKind = WireConstructionKind(self.wireConstructionKind)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class CableInfo(WireInfo):
    """
    Cable data.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["CableInfo"]
    class_class_curie: ClassVar[str] = "cim:CableInfo"
    class_name: ClassVar[str] = "CableInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.CableInfo

    constructionKind: Optional[Union[str, "CableConstructionKind"]] = None
    diameterOverCore: Optional[float] = None
    diameterOverInsulation: Optional[float] = None
    diameterOverJacket: Optional[float] = None
    diameterOverScreen: Optional[float] = None
    isStrandFill: Optional[Union[bool, Bool]] = None
    nominalTemperature: Optional[float] = None
    outerJacketKind: Optional[Union[str, "CableOuterJacketKind"]] = None
    sheathAsNeutral: Optional[Union[bool, Bool]] = None
    shieldMaterial: Optional[Union[str, "CableShieldMaterialKind"]] = None
    InsulationInfo: Optional[Union[dict, InsulationInfo]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.constructionKind is not None and not isinstance(self.constructionKind, CableConstructionKind):
            self.constructionKind = CableConstructionKind(self.constructionKind)

        if self.diameterOverCore is not None and not isinstance(self.diameterOverCore, float):
            self.diameterOverCore = float(self.diameterOverCore)

        if self.diameterOverInsulation is not None and not isinstance(self.diameterOverInsulation, float):
            self.diameterOverInsulation = float(self.diameterOverInsulation)

        if self.diameterOverJacket is not None and not isinstance(self.diameterOverJacket, float):
            self.diameterOverJacket = float(self.diameterOverJacket)

        if self.diameterOverScreen is not None and not isinstance(self.diameterOverScreen, float):
            self.diameterOverScreen = float(self.diameterOverScreen)

        if self.isStrandFill is not None and not isinstance(self.isStrandFill, Bool):
            self.isStrandFill = Bool(self.isStrandFill)

        if self.nominalTemperature is not None and not isinstance(self.nominalTemperature, float):
            self.nominalTemperature = float(self.nominalTemperature)

        if self.outerJacketKind is not None and not isinstance(self.outerJacketKind, CableOuterJacketKind):
            self.outerJacketKind = CableOuterJacketKind(self.outerJacketKind)

        if self.sheathAsNeutral is not None and not isinstance(self.sheathAsNeutral, Bool):
            self.sheathAsNeutral = Bool(self.sheathAsNeutral)

        if self.shieldMaterial is not None and not isinstance(self.shieldMaterial, CableShieldMaterialKind):
            self.shieldMaterial = CableShieldMaterialKind(self.shieldMaterial)

        if self.InsulationInfo is not None and not isinstance(self.InsulationInfo, InsulationInfo):
            self.InsulationInfo = InsulationInfo(**as_dict(self.InsulationInfo))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ConcentricNeutralCableInfo(CableInfo):
    """
    Concentric neutral cable data.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ConcentricNeutralCableInfo"]
    class_class_curie: ClassVar[str] = "cim:ConcentricNeutralCableInfo"
    class_name: ClassVar[str] = "ConcentricNeutralCableInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConcentricNeutralCableInfo

    diameterOverNeutral: Optional[float] = None
    neutralStrandCount: Optional[int] = None
    neutralStrandGmr: Optional[float] = None
    neutralStrandRadius: Optional[float] = None
    neutralStrandRDC20: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.diameterOverNeutral is not None and not isinstance(self.diameterOverNeutral, float):
            self.diameterOverNeutral = float(self.diameterOverNeutral)

        if self.neutralStrandCount is not None and not isinstance(self.neutralStrandCount, int):
            self.neutralStrandCount = int(self.neutralStrandCount)

        if self.neutralStrandGmr is not None and not isinstance(self.neutralStrandGmr, float):
            self.neutralStrandGmr = float(self.neutralStrandGmr)

        if self.neutralStrandRadius is not None and not isinstance(self.neutralStrandRadius, float):
            self.neutralStrandRadius = float(self.neutralStrandRadius)

        if self.neutralStrandRDC20 is not None and not isinstance(self.neutralStrandRDC20, float):
            self.neutralStrandRDC20 = float(self.neutralStrandRDC20)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OverheadWireInfo(WireInfo):
    """
    Overhead wire data.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["OverheadWireInfo"]
    class_class_curie: ClassVar[str] = "cim:OverheadWireInfo"
    class_name: ClassVar[str] = "OverheadWireInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.OverheadWireInfo

    wireConstructionKind: Optional[Union[str, "WireConstructionKind"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.wireConstructionKind is not None and not isinstance(self.wireConstructionKind, WireConstructionKind):
            self.wireConstructionKind = WireConstructionKind(self.wireConstructionKind)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TapeShieldCableInfo(CableInfo):
    """
    Tape shield cable data.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["TapeShieldCableInfo"]
    class_class_curie: ClassVar[str] = "cim:TapeShieldCableInfo"
    class_name: ClassVar[str] = "TapeShieldCableInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TapeShieldCableInfo

    tapeLap: Optional[float] = None
    tapeThickness: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.tapeLap is not None and not isinstance(self.tapeLap, float):
            self.tapeLap = float(self.tapeLap)

        if self.tapeThickness is not None and not isinstance(self.tapeThickness, float):
            self.tapeThickness = float(self.tapeThickness)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class WirePhaseInfo(YAMLRoot):
    """
    Information on a wire carrying a single phase.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["WirePhaseInfo"]
    class_class_curie: ClassVar[str] = "cim:WirePhaseInfo"
    class_name: ClassVar[str] = "WirePhaseInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.WirePhaseInfo

    phaseInfo: Optional[Union[str, "SinglePhaseKind"]] = None
    WireAssemblyInfo: Optional[Union[dict, WireAssemblyInfo]] = None
    WireInfo: Optional[Union[dict, WireInfo]] = None
    WirePosition: Optional[Union[dict, "WirePosition"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.phaseInfo is not None and not isinstance(self.phaseInfo, SinglePhaseKind):
            self.phaseInfo = SinglePhaseKind(self.phaseInfo)

        if self.WireAssemblyInfo is not None and not isinstance(self.WireAssemblyInfo, WireAssemblyInfo):
            self.WireAssemblyInfo = WireAssemblyInfo(**as_dict(self.WireAssemblyInfo))

        if self.WireInfo is not None and not isinstance(self.WireInfo, WireInfo):
            self.WireInfo = WireInfo(**as_dict(self.WireInfo))

        if self.WirePosition is not None and not isinstance(self.WirePosition, WirePosition):
            self.WirePosition = WirePosition(**as_dict(self.WirePosition))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class WirePosition(IdentifiedObject):
    """
    Identification, spacing and configuration of the wires of a conductor with respect to a structure.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["WirePosition"]
    class_class_curie: ClassVar[str] = "cim:WirePosition"
    class_name: ClassVar[str] = "WirePosition"
    class_model_uri: ClassVar[URIRef] = CIMTBL.WirePosition

    phase: Optional[Union[str, "SinglePhaseKind"]] = None
    sequenceNumber: Optional[int] = None
    xCoord: Optional[float] = None
    yCoord: Optional[float] = None
    WireSpacingInfo: Optional[Union[dict, "WireSpacingInfo"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.phase is not None and not isinstance(self.phase, SinglePhaseKind):
            self.phase = SinglePhaseKind(self.phase)

        if self.sequenceNumber is not None and not isinstance(self.sequenceNumber, int):
            self.sequenceNumber = int(self.sequenceNumber)

        if self.xCoord is not None and not isinstance(self.xCoord, float):
            self.xCoord = float(self.xCoord)

        if self.yCoord is not None and not isinstance(self.yCoord, float):
            self.yCoord = float(self.yCoord)

        if self.WireSpacingInfo is not None and not isinstance(self.WireSpacingInfo, WireSpacingInfo):
            self.WireSpacingInfo = WireSpacingInfo(**as_dict(self.WireSpacingInfo))

        super().__post_init__(**kwargs)


class WireSegment(Conductor):
    """
    A two terminal and power conducting device of negligible impedance and length represented as zero impedance device
    that can be used to connect auxiliary equipment to its terminals.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["WireSegment"]
    class_class_curie: ClassVar[str] = "cim:WireSegment"
    class_name: ClassVar[str] = "WireSegment"
    class_model_uri: ClassVar[URIRef] = CIMTBL.WireSegment


@dataclass(repr=False)
class WireSegmentPhase(PowerSystemResource):
    """
    Represents a single wire of an alternating current wire segment.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["WireSegmentPhase"]
    class_class_curie: ClassVar[str] = "cim:WireSegmentPhase"
    class_name: ClassVar[str] = "WireSegmentPhase"
    class_model_uri: ClassVar[URIRef] = CIMTBL.WireSegmentPhase

    phase: Optional[Union[str, "SinglePhaseKind"]] = None
    sequenceNumber: Optional[int] = None
    WireSegment: Optional[Union[dict, WireSegment]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.phase is not None and not isinstance(self.phase, SinglePhaseKind):
            self.phase = SinglePhaseKind(self.phase)

        if self.sequenceNumber is not None and not isinstance(self.sequenceNumber, int):
            self.sequenceNumber = int(self.sequenceNumber)

        if self.WireSegment is not None and not isinstance(self.WireSegment, WireSegment):
            self.WireSegment = WireSegment(**as_dict(self.WireSegment))

        super().__post_init__(**kwargs)


class WireSpacing(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["WireSpacing"]
    class_class_curie: ClassVar[str] = "cim:WireSpacing"
    class_name: ClassVar[str] = "WireSpacing"
    class_model_uri: ClassVar[URIRef] = CIMTBL.WireSpacing


class ConductorDistanceSpacing(WireSpacing):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["ConductorDistanceSpacing"]
    class_class_curie: ClassVar[str] = "cim:ConductorDistanceSpacing"
    class_name: ClassVar[str] = "ConductorDistanceSpacing"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConductorDistanceSpacing


@dataclass(repr=False)
class EquivalentDistanceSpacing(WireSpacing):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["EquivalentDistanceSpacing"]
    class_class_curie: ClassVar[str] = "cim:EquivalentDistanceSpacing"
    class_name: ClassVar[str] = "EquivalentDistanceSpacing"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EquivalentDistanceSpacing

    averageNeutralHeight: Optional[float] = None
    averagePhaseHeight: Optional[float] = None
    phaseToNeutralGMD: Optional[float] = None
    phaseToPhaseGMD: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.averageNeutralHeight is not None and not isinstance(self.averageNeutralHeight, float):
            self.averageNeutralHeight = float(self.averageNeutralHeight)

        if self.averagePhaseHeight is not None and not isinstance(self.averagePhaseHeight, float):
            self.averagePhaseHeight = float(self.averagePhaseHeight)

        if self.phaseToNeutralGMD is not None and not isinstance(self.phaseToNeutralGMD, float):
            self.phaseToNeutralGMD = float(self.phaseToNeutralGMD)

        if self.phaseToPhaseGMD is not None and not isinstance(self.phaseToPhaseGMD, float):
            self.phaseToPhaseGMD = float(self.phaseToPhaseGMD)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class WireSpacingInfo(AssetInfo):
    """
    Wire spacing data that associates multiple wire positions with the line segment, and allows to calculate line
    segment impedances. Number of phases can be derived from the number of associated wire positions whose phase is
    not neutral.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIM["WireSpacingInfo"]
    class_class_curie: ClassVar[str] = "cim:WireSpacingInfo"
    class_name: ClassVar[str] = "WireSpacingInfo"
    class_model_uri: ClassVar[URIRef] = CIMTBL.WireSpacingInfo

    isCable: Optional[Union[bool, Bool]] = None
    phaseWireCount: Optional[int] = None
    phaseWireSpacing: Optional[float] = None
    usage: Optional[Union[str, "WireUsageKind"]] = None
    DuctBank: Optional[Union[dict, DuctBank]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.isCable is not None and not isinstance(self.isCable, Bool):
            self.isCable = Bool(self.isCable)

        if self.phaseWireCount is not None and not isinstance(self.phaseWireCount, int):
            self.phaseWireCount = int(self.phaseWireCount)

        if self.phaseWireSpacing is not None and not isinstance(self.phaseWireSpacing, float):
            self.phaseWireSpacing = float(self.phaseWireSpacing)

        if self.usage is not None and not isinstance(self.usage, WireUsageKind):
            self.usage = WireUsageKind(self.usage)

        if self.DuctBank is not None and not isinstance(self.DuctBank, DuctBank):
            self.DuctBank = DuctBank(**as_dict(self.DuctBank))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TwoNodeMixin(YAMLRoot):
    """
    Node-breaker two-terminal connectivity (§3.5). Terminal 1/2 -> ConnectivityNode.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["TwoNodeMixin"]
    class_class_curie: ClassVar[str] = "cimtbl:TwoNodeMixin"
    class_name: ClassVar[str] = "TwoNodeMixin"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TwoNodeMixin

    node1: Optional[str] = None
    node2: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.node1 is not None and not isinstance(self.node1, str):
            self.node1 = str(self.node1)

        if self.node2 is not None and not isinstance(self.node2, str):
            self.node2 = str(self.node2)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TwoBusMixin(YAMLRoot):
    """
    Bus-branch two-terminal connectivity (§3.5). Terminal 1/2 -> TopologicalNode. Alternate header shape to
    TwoNodeMixin for the same class (§3.4) - never both on the same row.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["TwoBusMixin"]
    class_class_curie: ClassVar[str] = "cimtbl:TwoBusMixin"
    class_name: ClassVar[str] = "TwoBusMixin"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TwoBusMixin

    bus1: Optional[str] = None
    bus2: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.bus1 is not None and not isinstance(self.bus1, str):
            self.bus1 = str(self.bus1)

        if self.bus2 is not None and not isinstance(self.bus2, str):
            self.bus2 = str(self.bus2)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OneNodeMixin(YAMLRoot):
    """
    Node-breaker single-terminal connectivity (§3.5). Terminal -> ConnectivityNode.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["OneNodeMixin"]
    class_class_curie: ClassVar[str] = "cimtbl:OneNodeMixin"
    class_name: ClassVar[str] = "OneNodeMixin"
    class_model_uri: ClassVar[URIRef] = CIMTBL.OneNodeMixin

    node: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.node is not None and not isinstance(self.node, str):
            self.node = str(self.node)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PhasesMixin(YAMLRoot):
    """
    Compound phase string (e.g. "ABCN", "BC") driving per-phase child synthesis (§3.6). Not a CIM SinglePhaseKind -
    split into individual phase values by the connectivity backend (Phase 4), not this schema.
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["PhasesMixin"]
    class_class_curie: ClassVar[str] = "cimtbl:PhasesMixin"
    class_name: ClassVar[str] = "PhasesMixin"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhasesMixin

    phases: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.phases is not None and not isinstance(self.phases, str):
            self.phases = str(self.phases)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TemplateRefMixin(YAMLRoot):
    """
    By-association template reference (§3.7), e.g. PowerTransformer.Template -> TransformerAssembly, matched on
    endNumber. Plain FK-by-name string; resolution is Phase 4/5, not this schema (§12.2).
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["TemplateRefMixin"]
    class_class_curie: ClassVar[str] = "cimtbl:TemplateRefMixin"
    class_name: ClassVar[str] = "TemplateRefMixin"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TemplateRefMixin

    Template: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.Template is not None and not isinstance(self.Template, str):
            self.Template = str(self.Template)

        super().__post_init__(**kwargs)


class BaseVoltageRow(BaseVoltage):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["BaseVoltageRow"]
    class_class_curie: ClassVar[str] = "cimtbl:BaseVoltageRow"
    class_name: ClassVar[str] = "BaseVoltageRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BaseVoltageRow


class BaseFrequencyRow(BaseFrequency):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["BaseFrequencyRow"]
    class_class_curie: ClassVar[str] = "cimtbl:BaseFrequencyRow"
    class_name: ClassVar[str] = "BaseFrequencyRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BaseFrequencyRow


class BasePowerRow(BasePower):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["BasePowerRow"]
    class_class_curie: ClassVar[str] = "cimtbl:BasePowerRow"
    class_name: ClassVar[str] = "BasePowerRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BasePowerRow


class EnergySourceRow(EnergySource):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["EnergySourceRow"]
    class_class_curie: ClassVar[str] = "cimtbl:EnergySourceRow"
    class_name: ClassVar[str] = "EnergySourceRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EnergySourceRow


class LoadResponseCharacteristicRow(LoadResponseCharacteristic):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["LoadResponseCharacteristicRow"]
    class_class_curie: ClassVar[str] = "cimtbl:LoadResponseCharacteristicRow"
    class_name: ClassVar[str] = "LoadResponseCharacteristicRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.LoadResponseCharacteristicRow


class PerLengthPhaseImpedanceRow(PerLengthPhaseImpedance):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["PerLengthPhaseImpedanceRow"]
    class_class_curie: ClassVar[str] = "cimtbl:PerLengthPhaseImpedanceRow"
    class_name: ClassVar[str] = "PerLengthPhaseImpedanceRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PerLengthPhaseImpedanceRow


class PhaseImpedanceDataRow(PhaseImpedanceData):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["PhaseImpedanceDataRow"]
    class_class_curie: ClassVar[str] = "cimtbl:PhaseImpedanceDataRow"
    class_name: ClassVar[str] = "PhaseImpedanceDataRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhaseImpedanceDataRow


class ConductorDistanceSpacingRow(ConductorDistanceSpacing):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["ConductorDistanceSpacingRow"]
    class_class_curie: ClassVar[str] = "cimtbl:ConductorDistanceSpacingRow"
    class_name: ClassVar[str] = "ConductorDistanceSpacingRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConductorDistanceSpacingRow


class ConductorDistanceRow(ConductorDistance):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["ConductorDistanceRow"]
    class_class_curie: ClassVar[str] = "cimtbl:ConductorDistanceRow"
    class_name: ClassVar[str] = "ConductorDistanceRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ConductorDistanceRow


@dataclass(repr=False)
class ACLineSegmentRow(ACLineSegment):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["ACLineSegmentRow"]
    class_class_curie: ClassVar[str] = "cimtbl:ACLineSegmentRow"
    class_name: ClassVar[str] = "ACLineSegmentRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.ACLineSegmentRow

    node1: Optional[str] = None
    node2: Optional[str] = None
    bus1: Optional[str] = None
    bus2: Optional[str] = None
    phases: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.node1 is not None and not isinstance(self.node1, str):
            self.node1 = str(self.node1)

        if self.node2 is not None and not isinstance(self.node2, str):
            self.node2 = str(self.node2)

        if self.bus1 is not None and not isinstance(self.bus1, str):
            self.bus1 = str(self.bus1)

        if self.bus2 is not None and not isinstance(self.bus2, str):
            self.bus2 = str(self.bus2)

        if self.phases is not None and not isinstance(self.phases, str):
            self.phases = str(self.phases)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EnergyConsumerRow(EnergyConsumer):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["EnergyConsumerRow"]
    class_class_curie: ClassVar[str] = "cimtbl:EnergyConsumerRow"
    class_name: ClassVar[str] = "EnergyConsumerRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EnergyConsumerRow

    node: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.node is not None and not isinstance(self.node, str):
            self.node = str(self.node)

        super().__post_init__(**kwargs)


class EnergyConsumerPhaseRow(EnergyConsumerPhase):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["EnergyConsumerPhaseRow"]
    class_class_curie: ClassVar[str] = "cimtbl:EnergyConsumerPhaseRow"
    class_name: ClassVar[str] = "EnergyConsumerPhaseRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.EnergyConsumerPhaseRow


@dataclass(repr=False)
class LinearShuntCompensatorRow(LinearShuntCompensator):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["LinearShuntCompensatorRow"]
    class_class_curie: ClassVar[str] = "cimtbl:LinearShuntCompensatorRow"
    class_name: ClassVar[str] = "LinearShuntCompensatorRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.LinearShuntCompensatorRow

    node: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.node is not None and not isinstance(self.node, str):
            self.node = str(self.node)

        super().__post_init__(**kwargs)


class LinearShuntCompensatorPhaseRow(LinearShuntCompensatorPhase):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["LinearShuntCompensatorPhaseRow"]
    class_class_curie: ClassVar[str] = "cimtbl:LinearShuntCompensatorPhaseRow"
    class_name: ClassVar[str] = "LinearShuntCompensatorPhaseRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.LinearShuntCompensatorPhaseRow


@dataclass(repr=False)
class LoadBreakSwitchRow(LoadBreakSwitch):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["LoadBreakSwitchRow"]
    class_class_curie: ClassVar[str] = "cimtbl:LoadBreakSwitchRow"
    class_name: ClassVar[str] = "LoadBreakSwitchRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.LoadBreakSwitchRow

    node1: Optional[str] = None
    node2: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.node1 is not None and not isinstance(self.node1, str):
            self.node1 = str(self.node1)

        if self.node2 is not None and not isinstance(self.node2, str):
            self.node2 = str(self.node2)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FuseRow(Fuse):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["FuseRow"]
    class_class_curie: ClassVar[str] = "cimtbl:FuseRow"
    class_name: ClassVar[str] = "FuseRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.FuseRow

    node1: Optional[str] = None
    node2: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.node1 is not None and not isinstance(self.node1, str):
            self.node1 = str(self.node1)

        if self.node2 is not None and not isinstance(self.node2, str):
            self.node2 = str(self.node2)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class SectionaliserRow(Sectionaliser):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["SectionaliserRow"]
    class_class_curie: ClassVar[str] = "cimtbl:SectionaliserRow"
    class_name: ClassVar[str] = "SectionaliserRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SectionaliserRow

    node1: Optional[str] = None
    node2: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.node1 is not None and not isinstance(self.node1, str):
            self.node1 = str(self.node1)

        if self.node2 is not None and not isinstance(self.node2, str):
            self.node2 = str(self.node2)

        super().__post_init__(**kwargs)


class SwitchPhaseRow(SwitchPhase):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["SwitchPhaseRow"]
    class_class_curie: ClassVar[str] = "cimtbl:SwitchPhaseRow"
    class_name: ClassVar[str] = "SwitchPhaseRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.SwitchPhaseRow


@dataclass(repr=False)
class PowerElectronicsConnectionRow(PowerElectronicsConnection):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["PowerElectronicsConnectionRow"]
    class_class_curie: ClassVar[str] = "cimtbl:PowerElectronicsConnectionRow"
    class_name: ClassVar[str] = "PowerElectronicsConnectionRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerElectronicsConnectionRow

    node: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.node is not None and not isinstance(self.node, str):
            self.node = str(self.node)

        super().__post_init__(**kwargs)


class PhotoVoltaicUnitRow(PhotoVoltaicUnit):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["PhotoVoltaicUnitRow"]
    class_class_curie: ClassVar[str] = "cimtbl:PhotoVoltaicUnitRow"
    class_name: ClassVar[str] = "PhotoVoltaicUnitRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PhotoVoltaicUnitRow


class BatteryUnitRow(BatteryUnit):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["BatteryUnitRow"]
    class_class_curie: ClassVar[str] = "cimtbl:BatteryUnitRow"
    class_name: ClassVar[str] = "BatteryUnitRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.BatteryUnitRow


@dataclass(repr=False)
class PowerTransformerRow(PowerTransformer):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["PowerTransformerRow"]
    class_class_curie: ClassVar[str] = "cimtbl:PowerTransformerRow"
    class_name: ClassVar[str] = "PowerTransformerRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerTransformerRow

    Template: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.Template is not None and not isinstance(self.Template, str):
            self.Template = str(self.Template)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class PowerTransformerEndRow(PowerTransformerEnd):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["PowerTransformerEndRow"]
    class_class_curie: ClassVar[str] = "cimtbl:PowerTransformerEndRow"
    class_name: ClassVar[str] = "PowerTransformerEndRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.PowerTransformerEndRow

    node: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.node is not None and not isinstance(self.node, str):
            self.node = str(self.node)

        super().__post_init__(**kwargs)


class TransformerTankRow(TransformerTank):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["TransformerTankRow"]
    class_class_curie: ClassVar[str] = "cimtbl:TransformerTankRow"
    class_name: ClassVar[str] = "TransformerTankRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TransformerTankRow


class TransformerTankEndRow(TransformerTankEnd):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = CIMTBL["TransformerTankEndRow"]
    class_class_curie: ClassVar[str] = "cimtbl:TransformerTankEndRow"
    class_name: ClassVar[str] = "TransformerTankEndRow"
    class_model_uri: ClassVar[URIRef] = CIMTBL.TransformerTankEndRow


# Enumerations
class AssetKind(EnumDefinitionImpl):
    """
    Kinds of assets or asset components.
    """
    breakerAirBlastBreaker = PermissibleValue(
        text="breakerAirBlastBreaker",
        description="Air blast circuit breaker.",
        meaning=CIM["AssetKind.breakerAirBlastBreaker"])
    breakerBulkOilBreaker = PermissibleValue(
        text="breakerBulkOilBreaker",
        description="Bulk oil circuit breaker.",
        meaning=CIM["AssetKind.breakerBulkOilBreaker"])
    breakerInsulatingStackAssembly = PermissibleValue(
        text="breakerInsulatingStackAssembly",
        description="Breaker insulating stack assembly (for live tank breaker).",
        meaning=CIM["AssetKind.breakerInsulatingStackAssembly"])
    breakerMinimumOilBreaker = PermissibleValue(
        text="breakerMinimumOilBreaker",
        description="Minimum oil circuit breaker.",
        meaning=CIM["AssetKind.breakerMinimumOilBreaker"])
    breakerSF6DeadTankBreaker = PermissibleValue(
        text="breakerSF6DeadTankBreaker",
        description="SF6 dead tank breaker.",
        meaning=CIM["AssetKind.breakerSF6DeadTankBreaker"])
    breakerSF6LiveTankBreaker = PermissibleValue(
        text="breakerSF6LiveTankBreaker",
        description="SF6 live tank breaker.",
        meaning=CIM["AssetKind.breakerSF6LiveTankBreaker"])
    breakerTankAssembly = PermissibleValue(
        text="breakerTankAssembly",
        description="Breaker tank assembly.",
        meaning=CIM["AssetKind.breakerTankAssembly"])
    other = PermissibleValue(
        text="other",
        description="Other type of Asset. The type attribute may provide more details in this case.",
        meaning=CIM["AssetKind.other"])
    transformer = PermissibleValue(
        text="transformer",
        description="Transformer.",
        meaning=CIM["AssetKind.transformer"])
    transformerTank = PermissibleValue(
        text="transformerTank",
        description="Transformer tank.",
        meaning=CIM["AssetKind.transformerTank"])

    _defn = EnumDefinition(
        name="AssetKind",
        description="Kinds of assets or asset components.",
    )

class AsynchronousMachineKind(EnumDefinitionImpl):
    """
    Kind of Asynchronous Machine.
    """
    generator = PermissibleValue(
        text="generator",
        description="The Asynchronous Machine is a generator.",
        meaning=CIM["AsynchronousMachineKind.generator"])
    motor = PermissibleValue(
        text="motor",
        description="The Asynchronous Machine is a motor.",
        meaning=CIM["AsynchronousMachineKind.motor"])

    _defn = EnumDefinition(
        name="AsynchronousMachineKind",
        description="Kind of Asynchronous Machine.",
    )

class AuthorityKind(EnumDefinitionImpl):

    coordinated = PermissibleValue(
        text="coordinated",
        meaning=CIM["AuthorityKind.coordinated"])
    delegated = PermissibleValue(
        text="delegated",
        meaning=CIM["AuthorityKind.delegated"])
    emergency = PermissibleValue(
        text="emergency",
        meaning=CIM["AuthorityKind.emergency"])
    shared = PermissibleValue(
        text="shared",
        meaning=CIM["AuthorityKind.shared"])
    sole = PermissibleValue(
        text="sole",
        meaning=CIM["AuthorityKind.sole"])

    _defn = EnumDefinition(
        name="AuthorityKind",
    )

class BatteryStateKind(EnumDefinitionImpl):
    """
    The state of the battery unit.
    """
    charging = PermissibleValue(
        text="charging",
        description="Stored energy is increasing.",
        meaning=CIM["BatteryStateKind.charging"])
    discharging = PermissibleValue(
        text="discharging",
        description="Stored energy is decreasing.",
        meaning=CIM["BatteryStateKind.discharging"])
    empty = PermissibleValue(
        text="empty",
        description="Unable to discharge, and not charging.",
        meaning=CIM["BatteryStateKind.empty"])
    full = PermissibleValue(
        text="full",
        description="Unable to charge, and not discharging.",
        meaning=CIM["BatteryStateKind.full"])
    waiting = PermissibleValue(
        text="waiting",
        description="Neither charging nor discharging, but able to do so.",
        meaning=CIM["BatteryStateKind.waiting"])

    _defn = EnumDefinition(
        name="BatteryStateKind",
        description="The state of the battery unit.",
    )

class BatteryTypeKind(EnumDefinitionImpl):

    leadAcid = PermissibleValue(
        text="leadAcid",
        meaning=CIM["BatteryTypeKind.leadAcid"])
    lithiumIon = PermissibleValue(
        text="lithiumIon",
        meaning=CIM["BatteryTypeKind.lithiumIon"])
    lithiumIronPhosphate = PermissibleValue(
        text="lithiumIronPhosphate",
        meaning=CIM["BatteryTypeKind.lithiumIronPhosphate"])
    nickelMetalHydride = PermissibleValue(
        text="nickelMetalHydride",
        meaning=CIM["BatteryTypeKind.nickelMetalHydride"])
    other = PermissibleValue(
        text="other",
        meaning=CIM["BatteryTypeKind.other"])
    sodiumIon = PermissibleValue(
        text="sodiumIon",
        meaning=CIM["BatteryTypeKind.sodiumIon"])
    solidState = PermissibleValue(
        text="solidState",
        meaning=CIM["BatteryTypeKind.solidState"])

    _defn = EnumDefinition(
        name="BatteryTypeKind",
    )

class BreakerConfiguration(EnumDefinitionImpl):
    """
    Switching arrangement for bay.
    """
    breakerAndAHalf = PermissibleValue(
        text="breakerAndAHalf",
        description="Breaker and a half.",
        meaning=CIM["BreakerConfiguration.breakerAndAHalf"])
    doubleBreaker = PermissibleValue(
        text="doubleBreaker",
        description="Double breaker.",
        meaning=CIM["BreakerConfiguration.doubleBreaker"])
    noBreaker = PermissibleValue(
        text="noBreaker",
        description="No breaker.",
        meaning=CIM["BreakerConfiguration.noBreaker"])
    singleBreaker = PermissibleValue(
        text="singleBreaker",
        description="Single breaker.",
        meaning=CIM["BreakerConfiguration.singleBreaker"])

    _defn = EnumDefinition(
        name="BreakerConfiguration",
        description="Switching arrangement for bay.",
    )

class BusbarConfiguration(EnumDefinitionImpl):
    """
    Busbar layout for bay.
    """
    doubleBus = PermissibleValue(
        text="doubleBus",
        description="Double bus.",
        meaning=CIM["BusbarConfiguration.doubleBus"])
    mainWithTransfer = PermissibleValue(
        text="mainWithTransfer",
        description="Main bus with transfer bus.",
        meaning=CIM["BusbarConfiguration.mainWithTransfer"])
    ringBus = PermissibleValue(
        text="ringBus",
        description="Ring bus.",
        meaning=CIM["BusbarConfiguration.ringBus"])
    singleBus = PermissibleValue(
        text="singleBus",
        description="Single bus.",
        meaning=CIM["BusbarConfiguration.singleBus"])

    _defn = EnumDefinition(
        name="BusbarConfiguration",
        description="Busbar layout for bay.",
    )

class CableConstructionKind(EnumDefinitionImpl):
    """
    Kind of cable construction.
    """
    compacted = PermissibleValue(
        text="compacted",
        description="Compacted cable.",
        meaning=CIM["CableConstructionKind.compacted"])
    compressed = PermissibleValue(
        text="compressed",
        description="Compressed cable.",
        meaning=CIM["CableConstructionKind.compressed"])
    other = PermissibleValue(
        text="other",
        description="Other kind of cable construction.",
        meaning=CIM["CableConstructionKind.other"])
    sector = PermissibleValue(
        text="sector",
        description="Sector cable.",
        meaning=CIM["CableConstructionKind.sector"])
    segmental = PermissibleValue(
        text="segmental",
        description="Segmental cable.",
        meaning=CIM["CableConstructionKind.segmental"])
    solid = PermissibleValue(
        text="solid",
        description="Solid cable.",
        meaning=CIM["CableConstructionKind.solid"])
    stranded = PermissibleValue(
        text="stranded",
        description="Stranded cable.",
        meaning=CIM["CableConstructionKind.stranded"])

    _defn = EnumDefinition(
        name="CableConstructionKind",
        description="Kind of cable construction.",
    )

class CableOuterJacketKind(EnumDefinitionImpl):
    """
    Kind of cable outer jacket.
    """
    insulating = PermissibleValue(
        text="insulating",
        description="Insulating cable outer jacket.",
        meaning=CIM["CableOuterJacketKind.insulating"])
    linearLowDensityPolyethylene = PermissibleValue(
        text="linearLowDensityPolyethylene",
        description="Linear low density polyethylene cable outer jacket.",
        meaning=CIM["CableOuterJacketKind.linearLowDensityPolyethylene"])
    none = PermissibleValue(
        text="none",
        description="Cable has no outer jacket.",
        meaning=CIM["CableOuterJacketKind.none"])
    other = PermissibleValue(
        text="other",
        description="Pther kind of cable outer jacket.",
        meaning=CIM["CableOuterJacketKind.other"])
    polyethylene = PermissibleValue(
        text="polyethylene",
        description="Polyethylene cable outer jacket.",
        meaning=CIM["CableOuterJacketKind.polyethylene"])
    pvc = PermissibleValue(
        text="pvc",
        description="PVC cable outer jacket.",
        meaning=CIM["CableOuterJacketKind.pvc"])
    semiconducting = PermissibleValue(
        text="semiconducting",
        description="Semiconducting cable outer jacket.",
        meaning=CIM["CableOuterJacketKind.semiconducting"])

    _defn = EnumDefinition(
        name="CableOuterJacketKind",
        description="Kind of cable outer jacket.",
    )

class CableShieldMaterialKind(EnumDefinitionImpl):
    """
    Kind of cable shield material.
    """
    aluminum = PermissibleValue(
        text="aluminum",
        description="Aluminum cable shield.",
        meaning=CIM["CableShieldMaterialKind.aluminum"])
    copper = PermissibleValue(
        text="copper",
        description="Copper cable shield.",
        meaning=CIM["CableShieldMaterialKind.copper"])
    lead = PermissibleValue(
        text="lead",
        description="Lead cable shield.",
        meaning=CIM["CableShieldMaterialKind.lead"])
    other = PermissibleValue(
        text="other",
        description="Other kind of cable shield material.",
        meaning=CIM["CableShieldMaterialKind.other"])
    steel = PermissibleValue(
        text="steel",
        description="Steel cable shield.",
        meaning=CIM["CableShieldMaterialKind.steel"])

    _defn = EnumDefinition(
        name="CableShieldMaterialKind",
        description="Kind of cable shield material.",
    )

class ChargingModeKind(EnumDefinitionImpl):

    acLevel1 = PermissibleValue(
        text="acLevel1",
        meaning=CIM["ChargingModeKind.acLevel1"])
    acLevel2 = PermissibleValue(
        text="acLevel2",
        meaning=CIM["ChargingModeKind.acLevel2"])
    acLevel3 = PermissibleValue(
        text="acLevel3",
        meaning=CIM["ChargingModeKind.acLevel3"])
    batterySwap = PermissibleValue(
        text="batterySwap",
        meaning=CIM["ChargingModeKind.batterySwap"])
    dcFast = PermissibleValue(
        text="dcFast",
        meaning=CIM["ChargingModeKind.dcFast"])
    wireless = PermissibleValue(
        text="wireless",
        meaning=CIM["ChargingModeKind.wireless"])

    _defn = EnumDefinition(
        name="ChargingModeKind",
    )

class CommunicationMediumKind(EnumDefinitionImpl):

    cellular2G = PermissibleValue(
        text="cellular2G",
        meaning=CIM["CommunicationMediumKind.cellular2G"])
    cellular3G = PermissibleValue(
        text="cellular3G",
        meaning=CIM["CommunicationMediumKind.cellular3G"])
    cellular5G = PermissibleValue(
        text="cellular5G",
        meaning=CIM["CommunicationMediumKind.cellular5G"])
    cellularLTE = PermissibleValue(
        text="cellularLTE",
        meaning=CIM["CommunicationMediumKind.cellularLTE"])
    fiber = PermissibleValue(
        text="fiber",
        meaning=CIM["CommunicationMediumKind.fiber"])
    microwave = PermissibleValue(
        text="microwave",
        meaning=CIM["CommunicationMediumKind.microwave"])
    radio = PermissibleValue(
        text="radio",
        meaning=CIM["CommunicationMediumKind.radio"])

    _defn = EnumDefinition(
        name="CommunicationMediumKind",
    )

class CommunicationProtocolKind(EnumDefinitionImpl):

    dnp3 = PermissibleValue(
        text="dnp3",
        meaning=CIM["CommunicationProtocolKind.dnp3"])
    iccp = PermissibleValue(
        text="iccp",
        meaning=CIM["CommunicationProtocolKind.iccp"])
    iec61850 = PermissibleValue(
        text="iec61850",
        meaning=CIM["CommunicationProtocolKind.iec61850"])
    ieee2030_5 = PermissibleValue(
        text="ieee2030_5",
        meaning=CIM["CommunicationProtocolKind.ieee2030_5"])
    ieee2664 = PermissibleValue(
        text="ieee2664",
        meaning=CIM["CommunicationProtocolKind.ieee2664"])
    ieeeC37_118 = PermissibleValue(
        text="ieeeC37_118",
        meaning=CIM["CommunicationProtocolKind.ieeeC37_118"])
    modbus = PermissibleValue(
        text="modbus",
        meaning=CIM["CommunicationProtocolKind.modbus"])
    sunspecModbus = PermissibleValue(
        text="sunspecModbus",
        meaning=CIM["CommunicationProtocolKind.sunspecModbus"])

    _defn = EnumDefinition(
        name="CommunicationProtocolKind",
    )

class ConnectivityAreaKind(EnumDefinitionImpl):

    distributionArea = PermissibleValue(
        text="distributionArea",
        description="""A topologically continuous grouping of distribution feeders, typically divided by normal-open switches. The DistributionArea provides the highest-level description of the equipment controlled by the Distribution System Operator (DSO)""",
        meaning=CIM["ConnectivityAreaKind.distributionArea"])
    feederArea = PermissibleValue(
        text="feederArea",
        description="""The FeederArea contains all medium voltage equipment not contained in a SwitchArea or Substation / Bay. It also includes all Sectionalisers, Reclosers, and all other poletop and pad-mounted switchgear that form the boundary of a SwitchArea. It also includes all equipment between the feeder head terminal and the first switching device if the substation breaker is not included in Feeder EquipmentContainer""",
        meaning=CIM["ConnectivityAreaKind.feederArea"])
    microgrid = PermissibleValue(
        text="microgrid",
        description="""Containment of distribution equipment that 1) has clearly-defined electrical boundaries formed by one or more point of common coupling Switch objects and 2) that acts as a single controllable entity which can be operated in grid-connected or islanded mode. This covers both utility-owned distribution microgrids and customer-owned facility microgrids as defined in IEV 617-04-22.""",
        meaning=CIM["ConnectivityAreaKind.microgrid"])
    secondaryArea = PermissibleValue(
        text="secondaryArea",
        description="""Containment of low-voltage distribution Equipment and customer-owned Equipment with clearly defined electrical boundaries formed by the low-side terminal(s) of one or more PowerTransformer objects.""",
        meaning=CIM["ConnectivityAreaKind.secondaryArea"])
    switchArea = PermissibleValue(
        text="switchArea",
        description="""Containment of medium-voltage distribution Equipment with clearly defined electrical boundaries formed by one or more Switch objects. The SwitchArea contains all conductors, fuses, poletop equipment, and vault equipment. It also contains all secondary service transformers not contained in a SecondarySubstation.""",
        meaning=CIM["ConnectivityAreaKind.switchArea"])
    transmissionArea = PermissibleValue(
        text="transmissionArea",
        description="""The connectivity-based grouping of equipment forming a transmission system operator's area of responsibility""",
        meaning=CIM["ConnectivityAreaKind.transmissionArea"])

    _defn = EnumDefinition(
        name="ConnectivityAreaKind",
    )

class ControlAreaTypeKind(EnumDefinitionImpl):
    """
    The type of control area.
    """
    AGC = PermissibleValue(
        text="AGC",
        description="Used for automatic generation control.",
        meaning=CIM["ControlAreaTypeKind.AGC"])
    Forecast = PermissibleValue(
        text="Forecast",
        description="Used for load forecast.",
        meaning=CIM["ControlAreaTypeKind.Forecast"])
    Interchange = PermissibleValue(
        text="Interchange",
        description="Used for interchange specification or control.",
        meaning=CIM["ControlAreaTypeKind.Interchange"])

    _defn = EnumDefinition(
        name="ControlAreaTypeKind",
        description="The type of control area.",
    )

class CoolantType(EnumDefinitionImpl):
    """
    Method of cooling a machine.
    """
    air = PermissibleValue(
        text="air",
        description="Air.",
        meaning=CIM["CoolantType.air"])
    hydrogenGas = PermissibleValue(
        text="hydrogenGas",
        description="Hydrogen gas.",
        meaning=CIM["CoolantType.hydrogenGas"])
    water = PermissibleValue(
        text="water",
        description="Water.",
        meaning=CIM["CoolantType.water"])

    _defn = EnumDefinition(
        name="CoolantType",
        description="Method of cooling a machine.",
    )

class Currency(EnumDefinitionImpl):
    """
    Monetary currencies.  ISO 4217 standard including 3-character currency code.
    """
    AED = PermissibleValue(
        text="AED",
        description="United Arab Emirates dirham.",
        meaning=CIM["Currency.AED"])
    AFN = PermissibleValue(
        text="AFN",
        description="Afghan afghani.",
        meaning=CIM["Currency.AFN"])
    ALL = PermissibleValue(
        text="ALL",
        description="Albanian lek.",
        meaning=CIM["Currency.ALL"])
    AMD = PermissibleValue(
        text="AMD",
        description="Armenian dram.",
        meaning=CIM["Currency.AMD"])
    ANG = PermissibleValue(
        text="ANG",
        description="Netherlands Antillean guilder.",
        meaning=CIM["Currency.ANG"])
    AOA = PermissibleValue(
        text="AOA",
        description="Angolan kwanza.",
        meaning=CIM["Currency.AOA"])
    ARS = PermissibleValue(
        text="ARS",
        description="Argentine peso.",
        meaning=CIM["Currency.ARS"])
    AUD = PermissibleValue(
        text="AUD",
        description="Australian dollar.",
        meaning=CIM["Currency.AUD"])
    AWG = PermissibleValue(
        text="AWG",
        description="Aruban florin.",
        meaning=CIM["Currency.AWG"])
    AZN = PermissibleValue(
        text="AZN",
        description="Azerbaijani manat.",
        meaning=CIM["Currency.AZN"])
    BAM = PermissibleValue(
        text="BAM",
        description="Bosnia and Herzegovina convertible mark.",
        meaning=CIM["Currency.BAM"])
    BBD = PermissibleValue(
        text="BBD",
        description="Barbados dollar.",
        meaning=CIM["Currency.BBD"])
    BDT = PermissibleValue(
        text="BDT",
        description="Bangladeshi taka.",
        meaning=CIM["Currency.BDT"])
    BGN = PermissibleValue(
        text="BGN",
        description="Bulgarian lev.",
        meaning=CIM["Currency.BGN"])
    BHD = PermissibleValue(
        text="BHD",
        description="Bahraini dinar.",
        meaning=CIM["Currency.BHD"])
    BIF = PermissibleValue(
        text="BIF",
        description="Burundian franc.",
        meaning=CIM["Currency.BIF"])
    BMD = PermissibleValue(
        text="BMD",
        description="Bermudian dollar (customarily known as Bermuda dollar).",
        meaning=CIM["Currency.BMD"])
    BND = PermissibleValue(
        text="BND",
        description="Brunei dollar.",
        meaning=CIM["Currency.BND"])
    BOB = PermissibleValue(
        text="BOB",
        description="Boliviano.",
        meaning=CIM["Currency.BOB"])
    BOV = PermissibleValue(
        text="BOV",
        description="Bolivian Mvdol (funds code).",
        meaning=CIM["Currency.BOV"])
    BRL = PermissibleValue(
        text="BRL",
        description="Brazilian real.",
        meaning=CIM["Currency.BRL"])
    BSD = PermissibleValue(
        text="BSD",
        description="Bahamian dollar.",
        meaning=CIM["Currency.BSD"])
    BTN = PermissibleValue(
        text="BTN",
        description="Bhutanese ngultrum.",
        meaning=CIM["Currency.BTN"])
    BWP = PermissibleValue(
        text="BWP",
        description="Botswana pula.",
        meaning=CIM["Currency.BWP"])
    BYR = PermissibleValue(
        text="BYR",
        description="Belarusian ruble.",
        meaning=CIM["Currency.BYR"])
    BZD = PermissibleValue(
        text="BZD",
        description="Belize dollar.",
        meaning=CIM["Currency.BZD"])
    CAD = PermissibleValue(
        text="CAD",
        description="Canadian dollar.",
        meaning=CIM["Currency.CAD"])
    CDF = PermissibleValue(
        text="CDF",
        description="Congolese franc.",
        meaning=CIM["Currency.CDF"])
    CHF = PermissibleValue(
        text="CHF",
        description="Swiss franc.",
        meaning=CIM["Currency.CHF"])
    CLF = PermissibleValue(
        text="CLF",
        description="Unidad de Fomento (funds code), Chile.",
        meaning=CIM["Currency.CLF"])
    CLP = PermissibleValue(
        text="CLP",
        description="Chilean peso.",
        meaning=CIM["Currency.CLP"])
    CNY = PermissibleValue(
        text="CNY",
        description="Chinese yuan.",
        meaning=CIM["Currency.CNY"])
    COP = PermissibleValue(
        text="COP",
        description="Colombian peso.",
        meaning=CIM["Currency.COP"])
    COU = PermissibleValue(
        text="COU",
        description="Unidad de Valor Real.",
        meaning=CIM["Currency.COU"])
    CRC = PermissibleValue(
        text="CRC",
        description="Costa Rican colon.",
        meaning=CIM["Currency.CRC"])
    CUC = PermissibleValue(
        text="CUC",
        description="Cuban convertible peso.",
        meaning=CIM["Currency.CUC"])
    CUP = PermissibleValue(
        text="CUP",
        description="Cuban peso.",
        meaning=CIM["Currency.CUP"])
    CVE = PermissibleValue(
        text="CVE",
        description="Cape Verde escudo.",
        meaning=CIM["Currency.CVE"])
    CZK = PermissibleValue(
        text="CZK",
        description="Czech koruna.",
        meaning=CIM["Currency.CZK"])
    DJF = PermissibleValue(
        text="DJF",
        description="Djiboutian franc.",
        meaning=CIM["Currency.DJF"])
    DKK = PermissibleValue(
        text="DKK",
        description="Danish krone.",
        meaning=CIM["Currency.DKK"])
    DOP = PermissibleValue(
        text="DOP",
        description="Dominican peso.",
        meaning=CIM["Currency.DOP"])
    DZD = PermissibleValue(
        text="DZD",
        description="Algerian dinar.",
        meaning=CIM["Currency.DZD"])
    EEK = PermissibleValue(
        text="EEK",
        description="Estonian kroon.",
        meaning=CIM["Currency.EEK"])
    EGP = PermissibleValue(
        text="EGP",
        description="Egyptian pound.",
        meaning=CIM["Currency.EGP"])
    ERN = PermissibleValue(
        text="ERN",
        description="Eritrean nakfa.",
        meaning=CIM["Currency.ERN"])
    ETB = PermissibleValue(
        text="ETB",
        description="Ethiopian birr.",
        meaning=CIM["Currency.ETB"])
    EUR = PermissibleValue(
        text="EUR",
        description="Euro.",
        meaning=CIM["Currency.EUR"])
    FJD = PermissibleValue(
        text="FJD",
        description="Fiji dollar.",
        meaning=CIM["Currency.FJD"])
    FKP = PermissibleValue(
        text="FKP",
        description="Falkland Islands pound.",
        meaning=CIM["Currency.FKP"])
    GBP = PermissibleValue(
        text="GBP",
        description="Pound sterling.",
        meaning=CIM["Currency.GBP"])
    GEL = PermissibleValue(
        text="GEL",
        description="Georgian lari.",
        meaning=CIM["Currency.GEL"])
    GHS = PermissibleValue(
        text="GHS",
        description="Ghanaian cedi.",
        meaning=CIM["Currency.GHS"])
    GIP = PermissibleValue(
        text="GIP",
        description="Gibraltar pound.",
        meaning=CIM["Currency.GIP"])
    GMD = PermissibleValue(
        text="GMD",
        description="Gambian dalasi.",
        meaning=CIM["Currency.GMD"])
    GNF = PermissibleValue(
        text="GNF",
        description="Guinean franc.",
        meaning=CIM["Currency.GNF"])
    GTQ = PermissibleValue(
        text="GTQ",
        description="Guatemalan quetzal.",
        meaning=CIM["Currency.GTQ"])
    GYD = PermissibleValue(
        text="GYD",
        description="Guyanese dollar.",
        meaning=CIM["Currency.GYD"])
    HKD = PermissibleValue(
        text="HKD",
        description="Hong Kong dollar.",
        meaning=CIM["Currency.HKD"])
    HNL = PermissibleValue(
        text="HNL",
        description="Honduran lempira.",
        meaning=CIM["Currency.HNL"])
    HRK = PermissibleValue(
        text="HRK",
        description="Croatian kuna.",
        meaning=CIM["Currency.HRK"])
    HTG = PermissibleValue(
        text="HTG",
        description="Haitian gourde.",
        meaning=CIM["Currency.HTG"])
    HUF = PermissibleValue(
        text="HUF",
        description="Hungarian forint.",
        meaning=CIM["Currency.HUF"])
    IDR = PermissibleValue(
        text="IDR",
        description="Indonesian rupiah.",
        meaning=CIM["Currency.IDR"])
    ILS = PermissibleValue(
        text="ILS",
        description="Israeli new sheqel.",
        meaning=CIM["Currency.ILS"])
    INR = PermissibleValue(
        text="INR",
        description="Indian rupee.",
        meaning=CIM["Currency.INR"])
    IQD = PermissibleValue(
        text="IQD",
        description="Iraqi dinar.",
        meaning=CIM["Currency.IQD"])
    IRR = PermissibleValue(
        text="IRR",
        description="Iranian rial.",
        meaning=CIM["Currency.IRR"])
    ISK = PermissibleValue(
        text="ISK",
        description="Icelandic krona.",
        meaning=CIM["Currency.ISK"])
    JMD = PermissibleValue(
        text="JMD",
        description="Jamaican dollar.",
        meaning=CIM["Currency.JMD"])
    JOD = PermissibleValue(
        text="JOD",
        description="Jordanian dinar.",
        meaning=CIM["Currency.JOD"])
    JPY = PermissibleValue(
        text="JPY",
        description="Japanese yen.",
        meaning=CIM["Currency.JPY"])
    KES = PermissibleValue(
        text="KES",
        description="Kenyan shilling.",
        meaning=CIM["Currency.KES"])
    KGS = PermissibleValue(
        text="KGS",
        description="Kyrgyzstani som.",
        meaning=CIM["Currency.KGS"])
    KHR = PermissibleValue(
        text="KHR",
        description="Cambodian riel.",
        meaning=CIM["Currency.KHR"])
    KMF = PermissibleValue(
        text="KMF",
        description="Comoro franc.",
        meaning=CIM["Currency.KMF"])
    KPW = PermissibleValue(
        text="KPW",
        description="North Korean won.",
        meaning=CIM["Currency.KPW"])
    KRW = PermissibleValue(
        text="KRW",
        description="South Korean won.",
        meaning=CIM["Currency.KRW"])
    KWD = PermissibleValue(
        text="KWD",
        description="Kuwaiti dinar.",
        meaning=CIM["Currency.KWD"])
    KYD = PermissibleValue(
        text="KYD",
        description="Cayman Islands dollar.",
        meaning=CIM["Currency.KYD"])
    KZT = PermissibleValue(
        text="KZT",
        description="Kazakhstani tenge.",
        meaning=CIM["Currency.KZT"])
    LAK = PermissibleValue(
        text="LAK",
        description="Lao kip.",
        meaning=CIM["Currency.LAK"])
    LBP = PermissibleValue(
        text="LBP",
        description="Lebanese pound.",
        meaning=CIM["Currency.LBP"])
    LKR = PermissibleValue(
        text="LKR",
        description="Sri Lanka rupee.",
        meaning=CIM["Currency.LKR"])
    LRD = PermissibleValue(
        text="LRD",
        description="Liberian dollar.",
        meaning=CIM["Currency.LRD"])
    LSL = PermissibleValue(
        text="LSL",
        description="Lesotho loti.",
        meaning=CIM["Currency.LSL"])
    LTL = PermissibleValue(
        text="LTL",
        description="Lithuanian litas.",
        meaning=CIM["Currency.LTL"])
    LVL = PermissibleValue(
        text="LVL",
        description="Latvian lats.",
        meaning=CIM["Currency.LVL"])
    LYD = PermissibleValue(
        text="LYD",
        description="Libyan dinar.",
        meaning=CIM["Currency.LYD"])
    MAD = PermissibleValue(
        text="MAD",
        description="Moroccan dirham.",
        meaning=CIM["Currency.MAD"])
    MDL = PermissibleValue(
        text="MDL",
        description="Moldovan leu.",
        meaning=CIM["Currency.MDL"])
    MGA = PermissibleValue(
        text="MGA",
        description="Malagasy ariary.",
        meaning=CIM["Currency.MGA"])
    MKD = PermissibleValue(
        text="MKD",
        description="Macedonian denar.",
        meaning=CIM["Currency.MKD"])
    MMK = PermissibleValue(
        text="MMK",
        description="Myanma kyat.",
        meaning=CIM["Currency.MMK"])
    MNT = PermissibleValue(
        text="MNT",
        description="Mongolian tugrik.",
        meaning=CIM["Currency.MNT"])
    MOP = PermissibleValue(
        text="MOP",
        description="Macanese pataca.",
        meaning=CIM["Currency.MOP"])
    MRO = PermissibleValue(
        text="MRO",
        description="Mauritanian ouguiya.",
        meaning=CIM["Currency.MRO"])
    MUR = PermissibleValue(
        text="MUR",
        description="Mauritian rupee.",
        meaning=CIM["Currency.MUR"])
    MVR = PermissibleValue(
        text="MVR",
        description="Maldivian rufiyaa.",
        meaning=CIM["Currency.MVR"])
    MWK = PermissibleValue(
        text="MWK",
        description="Malawian kwacha.",
        meaning=CIM["Currency.MWK"])
    MXN = PermissibleValue(
        text="MXN",
        description="Mexican peso.",
        meaning=CIM["Currency.MXN"])
    MYR = PermissibleValue(
        text="MYR",
        description="Malaysian ringgit.",
        meaning=CIM["Currency.MYR"])
    MZN = PermissibleValue(
        text="MZN",
        description="Mozambican metical.",
        meaning=CIM["Currency.MZN"])
    NAD = PermissibleValue(
        text="NAD",
        description="Namibian dollar.",
        meaning=CIM["Currency.NAD"])
    NGN = PermissibleValue(
        text="NGN",
        description="Nigerian naira.",
        meaning=CIM["Currency.NGN"])
    NIO = PermissibleValue(
        text="NIO",
        description="Cordoba oro.",
        meaning=CIM["Currency.NIO"])
    NOK = PermissibleValue(
        text="NOK",
        description="Norwegian krone.",
        meaning=CIM["Currency.NOK"])
    NPR = PermissibleValue(
        text="NPR",
        description="Nepalese rupee.",
        meaning=CIM["Currency.NPR"])
    NZD = PermissibleValue(
        text="NZD",
        description="New Zealand dollar.",
        meaning=CIM["Currency.NZD"])
    OMR = PermissibleValue(
        text="OMR",
        description="Omani rial.",
        meaning=CIM["Currency.OMR"])
    PAB = PermissibleValue(
        text="PAB",
        description="Panamanian balboa.",
        meaning=CIM["Currency.PAB"])
    PEN = PermissibleValue(
        text="PEN",
        description="Peruvian nuevo sol.",
        meaning=CIM["Currency.PEN"])
    PGK = PermissibleValue(
        text="PGK",
        description="Papua New Guinean kina.",
        meaning=CIM["Currency.PGK"])
    PHP = PermissibleValue(
        text="PHP",
        description="Philippine peso.",
        meaning=CIM["Currency.PHP"])
    PKR = PermissibleValue(
        text="PKR",
        description="Pakistani rupee.",
        meaning=CIM["Currency.PKR"])
    PLN = PermissibleValue(
        text="PLN",
        description="Polish zloty.",
        meaning=CIM["Currency.PLN"])
    PYG = PermissibleValue(
        text="PYG",
        description="Paraguayan guarani.",
        meaning=CIM["Currency.PYG"])
    QAR = PermissibleValue(
        text="QAR",
        description="Qatari rial.",
        meaning=CIM["Currency.QAR"])
    RON = PermissibleValue(
        text="RON",
        description="Romanian new leu.",
        meaning=CIM["Currency.RON"])
    RSD = PermissibleValue(
        text="RSD",
        description="Serbian dinar.",
        meaning=CIM["Currency.RSD"])
    RUB = PermissibleValue(
        text="RUB",
        description="Russian rouble.",
        meaning=CIM["Currency.RUB"])
    RWF = PermissibleValue(
        text="RWF",
        description="Rwandan franc.",
        meaning=CIM["Currency.RWF"])
    SAR = PermissibleValue(
        text="SAR",
        description="Saudi riyal.",
        meaning=CIM["Currency.SAR"])
    SBD = PermissibleValue(
        text="SBD",
        description="Solomon Islands dollar.",
        meaning=CIM["Currency.SBD"])
    SCR = PermissibleValue(
        text="SCR",
        description="Seychelles rupee.",
        meaning=CIM["Currency.SCR"])
    SDG = PermissibleValue(
        text="SDG",
        description="Sudanese pound.",
        meaning=CIM["Currency.SDG"])
    SEK = PermissibleValue(
        text="SEK",
        description="Swedish krona/kronor.",
        meaning=CIM["Currency.SEK"])
    SGD = PermissibleValue(
        text="SGD",
        description="Singapore dollar.",
        meaning=CIM["Currency.SGD"])
    SHP = PermissibleValue(
        text="SHP",
        description="Saint Helena pound.",
        meaning=CIM["Currency.SHP"])
    SLL = PermissibleValue(
        text="SLL",
        description="Sierra Leonean leone.",
        meaning=CIM["Currency.SLL"])
    SOS = PermissibleValue(
        text="SOS",
        description="Somali shilling.",
        meaning=CIM["Currency.SOS"])
    SRD = PermissibleValue(
        text="SRD",
        description="Surinamese dollar.",
        meaning=CIM["Currency.SRD"])
    STD = PermissibleValue(
        text="STD",
        description="Sao Tome and Principe dobra.",
        meaning=CIM["Currency.STD"])
    SYP = PermissibleValue(
        text="SYP",
        description="Syrian pound.",
        meaning=CIM["Currency.SYP"])
    SZL = PermissibleValue(
        text="SZL",
        description="Lilangeni.",
        meaning=CIM["Currency.SZL"])
    THB = PermissibleValue(
        text="THB",
        description="Thai baht.",
        meaning=CIM["Currency.THB"])
    TJS = PermissibleValue(
        text="TJS",
        description="Tajikistani somoni.",
        meaning=CIM["Currency.TJS"])
    TMT = PermissibleValue(
        text="TMT",
        description="Turkmenistani manat.",
        meaning=CIM["Currency.TMT"])
    TND = PermissibleValue(
        text="TND",
        description="Tunisian dinar.",
        meaning=CIM["Currency.TND"])
    TOP = PermissibleValue(
        text="TOP",
        description="Tongan pa'anga.",
        meaning=CIM["Currency.TOP"])
    TRY = PermissibleValue(
        text="TRY",
        description="Turkish lira.",
        meaning=CIM["Currency.TRY"])
    TTD = PermissibleValue(
        text="TTD",
        description="Trinidad and Tobago dollar.",
        meaning=CIM["Currency.TTD"])
    TWD = PermissibleValue(
        text="TWD",
        description="New Taiwan dollar.",
        meaning=CIM["Currency.TWD"])
    TZS = PermissibleValue(
        text="TZS",
        description="Tanzanian shilling.",
        meaning=CIM["Currency.TZS"])
    UAH = PermissibleValue(
        text="UAH",
        description="Ukrainian hryvnia.",
        meaning=CIM["Currency.UAH"])
    UGX = PermissibleValue(
        text="UGX",
        description="Ugandan shilling.",
        meaning=CIM["Currency.UGX"])
    USD = PermissibleValue(
        text="USD",
        description="United States dollar.",
        meaning=CIM["Currency.USD"])
    UYU = PermissibleValue(
        text="UYU",
        description="Uruguayan peso.",
        meaning=CIM["Currency.UYU"])
    UZS = PermissibleValue(
        text="UZS",
        description="Uzbekistan som.",
        meaning=CIM["Currency.UZS"])
    VEF = PermissibleValue(
        text="VEF",
        description="Venezuelan bolivar fuerte.",
        meaning=CIM["Currency.VEF"])
    VND = PermissibleValue(
        text="VND",
        description="Vietnamese Dong.",
        meaning=CIM["Currency.VND"])
    VUV = PermissibleValue(
        text="VUV",
        description="Vanuatu vatu.",
        meaning=CIM["Currency.VUV"])
    WST = PermissibleValue(
        text="WST",
        description="Samoan tala.",
        meaning=CIM["Currency.WST"])
    XAF = PermissibleValue(
        text="XAF",
        description="CFA franc BEAC.",
        meaning=CIM["Currency.XAF"])
    XCD = PermissibleValue(
        text="XCD",
        description="East Caribbean dollar.",
        meaning=CIM["Currency.XCD"])
    XOF = PermissibleValue(
        text="XOF",
        description="CFA Franc BCEAO.",
        meaning=CIM["Currency.XOF"])
    XPF = PermissibleValue(
        text="XPF",
        description="CFP franc.",
        meaning=CIM["Currency.XPF"])
    YER = PermissibleValue(
        text="YER",
        description="Yemeni rial.",
        meaning=CIM["Currency.YER"])
    ZAR = PermissibleValue(
        text="ZAR",
        description="South African rand.",
        meaning=CIM["Currency.ZAR"])
    ZMK = PermissibleValue(
        text="ZMK",
        description="Zambian kwacha.",
        meaning=CIM["Currency.ZMK"])
    ZWL = PermissibleValue(
        text="ZWL",
        description="Zimbabwe dollar.",
        meaning=CIM["Currency.ZWL"])

    _defn = EnumDefinition(
        name="Currency",
        description="Monetary currencies.  ISO 4217 standard including 3-character currency code.",
    )

class CurveStyle(EnumDefinitionImpl):
    """
    Style or shape of curve.
    """
    constantYValue = PermissibleValue(
        text="constantYValue",
        description="""The Y-axis values are assumed constant until the next curve point and prior to the first curve point.""",
        meaning=CIM["CurveStyle.constantYValue"])
    straightLineYValues = PermissibleValue(
        text="straightLineYValues",
        description="""The Y-axis values are assumed to be a straight line between values. Also known as linear interpolation.""",
        meaning=CIM["CurveStyle.straightLineYValues"])

    _defn = EnumDefinition(
        name="CurveStyle",
        description="Style or shape of curve.",
    )

class CyberImpactLevel(EnumDefinitionImpl):
    """
    NERC CIP impact level
    """
    high = PermissibleValue(
        text="high",
        meaning=CIM["CyberImpactLevel.high"])
    low = PermissibleValue(
        text="low",
        meaning=CIM["CyberImpactLevel.low"])
    medium = PermissibleValue(
        text="medium",
        meaning=CIM["CyberImpactLevel.medium"])
    none = PermissibleValue(
        text="none",
        meaning=CIM["CyberImpactLevel.none"])

    _defn = EnumDefinition(
        name="CyberImpactLevel",
        description="NERC CIP impact level",
    )

class EVTypeKind(EnumDefinitionImpl):
    """
    Type of EV (e.g., BEV, PHEV, bus, truck, motorcycle).
    """
    bEV = PermissibleValue(
        text="bEV",
        description="battery electric vehicle",
        meaning=CIM["EVTypeKind.bEV"])
    bus = PermissibleValue(
        text="bus",
        description="bus",
        meaning=CIM["EVTypeKind.bus"])
    motorcycle = PermissibleValue(
        text="motorcycle",
        description="motorcycle",
        meaning=CIM["EVTypeKind.motorcycle"])
    other = PermissibleValue(
        text="other",
        description="other",
        meaning=CIM["EVTypeKind.other"])
    phEV = PermissibleValue(
        text="phEV",
        description="plugin hybrid electric vehicle",
        meaning=CIM["EVTypeKind.phEV"])
    truck = PermissibleValue(
        text="truck",
        description="truck",
        meaning=CIM["EVTypeKind.truck"])

    _defn = EnumDefinition(
        name="EVTypeKind",
        description="Type of EV (e.g., BEV, PHEV, bus, truck, motorcycle).",
    )

class EarthModelKind(EnumDefinitionImpl):

    carson = PermissibleValue(
        text="carson",
        meaning=CIM["EarthModelKind.carson"])
    deri = PermissibleValue(
        text="deri",
        meaning=CIM["EarthModelKind.deri"])

    _defn = EnumDefinition(
        name="EarthModelKind",
    )

class FuelType(EnumDefinitionImpl):
    """
    Type of fuel.
    """
    brownCoalLignite = PermissibleValue(
        text="brownCoalLignite",
        description="Brown coal lignite.",
        meaning=CIM["FuelType.brownCoalLignite"])
    coal = PermissibleValue(
        text="coal",
        description="Generic coal, not including lignite type.",
        meaning=CIM["FuelType.coal"])
    coalDerivedGas = PermissibleValue(
        text="coalDerivedGas",
        description="Coal derived gas.",
        meaning=CIM["FuelType.coalDerivedGas"])
    gas = PermissibleValue(
        text="gas",
        description="Natural gas.",
        meaning=CIM["FuelType.gas"])
    hardCoal = PermissibleValue(
        text="hardCoal",
        description="Hard coal.",
        meaning=CIM["FuelType.hardCoal"])
    lignite = PermissibleValue(
        text="lignite",
        description="""The fuel is lignite coal. Note that this is a special type of coal, so the other enum of coal is reserved for hard coal types or if the exact type of coal is not known.""",
        meaning=CIM["FuelType.lignite"])
    oil = PermissibleValue(
        text="oil",
        description="Oil.",
        meaning=CIM["FuelType.oil"])
    oilShale = PermissibleValue(
        text="oilShale",
        description="Oil Shale.",
        meaning=CIM["FuelType.oilShale"])
    other = PermissibleValue(
        text="other",
        description="Any fuel type not included in the rest of the enumerated value.",
        meaning=CIM["FuelType.other"])
    peat = PermissibleValue(
        text="peat",
        description="Peat.",
        meaning=CIM["FuelType.peat"])

    _defn = EnumDefinition(
        name="FuelType",
        description="Type of fuel.",
    )

class GeneratorControlMode(EnumDefinitionImpl):
    """
    Unit control modes.
    """
    pulse = PermissibleValue(
        text="pulse",
        description="Pulse control mode.",
        meaning=CIM["GeneratorControlMode.pulse"])
    setpoint = PermissibleValue(
        text="setpoint",
        description="Setpoint control mode.",
        meaning=CIM["GeneratorControlMode.setpoint"])

    _defn = EnumDefinition(
        name="GeneratorControlMode",
        description="Unit control modes.",
    )

class GeneratorControlSource(EnumDefinitionImpl):
    """
    The source of controls for a generating unit.
    """
    agc = PermissibleValue(
        text="agc",
        meaning=CIM["GeneratorControlSource.agc"])
    con = PermissibleValue(
        text="con",
        meaning=CIM["GeneratorControlSource.con"])
    edc = PermissibleValue(
        text="edc",
        meaning=CIM["GeneratorControlSource.edc"])
    fwd = PermissibleValue(
        text="fwd",
        meaning=CIM["GeneratorControlSource.fwd"])
    lfc = PermissibleValue(
        text="lfc",
        meaning=CIM["GeneratorControlSource.lfc"])
    manual = PermissibleValue(
        text="manual",
        meaning=CIM["GeneratorControlSource.manual"])
    mrn = PermissibleValue(
        text="mrn",
        meaning=CIM["GeneratorControlSource.mrn"])
    offAGC = PermissibleValue(
        text="offAGC",
        description="Off of automatic generation control (AGC).",
        meaning=CIM["GeneratorControlSource.offAGC"])
    onAGC = PermissibleValue(
        text="onAGC",
        description="On automatic generation control (AGC).",
        meaning=CIM["GeneratorControlSource.onAGC"])
    plantControl = PermissibleValue(
        text="plantControl",
        description="Plant is controlling.",
        meaning=CIM["GeneratorControlSource.plantControl"])
    pmp = PermissibleValue(
        text="pmp",
        meaning=CIM["GeneratorControlSource.pmp"])
    rel = PermissibleValue(
        text="rel",
        meaning=CIM["GeneratorControlSource.rel"])
    res = PermissibleValue(
        text="res",
        meaning=CIM["GeneratorControlSource.res"])
    scp = PermissibleValue(
        text="scp",
        meaning=CIM["GeneratorControlSource.scp"])
    unavailable = PermissibleValue(
        text="unavailable",
        description="Not available.",
        meaning=CIM["GeneratorControlSource.unavailable"])

    _defn = EnumDefinition(
        name="GeneratorControlSource",
        description="The source of controls for a generating unit.",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "False",
            PermissibleValue(
                text="False",
                meaning=CIM["GeneratorControlSource.off"]))

class LimitKind(EnumDefinitionImpl):
    """
    Limit kinds.
    """
    alarmVoltage = PermissibleValue(
        text="alarmVoltage",
        description="Voltage alarm.",
        meaning=CIM["LimitKind.alarmVoltage"])
    highVoltage = PermissibleValue(
        text="highVoltage",
        description="""Referring to the rating of the equipments, a voltage too high can lead to accelerated ageing or the destruction of the equipment.This limit type may or may not have duration.""",
        meaning=CIM["LimitKind.highVoltage"])
    lowVoltage = PermissibleValue(
        text="lowVoltage",
        description="""A too low voltage can disturb the normal operation of some protections and transformer equipped with on-load tap changers, electronic power devices or can affect the behaviour of the auxiliaries of generation units.This limit type may or may not have duration.""",
        meaning=CIM["LimitKind.lowVoltage"])
    operationalVoltageLimit = PermissibleValue(
        text="operationalVoltageLimit",
        description="Operational voltage limit.",
        meaning=CIM["LimitKind.operationalVoltageLimit"])
    patl = PermissibleValue(
        text="patl",
        description="""The Permanent Admissible Transmission Loading (PATL) is the loading in amperes, MVA or MW that can be accepted by a network branch for an unlimited duration without any risk for the material.The OperationnalLimitType.isInfiniteDuration is set to true. There shall be only one OperationalLimitType of kind PATL per OperationalLimitSet if the PATL is ApparentPowerLimit, ActivePowerLimit, or CurrentLimit for a given Terminal or Equipment.""",
        meaning=CIM["LimitKind.patl"])
    patlt = PermissibleValue(
        text="patlt",
        description="""Permanent Admissible Transmission Loading Threshold  (PATLT) is a value in engineering units defined for PATL and calculated using a percentage less than 100 % of the PATL type intended to alert operators of an arising condition. The percentage should be given in the name of the OperationalLimitSet. The aceptableDuration is another way to express the severity of the limit.""",
        meaning=CIM["LimitKind.patlt"])
    stability = PermissibleValue(
        text="stability",
        description="Stability.",
        meaning=CIM["LimitKind.stability"])
    tatl = PermissibleValue(
        text="tatl",
        description="""Temporarily Admissible Transmission Loading (TATL) which is the loading in amperes, MVA or MW that can be accepted by a branch for a certain limited duration.The TATL can be defined in different ways:<ul>    <li>as a fixed percentage of the PATL for a given time (for example, 115% of the PATL that can be accepted during 15 minutes),</li></ul><ul>    <li>pairs of TATL type and Duration calculated for each line taking into account its particular configuration and conditions of functioning (for example, it can define a TATL acceptable during 20 minutes and another one acceptable during 10 minutes).</li></ul>Such a definition of TATL can depend on the initial operating conditions of the network element (sag situation of a line).The duration attribute can be used to define several TATL limit types. Hence multiple TATL limit values may exist having different durations.""",
        meaning=CIM["LimitKind.tatl"])
    tc = PermissibleValue(
        text="tc",
        description="""Tripping Current (TC) is the ultimate intensity without any delay. It is defined as the threshold the line will trip without any possible remedial actions.The tripping of the network element is ordered by protections against short circuits or by overload protections, but in any case, the activation delay of these protections is not compatible with the reaction delay of an operator (less than one minute).The duration is always zero if the OperationalLimitType.acceptableDuration is exchanged. Only one limit value exists for the TC type.""",
        meaning=CIM["LimitKind.tc"])
    tct = PermissibleValue(
        text="tct",
        description="""Tripping Current Threshold  (TCT) is a value in engineering units defined for TC and calculated using a percentage less than 100 % of the TC type intended to alert operators of an arising condition. The percentage should be given in the name of the OperationalLimitSet. The aceptableDuration is another way to express the severity of the limit.""",
        meaning=CIM["LimitKind.tct"])
    warningVoltage = PermissibleValue(
        text="warningVoltage",
        description="Voltage warning.",
        meaning=CIM["LimitKind.warningVoltage"])

    _defn = EnumDefinition(
        name="LimitKind",
        description="Limit kinds.",
    )

class MarineUnitKind(EnumDefinitionImpl):
    """
    Kind of marine energy capture.
    """
    currents = PermissibleValue(
        text="currents",
        description="""Capture energy from ocean current which are caused by forces like breaking waves, wind, coriolis effect etc.""",
        meaning=CIM["MarineUnitKind.currents"])
    other = PermissibleValue(
        text="other",
        description="Other way of capture energy from marine elements.",
        meaning=CIM["MarineUnitKind.other"])
    pressure = PermissibleValue(
        text="pressure",
        description="Capture energy from pressure.",
        meaning=CIM["MarineUnitKind.pressure"])
    tidal = PermissibleValue(
        text="tidal",
        description="""Capture energy from tidal power, which captures the energy of the current caused by the gravitational pull of the Sun and Moon.""",
        meaning=CIM["MarineUnitKind.tidal"])
    wave = PermissibleValue(
        text="wave",
        description="Capture energy from wind waves.",
        meaning=CIM["MarineUnitKind.wave"])

    _defn = EnumDefinition(
        name="MarineUnitKind",
        description="Kind of marine energy capture.",
    )

class MeasurementSourceKind(EnumDefinitionImpl):
    """
    Source from which the measurement has been obtained, such as SCADA, ICCP link, or a co-simulation
    """
    allocated = PermissibleValue(
        text="allocated",
        meaning=CIM["MeasurementSourceKind.allocated"])
    ami = PermissibleValue(
        text="ami",
        description="Measurement from a smart meter for advanced metering infrastructure",
        meaning=CIM["MeasurementSourceKind.ami"])
    calculated = PermissibleValue(
        text="calculated",
        meaning=CIM["MeasurementSourceKind.calculated"])
    estimated = PermissibleValue(
        text="estimated",
        meaning=CIM["MeasurementSourceKind.estimated"])
    forecasted = PermissibleValue(
        text="forecasted",
        meaning=CIM["MeasurementSourceKind.forecasted"])
    iccpLink = PermissibleValue(
        text="iccpLink",
        description="Value received from a remote control centre via ICCP, TASE.2, or other control centre protocol",
        meaning=CIM["MeasurementSourceKind.iccpLink"])
    operator = PermissibleValue(
        text="operator",
        description="Operated entered values (always manually maintained, PSR is not connected to an RTU)",
        meaning=CIM["MeasurementSourceKind.operator"])
    powerFlow = PermissibleValue(
        text="powerFlow",
        meaning=CIM["MeasurementSourceKind.powerFlow"])
    scada = PermissibleValue(
        text="scada",
        description="Telemetered values received from a local SCADA system",
        meaning=CIM["MeasurementSourceKind.scada"])
    thirdParty = PermissibleValue(
        text="thirdParty",
        description="Measurements received from a non-utility 3rd party, such as a DER aggregator",
        meaning=CIM["MeasurementSourceKind.thirdParty"])
    wams = PermissibleValue(
        text="wams",
        description="PMU values received over a wide area measurement system",
        meaning=CIM["MeasurementSourceKind.wams"])

    _defn = EnumDefinition(
        name="MeasurementSourceKind",
        description="Source from which the measurement has been obtained, such as SCADA, ICCP link, or a co-simulation",
    )

class OperationalLimitDirectionKind(EnumDefinitionImpl):
    """
    The direction attribute describes the side of  a limit that is a violation.
    """
    absoluteValue = PermissibleValue(
        text="absoluteValue",
        description="""An absoluteValue limit means that a monitored absolute value above the limit value is a violation.""",
        meaning=CIM["OperationalLimitDirectionKind.absoluteValue"])
    high = PermissibleValue(
        text="high",
        description="""High means that a monitored value above the limit value is a violation.   If applied to a terminal flow, the positive direction is into the terminal.""",
        meaning=CIM["OperationalLimitDirectionKind.high"])
    low = PermissibleValue(
        text="low",
        description="""Low means a monitored value below the limit is a violation.  If applied to a terminal flow, the positive direction is into the terminal.""",
        meaning=CIM["OperationalLimitDirectionKind.low"])

    _defn = EnumDefinition(
        name="OperationalLimitDirectionKind",
        description="The direction attribute describes the side of  a limit that is a violation.",
    )

class OrderedPhaseCodeKind(EnumDefinitionImpl):
    """
    In some use cases, the ordering of phases is important. The PhaseCode class does not represent order, but this
    class addresses such use cases. When two or more phases are present, the individual phases may occur in any order,
    but the neutral must always occur last. When only one phase and the neutral is present, that phase and the neutral
    may be re-ordered.
    """
    A = PermissibleValue(
        text="A",
        meaning=CIM["OrderedPhaseCodeKind.A"])
    AB = PermissibleValue(
        text="AB",
        meaning=CIM["OrderedPhaseCodeKind.AB"])
    ABC = PermissibleValue(
        text="ABC",
        meaning=CIM["OrderedPhaseCodeKind.ABC"])
    ABCN = PermissibleValue(
        text="ABCN",
        meaning=CIM["OrderedPhaseCodeKind.ABCN"])
    ABN = PermissibleValue(
        text="ABN",
        meaning=CIM["OrderedPhaseCodeKind.ABN"])
    AC = PermissibleValue(
        text="AC",
        meaning=CIM["OrderedPhaseCodeKind.AC"])
    ACB = PermissibleValue(
        text="ACB",
        meaning=CIM["OrderedPhaseCodeKind.ACB"])
    ACBN = PermissibleValue(
        text="ACBN",
        meaning=CIM["OrderedPhaseCodeKind.ACBN"])
    ACN = PermissibleValue(
        text="ACN",
        meaning=CIM["OrderedPhaseCodeKind.ACN"])
    AN = PermissibleValue(
        text="AN",
        meaning=CIM["OrderedPhaseCodeKind.AN"])
    B = PermissibleValue(
        text="B",
        meaning=CIM["OrderedPhaseCodeKind.B"])
    BA = PermissibleValue(
        text="BA",
        meaning=CIM["OrderedPhaseCodeKind.BA"])
    BAC = PermissibleValue(
        text="BAC",
        meaning=CIM["OrderedPhaseCodeKind.BAC"])
    BACN = PermissibleValue(
        text="BACN",
        meaning=CIM["OrderedPhaseCodeKind.BACN"])
    BAN = PermissibleValue(
        text="BAN",
        meaning=CIM["OrderedPhaseCodeKind.BAN"])
    BC = PermissibleValue(
        text="BC",
        meaning=CIM["OrderedPhaseCodeKind.BC"])
    BCA = PermissibleValue(
        text="BCA",
        meaning=CIM["OrderedPhaseCodeKind.BCA"])
    BCAN = PermissibleValue(
        text="BCAN",
        meaning=CIM["OrderedPhaseCodeKind.BCAN"])
    BCN = PermissibleValue(
        text="BCN",
        meaning=CIM["OrderedPhaseCodeKind.BCN"])
    BN = PermissibleValue(
        text="BN",
        meaning=CIM["OrderedPhaseCodeKind.BN"])
    C = PermissibleValue(
        text="C",
        meaning=CIM["OrderedPhaseCodeKind.C"])
    CA = PermissibleValue(
        text="CA",
        meaning=CIM["OrderedPhaseCodeKind.CA"])
    CAB = PermissibleValue(
        text="CAB",
        meaning=CIM["OrderedPhaseCodeKind.CAB"])
    CABN = PermissibleValue(
        text="CABN",
        meaning=CIM["OrderedPhaseCodeKind.CABN"])
    CAN = PermissibleValue(
        text="CAN",
        meaning=CIM["OrderedPhaseCodeKind.CAN"])
    CB = PermissibleValue(
        text="CB",
        meaning=CIM["OrderedPhaseCodeKind.CB"])
    CBA = PermissibleValue(
        text="CBA",
        meaning=CIM["OrderedPhaseCodeKind.CBA"])
    CBAN = PermissibleValue(
        text="CBAN",
        meaning=CIM["OrderedPhaseCodeKind.CBAN"])
    CBN = PermissibleValue(
        text="CBN",
        meaning=CIM["OrderedPhaseCodeKind.CBN"])
    CN = PermissibleValue(
        text="CN",
        meaning=CIM["OrderedPhaseCodeKind.CN"])
    NA = PermissibleValue(
        text="NA",
        meaning=CIM["OrderedPhaseCodeKind.NA"])
    NB = PermissibleValue(
        text="NB",
        meaning=CIM["OrderedPhaseCodeKind.NB"])
    NC = PermissibleValue(
        text="NC",
        meaning=CIM["OrderedPhaseCodeKind.NC"])
    Ns1 = PermissibleValue(
        text="Ns1",
        meaning=CIM["OrderedPhaseCodeKind.Ns1"])
    Ns2 = PermissibleValue(
        text="Ns2",
        meaning=CIM["OrderedPhaseCodeKind.Ns2"])
    X = PermissibleValue(
        text="X",
        meaning=CIM["OrderedPhaseCodeKind.X"])
    XN = PermissibleValue(
        text="XN",
        meaning=CIM["OrderedPhaseCodeKind.XN"])
    XY = PermissibleValue(
        text="XY",
        meaning=CIM["OrderedPhaseCodeKind.XY"])
    XYN = PermissibleValue(
        text="XYN",
        meaning=CIM["OrderedPhaseCodeKind.XYN"])
    none = PermissibleValue(
        text="none",
        meaning=CIM["OrderedPhaseCodeKind.none"])
    s1 = PermissibleValue(
        text="s1",
        meaning=CIM["OrderedPhaseCodeKind.s1"])
    s12 = PermissibleValue(
        text="s12",
        meaning=CIM["OrderedPhaseCodeKind.s12"])
    s12N = PermissibleValue(
        text="s12N",
        meaning=CIM["OrderedPhaseCodeKind.s12N"])
    s1N = PermissibleValue(
        text="s1N",
        meaning=CIM["OrderedPhaseCodeKind.s1N"])
    s2 = PermissibleValue(
        text="s2",
        meaning=CIM["OrderedPhaseCodeKind.s2"])
    s21 = PermissibleValue(
        text="s21",
        meaning=CIM["OrderedPhaseCodeKind.s21"])
    s21N = PermissibleValue(
        text="s21N",
        meaning=CIM["OrderedPhaseCodeKind.s21N"])
    s2N = PermissibleValue(
        text="s2N",
        meaning=CIM["OrderedPhaseCodeKind.s2N"])

    _defn = EnumDefinition(
        name="OrderedPhaseCodeKind",
        description="""In some use cases, the ordering of phases is important. The PhaseCode class does not represent order, but this class addresses such use cases. When two or more phases are present, the individual phases may occur in any order, but the neutral must always occur last. When only one phase and the neutral is present, that phase and the neutral may be re-ordered.""",
    )

class PetersenCoilModeKind(EnumDefinitionImpl):
    """
    The mode of operation for a Petersen coil.
    """
    automaticPositioning = PermissibleValue(
        text="automaticPositioning",
        description="Automatic positioning.",
        meaning=CIM["PetersenCoilModeKind.automaticPositioning"])
    fixed = PermissibleValue(
        text="fixed",
        description="Fixed position.",
        meaning=CIM["PetersenCoilModeKind.fixed"])
    manual = PermissibleValue(
        text="manual",
        description="Manual positioning.",
        meaning=CIM["PetersenCoilModeKind.manual"])

    _defn = EnumDefinition(
        name="PetersenCoilModeKind",
        description="The mode of operation for a Petersen coil.",
    )

class PhaseCode(EnumDefinitionImpl):
    """
    Enumeration of phase identifiers used to designate the combination of phase and/or neutral conductors at a
    terminal, measurement or equipment modelled as a single-line balanced equivalent.This is an unordered enumeration
    of phase identifiers. Allows designation of phases for both transmission and distribution equipment, circuits and
    loads. The enumeration, by itself, does not describe how the phases are connected together or connected to ground.
    Ground is not explicitly denoted as a phase.Residential and small commercial loads are often served from
    single-phase, or split-phase, secondary circuits. For the example of s12N, phases 1 and 2 refer to hot wires that
    are 180 degrees out of phase, while N refers to the neutral wire. Through single-phase transformer connections,
    these secondary circuits may be served from one or two of the primary phases A, B, and C. For three-phase loads,
    use the A, B, C phase codes instead of s12N.The integer values are from IEC 61968-9 to support revenue metering
    applications.
    """
    A = PermissibleValue(
        text="A",
        description="Phase A.",
        meaning=CIM["PhaseCode.A"])
    AB = PermissibleValue(
        text="AB",
        description="Phases A and B.",
        meaning=CIM["PhaseCode.AB"])
    ABC = PermissibleValue(
        text="ABC",
        description="Phases A, B, and C.",
        meaning=CIM["PhaseCode.ABC"])
    ABCN = PermissibleValue(
        text="ABCN",
        description="Phases A, B, C, and N.",
        meaning=CIM["PhaseCode.ABCN"])
    ABN = PermissibleValue(
        text="ABN",
        description="Phases A, B, and neutral.",
        meaning=CIM["PhaseCode.ABN"])
    AC = PermissibleValue(
        text="AC",
        description="Phases A and C.",
        meaning=CIM["PhaseCode.AC"])
    ACN = PermissibleValue(
        text="ACN",
        description="Phases A, C and neutral.",
        meaning=CIM["PhaseCode.ACN"])
    AN = PermissibleValue(
        text="AN",
        description="Phases A and neutral.",
        meaning=CIM["PhaseCode.AN"])
    B = PermissibleValue(
        text="B",
        description="Phase B.",
        meaning=CIM["PhaseCode.B"])
    BC = PermissibleValue(
        text="BC",
        description="Phases B and C.",
        meaning=CIM["PhaseCode.BC"])
    BCN = PermissibleValue(
        text="BCN",
        description="Phases B, C, and neutral.",
        meaning=CIM["PhaseCode.BCN"])
    BN = PermissibleValue(
        text="BN",
        description="Phases B and neutral.",
        meaning=CIM["PhaseCode.BN"])
    C = PermissibleValue(
        text="C",
        description="Phase C.",
        meaning=CIM["PhaseCode.C"])
    CN = PermissibleValue(
        text="CN",
        description="Phases C and neutral.",
        meaning=CIM["PhaseCode.CN"])
    N = PermissibleValue(
        text="N",
        description="Neutral phase.",
        meaning=CIM["PhaseCode.N"])
    X = PermissibleValue(
        text="X",
        description="Unknown non-neutral phase.",
        meaning=CIM["PhaseCode.X"])
    XN = PermissibleValue(
        text="XN",
        description="Unknown non-neutral phase plus neutral.",
        meaning=CIM["PhaseCode.XN"])
    XY = PermissibleValue(
        text="XY",
        description="Two unknown non-neutral phases.",
        meaning=CIM["PhaseCode.XY"])
    XYN = PermissibleValue(
        text="XYN",
        description="Two unknown non-neutral phases plus neutral.",
        meaning=CIM["PhaseCode.XYN"])
    none = PermissibleValue(
        text="none",
        description="No phases specified.",
        meaning=CIM["PhaseCode.none"])
    s1 = PermissibleValue(
        text="s1",
        description="Secondary phase 1.",
        meaning=CIM["PhaseCode.s1"])
    s12 = PermissibleValue(
        text="s12",
        description="Secondary phase 1 and 2.",
        meaning=CIM["PhaseCode.s12"])
    s12N = PermissibleValue(
        text="s12N",
        description="Secondary phases 1, 2, and neutral.",
        meaning=CIM["PhaseCode.s12N"])
    s1N = PermissibleValue(
        text="s1N",
        description="Secondary phase 1 and neutral.",
        meaning=CIM["PhaseCode.s1N"])
    s2 = PermissibleValue(
        text="s2",
        description="Secondary phase 2.",
        meaning=CIM["PhaseCode.s2"])
    s2N = PermissibleValue(
        text="s2N",
        description="Secondary phase 2 and neutral.",
        meaning=CIM["PhaseCode.s2N"])

    _defn = EnumDefinition(
        name="PhaseCode",
        description="""Enumeration of phase identifiers used to designate the combination of phase and/or neutral conductors at a terminal, measurement or equipment modelled as a single-line balanced equivalent.This is an unordered enumeration of phase identifiers.  Allows designation of phases for both transmission and distribution equipment, circuits and loads.   The enumeration, by itself, does not describe how the phases are connected together or connected to ground.  Ground is not explicitly denoted as a phase.Residential and small commercial loads are often served from single-phase, or split-phase, secondary circuits. For the example of s12N, phases 1 and 2 refer to hot wires that are 180 degrees out of phase, while N refers to the neutral wire. Through single-phase transformer connections, these secondary circuits may be served from one or two of the primary phases A, B, and C. For three-phase loads, use the A, B, C phase codes instead of s12N.The integer values are from IEC 61968-9 to support revenue metering applications.""",
    )

class PhaseCountKind(EnumDefinitionImpl):
    """
    Number of phases supported by a device.
    """
    other = PermissibleValue(
        text="other",
        description="Other",
        meaning=CIM["PhaseCountKind.other"])
    singlePhase = PermissibleValue(
        text="singlePhase",
        description="Single phase",
        meaning=CIM["PhaseCountKind.singlePhase"])
    threePhase = PermissibleValue(
        text="threePhase",
        description="Three phases",
        meaning=CIM["PhaseCountKind.threePhase"])

    _defn = EnumDefinition(
        name="PhaseCountKind",
        description="Number of phases supported by a device.",
    )

class PhaseShuntConnectionKind(EnumDefinitionImpl):
    """
    The configuration of phase connections for a single terminal device such as a load or capacitor.
    """
    D = PermissibleValue(
        text="D",
        description="Delta connection.",
        meaning=CIM["PhaseShuntConnectionKind.D"])
    G = PermissibleValue(
        text="G",
        description="""Ground connection; use when explicit connection to ground needs to be expressed in combination with the phase code, such as for electrical wire/cable or for meters.""",
        meaning=CIM["PhaseShuntConnectionKind.G"])
    I = PermissibleValue(
        text="I",
        description="Independent winding, for single-phase connections.",
        meaning=CIM["PhaseShuntConnectionKind.I"])
    Y = PermissibleValue(
        text="Y",
        description="Wye connection.",
        meaning=CIM["PhaseShuntConnectionKind.Y"])
    Yn = PermissibleValue(
        text="Yn",
        description="Wye, with neutral brought out for grounding.",
        meaning=CIM["PhaseShuntConnectionKind.Yn"])

    _defn = EnumDefinition(
        name="PhaseShuntConnectionKind",
        description="The configuration of phase connections for a single terminal device such as a load or capacitor.",
    )

class PotentialTransformerKind(EnumDefinitionImpl):
    """
    The construction kind of the potential transformer.
    """
    capacitiveCoupling = PermissibleValue(
        text="capacitiveCoupling",
        description="The potential transformer is using capacitive coupling to create secondary voltage.",
        meaning=CIM["PotentialTransformerKind.capacitiveCoupling"])
    inductive = PermissibleValue(
        text="inductive",
        description="The potential transformer is using induction coils to create secondary voltage.",
        meaning=CIM["PotentialTransformerKind.inductive"])

    _defn = EnumDefinition(
        name="PotentialTransformerKind",
        description="The construction kind of the potential transformer.",
    )

class PowerElectricalChemicalUnitKind(EnumDefinitionImpl):
    """
    Kind of power electrical chemical unit.
    """
    electrolyticCell = PermissibleValue(
        text="electrolyticCell",
        description="""An electrolytic cell is an electrochemical cell that drives a non-spontaneous redox reaction through the application of electrical energy. Example are the decomposition of water into hydrogen and oxygen.""",
        meaning=CIM["PowerElectricalChemicalUnitKind.electrolyticCell"])
    fuelCell = PermissibleValue(
        text="fuelCell",
        description="""A fuel cell is an electrochemical cell that converts the chemical energy from a fuel into electricity through an electrochemical reaction of hydrogen fuel with oxygen or another oxidizing agent.""",
        meaning=CIM["PowerElectricalChemicalUnitKind.fuelCell"])
    other = PermissibleValue(
        text="other",
        description="Other type of cell used in chemical reactions.",
        meaning=CIM["PowerElectricalChemicalUnitKind.other"])

    _defn = EnumDefinition(
        name="PowerElectricalChemicalUnitKind",
        description="Kind of power electrical chemical unit.",
    )

class RegulatingControlModeKind(EnumDefinitionImpl):
    """
    The kind of regulation model.   For example regulating voltage, reactive power, active power, etc.
    """
    activePower = PermissibleValue(
        text="activePower",
        description="Active power is specified.",
        meaning=CIM["RegulatingControlModeKind.activePower"])
    admittance = PermissibleValue(
        text="admittance",
        description="Admittance is specified.",
        meaning=CIM["RegulatingControlModeKind.admittance"])
    currentFlow = PermissibleValue(
        text="currentFlow",
        description="Current flow is specified.",
        meaning=CIM["RegulatingControlModeKind.currentFlow"])
    powerFactor = PermissibleValue(
        text="powerFactor",
        description="Power factor is specified.",
        meaning=CIM["RegulatingControlModeKind.powerFactor"])
    reactivePower = PermissibleValue(
        text="reactivePower",
        description="Reactive power is specified.",
        meaning=CIM["RegulatingControlModeKind.reactivePower"])
    temperature = PermissibleValue(
        text="temperature",
        description="Control switches on/off based on the local temperature (i.e., a thermostat).",
        meaning=CIM["RegulatingControlModeKind.temperature"])
    timeScheduled = PermissibleValue(
        text="timeScheduled",
        description="""Control switches on/off by time of day. The times may change on the weekend, or in different seasons.""",
        meaning=CIM["RegulatingControlModeKind.timeScheduled"])
    voltage = PermissibleValue(
        text="voltage",
        description="Voltage is specified.",
        meaning=CIM["RegulatingControlModeKind.voltage"])

    _defn = EnumDefinition(
        name="RegulatingControlModeKind",
        description="The kind of regulation model.   For example regulating voltage, reactive power, active power, etc.",
    )

class SSSCControlModeKind(EnumDefinitionImpl):
    """
    Control modes of the Static Synchronous Series Compensator (SSSC).
    """
    currentDroop = PermissibleValue(
        text="currentDroop",
        description="""<font color=#636671>The device injects a voltage proportional to the difference between the line current and the target value of the CurrentDroopControlFunction. There are capacitive and inductive operational regions.</font>""",
        meaning=CIM["SSSCControlModeKind.currentDroop"])
    effectiveReactance = PermissibleValue(
        text="effectiveReactance",
        description="""<font color=#636671>The device injects a voltage proportional to the line current to achieve the specified target value defined by the ImpedanceControlFunction. The voltage will vary according to the line current level.</font>""",
        meaning=CIM["SSSCControlModeKind.effectiveReactance"])
    monitoring = PermissibleValue(
        text="monitoring",
        description="""<font color=#636671>The device bypasses and a voltage injection is close to zero. In monitoring mode current is monitored.</font>""",
        meaning=CIM["SSSCControlModeKind.monitoring"])
    voltageInjection = PermissibleValue(
        text="voltageInjection",
        description="""<font color=#636671>The device injects a fixed voltage that is either inductive or capacitive according to the specified target value of the VoltageInjectionControlFunction. The effective reactance varies according to the flow of the line current.</font>""",
        meaning=CIM["SSSCControlModeKind.voltageInjection"])

    _defn = EnumDefinition(
        name="SSSCControlModeKind",
        description="Control modes of the Static Synchronous Series Compensator (SSSC).",
    )

class SVCControlMode(EnumDefinitionImpl):
    """
    Static VAr Compensator control mode.
    """
    reactivePower = PermissibleValue(
        text="reactivePower",
        description="Reactive power control.",
        meaning=CIM["SVCControlMode.reactivePower"])
    voltage = PermissibleValue(
        text="voltage",
        description="Voltage control.",
        meaning=CIM["SVCControlMode.voltage"])

    _defn = EnumDefinition(
        name="SVCControlMode",
        description="Static VAr Compensator control mode.",
    )

class ShortCircuitRotorKind(EnumDefinitionImpl):
    """
    Type of rotor, used by short circuit applications.
    """
    salientPole1 = PermissibleValue(
        text="salientPole1",
        description="Salient pole 1 in IEC 60909.",
        meaning=CIM["ShortCircuitRotorKind.salientPole1"])
    salientPole2 = PermissibleValue(
        text="salientPole2",
        description="Salient pole 2 in IEC 60909.",
        meaning=CIM["ShortCircuitRotorKind.salientPole2"])
    turboSeries1 = PermissibleValue(
        text="turboSeries1",
        description="Turbo Series 1 in IEC 60909.",
        meaning=CIM["ShortCircuitRotorKind.turboSeries1"])
    turboSeries2 = PermissibleValue(
        text="turboSeries2",
        description="Turbo series 2 in IEC 60909.",
        meaning=CIM["ShortCircuitRotorKind.turboSeries2"])

    _defn = EnumDefinition(
        name="ShortCircuitRotorKind",
        description="Type of rotor, used by short circuit applications.",
    )

class SinglePhaseKind(EnumDefinitionImpl):
    """
    Enumeration of phase identifiers used to designate the specific phase of conducting equipment modelled as
    individual unbalanced phases.Allows designation of specific phases for transmission and distribution equipment,
    circuits and loads.
    """
    A = PermissibleValue(
        text="A",
        description="Phase A.",
        meaning=CIM["SinglePhaseKind.A"])
    B = PermissibleValue(
        text="B",
        description="Phase B.",
        meaning=CIM["SinglePhaseKind.B"])
    C = PermissibleValue(
        text="C",
        description="Phase C.",
        meaning=CIM["SinglePhaseKind.C"])
    E = PermissibleValue(
        text="E",
        description="""Earth. Denotes physical earth for conductor spacing or devices connected directly to earth (e.g. earthing reactors, pole ground, single wire earth return).""",
        meaning=CIM["SinglePhaseKind.E"])
    N = PermissibleValue(
        text="N",
        description="Neutral.",
        meaning=CIM["SinglePhaseKind.N"])
    X = PermissibleValue(
        text="X",
        description="Unknown. Floating phases or undetermined phasing.",
        meaning=CIM["SinglePhaseKind.X"])
    s1 = PermissibleValue(
        text="s1",
        description="Secondary phase 1.",
        meaning=CIM["SinglePhaseKind.s1"])
    s2 = PermissibleValue(
        text="s2",
        description="Secondary phase 2.",
        meaning=CIM["SinglePhaseKind.s2"])

    _defn = EnumDefinition(
        name="SinglePhaseKind",
        description="""Enumeration of phase identifiers used to designate the specific phase of conducting equipment modelled as individual unbalanced phases.Allows designation of specific phases for transmission and distribution equipment, circuits and loads.""",
    )

class SinglePhaseMachineKind(EnumDefinitionImpl):

    capacitorStartMotor = PermissibleValue(
        text="capacitorStartMotor",
        meaning=CIM["SinglePhaseMachineKind.capacitorStartMotor"])
    permanentSplitCapacitorMotor = PermissibleValue(
        text="permanentSplitCapacitorMotor",
        meaning=CIM["SinglePhaseMachineKind.permanentSplitCapacitorMotor"])
    shadedPoleMotor = PermissibleValue(
        text="shadedPoleMotor",
        meaning=CIM["SinglePhaseMachineKind.shadedPoleMotor"])
    splitPhaseMotor = PermissibleValue(
        text="splitPhaseMotor",
        meaning=CIM["SinglePhaseMachineKind.splitPhaseMotor"])
    squirrelCageInductionGenerator = PermissibleValue(
        text="squirrelCageInductionGenerator",
        meaning=CIM["SinglePhaseMachineKind.squirrelCageInductionGenerator"])

    _defn = EnumDefinition(
        name="SinglePhaseMachineKind",
    )

class SynchronousMachineKind(EnumDefinitionImpl):
    """
    Synchronous machine type.
    """
    condenser = PermissibleValue(
        text="condenser",
        description="Indicates the synchronous machine can operate as a condenser.",
        meaning=CIM["SynchronousMachineKind.condenser"])
    generator = PermissibleValue(
        text="generator",
        description="Indicates the synchronous machine can operate as a generator.",
        meaning=CIM["SynchronousMachineKind.generator"])
    generatorOrCondenser = PermissibleValue(
        text="generatorOrCondenser",
        description="Indicates the synchronous machine can operate as a generator or as a condenser.",
        meaning=CIM["SynchronousMachineKind.generatorOrCondenser"])
    generatorOrCondenserOrMotor = PermissibleValue(
        text="generatorOrCondenserOrMotor",
        description="Indicates the synchronous machine can operate as a generator or as a condenser or as a motor.",
        meaning=CIM["SynchronousMachineKind.generatorOrCondenserOrMotor"])
    generatorOrMotor = PermissibleValue(
        text="generatorOrMotor",
        description="Indicates the synchronous machine can operate as a generator or as a motor.",
        meaning=CIM["SynchronousMachineKind.generatorOrMotor"])
    motor = PermissibleValue(
        text="motor",
        description="Indicates the synchronous machine can operate as a motor.",
        meaning=CIM["SynchronousMachineKind.motor"])
    motorOrCondenser = PermissibleValue(
        text="motorOrCondenser",
        description="Indicates the synchronous machine can operate as a motor or as a condenser.",
        meaning=CIM["SynchronousMachineKind.motorOrCondenser"])

    _defn = EnumDefinition(
        name="SynchronousMachineKind",
        description="Synchronous machine type.",
    )

class SynchronousMachineOperatingMode(EnumDefinitionImpl):
    """
    Synchronous machine operating mode.
    """
    condenser = PermissibleValue(
        text="condenser",
        description="Operating as condenser.",
        meaning=CIM["SynchronousMachineOperatingMode.condenser"])
    generator = PermissibleValue(
        text="generator",
        description="Operating as generator.",
        meaning=CIM["SynchronousMachineOperatingMode.generator"])
    motor = PermissibleValue(
        text="motor",
        description="Operating as motor.",
        meaning=CIM["SynchronousMachineOperatingMode.motor"])

    _defn = EnumDefinition(
        name="SynchronousMachineOperatingMode",
        description="Synchronous machine operating mode.",
    )

class SynchrophaserUsageKind(EnumDefinitionImpl):

    measurement = PermissibleValue(
        text="measurement",
        meaning=CIM["SynchrophaserUsageKind.measurement"])
    protection = PermissibleValue(
        text="protection",
        meaning=CIM["SynchrophaserUsageKind.protection"])

    _defn = EnumDefinition(
        name="SynchrophaserUsageKind",
    )

class TimeSourceKind(EnumDefinitionImpl):

    atomicClock = PermissibleValue(
        text="atomicClock",
        description="local rubidium or cesium clock",
        meaning=CIM["TimeSourceKind.atomicClock"])
    crystalOscillator = PermissibleValue(
        text="crystalOscillator",
        description="quartz or other crystal oscillator",
        meaning=CIM["TimeSourceKind.crystalOscillator"])
    gnss = PermissibleValue(
        text="gnss",
        description="Other global navigation satellite systems, such as BeiDeo, Galileo, or GLONASS",
        meaning=CIM["TimeSourceKind.gnss"])
    gps = PermissibleValue(
        text="gps",
        description="global positioning system",
        meaning=CIM["TimeSourceKind.gps"])
    ntp = PermissibleValue(
        text="ntp",
        description="network time protocol",
        meaning=CIM["TimeSourceKind.ntp"])
    ptp = PermissibleValue(
        text="ptp",
        description="precision time protocol via IEEE Std. 1588",
        meaning=CIM["TimeSourceKind.ptp"])
    radioTime = PermissibleValue(
        text="radioTime",
        description="radio time source such WWVB or MSF",
        meaning=CIM["TimeSourceKind.radioTime"])

    _defn = EnumDefinition(
        name="TimeSourceKind",
    )

class TopologicalAreaKind(EnumDefinitionImpl):
    """
    Topological structure of an area
    """
    loop = PermissibleValue(
        text="loop",
        description="""Topological loop through a distribution circuit. May be created with an abnormal switching configuration.""",
        meaning=CIM["TopologicalAreaKind.loop"])
    meshed = PermissibleValue(
        text="meshed",
        description="Meshed topology found within transmission networks and urban low-voltage meshed networks.",
        meaning=CIM["TopologicalAreaKind.meshed"])
    radial = PermissibleValue(
        text="radial",
        description="Topologically radial area",
        meaning=CIM["TopologicalAreaKind.radial"])

    _defn = EnumDefinition(
        name="TopologicalAreaKind",
        description="Topological structure of an area",
    )

class TopologicalUsageKind(EnumDefinitionImpl):
    """
    Usage of switch as a boundary device across persistent connectivity areas, such as across a
    transmission-distribution boundary
    """
    acrossDistributionArea = PermissibleValue(
        text="acrossDistributionArea",
        description="""Denotes a tie switch (often normally-open) between two feeders served by different Normal Energizing Substation. Closing this switch could create a medium-voltage loop between transmission Topological Nodes.""",
        meaning=CIM["TopologicalUsageKind.acrossDistributionArea"])
    acrossFeederArea = PermissibleValue(
        text="acrossFeederArea",
        description="""Denotes a tie switch (often normally-open) between two feeders served by the same Normal Energizing Substation""",
        meaning=CIM["TopologicalUsageKind.acrossFeederArea"])
    acrossSwitchArea = PermissibleValue(
        text="acrossSwitchArea",
        description="Denotes recloser or sectionaliser used to divide a feeder into switch areas",
        meaning=CIM["TopologicalUsageKind.acrossSwitchArea"])
    acrossTDInterface = PermissibleValue(
        text="acrossTDInterface",
        description="""Denotes a boundary switch across a transmission-distribution interface. The switch may have multiple ownerships and may require consensus between entities to open/close.""",
        meaning=CIM["TopologicalUsageKind.acrossTDInterface"])
    acrossTransmissionArea = PermissibleValue(
        text="acrossTransmissionArea",
        description="""Denotes a switch serving as an ownership boundary between two transmission areas of responsibility. The switch may have multiple ownerships and may require consensus between entities to open/close.""",
        meaning=CIM["TopologicalUsageKind.acrossTransmissionArea"])
    busTie = PermissibleValue(
        text="busTie",
        description="""Denotes a bus tie switch in a transmission substation. May require Switch.Retained be set to True.""",
        meaning=CIM["TopologicalUsageKind.busTie"])
    bypass = PermissibleValue(
        text="bypass",
        description="""Denotes a bypass switch in a transmission substation, either for maintenance or to bypass a SeriesCompensator. May require Switch.Retained be set to True.""",
        meaning=CIM["TopologicalUsageKind.bypass"])

    _defn = EnumDefinition(
        name="TopologicalUsageKind",
        description="""Usage of switch as a boundary device across persistent connectivity areas, such as across a transmission-distribution boundary""",
    )

class UnitMultiplier(EnumDefinitionImpl):
    """
    The unit multipliers defined for the CIM. When applied to unit symbols, the unit symbol is treated as a derived
    unit. Regardless of the contents of the unit symbol text, the unit symbol shall be treated as if it were a
    single-character unit symbol. Unit symbols should not contain multipliers, and it should be left to the multiplier
    to define the multiple for an entire data type.For example, if a unit symbol is m2Pers and the multiplier is k,
    then the value is k(m**2/s), and the multiplier applies to the entire final value, not to any individual part of
    the value. This can be conceptualized by substituting a derived unit symbol for the unit type. If one imagines
    that the symbol &#222; represents the derived unit m2Pers, then applying the multiplier k can be conceptualized
    simply as k&#222;.For example, the SI unit for mass is kg and not g. If the unit symbol is defined as kg, then the
    multiplier is applied to kg as a whole and does not replace the k in front of the g. In this case, the multiplier
    of m would be used with the unit symbol of kg to represent one gram. As a text string, this violates the
    instructions in IEC 80000-1. However, because the unit symbol in CIM is treated as a derived unit instead of as an
    SI unit, it makes more sense to conceptualize the kg as if it were replaced by one of the proposed replacements
    for the SI mass symbol. If one imagines that the kg were replaced by a symbol &#222;, then it is easier to
    conceptualize the multiplier m as creating the proper unit m&#222;, and not the forbidden unit mkg.
    """
    E = PermissibleValue(
        text="E",
        description="Exa 10**18.",
        meaning=CIM["UnitMultiplier.E"])
    G = PermissibleValue(
        text="G",
        description="Giga 10**9.",
        meaning=CIM["UnitMultiplier.G"])
    M = PermissibleValue(
        text="M",
        description="Mega 10**6.",
        meaning=CIM["UnitMultiplier.M"])
    P = PermissibleValue(
        text="P",
        description="Peta 10**15.",
        meaning=CIM["UnitMultiplier.P"])
    T = PermissibleValue(
        text="T",
        description="Tera 10**12.",
        meaning=CIM["UnitMultiplier.T"])
    Y = PermissibleValue(
        text="Y",
        description="Yotta 10**24.",
        meaning=CIM["UnitMultiplier.Y"])
    Z = PermissibleValue(
        text="Z",
        description="Zetta 10**21.",
        meaning=CIM["UnitMultiplier.Z"])
    a = PermissibleValue(
        text="a",
        description="Atto 10**-18.",
        meaning=CIM["UnitMultiplier.a"])
    c = PermissibleValue(
        text="c",
        description="Centi 10**-2.",
        meaning=CIM["UnitMultiplier.c"])
    d = PermissibleValue(
        text="d",
        description="Deci 10**-1.",
        meaning=CIM["UnitMultiplier.d"])
    da = PermissibleValue(
        text="da",
        description="Deca 10**1.",
        meaning=CIM["UnitMultiplier.da"])
    f = PermissibleValue(
        text="f",
        description="Femto 10**-15.",
        meaning=CIM["UnitMultiplier.f"])
    h = PermissibleValue(
        text="h",
        description="Hecto 10**2.",
        meaning=CIM["UnitMultiplier.h"])
    k = PermissibleValue(
        text="k",
        description="Kilo 10**3.",
        meaning=CIM["UnitMultiplier.k"])
    m = PermissibleValue(
        text="m",
        description="Milli 10**-3.",
        meaning=CIM["UnitMultiplier.m"])
    micro = PermissibleValue(
        text="micro",
        description="Micro 10**-6.",
        meaning=CIM["UnitMultiplier.micro"])
    n = PermissibleValue(
        text="n",
        description="Nano 10**-9.",
        meaning=CIM["UnitMultiplier.n"])
    none = PermissibleValue(
        text="none",
        description="No multiplier or equivalently multiply by 1.",
        meaning=CIM["UnitMultiplier.none"])
    p = PermissibleValue(
        text="p",
        description="Pico 10**-12.",
        meaning=CIM["UnitMultiplier.p"])
    y = PermissibleValue(
        text="y",
        description="Yocto 10**-24.",
        meaning=CIM["UnitMultiplier.y"])
    z = PermissibleValue(
        text="z",
        description="Zepto 10**-21.",
        meaning=CIM["UnitMultiplier.z"])

    _defn = EnumDefinition(
        name="UnitMultiplier",
        description="""The unit multipliers defined for the CIM. When applied to unit symbols, the unit symbol is treated as a derived unit. Regardless of the contents of the unit symbol text, the unit symbol shall be treated as if it were a single-character unit symbol. Unit symbols should not contain multipliers, and it should be left to the multiplier to define the multiple for an entire data type.For example, if a unit symbol is m2Pers and the multiplier is k, then the value is k(m**2/s), and the multiplier applies to the entire final value, not to any individual part of the value. This can be conceptualized by substituting a derived unit symbol for the unit type. If one imagines that the symbol &#222; represents the derived unit m2Pers, then applying the multiplier k can be conceptualized simply as k&#222;.For example, the SI unit for mass is kg and not g.  If the unit symbol is defined as kg, then the multiplier is applied to kg as a whole and does not replace the k in front of the g. In this case, the multiplier of m would be used with the unit symbol of kg to represent one gram.  As a text string, this violates the instructions in IEC 80000-1. However, because the unit symbol in CIM is treated as a derived unit instead of as an SI unit, it makes more sense to conceptualize the kg as if it were replaced by one of the proposed replacements for the SI mass symbol. If one imagines that the kg were replaced by a symbol &#222;, then it is easier to conceptualize the multiplier m as creating the proper unit m&#222;, and not the forbidden unit mkg.""",
    )

class UnitSymbol(EnumDefinitionImpl):
    """
    The derived units defined for usage in the CIM. In some cases, the derived unit is equal to an SI unit. Whenever
    possible, the standard derived symbol is used instead of the formula for the derived unit. For example, the unit
    symbol Farad is defined as F instead of CPerV. In cases where a standard symbol does not exist for a derived unit,
    the formula for the unit is used as the unit symbol. For example, density does not have a standard symbol and so
    it is represented as kgPerm^3. With the exception of the kg, which is an SI unit, the unit symbols do not contain
    multipliers and therefore represent the base derived unit to which a multiplier can be applied as a whole.Every
    unit symbol is treated as an unparseable text as if it were a single-letter symbol. The meaning of each unit
    symbol is defined by the accompanying descriptive text and not by the text contents of the unit symbol.To allow
    the widest possible range of serializations without requiring special character handling, several substitutions
    are made which deviate from the format described in IEC 80000-1. The division symbol / is replaced by the letters
    Per. Exponents are written in plain text after the unit as m^3. The letters deg are used instead of the degree
    symbol. Any clarification of the meaning for a substitution is included in the description for the unit
    symbol.Non-SI units are included in list of unit symbols to allow sources of data to be correctly labelled with
    their non-SI units (for example, a GPS sensor that is reporting numbers that represent feet instead of meters).
    This allows software to use the unit symbol information correctly convert and scale the raw data of those sources
    into SI-based units.The integer values are used for harmonization with IEC 61850.
    """
    A = PermissibleValue(
        text="A",
        description="Current in amperes.",
        meaning=CIM["UnitSymbol.A"])
    A2 = PermissibleValue(
        text="A2",
        description="Amperes squared (A^2).",
        meaning=CIM["UnitSymbol.A2"])
    A2h = PermissibleValue(
        text="A2h",
        description="Ampere-squared hour, ampere-squared hour.",
        meaning=CIM["UnitSymbol.A2h"])
    A2s = PermissibleValue(
        text="A2s",
        description="Ampere squared time in square amperes (A^2*s).",
        meaning=CIM["UnitSymbol.A2s"])
    APerA = PermissibleValue(
        text="APerA",
        description="Current, ratio of amperages.",
        meaning=CIM["UnitSymbol.APerA"])
    APerm = PermissibleValue(
        text="APerm",
        description="Amperes per metre (A/m), magnetic field strength.",
        meaning=CIM["UnitSymbol.APerm"])
    Ah = PermissibleValue(
        text="Ah",
        description="Ampere-hours, ampere-hours.",
        meaning=CIM["UnitSymbol.Ah"])
    As = PermissibleValue(
        text="As",
        description="Ampere seconds (A*s).",
        meaning=CIM["UnitSymbol.As"])
    Bq = PermissibleValue(
        text="Bq",
        description="Radioactivity in becquerels (1/s).",
        meaning=CIM["UnitSymbol.Bq"])
    Btu = PermissibleValue(
        text="Btu",
        description="Energy, British Thermal Units.",
        meaning=CIM["UnitSymbol.Btu"])
    C = PermissibleValue(
        text="C",
        description="Electric charge in coulombs (A*s).",
        meaning=CIM["UnitSymbol.C"])
    CPerkg = PermissibleValue(
        text="CPerkg",
        description="Exposure (x rays), coulombs per kilogram.",
        meaning=CIM["UnitSymbol.CPerkg"])
    CPerm2 = PermissibleValue(
        text="CPerm2",
        description="Surface charge density, coulombs per square metre.",
        meaning=CIM["UnitSymbol.CPerm2"])
    CPerm3 = PermissibleValue(
        text="CPerm3",
        description="Electric charge density, coulombs per cubic metre.",
        meaning=CIM["UnitSymbol.CPerm3"])
    F = PermissibleValue(
        text="F",
        description="Electric capacitance in farads (C/V).",
        meaning=CIM["UnitSymbol.F"])
    FPerm = PermissibleValue(
        text="FPerm",
        description="Permittivity, farads per metre.",
        meaning=CIM["UnitSymbol.FPerm"])
    G = PermissibleValue(
        text="G",
        description="Magnetic flux density, gausses (1 G = 10e-4*T).",
        meaning=CIM["UnitSymbol.G"])
    Gy = PermissibleValue(
        text="Gy",
        description="Absorbed dose in grays (J/kg).",
        meaning=CIM["UnitSymbol.Gy"])
    GyPers = PermissibleValue(
        text="GyPers",
        description="Absorbed dose rate, grays per second.",
        meaning=CIM["UnitSymbol.GyPers"])
    H = PermissibleValue(
        text="H",
        description="Electric inductance in henrys (Wb/A).",
        meaning=CIM["UnitSymbol.H"])
    HPerm = PermissibleValue(
        text="HPerm",
        description="Permeability, henrys per metre.",
        meaning=CIM["UnitSymbol.HPerm"])
    Hz = PermissibleValue(
        text="Hz",
        description="Frequency in hertz (1/s).",
        meaning=CIM["UnitSymbol.Hz"])
    HzPerHz = PermissibleValue(
        text="HzPerHz",
        description="Frequency, rate of frequency change.",
        meaning=CIM["UnitSymbol.HzPerHz"])
    HzPers = PermissibleValue(
        text="HzPers",
        description="Rate of change of frequency in hertz per second.",
        meaning=CIM["UnitSymbol.HzPers"])
    J = PermissibleValue(
        text="J",
        description="Energy in joules (N*m = C*V = W*s).",
        meaning=CIM["UnitSymbol.J"])
    JPerK = PermissibleValue(
        text="JPerK",
        description="Heat capacity in joules/kelvin.",
        meaning=CIM["UnitSymbol.JPerK"])
    JPerkg = PermissibleValue(
        text="JPerkg",
        description="Specific energy, J/kg.",
        meaning=CIM["UnitSymbol.JPerkg"])
    JPerkgK = PermissibleValue(
        text="JPerkgK",
        description="Specific heat capacity, specific entropy, joules per kilogram Kelvin.",
        meaning=CIM["UnitSymbol.JPerkgK"])
    JPerm2 = PermissibleValue(
        text="JPerm2",
        description="Insulation energy density, joules per square metre or watt second per square metre.",
        meaning=CIM["UnitSymbol.JPerm2"])
    JPerm3 = PermissibleValue(
        text="JPerm3",
        description="Energy density, joules per cubic metre.",
        meaning=CIM["UnitSymbol.JPerm3"])
    JPermol = PermissibleValue(
        text="JPermol",
        description="Molar energy, joules per mole.",
        meaning=CIM["UnitSymbol.JPermol"])
    JPermolK = PermissibleValue(
        text="JPermolK",
        description="Molar entropy, molar heat capacity, joules per mole kelvin.",
        meaning=CIM["UnitSymbol.JPermolK"])
    JPers = PermissibleValue(
        text="JPers",
        description="Energy rate in joules per second (J/s).",
        meaning=CIM["UnitSymbol.JPers"])
    K = PermissibleValue(
        text="K",
        description="Temperature in kelvins.",
        meaning=CIM["UnitSymbol.K"])
    KPers = PermissibleValue(
        text="KPers",
        description="Temperature change rate in kelvins per second.",
        meaning=CIM["UnitSymbol.KPers"])
    M = PermissibleValue(
        text="M",
        description="Length, nautical miles (1 M = 1852 m).",
        meaning=CIM["UnitSymbol.M"])
    Mx = PermissibleValue(
        text="Mx",
        description="Magnetic flux, maxwells (1 Mx = 10-8 Wb).",
        meaning=CIM["UnitSymbol.Mx"])
    N = PermissibleValue(
        text="N",
        description="Force in newtons (kg*m/s^2).",
        meaning=CIM["UnitSymbol.N"])
    NPerm = PermissibleValue(
        text="NPerm",
        description="Surface tension, newton per metre.",
        meaning=CIM["UnitSymbol.NPerm"])
    Nm = PermissibleValue(
        text="Nm",
        description="Moment of force, newton metres.",
        meaning=CIM["UnitSymbol.Nm"])
    Oe = PermissibleValue(
        text="Oe",
        description="Magnetic field in oersteds, (1 Oe = (10^3/(4*pi)) A/m = 79.57747 A/m).",
        meaning=CIM["UnitSymbol.Oe"])
    Pa = PermissibleValue(
        text="Pa",
        description="""Pressure in pascals (N/m^2). Note: the absolute or relative measurement of pressure is implied with this entry. See below for more explicit forms.""",
        meaning=CIM["UnitSymbol.Pa"])
    PaPers = PermissibleValue(
        text="PaPers",
        description="Pressure change rate in pascals per second.",
        meaning=CIM["UnitSymbol.PaPers"])
    Pas = PermissibleValue(
        text="Pas",
        description="Dynamic viscosity, pascal seconds.",
        meaning=CIM["UnitSymbol.Pas"])
    Q = PermissibleValue(
        text="Q",
        description="Quantity power, Q.",
        meaning=CIM["UnitSymbol.Q"])
    Qh = PermissibleValue(
        text="Qh",
        description="Quantity energy, Qh.",
        meaning=CIM["UnitSymbol.Qh"])
    S = PermissibleValue(
        text="S",
        description="Conductance in siemens.",
        meaning=CIM["UnitSymbol.S"])
    SPerm = PermissibleValue(
        text="SPerm",
        description="Conductance per length (F/m).",
        meaning=CIM["UnitSymbol.SPerm"])
    Sv = PermissibleValue(
        text="Sv",
        description="Dose equivalent in sieverts (J/kg).",
        meaning=CIM["UnitSymbol.Sv"])
    T = PermissibleValue(
        text="T",
        description="Magnetic flux density in teslas (Wb/m^2).",
        meaning=CIM["UnitSymbol.T"])
    V = PermissibleValue(
        text="V",
        description="Electric potential in volts (W/A).",
        meaning=CIM["UnitSymbol.V"])
    V2 = PermissibleValue(
        text="V2",
        description="Volt squared (W^2/A^2).",
        meaning=CIM["UnitSymbol.V2"])
    V2h = PermissibleValue(
        text="V2h",
        description="Volt-squared hour, volt-squared-hours.",
        meaning=CIM["UnitSymbol.V2h"])
    VA = PermissibleValue(
        text="VA",
        description="Apparent power in volt amperes. See also real power and reactive power.",
        meaning=CIM["UnitSymbol.VA"])
    VAh = PermissibleValue(
        text="VAh",
        description="Apparent energy in volt ampere hours.",
        meaning=CIM["UnitSymbol.VAh"])
    VAr = PermissibleValue(
        text="VAr",
        description="""Reactive power in volt amperes reactive. The reactive or imaginary component of electrical power (V*I*sin(phi)). (See also real power and apparent power).Note: Different meter designs use different methods to arrive at their results. Some meters may compute reactive power as an arithmetic value, while others compute the value vectorially. The data consumer should determine the method in use and the suitability of the measurement for the intended purpose.""",
        meaning=CIM["UnitSymbol.VAr"])
    VArh = PermissibleValue(
        text="VArh",
        description="Reactive energy in volt ampere reactive hours.",
        meaning=CIM["UnitSymbol.VArh"])
    VPerHz = PermissibleValue(
        text="VPerHz",
        description="Magnetic flux in volt per hertz.",
        meaning=CIM["UnitSymbol.VPerHz"])
    VPerV = PermissibleValue(
        text="VPerV",
        description="Voltage, ratio of voltages.",
        meaning=CIM["UnitSymbol.VPerV"])
    VPerVA = PermissibleValue(
        text="VPerVA",
        description="""Power factor, PF, the ratio of the active power to the apparent power.  Note: The sign convention used for power factor will differ between IEC meters and EEI (ANSI) meters. It is assumed that the data consumers understand the type of meter being used and agree on the sign convention in use at any given utility.""",
        meaning=CIM["UnitSymbol.VPerVA"])
    VPerVAr = PermissibleValue(
        text="VPerVAr",
        description="""Power factor, PF, the ratio of the active power to the apparent power. Note: The sign convention used for power factor will differ between IEC meters and EEI (ANSI) meters. It is assumed that the data consumers understand the type of meter being used and agree on the sign convention in use at any given utility.""",
        meaning=CIM["UnitSymbol.VPerVAr"])
    VPerm = PermissibleValue(
        text="VPerm",
        description="Electric field strength, volts per metre.",
        meaning=CIM["UnitSymbol.VPerm"])
    Vh = PermissibleValue(
        text="Vh",
        description="Volt-hour, Volt hours.",
        meaning=CIM["UnitSymbol.Vh"])
    Vs = PermissibleValue(
        text="Vs",
        description="Volt seconds (Ws/A).",
        meaning=CIM["UnitSymbol.Vs"])
    W = PermissibleValue(
        text="W",
        description="""Real power in watts (J/s). Electrical power may have real and reactive components. The real portion of electrical power (I^2*R or V*I*cos(phi)), is expressed in Watts. See also apparent power and reactive power.""",
        meaning=CIM["UnitSymbol.W"])
    WPerA = PermissibleValue(
        text="WPerA",
        description="Active power per current flow, watts per Ampere.",
        meaning=CIM["UnitSymbol.WPerA"])
    WPerW = PermissibleValue(
        text="WPerW",
        description="Signal Strength, ratio of power.",
        meaning=CIM["UnitSymbol.WPerW"])
    WPerm2 = PermissibleValue(
        text="WPerm2",
        description="Heat flux density, irradiance, watts per square metre.",
        meaning=CIM["UnitSymbol.WPerm2"])
    WPerm2sr = PermissibleValue(
        text="WPerm2sr",
        description="Radiance, watts per square metre steradian.",
        meaning=CIM["UnitSymbol.WPerm2sr"])
    WPermK = PermissibleValue(
        text="WPermK",
        description="Thermal conductivity in watt/metres kelvin.",
        meaning=CIM["UnitSymbol.WPermK"])
    WPers = PermissibleValue(
        text="WPers",
        description="Ramp rate in watts per second.",
        meaning=CIM["UnitSymbol.WPers"])
    WPersr = PermissibleValue(
        text="WPersr",
        description="Radiant intensity, watts per steradian.",
        meaning=CIM["UnitSymbol.WPersr"])
    Wb = PermissibleValue(
        text="Wb",
        description="Magnetic flux in webers (V*s).",
        meaning=CIM["UnitSymbol.Wb"])
    Wh = PermissibleValue(
        text="Wh",
        description="Real energy in watt hours.",
        meaning=CIM["UnitSymbol.Wh"])
    anglemin = PermissibleValue(
        text="anglemin",
        description="Plane angle, minutes.",
        meaning=CIM["UnitSymbol.anglemin"])
    anglesec = PermissibleValue(
        text="anglesec",
        description="Plane angle, seconds.",
        meaning=CIM["UnitSymbol.anglesec"])
    bar = PermissibleValue(
        text="bar",
        description="Pressure in bars, (1 bar = 100 kPa).",
        meaning=CIM["UnitSymbol.bar"])
    cd = PermissibleValue(
        text="cd",
        description="Luminous intensity in candelas.",
        meaning=CIM["UnitSymbol.cd"])
    charPers = PermissibleValue(
        text="charPers",
        description="Data rate (baud) in characters per second.",
        meaning=CIM["UnitSymbol.charPers"])
    character = PermissibleValue(
        text="character",
        description="Number of characters.",
        meaning=CIM["UnitSymbol.character"])
    cosPhi = PermissibleValue(
        text="cosPhi",
        description="""Power factor, dimensionless.Note 1: This definition of power factor only holds for balanced systems. See the alternative definition under code 153.Note 2�: Beware of differing sign conventions in use between the IEC and EEI. It is assumed that the data consumer understands the type of meter in use and the sign convention in use by the utility.""",
        meaning=CIM["UnitSymbol.cosPhi"])
    count = PermissibleValue(
        text="count",
        description="Amount of substance, counter value.",
        meaning=CIM["UnitSymbol.count"])
    d = PermissibleValue(
        text="d",
        description="Time in days, day = 24 h = 86400 s.",
        meaning=CIM["UnitSymbol.d"])
    dB = PermissibleValue(
        text="dB",
        description="""Sound pressure level in decibels. Note:  multiplier d is included in this unit symbol for compatibility with IEC 61850-7-3.""",
        meaning=CIM["UnitSymbol.dB"])
    dBm = PermissibleValue(
        text="dBm",
        description="""Power level (logarithmic ratio of signal strength , Bel-mW), normalized to 1 mW. Note:  multiplier d is included in this unit symbol for compatibility with IEC 61850-7-3.""",
        meaning=CIM["UnitSymbol.dBm"])
    deg = PermissibleValue(
        text="deg",
        description="Plane angle in degrees.",
        meaning=CIM["UnitSymbol.deg"])
    degC = PermissibleValue(
        text="degC",
        description="Relative temperature in degrees Celsius (degC).",
        meaning=CIM["UnitSymbol.degC"])
    ft3 = PermissibleValue(
        text="ft3",
        description="Volume, cubic feet.",
        meaning=CIM["UnitSymbol.ft3"])
    gPerg = PermissibleValue(
        text="gPerg",
        description="Concentration, The ratio of the mass of a solute divided by the mass of  the solution.",
        meaning=CIM["UnitSymbol.gPerg"])
    gal = PermissibleValue(
        text="gal",
        description="Volume in gallons, US gallon (1 gal = 231 in^3 = 128 fl ounce).",
        meaning=CIM["UnitSymbol.gal"])
    h = PermissibleValue(
        text="h",
        description="Time in hours, hour = 60 min = 3600 s.",
        meaning=CIM["UnitSymbol.h"])
    ha = PermissibleValue(
        text="ha",
        description="Area, hectares.",
        meaning=CIM["UnitSymbol.ha"])
    kat = PermissibleValue(
        text="kat",
        description="Catalytic activity, katal = mol/s.",
        meaning=CIM["UnitSymbol.kat"])
    katPerm3 = PermissibleValue(
        text="katPerm3",
        description="Catalytic activity concentration, katals per cubic metre.",
        meaning=CIM["UnitSymbol.katPerm3"])
    kg = PermissibleValue(
        text="kg",
        description="""Mass in kilograms. Note: multiplier k is included in this unit symbol for compatibility with IEC 61850-7-3.""",
        meaning=CIM["UnitSymbol.kg"])
    kgPerJ = PermissibleValue(
        text="kgPerJ",
        description="""Weight per energy in kilograms per joule (kg/J). Note: multiplier k is included in this unit symbol for compatibility with IEC 61850-7-3.""",
        meaning=CIM["UnitSymbol.kgPerJ"])
    kgPerm = PermissibleValue(
        text="kgPerm",
        description="""Mass per length in kilogram/metres (kg/m). Note: multiplier k is included in this unit symbol for compatibility with mass datatype.""",
        meaning=CIM["UnitSymbol.kgPerm"])
    kgPerm3 = PermissibleValue(
        text="kgPerm3",
        description="""Density in kilogram/cubic metres (kg/m^3). Note: multiplier k is included in this unit symbol for compatibility with IEC 61850-7-3.""",
        meaning=CIM["UnitSymbol.kgPerm3"])
    kgm = PermissibleValue(
        text="kgm",
        description="""Moment of mass in kilogram metres (kg*m) (first moment of mass). Note: multiplier k is included in this unit symbol for compatibility with IEC 61850-7-3.""",
        meaning=CIM["UnitSymbol.kgm"])
    kgm2 = PermissibleValue(
        text="kgm2",
        description="""Moment of mass in kilogram square metres (kg*m^2) (Second moment of mass, commonly called the moment of inertia). Note: multiplier k is included in this unit symbol for compatibility with IEC 61850-7-3.""",
        meaning=CIM["UnitSymbol.kgm2"])
    kn = PermissibleValue(
        text="kn",
        description="Speed, knots (1 kn = 1852/3600) m/s.",
        meaning=CIM["UnitSymbol.kn"])
    l = PermissibleValue(
        text="l",
        description="Volume in litres, litre = dm^3 = m^3/1000.",
        meaning=CIM["UnitSymbol.l"])
    lPerh = PermissibleValue(
        text="lPerh",
        description="Volumetric flow rate, litres per hour.",
        meaning=CIM["UnitSymbol.lPerh"])
    lPerl = PermissibleValue(
        text="lPerl",
        description="Concentration, The ratio of the volume of a solute divided by the volume of  the solution.",
        meaning=CIM["UnitSymbol.lPerl"])
    lPers = PermissibleValue(
        text="lPers",
        description="Volumetric flow rate in litres per second.",
        meaning=CIM["UnitSymbol.lPers"])
    lm = PermissibleValue(
        text="lm",
        description="Luminous flux in lumens (cd*sr).",
        meaning=CIM["UnitSymbol.lm"])
    lx = PermissibleValue(
        text="lx",
        description="Illuminance in lux (lm/m^2).",
        meaning=CIM["UnitSymbol.lx"])
    m = PermissibleValue(
        text="m",
        description="Length in metres.",
        meaning=CIM["UnitSymbol.m"])
    m2 = PermissibleValue(
        text="m2",
        description="Area in square metres (m^2).",
        meaning=CIM["UnitSymbol.m2"])
    m2Pers = PermissibleValue(
        text="m2Pers",
        description="Viscosity in square metres/second (m^2/s).",
        meaning=CIM["UnitSymbol.m2Pers"])
    m3 = PermissibleValue(
        text="m3",
        description="Volume in cubic metres (m^3).",
        meaning=CIM["UnitSymbol.m3"])
    m3Compensated = PermissibleValue(
        text="m3Compensated",
        description="Volume, cubic metres, with the value compensated for weather effects.",
        meaning=CIM["UnitSymbol.m3Compensated"])
    m3Perh = PermissibleValue(
        text="m3Perh",
        description="Volumetric flow rate, cubic metres per hour.",
        meaning=CIM["UnitSymbol.m3Perh"])
    m3Perkg = PermissibleValue(
        text="m3Perkg",
        description="Specific volume, cubic metres per kilogram, v.",
        meaning=CIM["UnitSymbol.m3Perkg"])
    m3Pers = PermissibleValue(
        text="m3Pers",
        description="Volumetric flow rate in cubic metres per second (m^3/s).",
        meaning=CIM["UnitSymbol.m3Pers"])
    m3Uncompensated = PermissibleValue(
        text="m3Uncompensated",
        description="Volume, cubic metres, with the value uncompensated for weather effects.",
        meaning=CIM["UnitSymbol.m3Uncompensated"])
    mPerm3 = PermissibleValue(
        text="mPerm3",
        description="Fuel efficiency in metres per cubic metres (m/m^3).",
        meaning=CIM["UnitSymbol.mPerm3"])
    mPers = PermissibleValue(
        text="mPers",
        description="Velocity in metres per second (m/s).",
        meaning=CIM["UnitSymbol.mPers"])
    mPers2 = PermissibleValue(
        text="mPers2",
        description="Acceleration in metres per second squared (m/s^2).",
        meaning=CIM["UnitSymbol.mPers2"])
    min = PermissibleValue(
        text="min",
        description="Time in minutes, minute  = 60 s.",
        meaning=CIM["UnitSymbol.min"])
    mmHg = PermissibleValue(
        text="mmHg",
        description="Pressure, millimetres of mercury (1 mmHg is approximately 133.3 Pa).",
        meaning=CIM["UnitSymbol.mmHg"])
    mol = PermissibleValue(
        text="mol",
        description="Amount of substance in moles.",
        meaning=CIM["UnitSymbol.mol"])
    molPerkg = PermissibleValue(
        text="molPerkg",
        description="Concentration, Molality, the amount of solute in moles and the amount of solvent in kilograms.",
        meaning=CIM["UnitSymbol.molPerkg"])
    molPerm3 = PermissibleValue(
        text="molPerm3",
        description="""Concentration, The amount of substance concentration, (c), the amount of solvent in moles divided by the volume of solution in m^3.""",
        meaning=CIM["UnitSymbol.molPerm3"])
    molPermol = PermissibleValue(
        text="molPermol",
        description="""Concentration, Molar fraction, the ratio of the molar amount of a solute divided by the molar amount of the solution.""",
        meaning=CIM["UnitSymbol.molPermol"])
    none = PermissibleValue(
        text="none",
        description="Dimension less quantity, e.g. count, per unit, etc.",
        meaning=CIM["UnitSymbol.none"])
    ohm = PermissibleValue(
        text="ohm",
        description="Electric resistance in ohms (V/A).",
        meaning=CIM["UnitSymbol.ohm"])
    ohmPerm = PermissibleValue(
        text="ohmPerm",
        description="Electric resistance per length in ohms per metre ((V/A)/m).",
        meaning=CIM["UnitSymbol.ohmPerm"])
    ohmm = PermissibleValue(
        text="ohmm",
        description="Resistivity, ohm metres, (rho).",
        meaning=CIM["UnitSymbol.ohmm"])
    onePerHz = PermissibleValue(
        text="onePerHz",
        description="Reciprocal of frequency (1/Hz).",
        meaning=CIM["UnitSymbol.onePerHz"])
    onePerm = PermissibleValue(
        text="onePerm",
        description="Wavenumber, reciprocal metres,  (1/m).",
        meaning=CIM["UnitSymbol.onePerm"])
    ppm = PermissibleValue(
        text="ppm",
        description="Concentration in parts per million.",
        meaning=CIM["UnitSymbol.ppm"])
    rad = PermissibleValue(
        text="rad",
        description="Plane angle in radians (m/m).",
        meaning=CIM["UnitSymbol.rad"])
    radPers = PermissibleValue(
        text="radPers",
        description="Angular velocity in radians per second (rad/s).",
        meaning=CIM["UnitSymbol.radPers"])
    radPers2 = PermissibleValue(
        text="radPers2",
        description="Angular acceleration, radians per second squared.",
        meaning=CIM["UnitSymbol.radPers2"])
    rev = PermissibleValue(
        text="rev",
        description="Amount of rotation, revolutions.",
        meaning=CIM["UnitSymbol.rev"])
    rotPers = PermissibleValue(
        text="rotPers",
        description="Rotations per second (1/s). See also Hz (1/s).",
        meaning=CIM["UnitSymbol.rotPers"])
    s = PermissibleValue(
        text="s",
        description="Time in seconds.",
        meaning=CIM["UnitSymbol.s"])
    sPers = PermissibleValue(
        text="sPers",
        description="Time, Ratio of time.",
        meaning=CIM["UnitSymbol.sPers"])
    sr = PermissibleValue(
        text="sr",
        description="Solid angle in steradians (m^2/m^2).",
        meaning=CIM["UnitSymbol.sr"])
    therm = PermissibleValue(
        text="therm",
        description="Energy, therms.",
        meaning=CIM["UnitSymbol.therm"])
    tonne = PermissibleValue(
        text="tonne",
        description="Mass in tons, tonne or metric ton (1000 kg = 1 Mg).",
        meaning=CIM["UnitSymbol.tonne"])

    _defn = EnumDefinition(
        name="UnitSymbol",
        description="""The derived units defined for usage in the CIM. In some cases, the derived unit is equal to an SI unit. Whenever possible, the standard derived symbol is used instead of the formula for the derived unit. For example, the unit symbol Farad is defined as F instead of CPerV. In cases where a standard symbol does not exist for a derived unit, the formula for the unit is used as the unit symbol. For example, density does not have a standard symbol and so it is represented as kgPerm^3. With the exception of the kg, which is an SI unit, the unit symbols do not contain multipliers and therefore represent the base derived unit to which a multiplier can be applied as a whole.Every unit symbol is treated as an unparseable text as if it were a single-letter symbol. The meaning of each unit symbol is defined by the accompanying descriptive text and not by the text contents of the unit symbol.To allow the widest possible range of serializations without requiring special character handling, several substitutions are made which deviate from the format described in IEC 80000-1. The division symbol / is replaced by the letters Per. Exponents are written in plain text after the unit as m^3. The letters deg are used instead of the degree symbol. Any clarification of the meaning for a substitution is included in the description for the unit symbol.Non-SI units are included in list of unit symbols to allow sources of data to be correctly labelled with their non-SI units (for example, a GPS sensor that is reporting numbers that represent feet instead of meters). This allows software to use the unit symbol information correctly convert and scale the raw data of those sources into SI-based units.The integer values are used for harmonization with IEC 61850.""",
    )

class WindGenUnitKind(EnumDefinitionImpl):
    """
    Kind of wind generating unit.
    """
    offshore = PermissibleValue(
        text="offshore",
        description="The wind generating unit is located offshore.",
        meaning=CIM["WindGenUnitKind.offshore"])
    onshore = PermissibleValue(
        text="onshore",
        description="The wind generating unit is located onshore.",
        meaning=CIM["WindGenUnitKind.onshore"])

    _defn = EnumDefinition(
        name="WindGenUnitKind",
        description="Kind of wind generating unit.",
    )

class WindingConnection(EnumDefinitionImpl):
    """
    Winding connection type.
    """
    A = PermissibleValue(
        text="A",
        description="Autotransformer common winding.",
        meaning=CIM["WindingConnection.A"])
    D = PermissibleValue(
        text="D",
        description="Delta.",
        meaning=CIM["WindingConnection.D"])
    I = PermissibleValue(
        text="I",
        description="Independent winding, for single-phase connections.",
        meaning=CIM["WindingConnection.I"])
    Y = PermissibleValue(
        text="Y",
        description="Wye.",
        meaning=CIM["WindingConnection.Y"])
    Yn = PermissibleValue(
        text="Yn",
        description="Wye, with neutral brought out for grounding.",
        meaning=CIM["WindingConnection.Yn"])
    Z = PermissibleValue(
        text="Z",
        description="ZigZag.",
        meaning=CIM["WindingConnection.Z"])
    Zn = PermissibleValue(
        text="Zn",
        description="ZigZag, with neutral brought out for grounding.",
        meaning=CIM["WindingConnection.Zn"])

    _defn = EnumDefinition(
        name="WindingConnection",
        description="Winding connection type.",
    )

class WireConstructionKind(EnumDefinitionImpl):
    """
    Kind of cable construction.
    """
    annular = PermissibleValue(
        text="annular",
        meaning=CIM["WireConstructionKind.annular"])
    bunch = PermissibleValue(
        text="bunch",
        meaning=CIM["WireConstructionKind.bunch"])
    compacted = PermissibleValue(
        text="compacted",
        meaning=CIM["WireConstructionKind.compacted"])
    compressed = PermissibleValue(
        text="compressed",
        meaning=CIM["WireConstructionKind.compressed"])
    concentric = PermissibleValue(
        text="concentric",
        meaning=CIM["WireConstructionKind.concentric"])
    other = PermissibleValue(
        text="other",
        description="Other kind of cable construction.",
        meaning=CIM["WireConstructionKind.other"])
    segmental = PermissibleValue(
        text="segmental",
        meaning=CIM["WireConstructionKind.segmental"])
    solid = PermissibleValue(
        text="solid",
        description="Solid cable.",
        meaning=CIM["WireConstructionKind.solid"])
    stranded = PermissibleValue(
        text="stranded",
        description="Stranded cable.",
        meaning=CIM["WireConstructionKind.stranded"])

    _defn = EnumDefinition(
        name="WireConstructionKind",
        description="Kind of cable construction.",
    )

class WireInstallationKind(EnumDefinitionImpl):

    overheadBare = PermissibleValue(
        text="overheadBare",
        meaning=CIM["WireInstallationKind.overheadBare"])
    overheadSpacerCable = PermissibleValue(
        text="overheadSpacerCable",
        meaning=CIM["WireInstallationKind.overheadSpacerCable"])
    overheadTreeWire = PermissibleValue(
        text="overheadTreeWire",
        meaning=CIM["WireInstallationKind.overheadTreeWire"])
    undergroundConduit = PermissibleValue(
        text="undergroundConduit",
        meaning=CIM["WireInstallationKind.undergroundConduit"])
    undergroundDirectBury = PermissibleValue(
        text="undergroundDirectBury",
        meaning=CIM["WireInstallationKind.undergroundDirectBury"])
    undergroundDuctBank = PermissibleValue(
        text="undergroundDuctBank",
        meaning=CIM["WireInstallationKind.undergroundDuctBank"])

    _defn = EnumDefinition(
        name="WireInstallationKind",
    )

class WireInsulationKind(EnumDefinitionImpl):
    """
    Kind of wire insulation.
    """
    asbestosAndVarnishedCambric = PermissibleValue(
        text="asbestosAndVarnishedCambric",
        description="Asbestos and varnished cambric wire insulation.",
        meaning=CIM["WireInsulationKind.asbestosAndVarnishedCambric"])
    beltedPilc = PermissibleValue(
        text="beltedPilc",
        description="Belted pilc wire insulation.",
        meaning=CIM["WireInsulationKind.beltedPilc"])
    butyl = PermissibleValue(
        text="butyl",
        description="Butyl wire insulation.",
        meaning=CIM["WireInsulationKind.butyl"])
    crosslinkedPolyethylene = PermissibleValue(
        text="crosslinkedPolyethylene",
        description="Crosslinked polyethylene wire insulation.",
        meaning=CIM["WireInsulationKind.crosslinkedPolyethylene"])
    ethylenePropyleneRubber = PermissibleValue(
        text="ethylenePropyleneRubber",
        description="Ethylene propylene rubber wire insulation.",
        meaning=CIM["WireInsulationKind.ethylenePropyleneRubber"])
    highMolecularWeightPolyethylene = PermissibleValue(
        text="highMolecularWeightPolyethylene",
        description="High nolecular weight polyethylene wire insulation.",
        meaning=CIM["WireInsulationKind.highMolecularWeightPolyethylene"])
    highPressureFluidFilled = PermissibleValue(
        text="highPressureFluidFilled",
        description="High pressure fluid filled wire insulation.",
        meaning=CIM["WireInsulationKind.highPressureFluidFilled"])
    lowCapacitanceRubber = PermissibleValue(
        text="lowCapacitanceRubber",
        description="Low capacitance rubber wire insulation.",
        meaning=CIM["WireInsulationKind.lowCapacitanceRubber"])
    oilPaper = PermissibleValue(
        text="oilPaper",
        description="Oil paper wire insulation.",
        meaning=CIM["WireInsulationKind.oilPaper"])
    other = PermissibleValue(
        text="other",
        description="Other kind of wire insulation.",
        meaning=CIM["WireInsulationKind.other"])
    ozoneResistantRubber = PermissibleValue(
        text="ozoneResistantRubber",
        description="Ozone resistant rubber wire insulation.",
        meaning=CIM["WireInsulationKind.ozoneResistantRubber"])
    rubber = PermissibleValue(
        text="rubber",
        description="Rubber wire insulation.",
        meaning=CIM["WireInsulationKind.rubber"])
    siliconRubber = PermissibleValue(
        text="siliconRubber",
        description="Silicon rubber wire insulation.",
        meaning=CIM["WireInsulationKind.siliconRubber"])
    treeResistantHighMolecularWeightPolyethylene = PermissibleValue(
        text="treeResistantHighMolecularWeightPolyethylene",
        description="Tree resistant high molecular weight polyethylene wire insulation.",
        meaning=CIM["WireInsulationKind.treeResistantHighMolecularWeightPolyethylene"])
    treeRetardantCrosslinkedPolyethylene = PermissibleValue(
        text="treeRetardantCrosslinkedPolyethylene",
        description="Tree retardant crosslinked polyethylene wire insulation.",
        meaning=CIM["WireInsulationKind.treeRetardantCrosslinkedPolyethylene"])
    unbeltedPilc = PermissibleValue(
        text="unbeltedPilc",
        description="Unbelted pilc wire insulation.",
        meaning=CIM["WireInsulationKind.unbeltedPilc"])
    varnishedCambricCloth = PermissibleValue(
        text="varnishedCambricCloth",
        description="Varnished cambric cloth wire insulation.",
        meaning=CIM["WireInsulationKind.varnishedCambricCloth"])
    varnishedDacronGlass = PermissibleValue(
        text="varnishedDacronGlass",
        description="Varnished dacron glass wire insulation.",
        meaning=CIM["WireInsulationKind.varnishedDacronGlass"])

    _defn = EnumDefinition(
        name="WireInsulationKind",
        description="Kind of wire insulation.",
    )

class WireMaterialKind(EnumDefinitionImpl):
    """
    Kind of wire material.
    """
    aaac = PermissibleValue(
        text="aaac",
        description="Aluminum-alloy conductor steel reinforced.",
        meaning=CIM["WireMaterialKind.aaac"])
    acsr = PermissibleValue(
        text="acsr",
        description="Aluminum conductor steel reinforced.",
        meaning=CIM["WireMaterialKind.acsr"])
    aluminum = PermissibleValue(
        text="aluminum",
        description="Aluminum wire.",
        meaning=CIM["WireMaterialKind.aluminum"])
    aluminumAlloy = PermissibleValue(
        text="aluminumAlloy",
        description="Aluminum-alloy wire.",
        meaning=CIM["WireMaterialKind.aluminumAlloy"])
    aluminumAlloySteel = PermissibleValue(
        text="aluminumAlloySteel",
        description="Aluminum-alloy-steel wire.",
        meaning=CIM["WireMaterialKind.aluminumAlloySteel"])
    aluminumSteel = PermissibleValue(
        text="aluminumSteel",
        description="Aluminum-steel wire.",
        meaning=CIM["WireMaterialKind.aluminumSteel"])
    copper = PermissibleValue(
        text="copper",
        description="Copper wire.",
        meaning=CIM["WireMaterialKind.copper"])
    other = PermissibleValue(
        text="other",
        description="Other wire material.",
        meaning=CIM["WireMaterialKind.other"])
    steel = PermissibleValue(
        text="steel",
        description="Steel wire.",
        meaning=CIM["WireMaterialKind.steel"])

    _defn = EnumDefinition(
        name="WireMaterialKind",
        description="Kind of wire material.",
    )

class WireUsageKind(EnumDefinitionImpl):
    """
    Kind of wire usage.
    """
    distribution = PermissibleValue(
        text="distribution",
        description="Wire is used in medium voltage network.",
        meaning=CIM["WireUsageKind.distribution"])
    other = PermissibleValue(
        text="other",
        description="Other kind of wire usage.",
        meaning=CIM["WireUsageKind.other"])
    secondary = PermissibleValue(
        text="secondary",
        description="Wire is used in low voltage circuit.",
        meaning=CIM["WireUsageKind.secondary"])
    transmission = PermissibleValue(
        text="transmission",
        description="Wire is used in extra-high voltage or high voltage network.",
        meaning=CIM["WireUsageKind.transmission"])

    _defn = EnumDefinition(
        name="WireUsageKind",
        description="Kind of wire usage.",
    )

# Slots
class slots:
    pass

slots.aCDCTerminal__connected = Slot(uri=CIM['ACDCTerminal.connected'], name="aCDCTerminal__connected", curie=CIM.curie('ACDCTerminal.connected'),
                   model_uri=CIMTBL.aCDCTerminal__connected, domain=None, range=Optional[Union[bool, Bool]])

slots.aCDCTerminal__sequenceNumber = Slot(uri=CIM['ACDCTerminal.sequenceNumber'], name="aCDCTerminal__sequenceNumber", curie=CIM.curie('ACDCTerminal.sequenceNumber'),
                   model_uri=CIMTBL.aCDCTerminal__sequenceNumber, domain=None, range=Optional[int])

slots.aCDCTerminal__BusNameMarker = Slot(uri=CIM['ACDCTerminal.BusNameMarker'], name="aCDCTerminal__BusNameMarker", curie=CIM.curie('ACDCTerminal.BusNameMarker'),
                   model_uri=CIMTBL.aCDCTerminal__BusNameMarker, domain=None, range=Optional[Union[dict, BusNameMarker]])

slots.aCLineSegment__b0ch = Slot(uri=CIM['ACLineSegment.b0ch'], name="aCLineSegment__b0ch", curie=CIM.curie('ACLineSegment.b0ch'),
                   model_uri=CIMTBL.aCLineSegment__b0ch, domain=None, range=Optional[float])

slots.aCLineSegment__bch = Slot(uri=CIM['ACLineSegment.bch'], name="aCLineSegment__bch", curie=CIM.curie('ACLineSegment.bch'),
                   model_uri=CIMTBL.aCLineSegment__bch, domain=None, range=Optional[float])

slots.aCLineSegment__circuitNumber = Slot(uri=CIM['ACLineSegment.circuitNumber'], name="aCLineSegment__circuitNumber", curie=CIM.curie('ACLineSegment.circuitNumber'),
                   model_uri=CIMTBL.aCLineSegment__circuitNumber, domain=None, range=Optional[int])

slots.aCLineSegment__g0ch = Slot(uri=CIM['ACLineSegment.g0ch'], name="aCLineSegment__g0ch", curie=CIM.curie('ACLineSegment.g0ch'),
                   model_uri=CIMTBL.aCLineSegment__g0ch, domain=None, range=Optional[float])

slots.aCLineSegment__gch = Slot(uri=CIM['ACLineSegment.gch'], name="aCLineSegment__gch", curie=CIM.curie('ACLineSegment.gch'),
                   model_uri=CIMTBL.aCLineSegment__gch, domain=None, range=Optional[float])

slots.aCLineSegment__isUnderground = Slot(uri=CIM['ACLineSegment.isUnderground'], name="aCLineSegment__isUnderground", curie=CIM.curie('ACLineSegment.isUnderground'),
                   model_uri=CIMTBL.aCLineSegment__isUnderground, domain=None, range=Optional[Union[bool, Bool]])

slots.aCLineSegment__r = Slot(uri=CIM['ACLineSegment.r'], name="aCLineSegment__r", curie=CIM.curie('ACLineSegment.r'),
                   model_uri=CIMTBL.aCLineSegment__r, domain=None, range=Optional[float])

slots.aCLineSegment__r0 = Slot(uri=CIM['ACLineSegment.r0'], name="aCLineSegment__r0", curie=CIM.curie('ACLineSegment.r0'),
                   model_uri=CIMTBL.aCLineSegment__r0, domain=None, range=Optional[float])

slots.aCLineSegment__shortCircuitEndTemperature = Slot(uri=CIM['ACLineSegment.shortCircuitEndTemperature'], name="aCLineSegment__shortCircuitEndTemperature", curie=CIM.curie('ACLineSegment.shortCircuitEndTemperature'),
                   model_uri=CIMTBL.aCLineSegment__shortCircuitEndTemperature, domain=None, range=Optional[float])

slots.aCLineSegment__x = Slot(uri=CIM['ACLineSegment.x'], name="aCLineSegment__x", curie=CIM.curie('ACLineSegment.x'),
                   model_uri=CIMTBL.aCLineSegment__x, domain=None, range=Optional[float])

slots.aCLineSegment__x0 = Slot(uri=CIM['ACLineSegment.x0'], name="aCLineSegment__x0", curie=CIM.curie('ACLineSegment.x0'),
                   model_uri=CIMTBL.aCLineSegment__x0, domain=None, range=Optional[float])

slots.aCLineSegment__EarthResistivity = Slot(uri=CIM['ACLineSegment.EarthResistivity'], name="aCLineSegment__EarthResistivity", curie=CIM.curie('ACLineSegment.EarthResistivity'),
                   model_uri=CIMTBL.aCLineSegment__EarthResistivity, domain=None, range=Optional[Union[dict, EarthResistivity]])

slots.aCLineSegment__PerLengthImpedance = Slot(uri=CIM['ACLineSegment.PerLengthImpedance'], name="aCLineSegment__PerLengthImpedance", curie=CIM.curie('ACLineSegment.PerLengthImpedance'),
                   model_uri=CIMTBL.aCLineSegment__PerLengthImpedance, domain=None, range=Optional[Union[dict, PerLengthImpedance]])

slots.aCLineSegment__WireSpacing = Slot(uri=CIM['ACLineSegment.WireSpacing'], name="aCLineSegment__WireSpacing", curie=CIM.curie('ACLineSegment.WireSpacing'),
                   model_uri=CIMTBL.aCLineSegment__WireSpacing, domain=None, range=Optional[Union[dict, WireSpacing]])

slots.aCLineSegment__WireSpacingInfo = Slot(uri=CIM['ACLineSegment.WireSpacingInfo'], name="aCLineSegment__WireSpacingInfo", curie=CIM.curie('ACLineSegment.WireSpacingInfo'),
                   model_uri=CIMTBL.aCLineSegment__WireSpacingInfo, domain=None, range=Optional[Union[dict, WireSpacingInfo]])

slots.aCLineSegmentPhase__phase = Slot(uri=CIM['ACLineSegmentPhase.phase'], name="aCLineSegmentPhase__phase", curie=CIM.curie('ACLineSegmentPhase.phase'),
                   model_uri=CIMTBL.aCLineSegmentPhase__phase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.aCLineSegmentPhase__sequenceNumber = Slot(uri=CIM['ACLineSegmentPhase.sequenceNumber'], name="aCLineSegmentPhase__sequenceNumber", curie=CIM.curie('ACLineSegmentPhase.sequenceNumber'),
                   model_uri=CIMTBL.aCLineSegmentPhase__sequenceNumber, domain=None, range=Optional[int])

slots.aCLineSegmentPhase__ACLineSegment = Slot(uri=CIM['ACLineSegmentPhase.ACLineSegment'], name="aCLineSegmentPhase__ACLineSegment", curie=CIM.curie('ACLineSegmentPhase.ACLineSegment'),
                   model_uri=CIMTBL.aCLineSegmentPhase__ACLineSegment, domain=None, range=Optional[Union[dict, ACLineSegment]])

slots.aCLineSegmentPhase__WireInfo = Slot(uri=CIM['ACLineSegmentPhase.WireInfo'], name="aCLineSegmentPhase__WireInfo", curie=CIM.curie('ACLineSegmentPhase.WireInfo'),
                   model_uri=CIMTBL.aCLineSegmentPhase__WireInfo, domain=None, range=Optional[Union[dict, WireInfo]])

slots.aCPointOfCommonCoupling__ConnectivityNode = Slot(uri=CIM['ACPointOfCommonCoupling.ConnectivityNode'], name="aCPointOfCommonCoupling__ConnectivityNode", curie=CIM.curie('ACPointOfCommonCoupling.ConnectivityNode'),
                   model_uri=CIMTBL.aCPointOfCommonCoupling__ConnectivityNode, domain=None, range=Optional[Union[dict, ConnectivityNode]])

slots.aCPointOfCommonCoupling__DCConverterUnit = Slot(uri=CIM['ACPointOfCommonCoupling.DCConverterUnit'], name="aCPointOfCommonCoupling__DCConverterUnit", curie=CIM.curie('ACPointOfCommonCoupling.DCConverterUnit'),
                   model_uri=CIMTBL.aCPointOfCommonCoupling__DCConverterUnit, domain=None, range=Optional[Union[dict, DCConverterUnit]])

slots.activePowerLimit__normalValue = Slot(uri=CIM['ActivePowerLimit.normalValue'], name="activePowerLimit__normalValue", curie=CIM.curie('ActivePowerLimit.normalValue'),
                   model_uri=CIMTBL.activePowerLimit__normalValue, domain=None, range=Optional[float])

slots.activePowerLimit__value = Slot(uri=CIM['ActivePowerLimit.value'], name="activePowerLimit__value", curie=CIM.curie('ActivePowerLimit.value'),
                   model_uri=CIMTBL.activePowerLimit__value, domain=None, range=Optional[float])

slots.altGeneratingUnitMeas__priority = Slot(uri=CIM['AltGeneratingUnitMeas.priority'], name="altGeneratingUnitMeas__priority", curie=CIM.curie('AltGeneratingUnitMeas.priority'),
                   model_uri=CIMTBL.altGeneratingUnitMeas__priority, domain=None, range=Optional[int])

slots.altGeneratingUnitMeas__AnalogValue = Slot(uri=CIM['AltGeneratingUnitMeas.AnalogValue'], name="altGeneratingUnitMeas__AnalogValue", curie=CIM.curie('AltGeneratingUnitMeas.AnalogValue'),
                   model_uri=CIMTBL.altGeneratingUnitMeas__AnalogValue, domain=None, range=Optional[Union[dict, AnalogValue]])

slots.altGeneratingUnitMeas__ControlAreaGeneratingUnit = Slot(uri=CIM['AltGeneratingUnitMeas.ControlAreaGeneratingUnit'], name="altGeneratingUnitMeas__ControlAreaGeneratingUnit", curie=CIM.curie('AltGeneratingUnitMeas.ControlAreaGeneratingUnit'),
                   model_uri=CIMTBL.altGeneratingUnitMeas__ControlAreaGeneratingUnit, domain=None, range=Optional[Union[dict, ControlAreaGeneratingUnit]])

slots.altTieMeas__priority = Slot(uri=CIM['AltTieMeas.priority'], name="altTieMeas__priority", curie=CIM.curie('AltTieMeas.priority'),
                   model_uri=CIMTBL.altTieMeas__priority, domain=None, range=Optional[int])

slots.altTieMeas__AnalogValue = Slot(uri=CIM['AltTieMeas.AnalogValue'], name="altTieMeas__AnalogValue", curie=CIM.curie('AltTieMeas.AnalogValue'),
                   model_uri=CIMTBL.altTieMeas__AnalogValue, domain=None, range=Optional[Union[dict, AnalogValue]])

slots.altTieMeas__TieFlow = Slot(uri=CIM['AltTieMeas.TieFlow'], name="altTieMeas__TieFlow", curie=CIM.curie('AltTieMeas.TieFlow'),
                   model_uri=CIMTBL.altTieMeas__TieFlow, domain=None, range=Optional[Union[dict, TieFlow]])

slots.analogValue__value = Slot(uri=CIM['AnalogValue.value'], name="analogValue__value", curie=CIM.curie('AnalogValue.value'),
                   model_uri=CIMTBL.analogValue__value, domain=None, range=Optional[float])

slots.analogValue__Analog = Slot(uri=CIM['AnalogValue.Analog'], name="analogValue__Analog", curie=CIM.curie('AnalogValue.Analog'),
                   model_uri=CIMTBL.analogValue__Analog, domain=None, range=Optional[Union[dict, Analog]])

slots.angleBusbarInfo__crossSectionWidth = Slot(uri=CIM['AngleBusbarInfo.crossSectionWidth'], name="angleBusbarInfo__crossSectionWidth", curie=CIM.curie('AngleBusbarInfo.crossSectionWidth'),
                   model_uri=CIMTBL.angleBusbarInfo__crossSectionWidth, domain=None, range=Optional[float])

slots.angleBusbarInfo__thickness = Slot(uri=CIM['AngleBusbarInfo.thickness'], name="angleBusbarInfo__thickness", curie=CIM.curie('AngleBusbarInfo.thickness'),
                   model_uri=CIMTBL.angleBusbarInfo__thickness, domain=None, range=Optional[float])

slots.apparentPowerLimit__normalValue = Slot(uri=CIM['ApparentPowerLimit.normalValue'], name="apparentPowerLimit__normalValue", curie=CIM.curie('ApparentPowerLimit.normalValue'),
                   model_uri=CIMTBL.apparentPowerLimit__normalValue, domain=None, range=Optional[float])

slots.apparentPowerLimit__value = Slot(uri=CIM['ApparentPowerLimit.value'], name="apparentPowerLimit__value", curie=CIM.curie('ApparentPowerLimit.value'),
                   model_uri=CIMTBL.apparentPowerLimit__value, domain=None, range=Optional[float])

slots.areaInterchangeController__pTolerance = Slot(uri=CIM['AreaInterchangeController.pTolerance'], name="areaInterchangeController__pTolerance", curie=CIM.curie('AreaInterchangeController.pTolerance'),
                   model_uri=CIMTBL.areaInterchangeController__pTolerance, domain=None, range=Optional[float])

slots.areaInterchangeController__ControlArea = Slot(uri=CIM['AreaInterchangeController.ControlArea'], name="areaInterchangeController__ControlArea", curie=CIM.curie('AreaInterchangeController.ControlArea'),
                   model_uri=CIMTBL.areaInterchangeController__ControlArea, domain=None, range=Optional[Union[dict, ControlArea]])

slots.assetInfo__CatalogAssetType = Slot(uri=CIM['AssetInfo.CatalogAssetType'], name="assetInfo__CatalogAssetType", curie=CIM.curie('AssetInfo.CatalogAssetType'),
                   model_uri=CIMTBL.assetInfo__CatalogAssetType, domain=None, range=Optional[Union[dict, CatalogAssetType]])

slots.assetInfo__ProductAssetModel = Slot(uri=CIM['AssetInfo.ProductAssetModel'], name="assetInfo__ProductAssetModel", curie=CIM.curie('AssetInfo.ProductAssetModel'),
                   model_uri=CIMTBL.assetInfo__ProductAssetModel, domain=None, range=Optional[Union[dict, ProductAssetModel]])

slots.asynchronousMachine__asynchronousMachineType = Slot(uri=CIM['AsynchronousMachine.asynchronousMachineType'], name="asynchronousMachine__asynchronousMachineType", curie=CIM.curie('AsynchronousMachine.asynchronousMachineType'),
                   model_uri=CIMTBL.asynchronousMachine__asynchronousMachineType, domain=None, range=Optional[Union[str, "AsynchronousMachineKind"]])

slots.asynchronousMachine__converterFedDrive = Slot(uri=CIM['AsynchronousMachine.converterFedDrive'], name="asynchronousMachine__converterFedDrive", curie=CIM.curie('AsynchronousMachine.converterFedDrive'),
                   model_uri=CIMTBL.asynchronousMachine__converterFedDrive, domain=None, range=Optional[Union[bool, Bool]])

slots.asynchronousMachine__efficiency = Slot(uri=CIM['AsynchronousMachine.efficiency'], name="asynchronousMachine__efficiency", curie=CIM.curie('AsynchronousMachine.efficiency'),
                   model_uri=CIMTBL.asynchronousMachine__efficiency, domain=None, range=Optional[float])

slots.asynchronousMachine__iaIrRatio = Slot(uri=CIM['AsynchronousMachine.iaIrRatio'], name="asynchronousMachine__iaIrRatio", curie=CIM.curie('AsynchronousMachine.iaIrRatio'),
                   model_uri=CIMTBL.asynchronousMachine__iaIrRatio, domain=None, range=Optional[float])

slots.asynchronousMachine__nominalFrequency = Slot(uri=CIM['AsynchronousMachine.nominalFrequency'], name="asynchronousMachine__nominalFrequency", curie=CIM.curie('AsynchronousMachine.nominalFrequency'),
                   model_uri=CIMTBL.asynchronousMachine__nominalFrequency, domain=None, range=Optional[float])

slots.asynchronousMachine__nominalSpeed = Slot(uri=CIM['AsynchronousMachine.nominalSpeed'], name="asynchronousMachine__nominalSpeed", curie=CIM.curie('AsynchronousMachine.nominalSpeed'),
                   model_uri=CIMTBL.asynchronousMachine__nominalSpeed, domain=None, range=Optional[float])

slots.asynchronousMachine__polePairNumber = Slot(uri=CIM['AsynchronousMachine.polePairNumber'], name="asynchronousMachine__polePairNumber", curie=CIM.curie('AsynchronousMachine.polePairNumber'),
                   model_uri=CIMTBL.asynchronousMachine__polePairNumber, domain=None, range=Optional[int])

slots.asynchronousMachine__ratedMechanicalPower = Slot(uri=CIM['AsynchronousMachine.ratedMechanicalPower'], name="asynchronousMachine__ratedMechanicalPower", curie=CIM.curie('AsynchronousMachine.ratedMechanicalPower'),
                   model_uri=CIMTBL.asynchronousMachine__ratedMechanicalPower, domain=None, range=Optional[float])

slots.asynchronousMachine__reversible = Slot(uri=CIM['AsynchronousMachine.reversible'], name="asynchronousMachine__reversible", curie=CIM.curie('AsynchronousMachine.reversible'),
                   model_uri=CIMTBL.asynchronousMachine__reversible, domain=None, range=Optional[Union[bool, Bool]])

slots.asynchronousMachine__rr1 = Slot(uri=CIM['AsynchronousMachine.rr1'], name="asynchronousMachine__rr1", curie=CIM.curie('AsynchronousMachine.rr1'),
                   model_uri=CIMTBL.asynchronousMachine__rr1, domain=None, range=Optional[float])

slots.asynchronousMachine__rr2 = Slot(uri=CIM['AsynchronousMachine.rr2'], name="asynchronousMachine__rr2", curie=CIM.curie('AsynchronousMachine.rr2'),
                   model_uri=CIMTBL.asynchronousMachine__rr2, domain=None, range=Optional[float])

slots.asynchronousMachine__rxLockedRotorRatio = Slot(uri=CIM['AsynchronousMachine.rxLockedRotorRatio'], name="asynchronousMachine__rxLockedRotorRatio", curie=CIM.curie('AsynchronousMachine.rxLockedRotorRatio'),
                   model_uri=CIMTBL.asynchronousMachine__rxLockedRotorRatio, domain=None, range=Optional[float])

slots.asynchronousMachine__tpo = Slot(uri=CIM['AsynchronousMachine.tpo'], name="asynchronousMachine__tpo", curie=CIM.curie('AsynchronousMachine.tpo'),
                   model_uri=CIMTBL.asynchronousMachine__tpo, domain=None, range=Optional[float])

slots.asynchronousMachine__tppo = Slot(uri=CIM['AsynchronousMachine.tppo'], name="asynchronousMachine__tppo", curie=CIM.curie('AsynchronousMachine.tppo'),
                   model_uri=CIMTBL.asynchronousMachine__tppo, domain=None, range=Optional[float])

slots.asynchronousMachine__xlr1 = Slot(uri=CIM['AsynchronousMachine.xlr1'], name="asynchronousMachine__xlr1", curie=CIM.curie('AsynchronousMachine.xlr1'),
                   model_uri=CIMTBL.asynchronousMachine__xlr1, domain=None, range=Optional[float])

slots.asynchronousMachine__xlr2 = Slot(uri=CIM['AsynchronousMachine.xlr2'], name="asynchronousMachine__xlr2", curie=CIM.curie('AsynchronousMachine.xlr2'),
                   model_uri=CIMTBL.asynchronousMachine__xlr2, domain=None, range=Optional[float])

slots.asynchronousMachine__xm = Slot(uri=CIM['AsynchronousMachine.xm'], name="asynchronousMachine__xm", curie=CIM.curie('AsynchronousMachine.xm'),
                   model_uri=CIMTBL.asynchronousMachine__xm, domain=None, range=Optional[float])

slots.asynchronousMachine__xp = Slot(uri=CIM['AsynchronousMachine.xp'], name="asynchronousMachine__xp", curie=CIM.curie('AsynchronousMachine.xp'),
                   model_uri=CIMTBL.asynchronousMachine__xp, domain=None, range=Optional[float])

slots.asynchronousMachine__xpp = Slot(uri=CIM['AsynchronousMachine.xpp'], name="asynchronousMachine__xpp", curie=CIM.curie('AsynchronousMachine.xpp'),
                   model_uri=CIMTBL.asynchronousMachine__xpp, domain=None, range=Optional[float])

slots.asynchronousMachine__xs = Slot(uri=CIM['AsynchronousMachine.xs'], name="asynchronousMachine__xs", curie=CIM.curie('AsynchronousMachine.xs'),
                   model_uri=CIMTBL.asynchronousMachine__xs, domain=None, range=Optional[float])

slots.asynchronousMachine__AsynchronousMachineDynamics = Slot(uri=CIM['AsynchronousMachine.AsynchronousMachineDynamics'], name="asynchronousMachine__AsynchronousMachineDynamics", curie=CIM.curie('AsynchronousMachine.AsynchronousMachineDynamics'),
                   model_uri=CIMTBL.asynchronousMachine__AsynchronousMachineDynamics, domain=None, range=Optional[Union[dict, AsynchronousMachineDynamics]])

slots.bareWireInfo__wireConstructionKind = Slot(uri=CIM['BareWireInfo.wireConstructionKind'], name="bareWireInfo__wireConstructionKind", curie=CIM.curie('BareWireInfo.wireConstructionKind'),
                   model_uri=CIMTBL.bareWireInfo__wireConstructionKind, domain=None, range=Optional[Union[str, "WireConstructionKind"]])

slots.baseFrequency__frequency = Slot(uri=CIM['BaseFrequency.frequency'], name="baseFrequency__frequency", curie=CIM.curie('BaseFrequency.frequency'),
                   model_uri=CIMTBL.baseFrequency__frequency, domain=None, range=Optional[float])

slots.basePower__basePower = Slot(uri=CIM['BasePower.basePower'], name="basePower__basePower", curie=CIM.curie('BasePower.basePower'),
                   model_uri=CIMTBL.basePower__basePower, domain=None, range=Optional[float])

slots.baseVoltage__nominalVoltage = Slot(uri=CIM['BaseVoltage.nominalVoltage'], name="baseVoltage__nominalVoltage", curie=CIM.curie('BaseVoltage.nominalVoltage'),
                   model_uri=CIMTBL.baseVoltage__nominalVoltage, domain=None, range=Optional[float])

slots.basicIntervalSchedule__startTime = Slot(uri=CIM['BasicIntervalSchedule.startTime'], name="basicIntervalSchedule__startTime", curie=CIM.curie('BasicIntervalSchedule.startTime'),
                   model_uri=CIMTBL.basicIntervalSchedule__startTime, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.basicIntervalSchedule__value1Description = Slot(uri=CIM['BasicIntervalSchedule.value1Description'], name="basicIntervalSchedule__value1Description", curie=CIM.curie('BasicIntervalSchedule.value1Description'),
                   model_uri=CIMTBL.basicIntervalSchedule__value1Description, domain=None, range=Optional[str])

slots.basicIntervalSchedule__value1Multiplier = Slot(uri=CIM['BasicIntervalSchedule.value1Multiplier'], name="basicIntervalSchedule__value1Multiplier", curie=CIM.curie('BasicIntervalSchedule.value1Multiplier'),
                   model_uri=CIMTBL.basicIntervalSchedule__value1Multiplier, domain=None, range=Optional[Union[str, "UnitMultiplier"]])

slots.basicIntervalSchedule__value1Unit = Slot(uri=CIM['BasicIntervalSchedule.value1Unit'], name="basicIntervalSchedule__value1Unit", curie=CIM.curie('BasicIntervalSchedule.value1Unit'),
                   model_uri=CIMTBL.basicIntervalSchedule__value1Unit, domain=None, range=Optional[Union[str, "UnitSymbol"]])

slots.basicIntervalSchedule__value2Description = Slot(uri=CIM['BasicIntervalSchedule.value2Description'], name="basicIntervalSchedule__value2Description", curie=CIM.curie('BasicIntervalSchedule.value2Description'),
                   model_uri=CIMTBL.basicIntervalSchedule__value2Description, domain=None, range=Optional[str])

slots.basicIntervalSchedule__value2Multiplier = Slot(uri=CIM['BasicIntervalSchedule.value2Multiplier'], name="basicIntervalSchedule__value2Multiplier", curie=CIM.curie('BasicIntervalSchedule.value2Multiplier'),
                   model_uri=CIMTBL.basicIntervalSchedule__value2Multiplier, domain=None, range=Optional[Union[str, "UnitMultiplier"]])

slots.basicIntervalSchedule__value2Unit = Slot(uri=CIM['BasicIntervalSchedule.value2Unit'], name="basicIntervalSchedule__value2Unit", curie=CIM.curie('BasicIntervalSchedule.value2Unit'),
                   model_uri=CIMTBL.basicIntervalSchedule__value2Unit, domain=None, range=Optional[Union[str, "UnitSymbol"]])

slots.basicIntervalSchedule__value3Description = Slot(uri=CIM['BasicIntervalSchedule.value3Description'], name="basicIntervalSchedule__value3Description", curie=CIM.curie('BasicIntervalSchedule.value3Description'),
                   model_uri=CIMTBL.basicIntervalSchedule__value3Description, domain=None, range=Optional[str])

slots.basicIntervalSchedule__value3Multiplier = Slot(uri=CIM['BasicIntervalSchedule.value3Multiplier'], name="basicIntervalSchedule__value3Multiplier", curie=CIM.curie('BasicIntervalSchedule.value3Multiplier'),
                   model_uri=CIMTBL.basicIntervalSchedule__value3Multiplier, domain=None, range=Optional[Union[str, "UnitMultiplier"]])

slots.basicIntervalSchedule__value3Unit = Slot(uri=CIM['BasicIntervalSchedule.value3Unit'], name="basicIntervalSchedule__value3Unit", curie=CIM.curie('BasicIntervalSchedule.value3Unit'),
                   model_uri=CIMTBL.basicIntervalSchedule__value3Unit, domain=None, range=Optional[Union[str, "UnitSymbol"]])

slots.batteryInfo__batteryType = Slot(uri=CIM['BatteryInfo.batteryType'], name="batteryInfo__batteryType", curie=CIM.curie('BatteryInfo.batteryType'),
                   model_uri=CIMTBL.batteryInfo__batteryType, domain=None, range=Optional[Union[str, "BatteryTypeKind"]])

slots.batteryInfo__cellChemistry = Slot(uri=CIM['BatteryInfo.cellChemistry'], name="batteryInfo__cellChemistry", curie=CIM.curie('BatteryInfo.cellChemistry'),
                   model_uri=CIMTBL.batteryInfo__cellChemistry, domain=None, range=Optional[str])

slots.batteryInfo__numberOfCells = Slot(uri=CIM['BatteryInfo.numberOfCells'], name="batteryInfo__numberOfCells", curie=CIM.curie('BatteryInfo.numberOfCells'),
                   model_uri=CIMTBL.batteryInfo__numberOfCells, domain=None, range=Optional[int])

slots.batteryInfo__ratedCapacity = Slot(uri=CIM['BatteryInfo.ratedCapacity'], name="batteryInfo__ratedCapacity", curie=CIM.curie('BatteryInfo.ratedCapacity'),
                   model_uri=CIMTBL.batteryInfo__ratedCapacity, domain=None, range=Optional[float])

slots.batteryInfo__usableCapacity = Slot(uri=CIM['BatteryInfo.usableCapacity'], name="batteryInfo__usableCapacity", curie=CIM.curie('BatteryInfo.usableCapacity'),
                   model_uri=CIMTBL.batteryInfo__usableCapacity, domain=None, range=Optional[float])

slots.batteryUnit__batteryState = Slot(uri=CIM['BatteryUnit.batteryState'], name="batteryUnit__batteryState", curie=CIM.curie('BatteryUnit.batteryState'),
                   model_uri=CIMTBL.batteryUnit__batteryState, domain=None, range=Optional[Union[str, "BatteryStateKind"]])

slots.batteryUnit__chargingEfficiency = Slot(uri=CIM['BatteryUnit.chargingEfficiency'], name="batteryUnit__chargingEfficiency", curie=CIM.curie('BatteryUnit.chargingEfficiency'),
                   model_uri=CIMTBL.batteryUnit__chargingEfficiency, domain=None, range=Optional[float])

slots.batteryUnit__dischargingEfficiency = Slot(uri=CIM['BatteryUnit.dischargingEfficiency'], name="batteryUnit__dischargingEfficiency", curie=CIM.curie('BatteryUnit.dischargingEfficiency'),
                   model_uri=CIMTBL.batteryUnit__dischargingEfficiency, domain=None, range=Optional[float])

slots.batteryUnit__idlingP = Slot(uri=CIM['BatteryUnit.idlingP'], name="batteryUnit__idlingP", curie=CIM.curie('BatteryUnit.idlingP'),
                   model_uri=CIMTBL.batteryUnit__idlingP, domain=None, range=Optional[float])

slots.batteryUnit__idlingQ = Slot(uri=CIM['BatteryUnit.idlingQ'], name="batteryUnit__idlingQ", curie=CIM.curie('BatteryUnit.idlingQ'),
                   model_uri=CIMTBL.batteryUnit__idlingQ, domain=None, range=Optional[float])

slots.batteryUnit__minimumE = Slot(uri=CIM['BatteryUnit.minimumE'], name="batteryUnit__minimumE", curie=CIM.curie('BatteryUnit.minimumE'),
                   model_uri=CIMTBL.batteryUnit__minimumE, domain=None, range=Optional[float])

slots.batteryUnit__ratedE = Slot(uri=CIM['BatteryUnit.ratedE'], name="batteryUnit__ratedE", curie=CIM.curie('BatteryUnit.ratedE'),
                   model_uri=CIMTBL.batteryUnit__ratedE, domain=None, range=Optional[float])

slots.batteryUnit__storedE = Slot(uri=CIM['BatteryUnit.storedE'], name="batteryUnit__storedE", curie=CIM.curie('BatteryUnit.storedE'),
                   model_uri=CIMTBL.batteryUnit__storedE, domain=None, range=Optional[float])

slots.bay__bayEnergyMeasFlag = Slot(uri=CIM['Bay.bayEnergyMeasFlag'], name="bay__bayEnergyMeasFlag", curie=CIM.curie('Bay.bayEnergyMeasFlag'),
                   model_uri=CIMTBL.bay__bayEnergyMeasFlag, domain=None, range=Optional[Union[bool, Bool]])

slots.bay__bayPowerMeasFlag = Slot(uri=CIM['Bay.bayPowerMeasFlag'], name="bay__bayPowerMeasFlag", curie=CIM.curie('Bay.bayPowerMeasFlag'),
                   model_uri=CIMTBL.bay__bayPowerMeasFlag, domain=None, range=Optional[Union[bool, Bool]])

slots.bay__breakerConfiguration = Slot(uri=CIM['Bay.breakerConfiguration'], name="bay__breakerConfiguration", curie=CIM.curie('Bay.breakerConfiguration'),
                   model_uri=CIMTBL.bay__breakerConfiguration, domain=None, range=Optional[Union[str, "BreakerConfiguration"]])

slots.bay__busBarConfiguration = Slot(uri=CIM['Bay.busBarConfiguration'], name="bay__busBarConfiguration", curie=CIM.curie('Bay.busBarConfiguration'),
                   model_uri=CIMTBL.bay__busBarConfiguration, domain=None, range=Optional[Union[str, "BusbarConfiguration"]])

slots.bay__Substation = Slot(uri=CIM['Bay.Substation'], name="bay__Substation", curie=CIM.curie('Bay.Substation'),
                   model_uri=CIMTBL.bay__Substation, domain=None, range=Optional[Union[dict, Substation]])

slots.bay__VoltageLevel = Slot(uri=CIM['Bay.VoltageLevel'], name="bay__VoltageLevel", curie=CIM.curie('Bay.VoltageLevel'),
                   model_uri=CIMTBL.bay__VoltageLevel, domain=None, range=Optional[Union[dict, VoltageLevel]])

slots.branchGroup__maximumActivePower = Slot(uri=CIM['BranchGroup.maximumActivePower'], name="branchGroup__maximumActivePower", curie=CIM.curie('BranchGroup.maximumActivePower'),
                   model_uri=CIMTBL.branchGroup__maximumActivePower, domain=None, range=Optional[float])

slots.branchGroup__maximumReactivePower = Slot(uri=CIM['BranchGroup.maximumReactivePower'], name="branchGroup__maximumReactivePower", curie=CIM.curie('BranchGroup.maximumReactivePower'),
                   model_uri=CIMTBL.branchGroup__maximumReactivePower, domain=None, range=Optional[float])

slots.branchGroup__minimumActivePower = Slot(uri=CIM['BranchGroup.minimumActivePower'], name="branchGroup__minimumActivePower", curie=CIM.curie('BranchGroup.minimumActivePower'),
                   model_uri=CIMTBL.branchGroup__minimumActivePower, domain=None, range=Optional[float])

slots.branchGroup__minimumReactivePower = Slot(uri=CIM['BranchGroup.minimumReactivePower'], name="branchGroup__minimumReactivePower", curie=CIM.curie('BranchGroup.minimumReactivePower'),
                   model_uri=CIMTBL.branchGroup__minimumReactivePower, domain=None, range=Optional[float])

slots.branchGroup__monitorActivePower = Slot(uri=CIM['BranchGroup.monitorActivePower'], name="branchGroup__monitorActivePower", curie=CIM.curie('BranchGroup.monitorActivePower'),
                   model_uri=CIMTBL.branchGroup__monitorActivePower, domain=None, range=Optional[Union[bool, Bool]])

slots.branchGroup__monitorReactivePower = Slot(uri=CIM['BranchGroup.monitorReactivePower'], name="branchGroup__monitorReactivePower", curie=CIM.curie('BranchGroup.monitorReactivePower'),
                   model_uri=CIMTBL.branchGroup__monitorReactivePower, domain=None, range=Optional[Union[bool, Bool]])

slots.branchGroupTerminal__positiveFlowIn = Slot(uri=CIM['BranchGroupTerminal.positiveFlowIn'], name="branchGroupTerminal__positiveFlowIn", curie=CIM.curie('BranchGroupTerminal.positiveFlowIn'),
                   model_uri=CIMTBL.branchGroupTerminal__positiveFlowIn, domain=None, range=Optional[Union[bool, Bool]])

slots.branchGroupTerminal__BranchGroup = Slot(uri=CIM['BranchGroupTerminal.BranchGroup'], name="branchGroupTerminal__BranchGroup", curie=CIM.curie('BranchGroupTerminal.BranchGroup'),
                   model_uri=CIMTBL.branchGroupTerminal__BranchGroup, domain=None, range=Optional[Union[dict, BranchGroup]])

slots.branchGroupTerminal__Terminal = Slot(uri=CIM['BranchGroupTerminal.Terminal'], name="branchGroupTerminal__Terminal", curie=CIM.curie('BranchGroupTerminal.Terminal'),
                   model_uri=CIMTBL.branchGroupTerminal__Terminal, domain=None, range=Optional[Union[dict, Terminal]])

slots.breaker__inTransitTime = Slot(uri=CIM['Breaker.inTransitTime'], name="breaker__inTransitTime", curie=CIM.curie('Breaker.inTransitTime'),
                   model_uri=CIMTBL.breaker__inTransitTime, domain=None, range=Optional[float])

slots.bundleConfiguration__conductorCount = Slot(uri=CIM['BundleConfiguration.conductorCount'], name="bundleConfiguration__conductorCount", curie=CIM.curie('BundleConfiguration.conductorCount'),
                   model_uri=CIMTBL.bundleConfiguration__conductorCount, domain=None, range=Optional[int])

slots.bundleConfiguration__conductorSpacing = Slot(uri=CIM['BundleConfiguration.conductorSpacing'], name="bundleConfiguration__conductorSpacing", curie=CIM.curie('BundleConfiguration.conductorSpacing'),
                   model_uri=CIMTBL.bundleConfiguration__conductorSpacing, domain=None, range=Optional[float])

slots.bundleConfiguration__gmr = Slot(uri=CIM['BundleConfiguration.gmr'], name="bundleConfiguration__gmr", curie=CIM.curie('BundleConfiguration.gmr'),
                   model_uri=CIMTBL.bundleConfiguration__gmr, domain=None, range=Optional[float])

slots.bundleConfiguration__radius = Slot(uri=CIM['BundleConfiguration.radius'], name="bundleConfiguration__radius", curie=CIM.curie('BundleConfiguration.radius'),
                   model_uri=CIMTBL.bundleConfiguration__radius, domain=None, range=Optional[float])

slots.bundleConfiguration__WireInfo = Slot(uri=CIM['BundleConfiguration.WireInfo'], name="bundleConfiguration__WireInfo", curie=CIM.curie('BundleConfiguration.WireInfo'),
                   model_uri=CIMTBL.bundleConfiguration__WireInfo, domain=None, range=Optional[Union[dict, WireInfo]])

slots.busNameMarker__priority = Slot(uri=CIM['BusNameMarker.priority'], name="busNameMarker__priority", curie=CIM.curie('BusNameMarker.priority'),
                   model_uri=CIMTBL.busNameMarker__priority, domain=None, range=Optional[int])

slots.busNameMarker__ReportingGroup = Slot(uri=CIM['BusNameMarker.ReportingGroup'], name="busNameMarker__ReportingGroup", curie=CIM.curie('BusNameMarker.ReportingGroup'),
                   model_uri=CIMTBL.busNameMarker__ReportingGroup, domain=None, range=Optional[Union[dict, ReportingGroup]])

slots.busNameMarker__TopologicalNode = Slot(uri=CIM['BusNameMarker.TopologicalNode'], name="busNameMarker__TopologicalNode", curie=CIM.curie('BusNameMarker.TopologicalNode'),
                   model_uri=CIMTBL.busNameMarker__TopologicalNode, domain=None, range=Optional[Union[dict, TopologicalNode]])

slots.busSegment__Retain = Slot(uri=CIM['BusSegment.Retain'], name="busSegment__Retain", curie=CIM.curie('BusSegment.Retain'),
                   model_uri=CIMTBL.busSegment__Retain, domain=None, range=Optional[Union[bool, Bool]])

slots.busSegment__retained = Slot(uri=CIM['BusSegment.retained'], name="busSegment__retained", curie=CIM.curie('BusSegment.retained'),
                   model_uri=CIMTBL.busSegment__retained, domain=None, range=Optional[Union[bool, Bool]])

slots.busbarSection__ipMax = Slot(uri=CIM['BusbarSection.ipMax'], name="busbarSection__ipMax", curie=CIM.curie('BusbarSection.ipMax'),
                   model_uri=CIMTBL.busbarSection__ipMax, domain=None, range=Optional[float])

slots.busbarSection__VoltageControlZone = Slot(uri=CIM['BusbarSection.VoltageControlZone'], name="busbarSection__VoltageControlZone", curie=CIM.curie('BusbarSection.VoltageControlZone'),
                   model_uri=CIMTBL.busbarSection__VoltageControlZone, domain=None, range=Optional[Union[dict, VoltageControlZone]])

slots.cableArmorInfo__diameterOverArmor = Slot(uri=CIM['CableArmorInfo.diameterOverArmor'], name="cableArmorInfo__diameterOverArmor", curie=CIM.curie('CableArmorInfo.diameterOverArmor'),
                   model_uri=CIMTBL.cableArmorInfo__diameterOverArmor, domain=None, range=Optional[float])

slots.cableArmorInfo__layLength = Slot(uri=CIM['CableArmorInfo.layLength'], name="cableArmorInfo__layLength", curie=CIM.curie('CableArmorInfo.layLength'),
                   model_uri=CIMTBL.cableArmorInfo__layLength, domain=None, range=Optional[float])

slots.cableArmorInfo__strandRadius = Slot(uri=CIM['CableArmorInfo.strandRadius'], name="cableArmorInfo__strandRadius", curie=CIM.curie('CableArmorInfo.strandRadius'),
                   model_uri=CIMTBL.cableArmorInfo__strandRadius, domain=None, range=Optional[float])

slots.cableArmorInfo__tapeLap = Slot(uri=CIM['CableArmorInfo.tapeLap'], name="cableArmorInfo__tapeLap", curie=CIM.curie('CableArmorInfo.tapeLap'),
                   model_uri=CIMTBL.cableArmorInfo__tapeLap, domain=None, range=Optional[float])

slots.cableArmorInfo__tapeThickness = Slot(uri=CIM['CableArmorInfo.tapeThickness'], name="cableArmorInfo__tapeThickness", curie=CIM.curie('CableArmorInfo.tapeThickness'),
                   model_uri=CIMTBL.cableArmorInfo__tapeThickness, domain=None, range=Optional[float])

slots.cableArmorInfo__TapeWidth = Slot(uri=CIM['CableArmorInfo.TapeWidth'], name="cableArmorInfo__TapeWidth", curie=CIM.curie('CableArmorInfo.TapeWidth'),
                   model_uri=CIMTBL.cableArmorInfo__TapeWidth, domain=None, range=Optional[float])

slots.cableArmorInfo__Thickness = Slot(uri=CIM['CableArmorInfo.Thickness'], name="cableArmorInfo__Thickness", curie=CIM.curie('CableArmorInfo.Thickness'),
                   model_uri=CIMTBL.cableArmorInfo__Thickness, domain=None, range=Optional[float])

slots.cableInfo__constructionKind = Slot(uri=CIM['CableInfo.constructionKind'], name="cableInfo__constructionKind", curie=CIM.curie('CableInfo.constructionKind'),
                   model_uri=CIMTBL.cableInfo__constructionKind, domain=None, range=Optional[Union[str, "CableConstructionKind"]])

slots.cableInfo__diameterOverCore = Slot(uri=CIM['CableInfo.diameterOverCore'], name="cableInfo__diameterOverCore", curie=CIM.curie('CableInfo.diameterOverCore'),
                   model_uri=CIMTBL.cableInfo__diameterOverCore, domain=None, range=Optional[float])

slots.cableInfo__diameterOverInsulation = Slot(uri=CIM['CableInfo.diameterOverInsulation'], name="cableInfo__diameterOverInsulation", curie=CIM.curie('CableInfo.diameterOverInsulation'),
                   model_uri=CIMTBL.cableInfo__diameterOverInsulation, domain=None, range=Optional[float])

slots.cableInfo__diameterOverJacket = Slot(uri=CIM['CableInfo.diameterOverJacket'], name="cableInfo__diameterOverJacket", curie=CIM.curie('CableInfo.diameterOverJacket'),
                   model_uri=CIMTBL.cableInfo__diameterOverJacket, domain=None, range=Optional[float])

slots.cableInfo__diameterOverScreen = Slot(uri=CIM['CableInfo.diameterOverScreen'], name="cableInfo__diameterOverScreen", curie=CIM.curie('CableInfo.diameterOverScreen'),
                   model_uri=CIMTBL.cableInfo__diameterOverScreen, domain=None, range=Optional[float])

slots.cableInfo__isStrandFill = Slot(uri=CIM['CableInfo.isStrandFill'], name="cableInfo__isStrandFill", curie=CIM.curie('CableInfo.isStrandFill'),
                   model_uri=CIMTBL.cableInfo__isStrandFill, domain=None, range=Optional[Union[bool, Bool]])

slots.cableInfo__nominalTemperature = Slot(uri=CIM['CableInfo.nominalTemperature'], name="cableInfo__nominalTemperature", curie=CIM.curie('CableInfo.nominalTemperature'),
                   model_uri=CIMTBL.cableInfo__nominalTemperature, domain=None, range=Optional[float])

slots.cableInfo__outerJacketKind = Slot(uri=CIM['CableInfo.outerJacketKind'], name="cableInfo__outerJacketKind", curie=CIM.curie('CableInfo.outerJacketKind'),
                   model_uri=CIMTBL.cableInfo__outerJacketKind, domain=None, range=Optional[Union[str, "CableOuterJacketKind"]])

slots.cableInfo__sheathAsNeutral = Slot(uri=CIM['CableInfo.sheathAsNeutral'], name="cableInfo__sheathAsNeutral", curie=CIM.curie('CableInfo.sheathAsNeutral'),
                   model_uri=CIMTBL.cableInfo__sheathAsNeutral, domain=None, range=Optional[Union[bool, Bool]])

slots.cableInfo__shieldMaterial = Slot(uri=CIM['CableInfo.shieldMaterial'], name="cableInfo__shieldMaterial", curie=CIM.curie('CableInfo.shieldMaterial'),
                   model_uri=CIMTBL.cableInfo__shieldMaterial, domain=None, range=Optional[Union[str, "CableShieldMaterialKind"]])

slots.cableInfo__InsulationInfo = Slot(uri=CIM['CableInfo.InsulationInfo'], name="cableInfo__InsulationInfo", curie=CIM.curie('CableInfo.InsulationInfo'),
                   model_uri=CIMTBL.cableInfo__InsulationInfo, domain=None, range=Optional[Union[dict, InsulationInfo]])

slots.catalogAssetType__estimatedUnitCost = Slot(uri=CIM['CatalogAssetType.estimatedUnitCost'], name="catalogAssetType__estimatedUnitCost", curie=CIM.curie('CatalogAssetType.estimatedUnitCost'),
                   model_uri=CIMTBL.catalogAssetType__estimatedUnitCost, domain=None, range=Optional[Decimal])

slots.catalogAssetType__kind = Slot(uri=CIM['CatalogAssetType.kind'], name="catalogAssetType__kind", curie=CIM.curie('CatalogAssetType.kind'),
                   model_uri=CIMTBL.catalogAssetType__kind, domain=None, range=Optional[Union[str, "AssetKind"]])

slots.catalogAssetType__stockItem = Slot(uri=CIM['CatalogAssetType.stockItem'], name="catalogAssetType__stockItem", curie=CIM.curie('CatalogAssetType.stockItem'),
                   model_uri=CIMTBL.catalogAssetType__stockItem, domain=None, range=Optional[Union[bool, Bool]])

slots.catalogAssetType__type = Slot(uri=CIM['CatalogAssetType.type'], name="catalogAssetType__type", curie=CIM.curie('CatalogAssetType.type'),
                   model_uri=CIMTBL.catalogAssetType__type, domain=None, range=Optional[str])

slots.chargingStation__networkProvider = Slot(uri=CIM['ChargingStation.networkProvider'], name="chargingStation__networkProvider", curie=CIM.curie('ChargingStation.networkProvider'),
                   model_uri=CIMTBL.chargingStation__networkProvider, domain=None, range=Optional[str])

slots.chargingStation__operatorName = Slot(uri=CIM['ChargingStation.operatorName'], name="chargingStation__operatorName", curie=CIM.curie('ChargingStation.operatorName'),
                   model_uri=CIMTBL.chargingStation__operatorName, domain=None, range=Optional[str])

slots.chargingStation__paymentMethods = Slot(uri=CIM['ChargingStation.paymentMethods'], name="chargingStation__paymentMethods", curie=CIM.curie('ChargingStation.paymentMethods'),
                   model_uri=CIMTBL.chargingStation__paymentMethods, domain=None, range=Optional[str])

slots.chargingStation__phoneSupport = Slot(uri=CIM['ChargingStation.phoneSupport'], name="chargingStation__phoneSupport", curie=CIM.curie('ChargingStation.phoneSupport'),
                   model_uri=CIMTBL.chargingStation__phoneSupport, domain=None, range=Optional[str])

slots.chargingStation__weatherProtection = Slot(uri=CIM['ChargingStation.weatherProtection'], name="chargingStation__weatherProtection", curie=CIM.curie('ChargingStation.weatherProtection'),
                   model_uri=CIMTBL.chargingStation__weatherProtection, domain=None, range=Optional[Union[bool, Bool]])

slots.chargingStation__ChargingConnector = Slot(uri=CIM['ChargingStation.ChargingConnector'], name="chargingStation__ChargingConnector", curie=CIM.curie('ChargingStation.ChargingConnector'),
                   model_uri=CIMTBL.chargingStation__ChargingConnector, domain=None, range=Optional[Union[dict, ChargingConnectorInfo]])

slots.clamp__lengthFromTerminal1 = Slot(uri=CIM['Clamp.lengthFromTerminal1'], name="clamp__lengthFromTerminal1", curie=CIM.curie('Clamp.lengthFromTerminal1'),
                   model_uri=CIMTBL.clamp__lengthFromTerminal1, domain=None, range=Optional[float])

slots.clamp__ACLineSegment = Slot(uri=CIM['Clamp.ACLineSegment'], name="clamp__ACLineSegment", curie=CIM.curie('Clamp.ACLineSegment'),
                   model_uri=CIMTBL.clamp__ACLineSegment, domain=None, range=Optional[Union[dict, ACLineSegment]])

slots.communicationLink__communicationMediumKind = Slot(uri=CIM['CommunicationLink.communicationMediumKind'], name="communicationLink__communicationMediumKind", curie=CIM.curie('CommunicationLink.communicationMediumKind'),
                   model_uri=CIMTBL.communicationLink__communicationMediumKind, domain=None, range=Optional[Union[str, "CommunicationMediumKind"]])

slots.communicationLink__communicationProtocolType = Slot(uri=CIM['CommunicationLink.communicationProtocolType'], name="communicationLink__communicationProtocolType", curie=CIM.curie('CommunicationLink.communicationProtocolType'),
                   model_uri=CIMTBL.communicationLink__communicationProtocolType, domain=None, range=Optional[Union[str, "CommunicationProtocolKind"]])

slots.communicationLink__BilateralExchangeActor = Slot(uri=CIM['CommunicationLink.BilateralExchangeActor'], name="communicationLink__BilateralExchangeActor", curie=CIM.curie('CommunicationLink.BilateralExchangeActor'),
                   model_uri=CIMTBL.communicationLink__BilateralExchangeActor, domain=None, range=Optional[Union[dict, BilateralExchangeActor]])

slots.compositeSwitch__compositeSwitchType = Slot(uri=CIM['CompositeSwitch.compositeSwitchType'], name="compositeSwitch__compositeSwitchType", curie=CIM.curie('CompositeSwitch.compositeSwitchType'),
                   model_uri=CIMTBL.compositeSwitch__compositeSwitchType, domain=None, range=Optional[str])

slots.concentricNeutralCableInfo__diameterOverNeutral = Slot(uri=CIM['ConcentricNeutralCableInfo.diameterOverNeutral'], name="concentricNeutralCableInfo__diameterOverNeutral", curie=CIM.curie('ConcentricNeutralCableInfo.diameterOverNeutral'),
                   model_uri=CIMTBL.concentricNeutralCableInfo__diameterOverNeutral, domain=None, range=Optional[float])

slots.concentricNeutralCableInfo__neutralStrandCount = Slot(uri=CIM['ConcentricNeutralCableInfo.neutralStrandCount'], name="concentricNeutralCableInfo__neutralStrandCount", curie=CIM.curie('ConcentricNeutralCableInfo.neutralStrandCount'),
                   model_uri=CIMTBL.concentricNeutralCableInfo__neutralStrandCount, domain=None, range=Optional[int])

slots.concentricNeutralCableInfo__neutralStrandGmr = Slot(uri=CIM['ConcentricNeutralCableInfo.neutralStrandGmr'], name="concentricNeutralCableInfo__neutralStrandGmr", curie=CIM.curie('ConcentricNeutralCableInfo.neutralStrandGmr'),
                   model_uri=CIMTBL.concentricNeutralCableInfo__neutralStrandGmr, domain=None, range=Optional[float])

slots.concentricNeutralCableInfo__neutralStrandRadius = Slot(uri=CIM['ConcentricNeutralCableInfo.neutralStrandRadius'], name="concentricNeutralCableInfo__neutralStrandRadius", curie=CIM.curie('ConcentricNeutralCableInfo.neutralStrandRadius'),
                   model_uri=CIMTBL.concentricNeutralCableInfo__neutralStrandRadius, domain=None, range=Optional[float])

slots.concentricNeutralCableInfo__neutralStrandRDC20 = Slot(uri=CIM['ConcentricNeutralCableInfo.neutralStrandRDC20'], name="concentricNeutralCableInfo__neutralStrandRDC20", curie=CIM.curie('ConcentricNeutralCableInfo.neutralStrandRDC20'),
                   model_uri=CIMTBL.concentricNeutralCableInfo__neutralStrandRDC20, domain=None, range=Optional[float])

slots.conductingAssetInfo__phaseCount = Slot(uri=CIM['ConductingAssetInfo.phaseCount'], name="conductingAssetInfo__phaseCount", curie=CIM.curie('ConductingAssetInfo.phaseCount'),
                   model_uri=CIMTBL.conductingAssetInfo__phaseCount, domain=None, range=Optional[Union[str, "PhaseCountKind"]])

slots.conductingAssetInfo__ratedCurrent = Slot(uri=CIM['ConductingAssetInfo.ratedCurrent'], name="conductingAssetInfo__ratedCurrent", curie=CIM.curie('ConductingAssetInfo.ratedCurrent'),
                   model_uri=CIMTBL.conductingAssetInfo__ratedCurrent, domain=None, range=Optional[float])

slots.conductingAssetInfo__ratedFrequency = Slot(uri=CIM['ConductingAssetInfo.ratedFrequency'], name="conductingAssetInfo__ratedFrequency", curie=CIM.curie('ConductingAssetInfo.ratedFrequency'),
                   model_uri=CIMTBL.conductingAssetInfo__ratedFrequency, domain=None, range=Optional[float])

slots.conductingAssetInfo__ratedVoltage = Slot(uri=CIM['ConductingAssetInfo.ratedVoltage'], name="conductingAssetInfo__ratedVoltage", curie=CIM.curie('ConductingAssetInfo.ratedVoltage'),
                   model_uri=CIMTBL.conductingAssetInfo__ratedVoltage, domain=None, range=Optional[float])

slots.conductingEquipment__BaseVoltage = Slot(uri=CIM['ConductingEquipment.BaseVoltage'], name="conductingEquipment__BaseVoltage", curie=CIM.curie('ConductingEquipment.BaseVoltage'),
                   model_uri=CIMTBL.conductingEquipment__BaseVoltage, domain=None, range=Optional[Union[dict, BaseVoltage]])

slots.conductingEquipment__GroundingAction = Slot(uri=CIM['ConductingEquipment.GroundingAction'], name="conductingEquipment__GroundingAction", curie=CIM.curie('ConductingEquipment.GroundingAction'),
                   model_uri=CIMTBL.conductingEquipment__GroundingAction, domain=None, range=Optional[Union[dict, GroundAction]])

slots.conductingEquipment__JumpingAction = Slot(uri=CIM['ConductingEquipment.JumpingAction'], name="conductingEquipment__JumpingAction", curie=CIM.curie('ConductingEquipment.JumpingAction'),
                   model_uri=CIMTBL.conductingEquipment__JumpingAction, domain=None, range=Optional[Union[dict, JumperAction]])

slots.conductingEquipment__Outage = Slot(uri=CIM['ConductingEquipment.Outage'], name="conductingEquipment__Outage", curie=CIM.curie('ConductingEquipment.Outage'),
                   model_uri=CIMTBL.conductingEquipment__Outage, domain=None, range=Optional[Union[dict, Outage]])

slots.conductor__length = Slot(uri=CIM['Conductor.length'], name="conductor__length", curie=CIM.curie('Conductor.length'),
                   model_uri=CIMTBL.conductor__length, domain=None, range=Optional[float])

slots.conductor__DamageCurve = Slot(uri=CIM['Conductor.DamageCurve'], name="conductor__DamageCurve", curie=CIM.curie('Conductor.DamageCurve'),
                   model_uri=CIMTBL.conductor__DamageCurve, domain=None, range=Optional[Union[dict, ConductorCharacteristicCurve]])

slots.conductorDistance__distance = Slot(uri=CIM['ConductorDistance.distance'], name="conductorDistance__distance", curie=CIM.curie('ConductorDistance.distance'),
                   model_uri=CIMTBL.conductorDistance__distance, domain=None, range=Optional[float])

slots.conductorDistance__fromPhase = Slot(uri=CIM['ConductorDistance.fromPhase'], name="conductorDistance__fromPhase", curie=CIM.curie('ConductorDistance.fromPhase'),
                   model_uri=CIMTBL.conductorDistance__fromPhase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.conductorDistance__fromSequenceNumber = Slot(uri=CIM['ConductorDistance.fromSequenceNumber'], name="conductorDistance__fromSequenceNumber", curie=CIM.curie('ConductorDistance.fromSequenceNumber'),
                   model_uri=CIMTBL.conductorDistance__fromSequenceNumber, domain=None, range=Optional[int])

slots.conductorDistance__toPhase = Slot(uri=CIM['ConductorDistance.toPhase'], name="conductorDistance__toPhase", curie=CIM.curie('ConductorDistance.toPhase'),
                   model_uri=CIMTBL.conductorDistance__toPhase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.conductorDistance__toSequenceNumber = Slot(uri=CIM['ConductorDistance.toSequenceNumber'], name="conductorDistance__toSequenceNumber", curie=CIM.curie('ConductorDistance.toSequenceNumber'),
                   model_uri=CIMTBL.conductorDistance__toSequenceNumber, domain=None, range=Optional[int])

slots.conductorDistance__WireSpacing = Slot(uri=CIM['ConductorDistance.WireSpacing'], name="conductorDistance__WireSpacing", curie=CIM.curie('ConductorDistance.WireSpacing'),
                   model_uri=CIMTBL.conductorDistance__WireSpacing, domain=None, range=Optional[Union[dict, ConductorDistanceSpacing]])

slots.conductorInfo__crossSection = Slot(uri=CIM['ConductorInfo.crossSection'], name="conductorInfo__crossSection", curie=CIM.curie('ConductorInfo.crossSection'),
                   model_uri=CIMTBL.conductorInfo__crossSection, domain=None, range=Optional[float])

slots.conductorInfo__material = Slot(uri=CIM['ConductorInfo.material'], name="conductorInfo__material", curie=CIM.curie('ConductorInfo.material'),
                   model_uri=CIMTBL.conductorInfo__material, domain=None, range=Optional[Union[str, "WireMaterialKind"]])

slots.conductorInfo__purpose = Slot(uri=CIM['ConductorInfo.purpose'], name="conductorInfo__purpose", curie=CIM.curie('ConductorInfo.purpose'),
                   model_uri=CIMTBL.conductorInfo__purpose, domain=None, range=Optional[str])

slots.conductorInfo__rAC25 = Slot(uri=CIM['ConductorInfo.rAC25'], name="conductorInfo__rAC25", curie=CIM.curie('ConductorInfo.rAC25'),
                   model_uri=CIMTBL.conductorInfo__rAC25, domain=None, range=Optional[float])

slots.conductorInfo__rAC50 = Slot(uri=CIM['ConductorInfo.rAC50'], name="conductorInfo__rAC50", curie=CIM.curie('ConductorInfo.rAC50'),
                   model_uri=CIMTBL.conductorInfo__rAC50, domain=None, range=Optional[float])

slots.conductorInfo__rAC75 = Slot(uri=CIM['ConductorInfo.rAC75'], name="conductorInfo__rAC75", curie=CIM.curie('ConductorInfo.rAC75'),
                   model_uri=CIMTBL.conductorInfo__rAC75, domain=None, range=Optional[float])

slots.conductorInfo__rDC20 = Slot(uri=CIM['ConductorInfo.rDC20'], name="conductorInfo__rDC20", curie=CIM.curie('ConductorInfo.rDC20'),
                   model_uri=CIMTBL.conductorInfo__rDC20, domain=None, range=Optional[float])

slots.conformLoad__LoadGroup = Slot(uri=CIM['ConformLoad.LoadGroup'], name="conformLoad__LoadGroup", curie=CIM.curie('ConformLoad.LoadGroup'),
                   model_uri=CIMTBL.conformLoad__LoadGroup, domain=None, range=Optional[Union[dict, ConformLoadGroup]])

slots.conformLoadSchedule__ConformLoadGroup = Slot(uri=CIM['ConformLoadSchedule.ConformLoadGroup'], name="conformLoadSchedule__ConformLoadGroup", curie=CIM.curie('ConformLoadSchedule.ConformLoadGroup'),
                   model_uri=CIMTBL.conformLoadSchedule__ConformLoadGroup, domain=None, range=Optional[Union[dict, ConformLoadGroup]])

slots.connectionAngleTapChanger__connectionAngleStepSize = Slot(uri=CIM['ConnectionAngleTapChanger.connectionAngleStepSize'], name="connectionAngleTapChanger__connectionAngleStepSize", curie=CIM.curie('ConnectionAngleTapChanger.connectionAngleStepSize'),
                   model_uri=CIMTBL.connectionAngleTapChanger__connectionAngleStepSize, domain=None, range=Optional[float])

slots.connectionAngleTapChanger__maxWindingConnectionAngle = Slot(uri=CIM['ConnectionAngleTapChanger.maxWindingConnectionAngle'], name="connectionAngleTapChanger__maxWindingConnectionAngle", curie=CIM.curie('ConnectionAngleTapChanger.maxWindingConnectionAngle'),
                   model_uri=CIMTBL.connectionAngleTapChanger__maxWindingConnectionAngle, domain=None, range=Optional[float])

slots.connectionAngleTapChanger__minWindingConnectionAngle = Slot(uri=CIM['ConnectionAngleTapChanger.minWindingConnectionAngle'], name="connectionAngleTapChanger__minWindingConnectionAngle", curie=CIM.curie('ConnectionAngleTapChanger.minWindingConnectionAngle'),
                   model_uri=CIMTBL.connectionAngleTapChanger__minWindingConnectionAngle, domain=None, range=Optional[float])

slots.connectionAngleTapChanger__normalWindingConnectionAngle = Slot(uri=CIM['ConnectionAngleTapChanger.normalWindingConnectionAngle'], name="connectionAngleTapChanger__normalWindingConnectionAngle", curie=CIM.curie('ConnectionAngleTapChanger.normalWindingConnectionAngle'),
                   model_uri=CIMTBL.connectionAngleTapChanger__normalWindingConnectionAngle, domain=None, range=Optional[float])

slots.connectionAngleTapChanger__windingConnectionAngle = Slot(uri=CIM['ConnectionAngleTapChanger.windingConnectionAngle'], name="connectionAngleTapChanger__windingConnectionAngle", curie=CIM.curie('ConnectionAngleTapChanger.windingConnectionAngle'),
                   model_uri=CIMTBL.connectionAngleTapChanger__windingConnectionAngle, domain=None, range=Optional[float])

slots.connectionAngleTapChangerTable__windingConnectionAngle = Slot(uri=CIM['ConnectionAngleTapChangerTable.windingConnectionAngle'], name="connectionAngleTapChangerTable__windingConnectionAngle", curie=CIM.curie('ConnectionAngleTapChangerTable.windingConnectionAngle'),
                   model_uri=CIMTBL.connectionAngleTapChangerTable__windingConnectionAngle, domain=None, range=Optional[float])

slots.connectionAngleTapChangerTable__ConnectionAngleTapChanger = Slot(uri=CIM['ConnectionAngleTapChangerTable.ConnectionAngleTapChanger'], name="connectionAngleTapChangerTable__ConnectionAngleTapChanger", curie=CIM.curie('ConnectionAngleTapChangerTable.ConnectionAngleTapChanger'),
                   model_uri=CIMTBL.connectionAngleTapChangerTable__ConnectionAngleTapChanger, domain=None, range=Optional[Union[dict, ConnectionAngleTapChanger]])

slots.connectivityArea__areaType = Slot(uri=CIM['ConnectivityArea.areaType'], name="connectivityArea__areaType", curie=CIM.curie('ConnectivityArea.areaType'),
                   model_uri=CIMTBL.connectivityArea__areaType, domain=None, range=Optional[Union[str, "ConnectivityAreaKind"]])

slots.connectivityArea__AdjacentArea = Slot(uri=CIM['ConnectivityArea.AdjacentArea'], name="connectivityArea__AdjacentArea", curie=CIM.curie('ConnectivityArea.AdjacentArea'),
                   model_uri=CIMTBL.connectivityArea__AdjacentArea, domain=None, range=Optional[Union[dict, ConnectivityArea]])

slots.connectivityArea__ContainedWithin = Slot(uri=CIM['ConnectivityArea.ContainedWithin'], name="connectivityArea__ContainedWithin", curie=CIM.curie('ConnectivityArea.ContainedWithin'),
                   model_uri=CIMTBL.connectivityArea__ContainedWithin, domain=None, range=Optional[Union[dict, ConnectivityArea]])

slots.connectivityNode__ACPointOfCommonCoupling = Slot(uri=CIM['ConnectivityNode.ACPointOfCommonCoupling'], name="connectivityNode__ACPointOfCommonCoupling", curie=CIM.curie('ConnectivityNode.ACPointOfCommonCoupling'),
                   model_uri=CIMTBL.connectivityNode__ACPointOfCommonCoupling, domain=None, range=Optional[Union[dict, ACPointOfCommonCoupling]])

slots.connectivityNode__BaseVoltage = Slot(uri=CIM['ConnectivityNode.BaseVoltage'], name="connectivityNode__BaseVoltage", curie=CIM.curie('ConnectivityNode.BaseVoltage'),
                   model_uri=CIMTBL.connectivityNode__BaseVoltage, domain=None, range=Optional[Union[dict, BaseVoltage]])

slots.connectivityNode__BoundaryPoint = Slot(uri=CIM['ConnectivityNode.BoundaryPoint'], name="connectivityNode__BoundaryPoint", curie=CIM.curie('ConnectivityNode.BoundaryPoint'),
                   model_uri=CIMTBL.connectivityNode__BoundaryPoint, domain=None, range=Optional[Union[dict, BoundaryPoint]])

slots.connectivityNode__ConnectivityNodeContainer = Slot(uri=CIM['ConnectivityNode.ConnectivityNodeContainer'], name="connectivityNode__ConnectivityNodeContainer", curie=CIM.curie('ConnectivityNode.ConnectivityNodeContainer'),
                   model_uri=CIMTBL.connectivityNode__ConnectivityNodeContainer, domain=None, range=Optional[Union[dict, ConnectivityNodeContainer]])

slots.connectivityNode__IndividualPnode = Slot(uri=CIM['ConnectivityNode.IndividualPnode'], name="connectivityNode__IndividualPnode", curie=CIM.curie('ConnectivityNode.IndividualPnode'),
                   model_uri=CIMTBL.connectivityNode__IndividualPnode, domain=None, range=Optional[Union[dict, IndividualPnode]])

slots.connectivityNode__TopologicalNode = Slot(uri=CIM['ConnectivityNode.TopologicalNode'], name="connectivityNode__TopologicalNode", curie=CIM.curie('ConnectivityNode.TopologicalNode'),
                   model_uri=CIMTBL.connectivityNode__TopologicalNode, domain=None, range=Optional[Union[dict, TopologicalNode]])

slots.controlArea__netInterchange = Slot(uri=CIM['ControlArea.netInterchange'], name="controlArea__netInterchange", curie=CIM.curie('ControlArea.netInterchange'),
                   model_uri=CIMTBL.controlArea__netInterchange, domain=None, range=Optional[float])

slots.controlArea__pTolerance = Slot(uri=CIM['ControlArea.pTolerance'], name="controlArea__pTolerance", curie=CIM.curie('ControlArea.pTolerance'),
                   model_uri=CIMTBL.controlArea__pTolerance, domain=None, range=Optional[float])

slots.controlArea__type = Slot(uri=CIM['ControlArea.type'], name="controlArea__type", curie=CIM.curie('ControlArea.type'),
                   model_uri=CIMTBL.controlArea__type, domain=None, range=Optional[Union[str, "ControlAreaTypeKind"]])

slots.controlArea__AreaInterchangeController = Slot(uri=CIM['ControlArea.AreaInterchangeController'], name="controlArea__AreaInterchangeController", curie=CIM.curie('ControlArea.AreaInterchangeController'),
                   model_uri=CIMTBL.controlArea__AreaInterchangeController, domain=None, range=Optional[Union[dict, AreaInterchangeController]])

slots.controlArea__EnergyArea = Slot(uri=CIM['ControlArea.EnergyArea'], name="controlArea__EnergyArea", curie=CIM.curie('ControlArea.EnergyArea'),
                   model_uri=CIMTBL.controlArea__EnergyArea, domain=None, range=Optional[Union[dict, EnergyArea]])

slots.controlArea__OutageCoordinationRegion = Slot(uri=CIM['ControlArea.OutageCoordinationRegion'], name="controlArea__OutageCoordinationRegion", curie=CIM.curie('ControlArea.OutageCoordinationRegion'),
                   model_uri=CIMTBL.controlArea__OutageCoordinationRegion, domain=None, range=Optional[Union[dict, OutageCoordinationRegion]])

slots.controlArea__PowerFrequencyController = Slot(uri=CIM['ControlArea.PowerFrequencyController'], name="controlArea__PowerFrequencyController", curie=CIM.curie('ControlArea.PowerFrequencyController'),
                   model_uri=CIMTBL.controlArea__PowerFrequencyController, domain=None, range=Optional[Union[dict, PowerFrequencyController]])

slots.controlArea__SystemOperator = Slot(uri=CIM['ControlArea.SystemOperator'], name="controlArea__SystemOperator", curie=CIM.curie('ControlArea.SystemOperator'),
                   model_uri=CIMTBL.controlArea__SystemOperator, domain=None, range=Optional[Union[dict, SystemOperator]])

slots.controlAreaGeneratingUnit__ControlArea = Slot(uri=CIM['ControlAreaGeneratingUnit.ControlArea'], name="controlAreaGeneratingUnit__ControlArea", curie=CIM.curie('ControlAreaGeneratingUnit.ControlArea'),
                   model_uri=CIMTBL.controlAreaGeneratingUnit__ControlArea, domain=None, range=Optional[Union[dict, ControlArea]])

slots.controlAreaGeneratingUnit__GeneratingUnit = Slot(uri=CIM['ControlAreaGeneratingUnit.GeneratingUnit'], name="controlAreaGeneratingUnit__GeneratingUnit", curie=CIM.curie('ControlAreaGeneratingUnit.GeneratingUnit'),
                   model_uri=CIMTBL.controlAreaGeneratingUnit__GeneratingUnit, domain=None, range=Optional[Union[dict, GeneratingUnit]])

slots.controlAreaPowerElectronicsUnit__ControlArea = Slot(uri=CIM['ControlAreaPowerElectronicsUnit.ControlArea'], name="controlAreaPowerElectronicsUnit__ControlArea", curie=CIM.curie('ControlAreaPowerElectronicsUnit.ControlArea'),
                   model_uri=CIMTBL.controlAreaPowerElectronicsUnit__ControlArea, domain=None, range=Optional[Union[dict, ControlArea]])

slots.controlAreaPowerElectronicsUnit__PowerElectronicsUnit = Slot(uri=CIM['ControlAreaPowerElectronicsUnit.PowerElectronicsUnit'], name="controlAreaPowerElectronicsUnit__PowerElectronicsUnit", curie=CIM.curie('ControlAreaPowerElectronicsUnit.PowerElectronicsUnit'),
                   model_uri=CIMTBL.controlAreaPowerElectronicsUnit__PowerElectronicsUnit, domain=None, range=Optional[Union[dict, PowerElectronicsUnit]])

slots.currentDroopControlFunction__droopCapacitive = Slot(uri=CIM['CurrentDroopControlFunction.droopCapacitive'], name="currentDroopControlFunction__droopCapacitive", curie=CIM.curie('CurrentDroopControlFunction.droopCapacitive'),
                   model_uri=CIMTBL.currentDroopControlFunction__droopCapacitive, domain=None, range=Optional[float])

slots.currentDroopControlFunction__droopInductive = Slot(uri=CIM['CurrentDroopControlFunction.droopInductive'], name="currentDroopControlFunction__droopInductive", curie=CIM.curie('CurrentDroopControlFunction.droopInductive'),
                   model_uri=CIMTBL.currentDroopControlFunction__droopInductive, domain=None, range=Optional[float])

slots.currentDroopControlFunction__offsetCapacitive = Slot(uri=CIM['CurrentDroopControlFunction.offsetCapacitive'], name="currentDroopControlFunction__offsetCapacitive", curie=CIM.curie('CurrentDroopControlFunction.offsetCapacitive'),
                   model_uri=CIMTBL.currentDroopControlFunction__offsetCapacitive, domain=None, range=Optional[float])

slots.currentDroopControlFunction__offsetInductive = Slot(uri=CIM['CurrentDroopControlFunction.offsetInductive'], name="currentDroopControlFunction__offsetInductive", curie=CIM.curie('CurrentDroopControlFunction.offsetInductive'),
                   model_uri=CIMTBL.currentDroopControlFunction__offsetInductive, domain=None, range=Optional[float])

slots.currentDroopControlFunction__targetValueCapacitive = Slot(uri=CIM['CurrentDroopControlFunction.targetValueCapacitive'], name="currentDroopControlFunction__targetValueCapacitive", curie=CIM.curie('CurrentDroopControlFunction.targetValueCapacitive'),
                   model_uri=CIMTBL.currentDroopControlFunction__targetValueCapacitive, domain=None, range=Optional[float])

slots.currentDroopControlFunction__targetValueInductive = Slot(uri=CIM['CurrentDroopControlFunction.targetValueInductive'], name="currentDroopControlFunction__targetValueInductive", curie=CIM.curie('CurrentDroopControlFunction.targetValueInductive'),
                   model_uri=CIMTBL.currentDroopControlFunction__targetValueInductive, domain=None, range=Optional[float])

slots.currentDroopOverride__mRID = Slot(uri=CIM['CurrentDroopOverride.mRID'], name="currentDroopOverride__mRID", curie=CIM.curie('CurrentDroopOverride.mRID'),
                   model_uri=CIMTBL.currentDroopOverride__mRID, domain=None, range=Optional[str])

slots.currentDroopOverride__droopCapacitive = Slot(uri=CIM['CurrentDroopOverride.droopCapacitive'], name="currentDroopOverride__droopCapacitive", curie=CIM.curie('CurrentDroopOverride.droopCapacitive'),
                   model_uri=CIMTBL.currentDroopOverride__droopCapacitive, domain=None, range=Optional[float])

slots.currentDroopOverride__droopInductive = Slot(uri=CIM['CurrentDroopOverride.droopInductive'], name="currentDroopOverride__droopInductive", curie=CIM.curie('CurrentDroopOverride.droopInductive'),
                   model_uri=CIMTBL.currentDroopOverride__droopInductive, domain=None, range=Optional[float])

slots.currentDroopOverride__enabled = Slot(uri=CIM['CurrentDroopOverride.enabled'], name="currentDroopOverride__enabled", curie=CIM.curie('CurrentDroopOverride.enabled'),
                   model_uri=CIMTBL.currentDroopOverride__enabled, domain=None, range=Optional[Union[bool, Bool]])

slots.currentDroopOverride__offsetCapacitiveI = Slot(uri=CIM['CurrentDroopOverride.offsetCapacitiveI'], name="currentDroopOverride__offsetCapacitiveI", curie=CIM.curie('CurrentDroopOverride.offsetCapacitiveI'),
                   model_uri=CIMTBL.currentDroopOverride__offsetCapacitiveI, domain=None, range=Optional[float])

slots.currentDroopOverride__offsetInductiveI = Slot(uri=CIM['CurrentDroopOverride.offsetInductiveI'], name="currentDroopOverride__offsetInductiveI", curie=CIM.curie('CurrentDroopOverride.offsetInductiveI'),
                   model_uri=CIMTBL.currentDroopOverride__offsetInductiveI, domain=None, range=Optional[float])

slots.currentDroopOverride__targetValueCapacitiveI = Slot(uri=CIM['CurrentDroopOverride.targetValueCapacitiveI'], name="currentDroopOverride__targetValueCapacitiveI", curie=CIM.curie('CurrentDroopOverride.targetValueCapacitiveI'),
                   model_uri=CIMTBL.currentDroopOverride__targetValueCapacitiveI, domain=None, range=Optional[float])

slots.currentDroopOverride__targetValueInductiveI = Slot(uri=CIM['CurrentDroopOverride.targetValueInductiveI'], name="currentDroopOverride__targetValueInductiveI", curie=CIM.curie('CurrentDroopOverride.targetValueInductiveI'),
                   model_uri=CIMTBL.currentDroopOverride__targetValueInductiveI, domain=None, range=Optional[float])

slots.currentDroopOverride__SSSCController = Slot(uri=CIM['CurrentDroopOverride.SSSCController'], name="currentDroopOverride__SSSCController", curie=CIM.curie('CurrentDroopOverride.SSSCController'),
                   model_uri=CIMTBL.currentDroopOverride__SSSCController, domain=None, range=Optional[Union[dict, SSSCController]])

slots.currentLimit__normalValue = Slot(uri=CIM['CurrentLimit.normalValue'], name="currentLimit__normalValue", curie=CIM.curie('CurrentLimit.normalValue'),
                   model_uri=CIMTBL.currentLimit__normalValue, domain=None, range=Optional[float])

slots.currentLimit__value = Slot(uri=CIM['CurrentLimit.value'], name="currentLimit__value", curie=CIM.curie('CurrentLimit.value'),
                   model_uri=CIMTBL.currentLimit__value, domain=None, range=Optional[float])

slots.currentTransformer__accuracyLimit = Slot(uri=CIM['CurrentTransformer.accuracyLimit'], name="currentTransformer__accuracyLimit", curie=CIM.curie('CurrentTransformer.accuracyLimit'),
                   model_uri=CIMTBL.currentTransformer__accuracyLimit, domain=None, range=Optional[float])

slots.currentTransformer__coreBurden = Slot(uri=CIM['CurrentTransformer.coreBurden'], name="currentTransformer__coreBurden", curie=CIM.curie('CurrentTransformer.coreBurden'),
                   model_uri=CIMTBL.currentTransformer__coreBurden, domain=None, range=Optional[float])

slots.currentTransformer__usage = Slot(uri=CIM['CurrentTransformer.usage'], name="currentTransformer__usage", curie=CIM.curie('CurrentTransformer.usage'),
                   model_uri=CIMTBL.currentTransformer__usage, domain=None, range=Optional[str])

slots.curve__curveStyle = Slot(uri=CIM['Curve.curveStyle'], name="curve__curveStyle", curie=CIM.curie('Curve.curveStyle'),
                   model_uri=CIMTBL.curve__curveStyle, domain=None, range=Optional[Union[str, "CurveStyle"]])

slots.curve__xMultiplier = Slot(uri=CIM['Curve.xMultiplier'], name="curve__xMultiplier", curie=CIM.curie('Curve.xMultiplier'),
                   model_uri=CIMTBL.curve__xMultiplier, domain=None, range=Optional[Union[str, "UnitMultiplier"]])

slots.curve__xUnit = Slot(uri=CIM['Curve.xUnit'], name="curve__xUnit", curie=CIM.curie('Curve.xUnit'),
                   model_uri=CIMTBL.curve__xUnit, domain=None, range=Optional[Union[str, "UnitSymbol"]])

slots.curve__y1Multiplier = Slot(uri=CIM['Curve.y1Multiplier'], name="curve__y1Multiplier", curie=CIM.curie('Curve.y1Multiplier'),
                   model_uri=CIMTBL.curve__y1Multiplier, domain=None, range=Optional[Union[str, "UnitMultiplier"]])

slots.curve__y1Unit = Slot(uri=CIM['Curve.y1Unit'], name="curve__y1Unit", curie=CIM.curie('Curve.y1Unit'),
                   model_uri=CIMTBL.curve__y1Unit, domain=None, range=Optional[Union[str, "UnitSymbol"]])

slots.curve__y2Multiplier = Slot(uri=CIM['Curve.y2Multiplier'], name="curve__y2Multiplier", curie=CIM.curie('Curve.y2Multiplier'),
                   model_uri=CIMTBL.curve__y2Multiplier, domain=None, range=Optional[Union[str, "UnitMultiplier"]])

slots.curve__y2Unit = Slot(uri=CIM['Curve.y2Unit'], name="curve__y2Unit", curie=CIM.curie('Curve.y2Unit'),
                   model_uri=CIMTBL.curve__y2Unit, domain=None, range=Optional[Union[str, "UnitSymbol"]])

slots.curve__y3Multiplier = Slot(uri=CIM['Curve.y3Multiplier'], name="curve__y3Multiplier", curie=CIM.curie('Curve.y3Multiplier'),
                   model_uri=CIMTBL.curve__y3Multiplier, domain=None, range=Optional[Union[str, "UnitMultiplier"]])

slots.curve__y3Unit = Slot(uri=CIM['Curve.y3Unit'], name="curve__y3Unit", curie=CIM.curie('Curve.y3Unit'),
                   model_uri=CIMTBL.curve__y3Unit, domain=None, range=Optional[Union[str, "UnitSymbol"]])

slots.curveData__xvalue = Slot(uri=CIM['CurveData.xvalue'], name="curveData__xvalue", curie=CIM.curie('CurveData.xvalue'),
                   model_uri=CIMTBL.curveData__xvalue, domain=None, range=Optional[float])

slots.curveData__y1value = Slot(uri=CIM['CurveData.y1value'], name="curveData__y1value", curie=CIM.curie('CurveData.y1value'),
                   model_uri=CIMTBL.curveData__y1value, domain=None, range=Optional[float])

slots.curveData__y2value = Slot(uri=CIM['CurveData.y2value'], name="curveData__y2value", curie=CIM.curie('CurveData.y2value'),
                   model_uri=CIMTBL.curveData__y2value, domain=None, range=Optional[float])

slots.curveData__y3value = Slot(uri=CIM['CurveData.y3value'], name="curveData__y3value", curie=CIM.curie('CurveData.y3value'),
                   model_uri=CIMTBL.curveData__y3value, domain=None, range=Optional[float])

slots.curveData__Curve = Slot(uri=CIM['CurveData.Curve'], name="curveData__Curve", curie=CIM.curie('CurveData.Curve'),
                   model_uri=CIMTBL.curveData__Curve, domain=None, range=Optional[Union[dict, Curve]])

slots.cut__lengthFromTerminal1 = Slot(uri=CIM['Cut.lengthFromTerminal1'], name="cut__lengthFromTerminal1", curie=CIM.curie('Cut.lengthFromTerminal1'),
                   model_uri=CIMTBL.cut__lengthFromTerminal1, domain=None, range=Optional[float])

slots.cut__ACLineSegment = Slot(uri=CIM['Cut.ACLineSegment'], name="cut__ACLineSegment", curie=CIM.curie('Cut.ACLineSegment'),
                   model_uri=CIMTBL.cut__ACLineSegment, domain=None, range=Optional[Union[dict, ACLineSegment]])

slots.cut__CutAction = Slot(uri=CIM['Cut.CutAction'], name="cut__CutAction", curie=CIM.curie('Cut.CutAction'),
                   model_uri=CIMTBL.cut__CutAction, domain=None, range=Optional[Union[dict, CutAction]])

slots.dateInterval__end = Slot(uri=CIM['DateInterval.end'], name="dateInterval__end", curie=CIM.curie('DateInterval.end'),
                   model_uri=CIMTBL.dateInterval__end, domain=None, range=Optional[Union[str, XSDDate]])

slots.dateInterval__start = Slot(uri=CIM['DateInterval.start'], name="dateInterval__start", curie=CIM.curie('DateInterval.start'),
                   model_uri=CIMTBL.dateInterval__start, domain=None, range=Optional[Union[str, XSDDate]])

slots.dateTimeInterval__end = Slot(uri=CIM['DateTimeInterval.end'], name="dateTimeInterval__end", curie=CIM.curie('DateTimeInterval.end'),
                   model_uri=CIMTBL.dateTimeInterval__end, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.dateTimeInterval__start = Slot(uri=CIM['DateTimeInterval.start'], name="dateTimeInterval__start", curie=CIM.curie('DateTimeInterval.start'),
                   model_uri=CIMTBL.dateTimeInterval__start, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.decimalQuantity__currency = Slot(uri=CIM['DecimalQuantity.currency'], name="decimalQuantity__currency", curie=CIM.curie('DecimalQuantity.currency'),
                   model_uri=CIMTBL.decimalQuantity__currency, domain=None, range=Optional[Union[str, "Currency"]])

slots.decimalQuantity__multiplier = Slot(uri=CIM['DecimalQuantity.multiplier'], name="decimalQuantity__multiplier", curie=CIM.curie('DecimalQuantity.multiplier'),
                   model_uri=CIMTBL.decimalQuantity__multiplier, domain=None, range=Optional[Union[str, "UnitMultiplier"]])

slots.decimalQuantity__unit = Slot(uri=CIM['DecimalQuantity.unit'], name="decimalQuantity__unit", curie=CIM.curie('DecimalQuantity.unit'),
                   model_uri=CIMTBL.decimalQuantity__unit, domain=None, range=Optional[Union[str, "UnitSymbol"]])

slots.decimalQuantity__value = Slot(uri=CIM['DecimalQuantity.value'], name="decimalQuantity__value", curie=CIM.curie('DecimalQuantity.value'),
                   model_uri=CIMTBL.decimalQuantity__value, domain=None, range=Optional[Decimal])

slots.discrete__maxValue = Slot(uri=CIM['Discrete.maxValue'], name="discrete__maxValue", curie=CIM.curie('Discrete.maxValue'),
                   model_uri=CIMTBL.discrete__maxValue, domain=None, range=Optional[int])

slots.discrete__minValue = Slot(uri=CIM['Discrete.minValue'], name="discrete__minValue", curie=CIM.curie('Discrete.minValue'),
                   model_uri=CIMTBL.discrete__minValue, domain=None, range=Optional[int])

slots.discrete__normalValue = Slot(uri=CIM['Discrete.normalValue'], name="discrete__normalValue", curie=CIM.curie('Discrete.normalValue'),
                   model_uri=CIMTBL.discrete__normalValue, domain=None, range=Optional[int])

slots.discrete__ValueAliasSet = Slot(uri=CIM['Discrete.ValueAliasSet'], name="discrete__ValueAliasSet", curie=CIM.curie('Discrete.ValueAliasSet'),
                   model_uri=CIMTBL.discrete__ValueAliasSet, domain=None, range=Optional[Union[dict, ValueAliasSet]])

slots.ductBank__circuitCount = Slot(uri=CIM['DuctBank.circuitCount'], name="ductBank__circuitCount", curie=CIM.curie('DuctBank.circuitCount'),
                   model_uri=CIMTBL.ductBank__circuitCount, domain=None, range=Optional[int])

slots.eVSE__chargingModeType = Slot(uri=CIM['EVSE.chargingModeType'], name="eVSE__chargingModeType", curie=CIM.curie('EVSE.chargingModeType'),
                   model_uri=CIMTBL.eVSE__chargingModeType, domain=None, range=Optional[Union[str, "ChargingModeKind"]])

slots.earthFaultCompensator__r = Slot(uri=CIM['EarthFaultCompensator.r'], name="earthFaultCompensator__r", curie=CIM.curie('EarthFaultCompensator.r'),
                   model_uri=CIMTBL.earthFaultCompensator__r, domain=None, range=Optional[float])

slots.earthResistivity__earthModelType = Slot(uri=CIM['EarthResistivity.earthModelType'], name="earthResistivity__earthModelType", curie=CIM.curie('EarthResistivity.earthModelType'),
                   model_uri=CIMTBL.earthResistivity__earthModelType, domain=None, range=Optional[Union[str, "EarthModelKind"]])

slots.earthResistivity__earthReturnGMR = Slot(uri=CIM['EarthResistivity.earthReturnGMR'], name="earthResistivity__earthReturnGMR", curie=CIM.curie('EarthResistivity.earthReturnGMR'),
                   model_uri=CIMTBL.earthResistivity__earthReturnGMR, domain=None, range=Optional[float])

slots.earthResistivity__rho = Slot(uri=CIM['EarthResistivity.rho'], name="earthResistivity__rho", curie=CIM.curie('EarthResistivity.rho'),
                   model_uri=CIMTBL.earthResistivity__rho, domain=None, range=Optional[float])

slots.electricVehicleInfo__batteryCapacity = Slot(uri=CIM['ElectricVehicleInfo.batteryCapacity'], name="electricVehicleInfo__batteryCapacity", curie=CIM.curie('ElectricVehicleInfo.batteryCapacity'),
                   model_uri=CIMTBL.electricVehicleInfo__batteryCapacity, domain=None, range=Optional[float])

slots.electricVehicleInfo__evType = Slot(uri=CIM['ElectricVehicleInfo.evType'], name="electricVehicleInfo__evType", curie=CIM.curie('ElectricVehicleInfo.evType'),
                   model_uri=CIMTBL.electricVehicleInfo__evType, domain=None, range=Optional[Union[str, "EVTypeKind"]])

slots.electricVehicleInfo__maxChargingRate = Slot(uri=CIM['ElectricVehicleInfo.maxChargingRate'], name="electricVehicleInfo__maxChargingRate", curie=CIM.curie('ElectricVehicleInfo.maxChargingRate'),
                   model_uri=CIMTBL.electricVehicleInfo__maxChargingRate, domain=None, range=Optional[float])

slots.electricVehicleInfo__v2gCapable = Slot(uri=CIM['ElectricVehicleInfo.v2gCapable'], name="electricVehicleInfo__v2gCapable", curie=CIM.curie('ElectricVehicleInfo.v2gCapable'),
                   model_uri=CIMTBL.electricVehicleInfo__v2gCapable, domain=None, range=Optional[Union[bool, Bool]])

slots.electricVehicleInfo__BatteryInfo = Slot(uri=CIM['ElectricVehicleInfo.BatteryInfo'], name="electricVehicleInfo__BatteryInfo", curie=CIM.curie('ElectricVehicleInfo.BatteryInfo'),
                   model_uri=CIMTBL.electricVehicleInfo__BatteryInfo, domain=None, range=Optional[Union[dict, BatteryInfo]])

slots.electricalVehicleUnit__v2gCapable = Slot(uri=CIM['ElectricalVehicleUnit.v2gCapable'], name="electricalVehicleUnit__v2gCapable", curie=CIM.curie('ElectricalVehicleUnit.v2gCapable'),
                   model_uri=CIMTBL.electricalVehicleUnit__v2gCapable, domain=None, range=Optional[Union[bool, Bool]])

slots.energyArea__ControlArea = Slot(uri=CIM['EnergyArea.ControlArea'], name="energyArea__ControlArea", curie=CIM.curie('EnergyArea.ControlArea'),
                   model_uri=CIMTBL.energyArea__ControlArea, domain=None, range=Optional[Union[dict, ControlArea]])

slots.energyConsumer__customerCount = Slot(uri=CIM['EnergyConsumer.customerCount'], name="energyConsumer__customerCount", curie=CIM.curie('EnergyConsumer.customerCount'),
                   model_uri=CIMTBL.energyConsumer__customerCount, domain=None, range=Optional[int])

slots.energyConsumer__grounded = Slot(uri=CIM['EnergyConsumer.grounded'], name="energyConsumer__grounded", curie=CIM.curie('EnergyConsumer.grounded'),
                   model_uri=CIMTBL.energyConsumer__grounded, domain=None, range=Optional[Union[bool, Bool]])

slots.energyConsumer__p = Slot(uri=CIM['EnergyConsumer.p'], name="energyConsumer__p", curie=CIM.curie('EnergyConsumer.p'),
                   model_uri=CIMTBL.energyConsumer__p, domain=None, range=Optional[float])

slots.energyConsumer__pfixed = Slot(uri=CIM['EnergyConsumer.pfixed'], name="energyConsumer__pfixed", curie=CIM.curie('EnergyConsumer.pfixed'),
                   model_uri=CIMTBL.energyConsumer__pfixed, domain=None, range=Optional[float])

slots.energyConsumer__pfixedPct = Slot(uri=CIM['EnergyConsumer.pfixedPct'], name="energyConsumer__pfixedPct", curie=CIM.curie('EnergyConsumer.pfixedPct'),
                   model_uri=CIMTBL.energyConsumer__pfixedPct, domain=None, range=Optional[float])

slots.energyConsumer__phaseConnection = Slot(uri=CIM['EnergyConsumer.phaseConnection'], name="energyConsumer__phaseConnection", curie=CIM.curie('EnergyConsumer.phaseConnection'),
                   model_uri=CIMTBL.energyConsumer__phaseConnection, domain=None, range=Optional[Union[str, "PhaseShuntConnectionKind"]])

slots.energyConsumer__q = Slot(uri=CIM['EnergyConsumer.q'], name="energyConsumer__q", curie=CIM.curie('EnergyConsumer.q'),
                   model_uri=CIMTBL.energyConsumer__q, domain=None, range=Optional[float])

slots.energyConsumer__qfixed = Slot(uri=CIM['EnergyConsumer.qfixed'], name="energyConsumer__qfixed", curie=CIM.curie('EnergyConsumer.qfixed'),
                   model_uri=CIMTBL.energyConsumer__qfixed, domain=None, range=Optional[float])

slots.energyConsumer__qfixedPct = Slot(uri=CIM['EnergyConsumer.qfixedPct'], name="energyConsumer__qfixedPct", curie=CIM.curie('EnergyConsumer.qfixedPct'),
                   model_uri=CIMTBL.energyConsumer__qfixedPct, domain=None, range=Optional[float])

slots.energyConsumer__AreaDispatchableUnit = Slot(uri=CIM['EnergyConsumer.AreaDispatchableUnit'], name="energyConsumer__AreaDispatchableUnit", curie=CIM.curie('EnergyConsumer.AreaDispatchableUnit'),
                   model_uri=CIMTBL.energyConsumer__AreaDispatchableUnit, domain=None, range=Optional[Union[dict, AreaDispatchableUnit]])

slots.energyConsumer__EnergyConsumerAction = Slot(uri=CIM['EnergyConsumer.EnergyConsumerAction'], name="energyConsumer__EnergyConsumerAction", curie=CIM.curie('EnergyConsumer.EnergyConsumerAction'),
                   model_uri=CIMTBL.energyConsumer__EnergyConsumerAction, domain=None, range=Optional[Union[dict, EnergyConsumerAction]])

slots.energyConsumer__LoadDynamics = Slot(uri=CIM['EnergyConsumer.LoadDynamics'], name="energyConsumer__LoadDynamics", curie=CIM.curie('EnergyConsumer.LoadDynamics'),
                   model_uri=CIMTBL.energyConsumer__LoadDynamics, domain=None, range=Optional[Union[dict, LoadDynamics]])

slots.energyConsumer__LoadResponse = Slot(uri=CIM['EnergyConsumer.LoadResponse'], name="energyConsumer__LoadResponse", curie=CIM.curie('EnergyConsumer.LoadResponse'),
                   model_uri=CIMTBL.energyConsumer__LoadResponse, domain=None, range=Optional[Union[dict, LoadResponseCharacteristic]])

slots.energyConsumer__PowerCutZone = Slot(uri=CIM['EnergyConsumer.PowerCutZone'], name="energyConsumer__PowerCutZone", curie=CIM.curie('EnergyConsumer.PowerCutZone'),
                   model_uri=CIMTBL.energyConsumer__PowerCutZone, domain=None, range=Optional[Union[dict, PowerCutZone]])

slots.energyConsumerPhase__p = Slot(uri=CIM['EnergyConsumerPhase.p'], name="energyConsumerPhase__p", curie=CIM.curie('EnergyConsumerPhase.p'),
                   model_uri=CIMTBL.energyConsumerPhase__p, domain=None, range=Optional[float])

slots.energyConsumerPhase__pfixed = Slot(uri=CIM['EnergyConsumerPhase.pfixed'], name="energyConsumerPhase__pfixed", curie=CIM.curie('EnergyConsumerPhase.pfixed'),
                   model_uri=CIMTBL.energyConsumerPhase__pfixed, domain=None, range=Optional[float])

slots.energyConsumerPhase__pfixedPct = Slot(uri=CIM['EnergyConsumerPhase.pfixedPct'], name="energyConsumerPhase__pfixedPct", curie=CIM.curie('EnergyConsumerPhase.pfixedPct'),
                   model_uri=CIMTBL.energyConsumerPhase__pfixedPct, domain=None, range=Optional[float])

slots.energyConsumerPhase__phase = Slot(uri=CIM['EnergyConsumerPhase.phase'], name="energyConsumerPhase__phase", curie=CIM.curie('EnergyConsumerPhase.phase'),
                   model_uri=CIMTBL.energyConsumerPhase__phase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.energyConsumerPhase__q = Slot(uri=CIM['EnergyConsumerPhase.q'], name="energyConsumerPhase__q", curie=CIM.curie('EnergyConsumerPhase.q'),
                   model_uri=CIMTBL.energyConsumerPhase__q, domain=None, range=Optional[float])

slots.energyConsumerPhase__qfixed = Slot(uri=CIM['EnergyConsumerPhase.qfixed'], name="energyConsumerPhase__qfixed", curie=CIM.curie('EnergyConsumerPhase.qfixed'),
                   model_uri=CIMTBL.energyConsumerPhase__qfixed, domain=None, range=Optional[float])

slots.energyConsumerPhase__qfixedPct = Slot(uri=CIM['EnergyConsumerPhase.qfixedPct'], name="energyConsumerPhase__qfixedPct", curie=CIM.curie('EnergyConsumerPhase.qfixedPct'),
                   model_uri=CIMTBL.energyConsumerPhase__qfixedPct, domain=None, range=Optional[float])

slots.energyConsumerPhase__EnergyConsumer = Slot(uri=CIM['EnergyConsumerPhase.EnergyConsumer'], name="energyConsumerPhase__EnergyConsumer", curie=CIM.curie('EnergyConsumerPhase.EnergyConsumer'),
                   model_uri=CIMTBL.energyConsumerPhase__EnergyConsumer, domain=None, range=Optional[Union[dict, EnergyConsumer]])

slots.energySource__activePower = Slot(uri=CIM['EnergySource.activePower'], name="energySource__activePower", curie=CIM.curie('EnergySource.activePower'),
                   model_uri=CIMTBL.energySource__activePower, domain=None, range=Optional[float])

slots.energySource__grounded = Slot(uri=CIM['EnergySource.grounded'], name="energySource__grounded", curie=CIM.curie('EnergySource.grounded'),
                   model_uri=CIMTBL.energySource__grounded, domain=None, range=Optional[Union[bool, Bool]])

slots.energySource__nominalVoltage = Slot(uri=CIM['EnergySource.nominalVoltage'], name="energySource__nominalVoltage", curie=CIM.curie('EnergySource.nominalVoltage'),
                   model_uri=CIMTBL.energySource__nominalVoltage, domain=None, range=Optional[float])

slots.energySource__pMax = Slot(uri=CIM['EnergySource.pMax'], name="energySource__pMax", curie=CIM.curie('EnergySource.pMax'),
                   model_uri=CIMTBL.energySource__pMax, domain=None, range=Optional[float])

slots.energySource__pMin = Slot(uri=CIM['EnergySource.pMin'], name="energySource__pMin", curie=CIM.curie('EnergySource.pMin'),
                   model_uri=CIMTBL.energySource__pMin, domain=None, range=Optional[float])

slots.energySource__r = Slot(uri=CIM['EnergySource.r'], name="energySource__r", curie=CIM.curie('EnergySource.r'),
                   model_uri=CIMTBL.energySource__r, domain=None, range=Optional[float])

slots.energySource__r0 = Slot(uri=CIM['EnergySource.r0'], name="energySource__r0", curie=CIM.curie('EnergySource.r0'),
                   model_uri=CIMTBL.energySource__r0, domain=None, range=Optional[float])

slots.energySource__r2 = Slot(uri=CIM['EnergySource.r2'], name="energySource__r2", curie=CIM.curie('EnergySource.r2'),
                   model_uri=CIMTBL.energySource__r2, domain=None, range=Optional[float])

slots.energySource__reactivePower = Slot(uri=CIM['EnergySource.reactivePower'], name="energySource__reactivePower", curie=CIM.curie('EnergySource.reactivePower'),
                   model_uri=CIMTBL.energySource__reactivePower, domain=None, range=Optional[float])

slots.energySource__voltageAngle = Slot(uri=CIM['EnergySource.voltageAngle'], name="energySource__voltageAngle", curie=CIM.curie('EnergySource.voltageAngle'),
                   model_uri=CIMTBL.energySource__voltageAngle, domain=None, range=Optional[float])

slots.energySource__voltageMagnitude = Slot(uri=CIM['EnergySource.voltageMagnitude'], name="energySource__voltageMagnitude", curie=CIM.curie('EnergySource.voltageMagnitude'),
                   model_uri=CIMTBL.energySource__voltageMagnitude, domain=None, range=Optional[float])

slots.energySource__x = Slot(uri=CIM['EnergySource.x'], name="energySource__x", curie=CIM.curie('EnergySource.x'),
                   model_uri=CIMTBL.energySource__x, domain=None, range=Optional[float])

slots.energySource__x0 = Slot(uri=CIM['EnergySource.x0'], name="energySource__x0", curie=CIM.curie('EnergySource.x0'),
                   model_uri=CIMTBL.energySource__x0, domain=None, range=Optional[float])

slots.energySource__x2 = Slot(uri=CIM['EnergySource.x2'], name="energySource__x2", curie=CIM.curie('EnergySource.x2'),
                   model_uri=CIMTBL.energySource__x2, domain=None, range=Optional[float])

slots.energySource__EnergySchedulingType = Slot(uri=CIM['EnergySource.EnergySchedulingType'], name="energySource__EnergySchedulingType", curie=CIM.curie('EnergySource.EnergySchedulingType'),
                   model_uri=CIMTBL.energySource__EnergySchedulingType, domain=None, range=Optional[Union[dict, EnergySchedulingType]])

slots.energySource__EnergySourceAction = Slot(uri=CIM['EnergySource.EnergySourceAction'], name="energySource__EnergySourceAction", curie=CIM.curie('EnergySource.EnergySourceAction'),
                   model_uri=CIMTBL.energySource__EnergySourceAction, domain=None, range=Optional[Union[dict, EnergySourceModification]])

slots.energySourcePhase__phase = Slot(uri=CIM['EnergySourcePhase.phase'], name="energySourcePhase__phase", curie=CIM.curie('EnergySourcePhase.phase'),
                   model_uri=CIMTBL.energySourcePhase__phase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.energySourcePhase__EnergySource = Slot(uri=CIM['EnergySourcePhase.EnergySource'], name="energySourcePhase__EnergySource", curie=CIM.curie('EnergySourcePhase.EnergySource'),
                   model_uri=CIMTBL.energySourcePhase__EnergySource, domain=None, range=Optional[Union[dict, EnergySource]])

slots.equipment__aggregate = Slot(uri=CIM['Equipment.aggregate'], name="equipment__aggregate", curie=CIM.curie('Equipment.aggregate'),
                   model_uri=CIMTBL.equipment__aggregate, domain=None, range=Optional[Union[bool, Bool]])

slots.equipment__inService = Slot(uri=CIM['Equipment.inService'], name="equipment__inService", curie=CIM.curie('Equipment.inService'),
                   model_uri=CIMTBL.equipment__inService, domain=None, range=Optional[Union[bool, Bool]])

slots.equipment__networkAnalysisEnabled = Slot(uri=CIM['Equipment.networkAnalysisEnabled'], name="equipment__networkAnalysisEnabled", curie=CIM.curie('Equipment.networkAnalysisEnabled'),
                   model_uri=CIMTBL.equipment__networkAnalysisEnabled, domain=None, range=Optional[Union[bool, Bool]])

slots.equipment__normallyInService = Slot(uri=CIM['Equipment.normallyInService'], name="equipment__normallyInService", curie=CIM.curie('Equipment.normallyInService'),
                   model_uri=CIMTBL.equipment__normallyInService, domain=None, range=Optional[Union[bool, Bool]])

slots.equipment__AdditionalEquipmentContainer = Slot(uri=CIM['Equipment.AdditionalEquipmentContainer'], name="equipment__AdditionalEquipmentContainer", curie=CIM.curie('Equipment.AdditionalEquipmentContainer'),
                   model_uri=CIMTBL.equipment__AdditionalEquipmentContainer, domain=None, range=Optional[Union[Union[dict, EquipmentContainer], list[Union[dict, EquipmentContainer]]]])

slots.equipment__EquipmentContainer = Slot(uri=CIM['Equipment.EquipmentContainer'], name="equipment__EquipmentContainer", curie=CIM.curie('Equipment.EquipmentContainer'),
                   model_uri=CIMTBL.equipment__EquipmentContainer, domain=None, range=Optional[Union[dict, EquipmentContainer]])

slots.equivalentDistanceSpacing__averageNeutralHeight = Slot(uri=CIM['EquivalentDistanceSpacing.averageNeutralHeight'], name="equivalentDistanceSpacing__averageNeutralHeight", curie=CIM.curie('EquivalentDistanceSpacing.averageNeutralHeight'),
                   model_uri=CIMTBL.equivalentDistanceSpacing__averageNeutralHeight, domain=None, range=Optional[float])

slots.equivalentDistanceSpacing__averagePhaseHeight = Slot(uri=CIM['EquivalentDistanceSpacing.averagePhaseHeight'], name="equivalentDistanceSpacing__averagePhaseHeight", curie=CIM.curie('EquivalentDistanceSpacing.averagePhaseHeight'),
                   model_uri=CIMTBL.equivalentDistanceSpacing__averagePhaseHeight, domain=None, range=Optional[float])

slots.equivalentDistanceSpacing__phaseToNeutralGMD = Slot(uri=CIM['EquivalentDistanceSpacing.phaseToNeutralGMD'], name="equivalentDistanceSpacing__phaseToNeutralGMD", curie=CIM.curie('EquivalentDistanceSpacing.phaseToNeutralGMD'),
                   model_uri=CIMTBL.equivalentDistanceSpacing__phaseToNeutralGMD, domain=None, range=Optional[float])

slots.equivalentDistanceSpacing__phaseToPhaseGMD = Slot(uri=CIM['EquivalentDistanceSpacing.phaseToPhaseGMD'], name="equivalentDistanceSpacing__phaseToPhaseGMD", curie=CIM.curie('EquivalentDistanceSpacing.phaseToPhaseGMD'),
                   model_uri=CIMTBL.equivalentDistanceSpacing__phaseToPhaseGMD, domain=None, range=Optional[float])

slots.externalNetworkInjection__governorSCD = Slot(uri=CIM['ExternalNetworkInjection.governorSCD'], name="externalNetworkInjection__governorSCD", curie=CIM.curie('ExternalNetworkInjection.governorSCD'),
                   model_uri=CIMTBL.externalNetworkInjection__governorSCD, domain=None, range=Optional[float])

slots.externalNetworkInjection__ikSecond = Slot(uri=CIM['ExternalNetworkInjection.ikSecond'], name="externalNetworkInjection__ikSecond", curie=CIM.curie('ExternalNetworkInjection.ikSecond'),
                   model_uri=CIMTBL.externalNetworkInjection__ikSecond, domain=None, range=Optional[Union[bool, Bool]])

slots.externalNetworkInjection__maxInitialSymShCCurrent = Slot(uri=CIM['ExternalNetworkInjection.maxInitialSymShCCurrent'], name="externalNetworkInjection__maxInitialSymShCCurrent", curie=CIM.curie('ExternalNetworkInjection.maxInitialSymShCCurrent'),
                   model_uri=CIMTBL.externalNetworkInjection__maxInitialSymShCCurrent, domain=None, range=Optional[float])

slots.externalNetworkInjection__maxP = Slot(uri=CIM['ExternalNetworkInjection.maxP'], name="externalNetworkInjection__maxP", curie=CIM.curie('ExternalNetworkInjection.maxP'),
                   model_uri=CIMTBL.externalNetworkInjection__maxP, domain=None, range=Optional[float])

slots.externalNetworkInjection__maxQ = Slot(uri=CIM['ExternalNetworkInjection.maxQ'], name="externalNetworkInjection__maxQ", curie=CIM.curie('ExternalNetworkInjection.maxQ'),
                   model_uri=CIMTBL.externalNetworkInjection__maxQ, domain=None, range=Optional[float])

slots.externalNetworkInjection__maxR0ToX0Ratio = Slot(uri=CIM['ExternalNetworkInjection.maxR0ToX0Ratio'], name="externalNetworkInjection__maxR0ToX0Ratio", curie=CIM.curie('ExternalNetworkInjection.maxR0ToX0Ratio'),
                   model_uri=CIMTBL.externalNetworkInjection__maxR0ToX0Ratio, domain=None, range=Optional[float])

slots.externalNetworkInjection__maxR1ToX1Ratio = Slot(uri=CIM['ExternalNetworkInjection.maxR1ToX1Ratio'], name="externalNetworkInjection__maxR1ToX1Ratio", curie=CIM.curie('ExternalNetworkInjection.maxR1ToX1Ratio'),
                   model_uri=CIMTBL.externalNetworkInjection__maxR1ToX1Ratio, domain=None, range=Optional[float])

slots.externalNetworkInjection__maxZ0ToZ1Ratio = Slot(uri=CIM['ExternalNetworkInjection.maxZ0ToZ1Ratio'], name="externalNetworkInjection__maxZ0ToZ1Ratio", curie=CIM.curie('ExternalNetworkInjection.maxZ0ToZ1Ratio'),
                   model_uri=CIMTBL.externalNetworkInjection__maxZ0ToZ1Ratio, domain=None, range=Optional[float])

slots.externalNetworkInjection__minInitialSymShCCurrent = Slot(uri=CIM['ExternalNetworkInjection.minInitialSymShCCurrent'], name="externalNetworkInjection__minInitialSymShCCurrent", curie=CIM.curie('ExternalNetworkInjection.minInitialSymShCCurrent'),
                   model_uri=CIMTBL.externalNetworkInjection__minInitialSymShCCurrent, domain=None, range=Optional[float])

slots.externalNetworkInjection__minP = Slot(uri=CIM['ExternalNetworkInjection.minP'], name="externalNetworkInjection__minP", curie=CIM.curie('ExternalNetworkInjection.minP'),
                   model_uri=CIMTBL.externalNetworkInjection__minP, domain=None, range=Optional[float])

slots.externalNetworkInjection__minQ = Slot(uri=CIM['ExternalNetworkInjection.minQ'], name="externalNetworkInjection__minQ", curie=CIM.curie('ExternalNetworkInjection.minQ'),
                   model_uri=CIMTBL.externalNetworkInjection__minQ, domain=None, range=Optional[float])

slots.externalNetworkInjection__minR0ToX0Ratio = Slot(uri=CIM['ExternalNetworkInjection.minR0ToX0Ratio'], name="externalNetworkInjection__minR0ToX0Ratio", curie=CIM.curie('ExternalNetworkInjection.minR0ToX0Ratio'),
                   model_uri=CIMTBL.externalNetworkInjection__minR0ToX0Ratio, domain=None, range=Optional[float])

slots.externalNetworkInjection__minR1ToX1Ratio = Slot(uri=CIM['ExternalNetworkInjection.minR1ToX1Ratio'], name="externalNetworkInjection__minR1ToX1Ratio", curie=CIM.curie('ExternalNetworkInjection.minR1ToX1Ratio'),
                   model_uri=CIMTBL.externalNetworkInjection__minR1ToX1Ratio, domain=None, range=Optional[float])

slots.externalNetworkInjection__minZ0ToZ1Ratio = Slot(uri=CIM['ExternalNetworkInjection.minZ0ToZ1Ratio'], name="externalNetworkInjection__minZ0ToZ1Ratio", curie=CIM.curie('ExternalNetworkInjection.minZ0ToZ1Ratio'),
                   model_uri=CIMTBL.externalNetworkInjection__minZ0ToZ1Ratio, domain=None, range=Optional[float])

slots.externalNetworkInjection__p = Slot(uri=CIM['ExternalNetworkInjection.p'], name="externalNetworkInjection__p", curie=CIM.curie('ExternalNetworkInjection.p'),
                   model_uri=CIMTBL.externalNetworkInjection__p, domain=None, range=Optional[float])

slots.externalNetworkInjection__q = Slot(uri=CIM['ExternalNetworkInjection.q'], name="externalNetworkInjection__q", curie=CIM.curie('ExternalNetworkInjection.q'),
                   model_uri=CIMTBL.externalNetworkInjection__q, domain=None, range=Optional[float])

slots.externalNetworkInjection__referencePriority = Slot(uri=CIM['ExternalNetworkInjection.referencePriority'], name="externalNetworkInjection__referencePriority", curie=CIM.curie('ExternalNetworkInjection.referencePriority'),
                   model_uri=CIMTBL.externalNetworkInjection__referencePriority, domain=None, range=Optional[int])

slots.externalNetworkInjection__voltageFactor = Slot(uri=CIM['ExternalNetworkInjection.voltageFactor'], name="externalNetworkInjection__voltageFactor", curie=CIM.curie('ExternalNetworkInjection.voltageFactor'),
                   model_uri=CIMTBL.externalNetworkInjection__voltageFactor, domain=None, range=Optional[float])

slots.fACTSEquipment__maxC = Slot(uri=CIM['FACTSEquipment.maxC'], name="fACTSEquipment__maxC", curie=CIM.curie('FACTSEquipment.maxC'),
                   model_uri=CIMTBL.fACTSEquipment__maxC, domain=None, range=Optional[float])

slots.fACTSEquipment__maxL = Slot(uri=CIM['FACTSEquipment.maxL'], name="fACTSEquipment__maxL", curie=CIM.curie('FACTSEquipment.maxL'),
                   model_uri=CIMTBL.fACTSEquipment__maxL, domain=None, range=Optional[float])

slots.fACTSEquipment__minC = Slot(uri=CIM['FACTSEquipment.minC'], name="fACTSEquipment__minC", curie=CIM.curie('FACTSEquipment.minC'),
                   model_uri=CIMTBL.fACTSEquipment__minC, domain=None, range=Optional[float])

slots.fACTSEquipment__minL = Slot(uri=CIM['FACTSEquipment.minL'], name="fACTSEquipment__minL", curie=CIM.curie('FACTSEquipment.minL'),
                   model_uri=CIMTBL.fACTSEquipment__minL, domain=None, range=Optional[float])

slots.fACTSEquipment__q = Slot(uri=CIM['FACTSEquipment.q'], name="fACTSEquipment__q", curie=CIM.curie('FACTSEquipment.q'),
                   model_uri=CIMTBL.fACTSEquipment__q, domain=None, range=Optional[float])

slots.fACTSEquipment__ratedC = Slot(uri=CIM['FACTSEquipment.ratedC'], name="fACTSEquipment__ratedC", curie=CIM.curie('FACTSEquipment.ratedC'),
                   model_uri=CIMTBL.fACTSEquipment__ratedC, domain=None, range=Optional[float])

slots.fACTSEquipment__ratedI = Slot(uri=CIM['FACTSEquipment.ratedI'], name="fACTSEquipment__ratedI", curie=CIM.curie('FACTSEquipment.ratedI'),
                   model_uri=CIMTBL.fACTSEquipment__ratedI, domain=None, range=Optional[float])

slots.fACTSEquipment__ratedL = Slot(uri=CIM['FACTSEquipment.ratedL'], name="fACTSEquipment__ratedL", curie=CIM.curie('FACTSEquipment.ratedL'),
                   model_uri=CIMTBL.fACTSEquipment__ratedL, domain=None, range=Optional[float])

slots.fACTSEquipment__ratedU = Slot(uri=CIM['FACTSEquipment.ratedU'], name="fACTSEquipment__ratedU", curie=CIM.curie('FACTSEquipment.ratedU'),
                   model_uri=CIMTBL.fACTSEquipment__ratedU, domain=None, range=Optional[float])

slots.fACTSEquipment__slope = Slot(uri=CIM['FACTSEquipment.slope'], name="fACTSEquipment__slope", curie=CIM.curie('FACTSEquipment.slope'),
                   model_uri=CIMTBL.fACTSEquipment__slope, domain=None, range=Optional[float])

slots.feeder__NormalEnergizingSubstation = Slot(uri=CIM['Feeder.NormalEnergizingSubstation'], name="feeder__NormalEnergizingSubstation", curie=CIM.curie('Feeder.NormalEnergizingSubstation'),
                   model_uri=CIMTBL.feeder__NormalEnergizingSubstation, domain=None, range=Optional[Union[dict, Substation]])

slots.feeder__SubSchedulingArea = Slot(uri=CIM['Feeder.SubSchedulingArea'], name="feeder__SubSchedulingArea", curie=CIM.curie('Feeder.SubSchedulingArea'),
                   model_uri=CIMTBL.feeder__SubSchedulingArea, domain=None, range=Optional[Union[dict, SubSchedulingArea]])

slots.floatQuantity__multiplier = Slot(uri=CIM['FloatQuantity.multiplier'], name="floatQuantity__multiplier", curie=CIM.curie('FloatQuantity.multiplier'),
                   model_uri=CIMTBL.floatQuantity__multiplier, domain=None, range=Optional[Union[str, "UnitMultiplier"]])

slots.floatQuantity__unit = Slot(uri=CIM['FloatQuantity.unit'], name="floatQuantity__unit", curie=CIM.curie('FloatQuantity.unit'),
                   model_uri=CIMTBL.floatQuantity__unit, domain=None, range=Optional[Union[str, "UnitSymbol"]])

slots.floatQuantity__value = Slot(uri=CIM['FloatQuantity.value'], name="floatQuantity__value", curie=CIM.curie('FloatQuantity.value'),
                   model_uri=CIMTBL.floatQuantity__value, domain=None, range=Optional[float])

slots.fossilFuel__fossilFuelType = Slot(uri=CIM['FossilFuel.fossilFuelType'], name="fossilFuel__fossilFuelType", curie=CIM.curie('FossilFuel.fossilFuelType'),
                   model_uri=CIMTBL.fossilFuel__fossilFuelType, domain=None, range=Optional[Union[str, "FuelType"]])

slots.fossilFuel__fuelCost = Slot(uri=CIM['FossilFuel.fuelCost'], name="fossilFuel__fuelCost", curie=CIM.curie('FossilFuel.fuelCost'),
                   model_uri=CIMTBL.fossilFuel__fuelCost, domain=None, range=Optional[float])

slots.fossilFuel__fuelDispatchCost = Slot(uri=CIM['FossilFuel.fuelDispatchCost'], name="fossilFuel__fuelDispatchCost", curie=CIM.curie('FossilFuel.fuelDispatchCost'),
                   model_uri=CIMTBL.fossilFuel__fuelDispatchCost, domain=None, range=Optional[float])

slots.fossilFuel__fuelEffFactor = Slot(uri=CIM['FossilFuel.fuelEffFactor'], name="fossilFuel__fuelEffFactor", curie=CIM.curie('FossilFuel.fuelEffFactor'),
                   model_uri=CIMTBL.fossilFuel__fuelEffFactor, domain=None, range=Optional[float])

slots.fossilFuel__fuelHandlingCost = Slot(uri=CIM['FossilFuel.fuelHandlingCost'], name="fossilFuel__fuelHandlingCost", curie=CIM.curie('FossilFuel.fuelHandlingCost'),
                   model_uri=CIMTBL.fossilFuel__fuelHandlingCost, domain=None, range=Optional[float])

slots.fossilFuel__fuelHeatContent = Slot(uri=CIM['FossilFuel.fuelHeatContent'], name="fossilFuel__fuelHeatContent", curie=CIM.curie('FossilFuel.fuelHeatContent'),
                   model_uri=CIMTBL.fossilFuel__fuelHeatContent, domain=None, range=Optional[float])

slots.fossilFuel__fuelMixture = Slot(uri=CIM['FossilFuel.fuelMixture'], name="fossilFuel__fuelMixture", curie=CIM.curie('FossilFuel.fuelMixture'),
                   model_uri=CIMTBL.fossilFuel__fuelMixture, domain=None, range=Optional[float])

slots.fossilFuel__fuelSulfur = Slot(uri=CIM['FossilFuel.fuelSulfur'], name="fossilFuel__fuelSulfur", curie=CIM.curie('FossilFuel.fuelSulfur'),
                   model_uri=CIMTBL.fossilFuel__fuelSulfur, domain=None, range=Optional[float])

slots.fossilFuel__highBreakpointP = Slot(uri=CIM['FossilFuel.highBreakpointP'], name="fossilFuel__highBreakpointP", curie=CIM.curie('FossilFuel.highBreakpointP'),
                   model_uri=CIMTBL.fossilFuel__highBreakpointP, domain=None, range=Optional[float])

slots.fossilFuel__lowBreakpointP = Slot(uri=CIM['FossilFuel.lowBreakpointP'], name="fossilFuel__lowBreakpointP", curie=CIM.curie('FossilFuel.lowBreakpointP'),
                   model_uri=CIMTBL.fossilFuel__lowBreakpointP, domain=None, range=Optional[float])

slots.fossilFuel__FuelStorage = Slot(uri=CIM['FossilFuel.FuelStorage'], name="fossilFuel__FuelStorage", curie=CIM.curie('FossilFuel.FuelStorage'),
                   model_uri=CIMTBL.fossilFuel__FuelStorage, domain=None, range=Optional[Union[dict, FuelStorage]])

slots.fossilFuel__ThermalGeneratingUnit = Slot(uri=CIM['FossilFuel.ThermalGeneratingUnit'], name="fossilFuel__ThermalGeneratingUnit", curie=CIM.curie('FossilFuel.ThermalGeneratingUnit'),
                   model_uri=CIMTBL.fossilFuel__ThermalGeneratingUnit, domain=None, range=Optional[Union[dict, ThermalGeneratingUnit]])

slots.frequencyConverter__frequency = Slot(uri=CIM['FrequencyConverter.frequency'], name="frequencyConverter__frequency", curie=CIM.curie('FrequencyConverter.frequency'),
                   model_uri=CIMTBL.frequencyConverter__frequency, domain=None, range=Optional[float])

slots.frequencyConverter__maxP = Slot(uri=CIM['FrequencyConverter.maxP'], name="frequencyConverter__maxP", curie=CIM.curie('FrequencyConverter.maxP'),
                   model_uri=CIMTBL.frequencyConverter__maxP, domain=None, range=Optional[float])

slots.frequencyConverter__maxU = Slot(uri=CIM['FrequencyConverter.maxU'], name="frequencyConverter__maxU", curie=CIM.curie('FrequencyConverter.maxU'),
                   model_uri=CIMTBL.frequencyConverter__maxU, domain=None, range=Optional[float])

slots.frequencyConverter__minP = Slot(uri=CIM['FrequencyConverter.minP'], name="frequencyConverter__minP", curie=CIM.curie('FrequencyConverter.minP'),
                   model_uri=CIMTBL.frequencyConverter__minP, domain=None, range=Optional[float])

slots.frequencyConverter__minU = Slot(uri=CIM['FrequencyConverter.minU'], name="frequencyConverter__minU", curie=CIM.curie('FrequencyConverter.minU'),
                   model_uri=CIMTBL.frequencyConverter__minU, domain=None, range=Optional[float])

slots.fuse__MiinimumMeltCurve = Slot(uri=CIM['Fuse.MiinimumMeltCurve'], name="fuse__MiinimumMeltCurve", curie=CIM.curie('Fuse.MiinimumMeltCurve'),
                   model_uri=CIMTBL.fuse__MiinimumMeltCurve, domain=None, range=Optional[Union[dict, FuseCharacteristicCurve]])

slots.fuse__TotalClearingTimeCurve = Slot(uri=CIM['Fuse.TotalClearingTimeCurve'], name="fuse__TotalClearingTimeCurve", curie=CIM.curie('Fuse.TotalClearingTimeCurve'),
                   model_uri=CIMTBL.fuse__TotalClearingTimeCurve, domain=None, range=Optional[Union[dict, FuseCharacteristicCurve]])

slots.generatingUnit__allocSpinResP = Slot(uri=CIM['GeneratingUnit.allocSpinResP'], name="generatingUnit__allocSpinResP", curie=CIM.curie('GeneratingUnit.allocSpinResP'),
                   model_uri=CIMTBL.generatingUnit__allocSpinResP, domain=None, range=Optional[float])

slots.generatingUnit__autoCntrlMarginP = Slot(uri=CIM['GeneratingUnit.autoCntrlMarginP'], name="generatingUnit__autoCntrlMarginP", curie=CIM.curie('GeneratingUnit.autoCntrlMarginP'),
                   model_uri=CIMTBL.generatingUnit__autoCntrlMarginP, domain=None, range=Optional[float])

slots.generatingUnit__baseP = Slot(uri=CIM['GeneratingUnit.baseP'], name="generatingUnit__baseP", curie=CIM.curie('GeneratingUnit.baseP'),
                   model_uri=CIMTBL.generatingUnit__baseP, domain=None, range=Optional[float])

slots.generatingUnit__controlDeadband = Slot(uri=CIM['GeneratingUnit.controlDeadband'], name="generatingUnit__controlDeadband", curie=CIM.curie('GeneratingUnit.controlDeadband'),
                   model_uri=CIMTBL.generatingUnit__controlDeadband, domain=None, range=Optional[float])

slots.generatingUnit__controlPulseHigh = Slot(uri=CIM['GeneratingUnit.controlPulseHigh'], name="generatingUnit__controlPulseHigh", curie=CIM.curie('GeneratingUnit.controlPulseHigh'),
                   model_uri=CIMTBL.generatingUnit__controlPulseHigh, domain=None, range=Optional[float])

slots.generatingUnit__controlPulseLow = Slot(uri=CIM['GeneratingUnit.controlPulseLow'], name="generatingUnit__controlPulseLow", curie=CIM.curie('GeneratingUnit.controlPulseLow'),
                   model_uri=CIMTBL.generatingUnit__controlPulseLow, domain=None, range=Optional[float])

slots.generatingUnit__controlResponseRate = Slot(uri=CIM['GeneratingUnit.controlResponseRate'], name="generatingUnit__controlResponseRate", curie=CIM.curie('GeneratingUnit.controlResponseRate'),
                   model_uri=CIMTBL.generatingUnit__controlResponseRate, domain=None, range=Optional[float])

slots.generatingUnit__efficiency = Slot(uri=CIM['GeneratingUnit.efficiency'], name="generatingUnit__efficiency", curie=CIM.curie('GeneratingUnit.efficiency'),
                   model_uri=CIMTBL.generatingUnit__efficiency, domain=None, range=Optional[float])

slots.generatingUnit__genControlMode = Slot(uri=CIM['GeneratingUnit.genControlMode'], name="generatingUnit__genControlMode", curie=CIM.curie('GeneratingUnit.genControlMode'),
                   model_uri=CIMTBL.generatingUnit__genControlMode, domain=None, range=Optional[Union[str, "GeneratorControlMode"]])

slots.generatingUnit__genControlSource = Slot(uri=CIM['GeneratingUnit.genControlSource'], name="generatingUnit__genControlSource", curie=CIM.curie('GeneratingUnit.genControlSource'),
                   model_uri=CIMTBL.generatingUnit__genControlSource, domain=None, range=Optional[Union[str, "GeneratorControlSource"]])

slots.generatingUnit__governorMPL = Slot(uri=CIM['GeneratingUnit.governorMPL'], name="generatingUnit__governorMPL", curie=CIM.curie('GeneratingUnit.governorMPL'),
                   model_uri=CIMTBL.generatingUnit__governorMPL, domain=None, range=Optional[float])

slots.generatingUnit__governorSCD = Slot(uri=CIM['GeneratingUnit.governorSCD'], name="generatingUnit__governorSCD", curie=CIM.curie('GeneratingUnit.governorSCD'),
                   model_uri=CIMTBL.generatingUnit__governorSCD, domain=None, range=Optional[float])

slots.generatingUnit__highControlLimit = Slot(uri=CIM['GeneratingUnit.highControlLimit'], name="generatingUnit__highControlLimit", curie=CIM.curie('GeneratingUnit.highControlLimit'),
                   model_uri=CIMTBL.generatingUnit__highControlLimit, domain=None, range=Optional[float])

slots.generatingUnit__initialP = Slot(uri=CIM['GeneratingUnit.initialP'], name="generatingUnit__initialP", curie=CIM.curie('GeneratingUnit.initialP'),
                   model_uri=CIMTBL.generatingUnit__initialP, domain=None, range=Optional[float])

slots.generatingUnit__longPF = Slot(uri=CIM['GeneratingUnit.longPF'], name="generatingUnit__longPF", curie=CIM.curie('GeneratingUnit.longPF'),
                   model_uri=CIMTBL.generatingUnit__longPF, domain=None, range=Optional[float])

slots.generatingUnit__lowControlLimit = Slot(uri=CIM['GeneratingUnit.lowControlLimit'], name="generatingUnit__lowControlLimit", curie=CIM.curie('GeneratingUnit.lowControlLimit'),
                   model_uri=CIMTBL.generatingUnit__lowControlLimit, domain=None, range=Optional[float])

slots.generatingUnit__lowerRampRate = Slot(uri=CIM['GeneratingUnit.lowerRampRate'], name="generatingUnit__lowerRampRate", curie=CIM.curie('GeneratingUnit.lowerRampRate'),
                   model_uri=CIMTBL.generatingUnit__lowerRampRate, domain=None, range=Optional[float])

slots.generatingUnit__maxEconomicP = Slot(uri=CIM['GeneratingUnit.maxEconomicP'], name="generatingUnit__maxEconomicP", curie=CIM.curie('GeneratingUnit.maxEconomicP'),
                   model_uri=CIMTBL.generatingUnit__maxEconomicP, domain=None, range=Optional[float])

slots.generatingUnit__maximumAllowableSpinningReserve = Slot(uri=CIM['GeneratingUnit.maximumAllowableSpinningReserve'], name="generatingUnit__maximumAllowableSpinningReserve", curie=CIM.curie('GeneratingUnit.maximumAllowableSpinningReserve'),
                   model_uri=CIMTBL.generatingUnit__maximumAllowableSpinningReserve, domain=None, range=Optional[float])

slots.generatingUnit__maxOperatingP = Slot(uri=CIM['GeneratingUnit.maxOperatingP'], name="generatingUnit__maxOperatingP", curie=CIM.curie('GeneratingUnit.maxOperatingP'),
                   model_uri=CIMTBL.generatingUnit__maxOperatingP, domain=None, range=Optional[float])

slots.generatingUnit__minEconomicP = Slot(uri=CIM['GeneratingUnit.minEconomicP'], name="generatingUnit__minEconomicP", curie=CIM.curie('GeneratingUnit.minEconomicP'),
                   model_uri=CIMTBL.generatingUnit__minEconomicP, domain=None, range=Optional[float])

slots.generatingUnit__minimumOffTime = Slot(uri=CIM['GeneratingUnit.minimumOffTime'], name="generatingUnit__minimumOffTime", curie=CIM.curie('GeneratingUnit.minimumOffTime'),
                   model_uri=CIMTBL.generatingUnit__minimumOffTime, domain=None, range=Optional[float])

slots.generatingUnit__minOperatingP = Slot(uri=CIM['GeneratingUnit.minOperatingP'], name="generatingUnit__minOperatingP", curie=CIM.curie('GeneratingUnit.minOperatingP'),
                   model_uri=CIMTBL.generatingUnit__minOperatingP, domain=None, range=Optional[float])

slots.generatingUnit__modelDetail = Slot(uri=CIM['GeneratingUnit.modelDetail'], name="generatingUnit__modelDetail", curie=CIM.curie('GeneratingUnit.modelDetail'),
                   model_uri=CIMTBL.generatingUnit__modelDetail, domain=None, range=Optional[int])

slots.generatingUnit__nominalP = Slot(uri=CIM['GeneratingUnit.nominalP'], name="generatingUnit__nominalP", curie=CIM.curie('GeneratingUnit.nominalP'),
                   model_uri=CIMTBL.generatingUnit__nominalP, domain=None, range=Optional[float])

slots.generatingUnit__normalPF = Slot(uri=CIM['GeneratingUnit.normalPF'], name="generatingUnit__normalPF", curie=CIM.curie('GeneratingUnit.normalPF'),
                   model_uri=CIMTBL.generatingUnit__normalPF, domain=None, range=Optional[float])

slots.generatingUnit__penaltyFactor = Slot(uri=CIM['GeneratingUnit.penaltyFactor'], name="generatingUnit__penaltyFactor", curie=CIM.curie('GeneratingUnit.penaltyFactor'),
                   model_uri=CIMTBL.generatingUnit__penaltyFactor, domain=None, range=Optional[float])

slots.generatingUnit__raiseRampRate = Slot(uri=CIM['GeneratingUnit.raiseRampRate'], name="generatingUnit__raiseRampRate", curie=CIM.curie('GeneratingUnit.raiseRampRate'),
                   model_uri=CIMTBL.generatingUnit__raiseRampRate, domain=None, range=Optional[float])

slots.generatingUnit__ratedGrossMaxP = Slot(uri=CIM['GeneratingUnit.ratedGrossMaxP'], name="generatingUnit__ratedGrossMaxP", curie=CIM.curie('GeneratingUnit.ratedGrossMaxP'),
                   model_uri=CIMTBL.generatingUnit__ratedGrossMaxP, domain=None, range=Optional[float])

slots.generatingUnit__ratedGrossMinP = Slot(uri=CIM['GeneratingUnit.ratedGrossMinP'], name="generatingUnit__ratedGrossMinP", curie=CIM.curie('GeneratingUnit.ratedGrossMinP'),
                   model_uri=CIMTBL.generatingUnit__ratedGrossMinP, domain=None, range=Optional[float])

slots.generatingUnit__ratedNetMaxP = Slot(uri=CIM['GeneratingUnit.ratedNetMaxP'], name="generatingUnit__ratedNetMaxP", curie=CIM.curie('GeneratingUnit.ratedNetMaxP'),
                   model_uri=CIMTBL.generatingUnit__ratedNetMaxP, domain=None, range=Optional[float])

slots.generatingUnit__shortPF = Slot(uri=CIM['GeneratingUnit.shortPF'], name="generatingUnit__shortPF", curie=CIM.curie('GeneratingUnit.shortPF'),
                   model_uri=CIMTBL.generatingUnit__shortPF, domain=None, range=Optional[float])

slots.generatingUnit__startupCost = Slot(uri=CIM['GeneratingUnit.startupCost'], name="generatingUnit__startupCost", curie=CIM.curie('GeneratingUnit.startupCost'),
                   model_uri=CIMTBL.generatingUnit__startupCost, domain=None, range=Optional[Decimal])

slots.generatingUnit__startupTime = Slot(uri=CIM['GeneratingUnit.startupTime'], name="generatingUnit__startupTime", curie=CIM.curie('GeneratingUnit.startupTime'),
                   model_uri=CIMTBL.generatingUnit__startupTime, domain=None, range=Optional[float])

slots.generatingUnit__tieLinePF = Slot(uri=CIM['GeneratingUnit.tieLinePF'], name="generatingUnit__tieLinePF", curie=CIM.curie('GeneratingUnit.tieLinePF'),
                   model_uri=CIMTBL.generatingUnit__tieLinePF, domain=None, range=Optional[float])

slots.generatingUnit__totalEfficiency = Slot(uri=CIM['GeneratingUnit.totalEfficiency'], name="generatingUnit__totalEfficiency", curie=CIM.curie('GeneratingUnit.totalEfficiency'),
                   model_uri=CIMTBL.generatingUnit__totalEfficiency, domain=None, range=Optional[float])

slots.generatingUnit__variableCost = Slot(uri=CIM['GeneratingUnit.variableCost'], name="generatingUnit__variableCost", curie=CIM.curie('GeneratingUnit.variableCost'),
                   model_uri=CIMTBL.generatingUnit__variableCost, domain=None, range=Optional[Decimal])

slots.gridEdgeDeviceInfo__apparentPowerMaximum = Slot(uri=CIM['GridEdgeDeviceInfo.apparentPowerMaximum'], name="gridEdgeDeviceInfo__apparentPowerMaximum", curie=CIM.curie('GridEdgeDeviceInfo.apparentPowerMaximum'),
                   model_uri=CIMTBL.gridEdgeDeviceInfo__apparentPowerMaximum, domain=None, range=Optional[float])

slots.gridEdgeDeviceInfo__ratedVoltageMax = Slot(uri=CIM['GridEdgeDeviceInfo.ratedVoltageMax'], name="gridEdgeDeviceInfo__ratedVoltageMax", curie=CIM.curie('GridEdgeDeviceInfo.ratedVoltageMax'),
                   model_uri=CIMTBL.gridEdgeDeviceInfo__ratedVoltageMax, domain=None, range=Optional[float])

slots.gridEdgeDeviceInfo__ratedVoltageMin = Slot(uri=CIM['GridEdgeDeviceInfo.ratedVoltageMin'], name="gridEdgeDeviceInfo__ratedVoltageMin", curie=CIM.curie('GridEdgeDeviceInfo.ratedVoltageMin'),
                   model_uri=CIMTBL.gridEdgeDeviceInfo__ratedVoltageMin, domain=None, range=Optional[float])

slots.ground__GroundAction = Slot(uri=CIM['Ground.GroundAction'], name="ground__GroundAction", curie=CIM.curie('Ground.GroundAction'),
                   model_uri=CIMTBL.ground__GroundAction, domain=None, range=Optional[Union[dict, GroundAction]])

slots.groundingImpedance__x = Slot(uri=CIM['GroundingImpedance.x'], name="groundingImpedance__x", curie=CIM.curie('GroundingImpedance.x'),
                   model_uri=CIMTBL.groundingImpedance__x, domain=None, range=Optional[float])

slots.iOPoint__IOPointSource = Slot(uri=CIM['IOPoint.IOPointSource'], name="iOPoint__IOPointSource", curie=CIM.curie('IOPoint.IOPointSource'),
                   model_uri=CIMTBL.iOPoint__IOPointSource, domain=None, range=Optional[Union[dict, IOPointSource]])

slots.identifiedObject__mRID = Slot(uri=CIM['IdentifiedObject.mRID'], name="identifiedObject__mRID", curie=CIM.curie('IdentifiedObject.mRID'),
                   model_uri=CIMTBL.identifiedObject__mRID, domain=None, range=Optional[str])

slots.identifiedObject__aliasName = Slot(uri=CIM['IdentifiedObject.aliasName'], name="identifiedObject__aliasName", curie=CIM.curie('IdentifiedObject.aliasName'),
                   model_uri=CIMTBL.identifiedObject__aliasName, domain=None, range=Optional[str])

slots.identifiedObject__description = Slot(uri=CIM['IdentifiedObject.description'], name="identifiedObject__description", curie=CIM.curie('IdentifiedObject.description'),
                   model_uri=CIMTBL.identifiedObject__description, domain=None, range=Optional[str])

slots.identifiedObject__name = Slot(uri=CIM['IdentifiedObject.name'], name="identifiedObject__name", curie=CIM.curie('IdentifiedObject.name'),
                   model_uri=CIMTBL.identifiedObject__name, domain=None, range=Optional[str])

slots.identifiedObject__InstanceSet = Slot(uri=CIM['IdentifiedObject.InstanceSet'], name="identifiedObject__InstanceSet", curie=CIM.curie('IdentifiedObject.InstanceSet'),
                   model_uri=CIMTBL.identifiedObject__InstanceSet, domain=None, range=Optional[Union[dict, InstanceSet]])

slots.impedanceTapChangerTablePoint__angle = Slot(uri=CIM['ImpedanceTapChangerTablePoint.angle'], name="impedanceTapChangerTablePoint__angle", curie=CIM.curie('ImpedanceTapChangerTablePoint.angle'),
                   model_uri=CIMTBL.impedanceTapChangerTablePoint__angle, domain=None, range=Optional[float])

slots.impedanceTapChangerTablePoint__ratio = Slot(uri=CIM['ImpedanceTapChangerTablePoint.ratio'], name="impedanceTapChangerTablePoint__ratio", curie=CIM.curie('ImpedanceTapChangerTablePoint.ratio'),
                   model_uri=CIMTBL.impedanceTapChangerTablePoint__ratio, domain=None, range=Optional[float])

slots.impedanceTapChangerTablePoint__rEnd1 = Slot(uri=CIM['ImpedanceTapChangerTablePoint.rEnd1'], name="impedanceTapChangerTablePoint__rEnd1", curie=CIM.curie('ImpedanceTapChangerTablePoint.rEnd1'),
                   model_uri=CIMTBL.impedanceTapChangerTablePoint__rEnd1, domain=None, range=Optional[float])

slots.impedanceTapChangerTablePoint__rEnd2 = Slot(uri=CIM['ImpedanceTapChangerTablePoint.rEnd2'], name="impedanceTapChangerTablePoint__rEnd2", curie=CIM.curie('ImpedanceTapChangerTablePoint.rEnd2'),
                   model_uri=CIMTBL.impedanceTapChangerTablePoint__rEnd2, domain=None, range=Optional[float])

slots.impedanceTapChangerTablePoint__rEnd3 = Slot(uri=CIM['ImpedanceTapChangerTablePoint.rEnd3'], name="impedanceTapChangerTablePoint__rEnd3", curie=CIM.curie('ImpedanceTapChangerTablePoint.rEnd3'),
                   model_uri=CIMTBL.impedanceTapChangerTablePoint__rEnd3, domain=None, range=Optional[float])

slots.impedanceTapChangerTablePoint__step = Slot(uri=CIM['ImpedanceTapChangerTablePoint.step'], name="impedanceTapChangerTablePoint__step", curie=CIM.curie('ImpedanceTapChangerTablePoint.step'),
                   model_uri=CIMTBL.impedanceTapChangerTablePoint__step, domain=None, range=Optional[int])

slots.impedanceTapChangerTablePoint__xEnd1 = Slot(uri=CIM['ImpedanceTapChangerTablePoint.xEnd1'], name="impedanceTapChangerTablePoint__xEnd1", curie=CIM.curie('ImpedanceTapChangerTablePoint.xEnd1'),
                   model_uri=CIMTBL.impedanceTapChangerTablePoint__xEnd1, domain=None, range=Optional[float])

slots.impedanceTapChangerTablePoint__xEnd2 = Slot(uri=CIM['ImpedanceTapChangerTablePoint.xEnd2'], name="impedanceTapChangerTablePoint__xEnd2", curie=CIM.curie('ImpedanceTapChangerTablePoint.xEnd2'),
                   model_uri=CIMTBL.impedanceTapChangerTablePoint__xEnd2, domain=None, range=Optional[float])

slots.impedanceTapChangerTablePoint__xEnd3 = Slot(uri=CIM['ImpedanceTapChangerTablePoint.xEnd3'], name="impedanceTapChangerTablePoint__xEnd3", curie=CIM.curie('ImpedanceTapChangerTablePoint.xEnd3'),
                   model_uri=CIMTBL.impedanceTapChangerTablePoint__xEnd3, domain=None, range=Optional[float])

slots.impedanceTapChangerTablePoint__ImpedanceTapChangerTable = Slot(uri=CIM['ImpedanceTapChangerTablePoint.ImpedanceTapChangerTable'], name="impedanceTapChangerTablePoint__ImpedanceTapChangerTable", curie=CIM.curie('ImpedanceTapChangerTablePoint.ImpedanceTapChangerTable'),
                   model_uri=CIMTBL.impedanceTapChangerTablePoint__ImpedanceTapChangerTable, domain=None, range=Optional[Union[dict, ImpedanceTapChangerTable]])

slots.impedanceTapChangerTabular__ImpedanceTapChangerTable = Slot(uri=CIM['ImpedanceTapChangerTabular.ImpedanceTapChangerTable'], name="impedanceTapChangerTabular__ImpedanceTapChangerTable", curie=CIM.curie('ImpedanceTapChangerTabular.ImpedanceTapChangerTable'),
                   model_uri=CIMTBL.impedanceTapChangerTabular__ImpedanceTapChangerTable, domain=None, range=Optional[Union[dict, ImpedanceTapChangerTable]])

slots.individualPnode__ConnectivityNode = Slot(uri=CIM['IndividualPnode.ConnectivityNode'], name="individualPnode__ConnectivityNode", curie=CIM.curie('IndividualPnode.ConnectivityNode'),
                   model_uri=CIMTBL.individualPnode__ConnectivityNode, domain=None, range=Optional[Union[dict, ConnectivityNode]])

slots.insulationInfo__insulated = Slot(uri=CIM['InsulationInfo.insulated'], name="insulationInfo__insulated", curie=CIM.curie('InsulationInfo.insulated'),
                   model_uri=CIMTBL.insulationInfo__insulated, domain=None, range=Optional[Union[bool, Bool]])

slots.insulationInfo__insulationMaterial = Slot(uri=CIM['InsulationInfo.insulationMaterial'], name="insulationInfo__insulationMaterial", curie=CIM.curie('InsulationInfo.insulationMaterial'),
                   model_uri=CIMTBL.insulationInfo__insulationMaterial, domain=None, range=Optional[Union[str, "WireInsulationKind"]])

slots.insulationInfo__insulationThickness = Slot(uri=CIM['InsulationInfo.insulationThickness'], name="insulationInfo__insulationThickness", curie=CIM.curie('InsulationInfo.insulationThickness'),
                   model_uri=CIMTBL.insulationInfo__insulationThickness, domain=None, range=Optional[float])

slots.insulationInfo__CableInfo = Slot(uri=CIM['InsulationInfo.CableInfo'], name="insulationInfo__CableInfo", curie=CIM.curie('InsulationInfo.CableInfo'),
                   model_uri=CIMTBL.insulationInfo__CableInfo, domain=None, range=Optional[Union[dict, CableInfo]])

slots.integerQuantity__multiplier = Slot(uri=CIM['IntegerQuantity.multiplier'], name="integerQuantity__multiplier", curie=CIM.curie('IntegerQuantity.multiplier'),
                   model_uri=CIMTBL.integerQuantity__multiplier, domain=None, range=Optional[Union[str, "UnitMultiplier"]])

slots.integerQuantity__unit = Slot(uri=CIM['IntegerQuantity.unit'], name="integerQuantity__unit", curie=CIM.curie('IntegerQuantity.unit'),
                   model_uri=CIMTBL.integerQuantity__unit, domain=None, range=Optional[Union[str, "UnitSymbol"]])

slots.integerQuantity__value = Slot(uri=CIM['IntegerQuantity.value'], name="integerQuantity__value", curie=CIM.curie('IntegerQuantity.value'),
                   model_uri=CIMTBL.integerQuantity__value, domain=None, range=Optional[int])

slots.inverterCapabilities__isModeCapableActivePowerReactivePower = Slot(uri=CIM['InverterCapabilities.isModeCapableActivePowerReactivePower'], name="inverterCapabilities__isModeCapableActivePowerReactivePower", curie=CIM.curie('InverterCapabilities.isModeCapableActivePowerReactivePower'),
                   model_uri=CIMTBL.inverterCapabilities__isModeCapableActivePowerReactivePower, domain=None, range=Optional[Union[bool, Bool]])

slots.inverterCapabilities__isModeCapableConstantPowerFactor = Slot(uri=CIM['InverterCapabilities.isModeCapableConstantPowerFactor'], name="inverterCapabilities__isModeCapableConstantPowerFactor", curie=CIM.curie('InverterCapabilities.isModeCapableConstantPowerFactor'),
                   model_uri=CIMTBL.inverterCapabilities__isModeCapableConstantPowerFactor, domain=None, range=Optional[Union[bool, Bool]])

slots.inverterCapabilities__isModeCapableConstantReactivePower = Slot(uri=CIM['InverterCapabilities.isModeCapableConstantReactivePower'], name="inverterCapabilities__isModeCapableConstantReactivePower", curie=CIM.curie('InverterCapabilities.isModeCapableConstantReactivePower'),
                   model_uri=CIMTBL.inverterCapabilities__isModeCapableConstantReactivePower, domain=None, range=Optional[Union[bool, Bool]])

slots.inverterCapabilities__isModeCapableFrequencyActivePower = Slot(uri=CIM['InverterCapabilities.isModeCapableFrequencyActivePower'], name="inverterCapabilities__isModeCapableFrequencyActivePower", curie=CIM.curie('InverterCapabilities.isModeCapableFrequencyActivePower'),
                   model_uri=CIMTBL.inverterCapabilities__isModeCapableFrequencyActivePower, domain=None, range=Optional[Union[bool, Bool]])

slots.inverterCapabilities__isModeCapableVoltageActivePower = Slot(uri=CIM['InverterCapabilities.isModeCapableVoltageActivePower'], name="inverterCapabilities__isModeCapableVoltageActivePower", curie=CIM.curie('InverterCapabilities.isModeCapableVoltageActivePower'),
                   model_uri=CIMTBL.inverterCapabilities__isModeCapableVoltageActivePower, domain=None, range=Optional[Union[bool, Bool]])

slots.inverterCapabilities__isModeCapableVoltageReactivePower = Slot(uri=CIM['InverterCapabilities.isModeCapableVoltageReactivePower'], name="inverterCapabilities__isModeCapableVoltageReactivePower", curie=CIM.curie('InverterCapabilities.isModeCapableVoltageReactivePower'),
                   model_uri=CIMTBL.inverterCapabilities__isModeCapableVoltageReactivePower, domain=None, range=Optional[Union[bool, Bool]])

slots.inverterCapabilities__isProtectionCapableEnterServiceAfterTrip = Slot(uri=CIM['InverterCapabilities.isProtectionCapableEnterServiceAfterTrip'], name="inverterCapabilities__isProtectionCapableEnterServiceAfterTrip", curie=CIM.curie('InverterCapabilities.isProtectionCapableEnterServiceAfterTrip'),
                   model_uri=CIMTBL.inverterCapabilities__isProtectionCapableEnterServiceAfterTrip, domain=None, range=Optional[Union[bool, Bool]])

slots.inverterCapabilities__isProtectionCapableFrequencyTrip = Slot(uri=CIM['InverterCapabilities.isProtectionCapableFrequencyTrip'], name="inverterCapabilities__isProtectionCapableFrequencyTrip", curie=CIM.curie('InverterCapabilities.isProtectionCapableFrequencyTrip'),
                   model_uri=CIMTBL.inverterCapabilities__isProtectionCapableFrequencyTrip, domain=None, range=Optional[Union[bool, Bool]])

slots.inverterCapabilities__isProtectionCapableLimitActivePower = Slot(uri=CIM['InverterCapabilities.isProtectionCapableLimitActivePower'], name="inverterCapabilities__isProtectionCapableLimitActivePower", curie=CIM.curie('InverterCapabilities.isProtectionCapableLimitActivePower'),
                   model_uri=CIMTBL.inverterCapabilities__isProtectionCapableLimitActivePower, domain=None, range=Optional[Union[bool, Bool]])

slots.inverterCapabilities__isProtectionCapableMomentaryCessation = Slot(uri=CIM['InverterCapabilities.isProtectionCapableMomentaryCessation'], name="inverterCapabilities__isProtectionCapableMomentaryCessation", curie=CIM.curie('InverterCapabilities.isProtectionCapableMomentaryCessation'),
                   model_uri=CIMTBL.inverterCapabilities__isProtectionCapableMomentaryCessation, domain=None, range=Optional[Union[bool, Bool]])

slots.inverterCapabilities__isProtectionCapableVoltageTrip = Slot(uri=CIM['InverterCapabilities.isProtectionCapableVoltageTrip'], name="inverterCapabilities__isProtectionCapableVoltageTrip", curie=CIM.curie('InverterCapabilities.isProtectionCapableVoltageTrip'),
                   model_uri=CIMTBL.inverterCapabilities__isProtectionCapableVoltageTrip, domain=None, range=Optional[Union[bool, Bool]])

slots.inverterInfo__activePowerRatingOverExcited = Slot(uri=CIM['InverterInfo.activePowerRatingOverExcited'], name="inverterInfo__activePowerRatingOverExcited", curie=CIM.curie('InverterInfo.activePowerRatingOverExcited'),
                   model_uri=CIMTBL.inverterInfo__activePowerRatingOverExcited, domain=None, range=Optional[float])

slots.inverterInfo__activePowerRatingUnderExcited = Slot(uri=CIM['InverterInfo.activePowerRatingUnderExcited'], name="inverterInfo__activePowerRatingUnderExcited", curie=CIM.curie('InverterInfo.activePowerRatingUnderExcited'),
                   model_uri=CIMTBL.inverterInfo__activePowerRatingUnderExcited, domain=None, range=Optional[float])

slots.inverterInfo__activePowerRatingUnityPowerFactor = Slot(uri=CIM['InverterInfo.activePowerRatingUnityPowerFactor'], name="inverterInfo__activePowerRatingUnityPowerFactor", curie=CIM.curie('InverterInfo.activePowerRatingUnityPowerFactor'),
                   model_uri=CIMTBL.inverterInfo__activePowerRatingUnityPowerFactor, domain=None, range=Optional[float])

slots.inverterInfo__powerFactorOverExcited = Slot(uri=CIM['InverterInfo.powerFactorOverExcited'], name="inverterInfo__powerFactorOverExcited", curie=CIM.curie('InverterInfo.powerFactorOverExcited'),
                   model_uri=CIMTBL.inverterInfo__powerFactorOverExcited, domain=None, range=Optional[float])

slots.inverterInfo__powerFactorUnderExcited = Slot(uri=CIM['InverterInfo.powerFactorUnderExcited'], name="inverterInfo__powerFactorUnderExcited", curie=CIM.curie('InverterInfo.powerFactorUnderExcited'),
                   model_uri=CIMTBL.inverterInfo__powerFactorUnderExcited, domain=None, range=Optional[float])

slots.inverterInfo__reactivePowerAbsorbedMax = Slot(uri=CIM['InverterInfo.reactivePowerAbsorbedMax'], name="inverterInfo__reactivePowerAbsorbedMax", curie=CIM.curie('InverterInfo.reactivePowerAbsorbedMax'),
                   model_uri=CIMTBL.inverterInfo__reactivePowerAbsorbedMax, domain=None, range=Optional[float])

slots.inverterInfo__reactivePowerInjectedMax = Slot(uri=CIM['InverterInfo.reactivePowerInjectedMax'], name="inverterInfo__reactivePowerInjectedMax", curie=CIM.curie('InverterInfo.reactivePowerInjectedMax'),
                   model_uri=CIMTBL.inverterInfo__reactivePowerInjectedMax, domain=None, range=Optional[float])

slots.inverterInfo__susceptanceOffline = Slot(uri=CIM['InverterInfo.susceptanceOffline'], name="inverterInfo__susceptanceOffline", curie=CIM.curie('InverterInfo.susceptanceOffline'),
                   model_uri=CIMTBL.inverterInfo__susceptanceOffline, domain=None, range=Optional[float])

slots.inverterInfo__InverterCapabilites = Slot(uri=CIM['InverterInfo.InverterCapabilites'], name="inverterInfo__InverterCapabilites", curie=CIM.curie('InverterInfo.InverterCapabilites'),
                   model_uri=CIMTBL.inverterInfo__InverterCapabilites, domain=None, range=Optional[Union[dict, InverterCapabilities]])

slots.irregularTimePoint__time = Slot(uri=CIM['IrregularTimePoint.time'], name="irregularTimePoint__time", curie=CIM.curie('IrregularTimePoint.time'),
                   model_uri=CIMTBL.irregularTimePoint__time, domain=None, range=Optional[float])

slots.irregularTimePoint__value1 = Slot(uri=CIM['IrregularTimePoint.value1'], name="irregularTimePoint__value1", curie=CIM.curie('IrregularTimePoint.value1'),
                   model_uri=CIMTBL.irregularTimePoint__value1, domain=None, range=Optional[float])

slots.irregularTimePoint__value2 = Slot(uri=CIM['IrregularTimePoint.value2'], name="irregularTimePoint__value2", curie=CIM.curie('IrregularTimePoint.value2'),
                   model_uri=CIMTBL.irregularTimePoint__value2, domain=None, range=Optional[float])

slots.irregularTimePoint__value3 = Slot(uri=CIM['IrregularTimePoint.value3'], name="irregularTimePoint__value3", curie=CIM.curie('IrregularTimePoint.value3'),
                   model_uri=CIMTBL.irregularTimePoint__value3, domain=None, range=Optional[float])

slots.irregularTimePoint__IntervalSchedule = Slot(uri=CIM['IrregularTimePoint.IntervalSchedule'], name="irregularTimePoint__IntervalSchedule", curie=CIM.curie('IrregularTimePoint.IntervalSchedule'),
                   model_uri=CIMTBL.irregularTimePoint__IntervalSchedule, domain=None, range=Optional[Union[dict, IrregularIntervalSchedule]])

slots.jumper__JumperAction = Slot(uri=CIM['Jumper.JumperAction'], name="jumper__JumperAction", curie=CIM.curie('Jumper.JumperAction'),
                   model_uri=CIMTBL.jumper__JumperAction, domain=None, range=Optional[Union[dict, JumperAction]])

slots.line__ACTieCorridor = Slot(uri=CIM['Line.ACTieCorridor'], name="line__ACTieCorridor", curie=CIM.curie('Line.ACTieCorridor'),
                   model_uri=CIMTBL.line__ACTieCorridor, domain=None, range=Optional[Union[dict, ACTieCorridor]])

slots.line__Region = Slot(uri=CIM['Line.Region'], name="line__Region", curie=CIM.curie('Line.Region'),
                   model_uri=CIMTBL.line__Region, domain=None, range=Optional[Union[dict, SubGeographicalRegion]])

slots.line__SchedulingArea = Slot(uri=CIM['Line.SchedulingArea'], name="line__SchedulingArea", curie=CIM.curie('Line.SchedulingArea'),
                   model_uri=CIMTBL.line__SchedulingArea, domain=None, range=Optional[Union[dict, SchedulingArea]])

slots.lineSegmentCoupling__coupledLineNumber = Slot(uri=CIM['LineSegmentCoupling.coupledLineNumber'], name="lineSegmentCoupling__coupledLineNumber", curie=CIM.curie('LineSegmentCoupling.coupledLineNumber'),
                   model_uri=CIMTBL.lineSegmentCoupling__coupledLineNumber, domain=None, range=Optional[int])

slots.lineSegmentCoupling__reverseFlow = Slot(uri=CIM['LineSegmentCoupling.reverseFlow'], name="lineSegmentCoupling__reverseFlow", curie=CIM.curie('LineSegmentCoupling.reverseFlow'),
                   model_uri=CIMTBL.lineSegmentCoupling__reverseFlow, domain=None, range=Optional[Union[bool, Bool]])

slots.lineSegmentCoupling__xOffset = Slot(uri=CIM['LineSegmentCoupling.xOffset'], name="lineSegmentCoupling__xOffset", curie=CIM.curie('LineSegmentCoupling.xOffset'),
                   model_uri=CIMTBL.lineSegmentCoupling__xOffset, domain=None, range=Optional[float])

slots.lineSegmentCoupling__ACLineSegment = Slot(uri=CIM['LineSegmentCoupling.ACLineSegment'], name="lineSegmentCoupling__ACLineSegment", curie=CIM.curie('LineSegmentCoupling.ACLineSegment'),
                   model_uri=CIMTBL.lineSegmentCoupling__ACLineSegment, domain=None, range=Optional[Union[dict, ACLineSegment]])

slots.lineSegmentCoupling__CoupledLineSegmentGroup = Slot(uri=CIM['LineSegmentCoupling.CoupledLineSegmentGroup'], name="lineSegmentCoupling__CoupledLineSegmentGroup", curie=CIM.curie('LineSegmentCoupling.CoupledLineSegmentGroup'),
                   model_uri=CIMTBL.lineSegmentCoupling__CoupledLineSegmentGroup, domain=None, range=Optional[Union[dict, CoupledLineSegmentGroup]])

slots.linearShuntCompensator__b0PerSection = Slot(uri=CIM['LinearShuntCompensator.b0PerSection'], name="linearShuntCompensator__b0PerSection", curie=CIM.curie('LinearShuntCompensator.b0PerSection'),
                   model_uri=CIMTBL.linearShuntCompensator__b0PerSection, domain=None, range=Optional[float])

slots.linearShuntCompensator__bPerSection = Slot(uri=CIM['LinearShuntCompensator.bPerSection'], name="linearShuntCompensator__bPerSection", curie=CIM.curie('LinearShuntCompensator.bPerSection'),
                   model_uri=CIMTBL.linearShuntCompensator__bPerSection, domain=None, range=Optional[float])

slots.linearShuntCompensator__g0PerSection = Slot(uri=CIM['LinearShuntCompensator.g0PerSection'], name="linearShuntCompensator__g0PerSection", curie=CIM.curie('LinearShuntCompensator.g0PerSection'),
                   model_uri=CIMTBL.linearShuntCompensator__g0PerSection, domain=None, range=Optional[float])

slots.linearShuntCompensator__gPerSection = Slot(uri=CIM['LinearShuntCompensator.gPerSection'], name="linearShuntCompensator__gPerSection", curie=CIM.curie('LinearShuntCompensator.gPerSection'),
                   model_uri=CIMTBL.linearShuntCompensator__gPerSection, domain=None, range=Optional[float])

slots.linearShuntCompensator__rPerSection = Slot(uri=CIM['LinearShuntCompensator.rPerSection'], name="linearShuntCompensator__rPerSection", curie=CIM.curie('LinearShuntCompensator.rPerSection'),
                   model_uri=CIMTBL.linearShuntCompensator__rPerSection, domain=None, range=Optional[float])

slots.linearShuntCompensator__xPerSection = Slot(uri=CIM['LinearShuntCompensator.xPerSection'], name="linearShuntCompensator__xPerSection", curie=CIM.curie('LinearShuntCompensator.xPerSection'),
                   model_uri=CIMTBL.linearShuntCompensator__xPerSection, domain=None, range=Optional[float])

slots.linearShuntCompensatorPhase__bPerSection = Slot(uri=CIM['LinearShuntCompensatorPhase.bPerSection'], name="linearShuntCompensatorPhase__bPerSection", curie=CIM.curie('LinearShuntCompensatorPhase.bPerSection'),
                   model_uri=CIMTBL.linearShuntCompensatorPhase__bPerSection, domain=None, range=Optional[float])

slots.linearShuntCompensatorPhase__gPerSection = Slot(uri=CIM['LinearShuntCompensatorPhase.gPerSection'], name="linearShuntCompensatorPhase__gPerSection", curie=CIM.curie('LinearShuntCompensatorPhase.gPerSection'),
                   model_uri=CIMTBL.linearShuntCompensatorPhase__gPerSection, domain=None, range=Optional[float])

slots.linearShuntCompensatorPhase__rPerSection = Slot(uri=CIM['LinearShuntCompensatorPhase.rPerSection'], name="linearShuntCompensatorPhase__rPerSection", curie=CIM.curie('LinearShuntCompensatorPhase.rPerSection'),
                   model_uri=CIMTBL.linearShuntCompensatorPhase__rPerSection, domain=None, range=Optional[float])

slots.linearShuntCompensatorPhase__strayInductancePerSection = Slot(uri=CIM['LinearShuntCompensatorPhase.strayInductancePerSection'], name="linearShuntCompensatorPhase__strayInductancePerSection", curie=CIM.curie('LinearShuntCompensatorPhase.strayInductancePerSection'),
                   model_uri=CIMTBL.linearShuntCompensatorPhase__strayInductancePerSection, domain=None, range=Optional[float])

slots.linearShuntCompensatorPhase__xPerSection = Slot(uri=CIM['LinearShuntCompensatorPhase.xPerSection'], name="linearShuntCompensatorPhase__xPerSection", curie=CIM.curie('LinearShuntCompensatorPhase.xPerSection'),
                   model_uri=CIMTBL.linearShuntCompensatorPhase__xPerSection, domain=None, range=Optional[float])

slots.loadArea__peakLoad = Slot(uri=CIM['LoadArea.peakLoad'], name="loadArea__peakLoad", curie=CIM.curie('LoadArea.peakLoad'),
                   model_uri=CIMTBL.loadArea__peakLoad, domain=None, range=Optional[float])

slots.loadGroup__SubLoadArea = Slot(uri=CIM['LoadGroup.SubLoadArea'], name="loadGroup__SubLoadArea", curie=CIM.curie('LoadGroup.SubLoadArea'),
                   model_uri=CIMTBL.loadGroup__SubLoadArea, domain=None, range=Optional[Union[dict, SubLoadArea]])

slots.loadResponseCharacteristic__exponentModel = Slot(uri=CIM['LoadResponseCharacteristic.exponentModel'], name="loadResponseCharacteristic__exponentModel", curie=CIM.curie('LoadResponseCharacteristic.exponentModel'),
                   model_uri=CIMTBL.loadResponseCharacteristic__exponentModel, domain=None, range=Optional[Union[bool, Bool]])

slots.loadResponseCharacteristic__pConstantCurrent = Slot(uri=CIM['LoadResponseCharacteristic.pConstantCurrent'], name="loadResponseCharacteristic__pConstantCurrent", curie=CIM.curie('LoadResponseCharacteristic.pConstantCurrent'),
                   model_uri=CIMTBL.loadResponseCharacteristic__pConstantCurrent, domain=None, range=Optional[float])

slots.loadResponseCharacteristic__pConstantImpedance = Slot(uri=CIM['LoadResponseCharacteristic.pConstantImpedance'], name="loadResponseCharacteristic__pConstantImpedance", curie=CIM.curie('LoadResponseCharacteristic.pConstantImpedance'),
                   model_uri=CIMTBL.loadResponseCharacteristic__pConstantImpedance, domain=None, range=Optional[float])

slots.loadResponseCharacteristic__pConstantPower = Slot(uri=CIM['LoadResponseCharacteristic.pConstantPower'], name="loadResponseCharacteristic__pConstantPower", curie=CIM.curie('LoadResponseCharacteristic.pConstantPower'),
                   model_uri=CIMTBL.loadResponseCharacteristic__pConstantPower, domain=None, range=Optional[float])

slots.loadResponseCharacteristic__pFrequencyExponent = Slot(uri=CIM['LoadResponseCharacteristic.pFrequencyExponent'], name="loadResponseCharacteristic__pFrequencyExponent", curie=CIM.curie('LoadResponseCharacteristic.pFrequencyExponent'),
                   model_uri=CIMTBL.loadResponseCharacteristic__pFrequencyExponent, domain=None, range=Optional[float])

slots.loadResponseCharacteristic__pVoltageExponent = Slot(uri=CIM['LoadResponseCharacteristic.pVoltageExponent'], name="loadResponseCharacteristic__pVoltageExponent", curie=CIM.curie('LoadResponseCharacteristic.pVoltageExponent'),
                   model_uri=CIMTBL.loadResponseCharacteristic__pVoltageExponent, domain=None, range=Optional[float])

slots.loadResponseCharacteristic__qConstantCurrent = Slot(uri=CIM['LoadResponseCharacteristic.qConstantCurrent'], name="loadResponseCharacteristic__qConstantCurrent", curie=CIM.curie('LoadResponseCharacteristic.qConstantCurrent'),
                   model_uri=CIMTBL.loadResponseCharacteristic__qConstantCurrent, domain=None, range=Optional[float])

slots.loadResponseCharacteristic__qConstantImpedance = Slot(uri=CIM['LoadResponseCharacteristic.qConstantImpedance'], name="loadResponseCharacteristic__qConstantImpedance", curie=CIM.curie('LoadResponseCharacteristic.qConstantImpedance'),
                   model_uri=CIMTBL.loadResponseCharacteristic__qConstantImpedance, domain=None, range=Optional[float])

slots.loadResponseCharacteristic__qConstantPower = Slot(uri=CIM['LoadResponseCharacteristic.qConstantPower'], name="loadResponseCharacteristic__qConstantPower", curie=CIM.curie('LoadResponseCharacteristic.qConstantPower'),
                   model_uri=CIMTBL.loadResponseCharacteristic__qConstantPower, domain=None, range=Optional[float])

slots.loadResponseCharacteristic__qFrequencyExponent = Slot(uri=CIM['LoadResponseCharacteristic.qFrequencyExponent'], name="loadResponseCharacteristic__qFrequencyExponent", curie=CIM.curie('LoadResponseCharacteristic.qFrequencyExponent'),
                   model_uri=CIMTBL.loadResponseCharacteristic__qFrequencyExponent, domain=None, range=Optional[float])

slots.loadResponseCharacteristic__qVoltageExponent = Slot(uri=CIM['LoadResponseCharacteristic.qVoltageExponent'], name="loadResponseCharacteristic__qVoltageExponent", curie=CIM.curie('LoadResponseCharacteristic.qVoltageExponent'),
                   model_uri=CIMTBL.loadResponseCharacteristic__qVoltageExponent, domain=None, range=Optional[float])

slots.lossCurve__FACTSEquipment = Slot(uri=CIM['LossCurve.FACTSEquipment'], name="lossCurve__FACTSEquipment", curie=CIM.curie('LossCurve.FACTSEquipment'),
                   model_uri=CIMTBL.lossCurve__FACTSEquipment, domain=None, range=Optional[Union[dict, FACTSEquipment]])

slots.measurement__measurementType = Slot(uri=CIM['Measurement.measurementType'], name="measurement__measurementType", curie=CIM.curie('Measurement.measurementType'),
                   model_uri=CIMTBL.measurement__measurementType, domain=None, range=Optional[str])

slots.measurement__phases = Slot(uri=CIM['Measurement.phases'], name="measurement__phases", curie=CIM.curie('Measurement.phases'),
                   model_uri=CIMTBL.measurement__phases, domain=None, range=Optional[Union[str, "PhaseCode"]])

slots.measurement__sourceType = Slot(uri=CIM['Measurement.sourceType'], name="measurement__sourceType", curie=CIM.curie('Measurement.sourceType'),
                   model_uri=CIMTBL.measurement__sourceType, domain=None, range=Optional[Union[str, "MeasurementSourceKind"]])

slots.measurement__unitMultiplier = Slot(uri=CIM['Measurement.unitMultiplier'], name="measurement__unitMultiplier", curie=CIM.curie('Measurement.unitMultiplier'),
                   model_uri=CIMTBL.measurement__unitMultiplier, domain=None, range=Optional[Union[str, "UnitMultiplier"]])

slots.measurement__unitSymbol = Slot(uri=CIM['Measurement.unitSymbol'], name="measurement__unitSymbol", curie=CIM.curie('Measurement.unitSymbol'),
                   model_uri=CIMTBL.measurement__unitSymbol, domain=None, range=Optional[Union[str, "UnitSymbol"]])

slots.measurement__Asset = Slot(uri=CIM['Measurement.Asset'], name="measurement__Asset", curie=CIM.curie('Measurement.Asset'),
                   model_uri=CIMTBL.measurement__Asset, domain=None, range=Optional[Union[dict, Asset]])

slots.measurement__CalculationMethodHierarchy = Slot(uri=CIM['Measurement.CalculationMethodHierarchy'], name="measurement__CalculationMethodHierarchy", curie=CIM.curie('Measurement.CalculationMethodHierarchy'),
                   model_uri=CIMTBL.measurement__CalculationMethodHierarchy, domain=None, range=Optional[Union[dict, CalculationMethodHierarchy]])

slots.measurement__MeasurementAction = Slot(uri=CIM['Measurement.MeasurementAction'], name="measurement__MeasurementAction", curie=CIM.curie('Measurement.MeasurementAction'),
                   model_uri=CIMTBL.measurement__MeasurementAction, domain=None, range=Optional[Union[dict, MeasurementAction]])

slots.measurement__MeasurementSystem = Slot(uri=CIM['Measurement.MeasurementSystem'], name="measurement__MeasurementSystem", curie=CIM.curie('Measurement.MeasurementSystem'),
                   model_uri=CIMTBL.measurement__MeasurementSystem, domain=None, range=Optional[Union[dict, MeasurementSystem]])

slots.measurement__PowerSystemResource = Slot(uri=CIM['Measurement.PowerSystemResource'], name="measurement__PowerSystemResource", curie=CIM.curie('Measurement.PowerSystemResource'),
                   model_uri=CIMTBL.measurement__PowerSystemResource, domain=None, range=Optional[Union[dict, PowerSystemResource]])

slots.measurement__Terminal = Slot(uri=CIM['Measurement.Terminal'], name="measurement__Terminal", curie=CIM.curie('Measurement.Terminal'),
                   model_uri=CIMTBL.measurement__Terminal, domain=None, range=Optional[Union[dict, ACDCTerminal]])

slots.measurementSystem__reportingRate = Slot(uri=CIM['MeasurementSystem.reportingRate'], name="measurementSystem__reportingRate", curie=CIM.curie('MeasurementSystem.reportingRate'),
                   model_uri=CIMTBL.measurementSystem__reportingRate, domain=None, range=Optional[float])

slots.measurementSystem__CommunicationLink = Slot(uri=CIM['MeasurementSystem.CommunicationLink'], name="measurementSystem__CommunicationLink", curie=CIM.curie('MeasurementSystem.CommunicationLink'),
                   model_uri=CIMTBL.measurementSystem__CommunicationLink, domain=None, range=Optional[Union[dict, CommunicationLink]])

slots.measurementValue__sensorAccuracy = Slot(uri=CIM['MeasurementValue.sensorAccuracy'], name="measurementValue__sensorAccuracy", curie=CIM.curie('MeasurementValue.sensorAccuracy'),
                   model_uri=CIMTBL.measurementValue__sensorAccuracy, domain=None, range=Optional[float])

slots.measurementValue__timeStamp = Slot(uri=CIM['MeasurementValue.timeStamp'], name="measurementValue__timeStamp", curie=CIM.curie('MeasurementValue.timeStamp'),
                   model_uri=CIMTBL.measurementValue__timeStamp, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.measurementValue__CalculationMethodHierarchy = Slot(uri=CIM['MeasurementValue.CalculationMethodHierarchy'], name="measurementValue__CalculationMethodHierarchy", curie=CIM.curie('MeasurementValue.CalculationMethodHierarchy'),
                   model_uri=CIMTBL.measurementValue__CalculationMethodHierarchy, domain=None, range=Optional[Union[dict, CalculationMethodHierarchy]])

slots.measurementValue__ErpPerson = Slot(uri=CIM['MeasurementValue.ErpPerson'], name="measurementValue__ErpPerson", curie=CIM.curie('MeasurementValue.ErpPerson'),
                   model_uri=CIMTBL.measurementValue__ErpPerson, domain=None, range=Optional[Union[dict, OldPerson]])

slots.measurementValue__MeasurementValueQuality = Slot(uri=CIM['MeasurementValue.MeasurementValueQuality'], name="measurementValue__MeasurementValueQuality", curie=CIM.curie('MeasurementValue.MeasurementValueQuality'),
                   model_uri=CIMTBL.measurementValue__MeasurementValueQuality, domain=None, range=Optional[Union[dict, MeasurementValueQuality]])

slots.measurementValue__MeasurementValueSource = Slot(uri=CIM['MeasurementValue.MeasurementValueSource'], name="measurementValue__MeasurementValueSource", curie=CIM.curie('MeasurementValue.MeasurementValueSource'),
                   model_uri=CIMTBL.measurementValue__MeasurementValueSource, domain=None, range=Optional[Union[dict, MeasurementValueSource]])

slots.measurementValue__RemoteSource = Slot(uri=CIM['MeasurementValue.RemoteSource'], name="measurementValue__RemoteSource", curie=CIM.curie('MeasurementValue.RemoteSource'),
                   model_uri=CIMTBL.measurementValue__RemoteSource, domain=None, range=Optional[Union[dict, RemoteSource]])

slots.measurementValueQuality__MeasurementValue = Slot(uri=CIM['MeasurementValueQuality.MeasurementValue'], name="measurementValueQuality__MeasurementValue", curie=CIM.curie('MeasurementValueQuality.MeasurementValue'),
                   model_uri=CIMTBL.measurementValueQuality__MeasurementValue, domain=None, range=Optional[Union[dict, MeasurementValue]])

slots.measurementVector__angle = Slot(uri=CIM['MeasurementVector.angle'], name="measurementVector__angle", curie=CIM.curie('MeasurementVector.angle'),
                   model_uri=CIMTBL.measurementVector__angle, domain=None, range=Optional[float])

slots.measurementVector__magnitude = Slot(uri=CIM['MeasurementVector.magnitude'], name="measurementVector__magnitude", curie=CIM.curie('MeasurementVector.magnitude'),
                   model_uri=CIMTBL.measurementVector__magnitude, domain=None, range=Optional[float])

slots.mobileElectricalUnit__ChargingUnit = Slot(uri=CIM['MobileElectricalUnit.ChargingUnit'], name="mobileElectricalUnit__ChargingUnit", curie=CIM.curie('MobileElectricalUnit.ChargingUnit'),
                   model_uri=CIMTBL.mobileElectricalUnit__ChargingUnit, domain=None, range=Optional[Union[dict, ChargingUnit]])

slots.monthDayInterval__end = Slot(uri=CIM['MonthDayInterval.end'], name="monthDayInterval__end", curie=CIM.curie('MonthDayInterval.end'),
                   model_uri=CIMTBL.monthDayInterval__end, domain=None, range=Optional[str])

slots.monthDayInterval__start = Slot(uri=CIM['MonthDayInterval.start'], name="monthDayInterval__start", curie=CIM.curie('MonthDayInterval.start'),
                   model_uri=CIMTBL.monthDayInterval__start, domain=None, range=Optional[str])

slots.mutualCoupling__b0ch = Slot(uri=CIM['MutualCoupling.b0ch'], name="mutualCoupling__b0ch", curie=CIM.curie('MutualCoupling.b0ch'),
                   model_uri=CIMTBL.mutualCoupling__b0ch, domain=None, range=Optional[float])

slots.mutualCoupling__distance11 = Slot(uri=CIM['MutualCoupling.distance11'], name="mutualCoupling__distance11", curie=CIM.curie('MutualCoupling.distance11'),
                   model_uri=CIMTBL.mutualCoupling__distance11, domain=None, range=Optional[float])

slots.mutualCoupling__distance12 = Slot(uri=CIM['MutualCoupling.distance12'], name="mutualCoupling__distance12", curie=CIM.curie('MutualCoupling.distance12'),
                   model_uri=CIMTBL.mutualCoupling__distance12, domain=None, range=Optional[float])

slots.mutualCoupling__distance21 = Slot(uri=CIM['MutualCoupling.distance21'], name="mutualCoupling__distance21", curie=CIM.curie('MutualCoupling.distance21'),
                   model_uri=CIMTBL.mutualCoupling__distance21, domain=None, range=Optional[float])

slots.mutualCoupling__distance22 = Slot(uri=CIM['MutualCoupling.distance22'], name="mutualCoupling__distance22", curie=CIM.curie('MutualCoupling.distance22'),
                   model_uri=CIMTBL.mutualCoupling__distance22, domain=None, range=Optional[float])

slots.mutualCoupling__g0ch = Slot(uri=CIM['MutualCoupling.g0ch'], name="mutualCoupling__g0ch", curie=CIM.curie('MutualCoupling.g0ch'),
                   model_uri=CIMTBL.mutualCoupling__g0ch, domain=None, range=Optional[float])

slots.mutualCoupling__r0 = Slot(uri=CIM['MutualCoupling.r0'], name="mutualCoupling__r0", curie=CIM.curie('MutualCoupling.r0'),
                   model_uri=CIMTBL.mutualCoupling__r0, domain=None, range=Optional[float])

slots.mutualCoupling__x0 = Slot(uri=CIM['MutualCoupling.x0'], name="mutualCoupling__x0", curie=CIM.curie('MutualCoupling.x0'),
                   model_uri=CIMTBL.mutualCoupling__x0, domain=None, range=Optional[float])

slots.mutualCoupling__First_Terminal = Slot(uri=CIM['MutualCoupling.First_Terminal'], name="mutualCoupling__First_Terminal", curie=CIM.curie('MutualCoupling.First_Terminal'),
                   model_uri=CIMTBL.mutualCoupling__First_Terminal, domain=None, range=Optional[Union[dict, Terminal]])

slots.mutualCoupling__Second_Terminal = Slot(uri=CIM['MutualCoupling.Second_Terminal'], name="mutualCoupling__Second_Terminal", curie=CIM.curie('MutualCoupling.Second_Terminal'),
                   model_uri=CIMTBL.mutualCoupling__Second_Terminal, domain=None, range=Optional[Union[dict, Terminal]])

slots.noLoadTest__energisedEndVoltage = Slot(uri=CIM['NoLoadTest.energisedEndVoltage'], name="noLoadTest__energisedEndVoltage", curie=CIM.curie('NoLoadTest.energisedEndVoltage'),
                   model_uri=CIMTBL.noLoadTest__energisedEndVoltage, domain=None, range=Optional[float])

slots.noLoadTest__excitingCurrent = Slot(uri=CIM['NoLoadTest.excitingCurrent'], name="noLoadTest__excitingCurrent", curie=CIM.curie('NoLoadTest.excitingCurrent'),
                   model_uri=CIMTBL.noLoadTest__excitingCurrent, domain=None, range=Optional[float])

slots.noLoadTest__excitingCurrentZero = Slot(uri=CIM['NoLoadTest.excitingCurrentZero'], name="noLoadTest__excitingCurrentZero", curie=CIM.curie('NoLoadTest.excitingCurrentZero'),
                   model_uri=CIMTBL.noLoadTest__excitingCurrentZero, domain=None, range=Optional[float])

slots.noLoadTest__loss = Slot(uri=CIM['NoLoadTest.loss'], name="noLoadTest__loss", curie=CIM.curie('NoLoadTest.loss'),
                   model_uri=CIMTBL.noLoadTest__loss, domain=None, range=Optional[float])

slots.noLoadTest__lossZero = Slot(uri=CIM['NoLoadTest.lossZero'], name="noLoadTest__lossZero", curie=CIM.curie('NoLoadTest.lossZero'),
                   model_uri=CIMTBL.noLoadTest__lossZero, domain=None, range=Optional[float])

slots.noLoadTest__EnergisedEnd = Slot(uri=CIM['NoLoadTest.EnergisedEnd'], name="noLoadTest__EnergisedEnd", curie=CIM.curie('NoLoadTest.EnergisedEnd'),
                   model_uri=CIMTBL.noLoadTest__EnergisedEnd, domain=None, range=Optional[Union[dict, TransformerEndInfo]])

slots.nonConformLoad__LoadGroup = Slot(uri=CIM['NonConformLoad.LoadGroup'], name="nonConformLoad__LoadGroup", curie=CIM.curie('NonConformLoad.LoadGroup'),
                   model_uri=CIMTBL.nonConformLoad__LoadGroup, domain=None, range=Optional[Union[dict, NonConformLoadGroup]])

slots.nonConformLoadSchedule__NonConformLoadGroup = Slot(uri=CIM['NonConformLoadSchedule.NonConformLoadGroup'], name="nonConformLoadSchedule__NonConformLoadGroup", curie=CIM.curie('NonConformLoadSchedule.NonConformLoadGroup'),
                   model_uri=CIMTBL.nonConformLoadSchedule__NonConformLoadGroup, domain=None, range=Optional[Union[dict, NonConformLoadGroup]])

slots.nonlinearShuntCompensatorPhasePoint__bTotal = Slot(uri=CIM['NonlinearShuntCompensatorPhasePoint.bTotal'], name="nonlinearShuntCompensatorPhasePoint__bTotal", curie=CIM.curie('NonlinearShuntCompensatorPhasePoint.bTotal'),
                   model_uri=CIMTBL.nonlinearShuntCompensatorPhasePoint__bTotal, domain=None, range=Optional[float])

slots.nonlinearShuntCompensatorPhasePoint__gTotal = Slot(uri=CIM['NonlinearShuntCompensatorPhasePoint.gTotal'], name="nonlinearShuntCompensatorPhasePoint__gTotal", curie=CIM.curie('NonlinearShuntCompensatorPhasePoint.gTotal'),
                   model_uri=CIMTBL.nonlinearShuntCompensatorPhasePoint__gTotal, domain=None, range=Optional[float])

slots.nonlinearShuntCompensatorPhasePoint__sectionNumber = Slot(uri=CIM['NonlinearShuntCompensatorPhasePoint.sectionNumber'], name="nonlinearShuntCompensatorPhasePoint__sectionNumber", curie=CIM.curie('NonlinearShuntCompensatorPhasePoint.sectionNumber'),
                   model_uri=CIMTBL.nonlinearShuntCompensatorPhasePoint__sectionNumber, domain=None, range=Optional[int])

slots.nonlinearShuntCompensatorPhasePoint__NonlinearShuntCompensatorPhase = Slot(uri=CIM['NonlinearShuntCompensatorPhasePoint.NonlinearShuntCompensatorPhase'], name="nonlinearShuntCompensatorPhasePoint__NonlinearShuntCompensatorPhase", curie=CIM.curie('NonlinearShuntCompensatorPhasePoint.NonlinearShuntCompensatorPhase'),
                   model_uri=CIMTBL.nonlinearShuntCompensatorPhasePoint__NonlinearShuntCompensatorPhase, domain=None, range=Optional[Union[dict, NonlinearShuntCompensatorPhase]])

slots.nonlinearShuntCompensatorPoint__b0Total = Slot(uri=CIM['NonlinearShuntCompensatorPoint.b0Total'], name="nonlinearShuntCompensatorPoint__b0Total", curie=CIM.curie('NonlinearShuntCompensatorPoint.b0Total'),
                   model_uri=CIMTBL.nonlinearShuntCompensatorPoint__b0Total, domain=None, range=Optional[float])

slots.nonlinearShuntCompensatorPoint__bTotal = Slot(uri=CIM['NonlinearShuntCompensatorPoint.bTotal'], name="nonlinearShuntCompensatorPoint__bTotal", curie=CIM.curie('NonlinearShuntCompensatorPoint.bTotal'),
                   model_uri=CIMTBL.nonlinearShuntCompensatorPoint__bTotal, domain=None, range=Optional[float])

slots.nonlinearShuntCompensatorPoint__g0Total = Slot(uri=CIM['NonlinearShuntCompensatorPoint.g0Total'], name="nonlinearShuntCompensatorPoint__g0Total", curie=CIM.curie('NonlinearShuntCompensatorPoint.g0Total'),
                   model_uri=CIMTBL.nonlinearShuntCompensatorPoint__g0Total, domain=None, range=Optional[float])

slots.nonlinearShuntCompensatorPoint__gTotal = Slot(uri=CIM['NonlinearShuntCompensatorPoint.gTotal'], name="nonlinearShuntCompensatorPoint__gTotal", curie=CIM.curie('NonlinearShuntCompensatorPoint.gTotal'),
                   model_uri=CIMTBL.nonlinearShuntCompensatorPoint__gTotal, domain=None, range=Optional[float])

slots.nonlinearShuntCompensatorPoint__sectionNumber = Slot(uri=CIM['NonlinearShuntCompensatorPoint.sectionNumber'], name="nonlinearShuntCompensatorPoint__sectionNumber", curie=CIM.curie('NonlinearShuntCompensatorPoint.sectionNumber'),
                   model_uri=CIMTBL.nonlinearShuntCompensatorPoint__sectionNumber, domain=None, range=Optional[int])

slots.nonlinearShuntCompensatorPoint__NonlinearShuntCompensator = Slot(uri=CIM['NonlinearShuntCompensatorPoint.NonlinearShuntCompensator'], name="nonlinearShuntCompensatorPoint__NonlinearShuntCompensator", curie=CIM.curie('NonlinearShuntCompensatorPoint.NonlinearShuntCompensator'),
                   model_uri=CIMTBL.nonlinearShuntCompensatorPoint__NonlinearShuntCompensator, domain=None, range=Optional[Union[dict, NonlinearShuntCompensator]])

slots.openCircuitTest__energisedEndStep = Slot(uri=CIM['OpenCircuitTest.energisedEndStep'], name="openCircuitTest__energisedEndStep", curie=CIM.curie('OpenCircuitTest.energisedEndStep'),
                   model_uri=CIMTBL.openCircuitTest__energisedEndStep, domain=None, range=Optional[int])

slots.openCircuitTest__energisedEndVoltage = Slot(uri=CIM['OpenCircuitTest.energisedEndVoltage'], name="openCircuitTest__energisedEndVoltage", curie=CIM.curie('OpenCircuitTest.energisedEndVoltage'),
                   model_uri=CIMTBL.openCircuitTest__energisedEndVoltage, domain=None, range=Optional[float])

slots.openCircuitTest__openEndStep = Slot(uri=CIM['OpenCircuitTest.openEndStep'], name="openCircuitTest__openEndStep", curie=CIM.curie('OpenCircuitTest.openEndStep'),
                   model_uri=CIMTBL.openCircuitTest__openEndStep, domain=None, range=Optional[int])

slots.openCircuitTest__openEndVoltage = Slot(uri=CIM['OpenCircuitTest.openEndVoltage'], name="openCircuitTest__openEndVoltage", curie=CIM.curie('OpenCircuitTest.openEndVoltage'),
                   model_uri=CIMTBL.openCircuitTest__openEndVoltage, domain=None, range=Optional[float])

slots.openCircuitTest__phaseShift = Slot(uri=CIM['OpenCircuitTest.phaseShift'], name="openCircuitTest__phaseShift", curie=CIM.curie('OpenCircuitTest.phaseShift'),
                   model_uri=CIMTBL.openCircuitTest__phaseShift, domain=None, range=Optional[float])

slots.openCircuitTest__EnergisedEnd = Slot(uri=CIM['OpenCircuitTest.EnergisedEnd'], name="openCircuitTest__EnergisedEnd", curie=CIM.curie('OpenCircuitTest.EnergisedEnd'),
                   model_uri=CIMTBL.openCircuitTest__EnergisedEnd, domain=None, range=Optional[Union[dict, TransformerEndInfo]])

slots.openCircuitTest__OpenEnd = Slot(uri=CIM['OpenCircuitTest.OpenEnd'], name="openCircuitTest__OpenEnd", curie=CIM.curie('OpenCircuitTest.OpenEnd'),
                   model_uri=CIMTBL.openCircuitTest__OpenEnd, domain=None, range=Optional[Union[dict, TransformerEndInfo]])

slots.operationalLimit__OperationalLimitSet = Slot(uri=CIM['OperationalLimit.OperationalLimitSet'], name="operationalLimit__OperationalLimitSet", curie=CIM.curie('OperationalLimit.OperationalLimitSet'),
                   model_uri=CIMTBL.operationalLimit__OperationalLimitSet, domain=None, range=Optional[Union[dict, OperationalLimitSet]])

slots.operationalLimit__OperationalLimitType = Slot(uri=CIM['OperationalLimit.OperationalLimitType'], name="operationalLimit__OperationalLimitType", curie=CIM.curie('OperationalLimit.OperationalLimitType'),
                   model_uri=CIMTBL.operationalLimit__OperationalLimitType, domain=None, range=Optional[Union[dict, OperationalLimitType]])

slots.operationalLimit__StepOperationalLimitTable = Slot(uri=CIM['OperationalLimit.StepOperationalLimitTable'], name="operationalLimit__StepOperationalLimitTable", curie=CIM.curie('OperationalLimit.StepOperationalLimitTable'),
                   model_uri=CIMTBL.operationalLimit__StepOperationalLimitTable, domain=None, range=Optional[Union[dict, StepOperationalLimitTable]])

slots.operationalLimitSet__Equipment = Slot(uri=CIM['OperationalLimitSet.Equipment'], name="operationalLimitSet__Equipment", curie=CIM.curie('OperationalLimitSet.Equipment'),
                   model_uri=CIMTBL.operationalLimitSet__Equipment, domain=None, range=Optional[Union[dict, Equipment]])

slots.operationalLimitSet__PowerTransferCorridor = Slot(uri=CIM['OperationalLimitSet.PowerTransferCorridor'], name="operationalLimitSet__PowerTransferCorridor", curie=CIM.curie('OperationalLimitSet.PowerTransferCorridor'),
                   model_uri=CIMTBL.operationalLimitSet__PowerTransferCorridor, domain=None, range=Optional[Union[dict, PowerTransferCorridor]])

slots.operationalLimitSet__Terminal = Slot(uri=CIM['OperationalLimitSet.Terminal'], name="operationalLimitSet__Terminal", curie=CIM.curie('OperationalLimitSet.Terminal'),
                   model_uri=CIMTBL.operationalLimitSet__Terminal, domain=None, range=Optional[Union[dict, ACDCTerminal]])

slots.operationalLimitType__acceptableDuration = Slot(uri=CIM['OperationalLimitType.acceptableDuration'], name="operationalLimitType__acceptableDuration", curie=CIM.curie('OperationalLimitType.acceptableDuration'),
                   model_uri=CIMTBL.operationalLimitType__acceptableDuration, domain=None, range=Optional[float])

slots.operationalLimitType__direction = Slot(uri=CIM['OperationalLimitType.direction'], name="operationalLimitType__direction", curie=CIM.curie('OperationalLimitType.direction'),
                   model_uri=CIMTBL.operationalLimitType__direction, domain=None, range=Optional[Union[str, "OperationalLimitDirectionKind"]])

slots.operationalLimitType__isInfiniteDuration = Slot(uri=CIM['OperationalLimitType.isInfiniteDuration'], name="operationalLimitType__isInfiniteDuration", curie=CIM.curie('OperationalLimitType.isInfiniteDuration'),
                   model_uri=CIMTBL.operationalLimitType__isInfiniteDuration, domain=None, range=Optional[Union[bool, Bool]])

slots.operationalLimitType__isMinimum = Slot(uri=CIM['OperationalLimitType.isMinimum'], name="operationalLimitType__isMinimum", curie=CIM.curie('OperationalLimitType.isMinimum'),
                   model_uri=CIMTBL.operationalLimitType__isMinimum, domain=None, range=Optional[Union[bool, Bool]])

slots.operationalLimitType__kind = Slot(uri=CIM['OperationalLimitType.kind'], name="operationalLimitType__kind", curie=CIM.curie('OperationalLimitType.kind'),
                   model_uri=CIMTBL.operationalLimitType__kind, domain=None, range=Optional[Union[str, "LimitKind"]])

slots.operationalLimitType__PermanentAmbientTemperatureDependencyCurve = Slot(uri=CIM['OperationalLimitType.PermanentAmbientTemperatureDependencyCurve'], name="operationalLimitType__PermanentAmbientTemperatureDependencyCurve", curie=CIM.curie('OperationalLimitType.PermanentAmbientTemperatureDependencyCurve'),
                   model_uri=CIMTBL.operationalLimitType__PermanentAmbientTemperatureDependencyCurve, domain=None, range=Optional[Union[dict, AmbientTemperatureDependencyCurve]])

slots.operationalLimitType__PermanentSolarRadiationCurve = Slot(uri=CIM['OperationalLimitType.PermanentSolarRadiationCurve'], name="operationalLimitType__PermanentSolarRadiationCurve", curie=CIM.curie('OperationalLimitType.PermanentSolarRadiationCurve'),
                   model_uri=CIMTBL.operationalLimitType__PermanentSolarRadiationCurve, domain=None, range=Optional[Union[dict, SolarRadiationDependencyCurve]])

slots.operationalLimitType__RecoveryOverloadLimitCurve = Slot(uri=CIM['OperationalLimitType.RecoveryOverloadLimitCurve'], name="operationalLimitType__RecoveryOverloadLimitCurve", curie=CIM.curie('OperationalLimitType.RecoveryOverloadLimitCurve'),
                   model_uri=CIMTBL.operationalLimitType__RecoveryOverloadLimitCurve, domain=None, range=Optional[Union[dict, RecoveryOverloadLimitCurve]])

slots.operationalLimitType__TemporaryBaseOverloadLimitCurve = Slot(uri=CIM['OperationalLimitType.TemporaryBaseOverloadLimitCurve'], name="operationalLimitType__TemporaryBaseOverloadLimitCurve", curie=CIM.curie('OperationalLimitType.TemporaryBaseOverloadLimitCurve'),
                   model_uri=CIMTBL.operationalLimitType__TemporaryBaseOverloadLimitCurve, domain=None, range=Optional[Union[dict, BaseOverloadLimitCurve]])

slots.operationalLimitType__TemporaryDurationOverloadLimitCurve = Slot(uri=CIM['OperationalLimitType.TemporaryDurationOverloadLimitCurve'], name="operationalLimitType__TemporaryDurationOverloadLimitCurve", curie=CIM.curie('OperationalLimitType.TemporaryDurationOverloadLimitCurve'),
                   model_uri=CIMTBL.operationalLimitType__TemporaryDurationOverloadLimitCurve, domain=None, range=Optional[Union[dict, DurationOverloadLimitCurve]])

slots.overheadWireInfo__wireConstructionKind = Slot(uri=CIM['OverheadWireInfo.wireConstructionKind'], name="overheadWireInfo__wireConstructionKind", curie=CIM.curie('OverheadWireInfo.wireConstructionKind'),
                   model_uri=CIMTBL.overheadWireInfo__wireConstructionKind, domain=None, range=Optional[Union[str, "WireConstructionKind"]])

slots.pMUConfiguration__anNmr = Slot(uri=CIM['PMUConfiguration.anNmr'], name="pMUConfiguration__anNmr", curie=CIM.curie('PMUConfiguration.anNmr'),
                   model_uri=CIMTBL.pMUConfiguration__anNmr, domain=None, range=Optional[int])

slots.pMUConfiguration__anScale = Slot(uri=CIM['PMUConfiguration.anScale'], name="pMUConfiguration__anScale", curie=CIM.curie('PMUConfiguration.anScale'),
                   model_uri=CIMTBL.pMUConfiguration__anScale, domain=None, range=Optional[str])

slots.pMUConfiguration__cfgCnt = Slot(uri=CIM['PMUConfiguration.cfgCnt'], name="pMUConfiguration__cfgCnt", curie=CIM.curie('PMUConfiguration.cfgCnt'),
                   model_uri=CIMTBL.pMUConfiguration__cfgCnt, domain=None, range=Optional[int])

slots.pMUConfiguration__chNam = Slot(uri=CIM['PMUConfiguration.chNam'], name="pMUConfiguration__chNam", curie=CIM.curie('PMUConfiguration.chNam'),
                   model_uri=CIMTBL.pMUConfiguration__chNam, domain=None, range=Optional[str])

slots.pMUConfiguration__dfdtNmr = Slot(uri=CIM['PMUConfiguration.dfdtNmr'], name="pMUConfiguration__dfdtNmr", curie=CIM.curie('PMUConfiguration.dfdtNmr'),
                   model_uri=CIMTBL.pMUConfiguration__dfdtNmr, domain=None, range=Optional[int])

slots.pMUConfiguration__dfdtScale = Slot(uri=CIM['PMUConfiguration.dfdtScale'], name="pMUConfiguration__dfdtScale", curie=CIM.curie('PMUConfiguration.dfdtScale'),
                   model_uri=CIMTBL.pMUConfiguration__dfdtScale, domain=None, range=Optional[str])

slots.pMUConfiguration__format = Slot(uri=CIM['PMUConfiguration.format'], name="pMUConfiguration__format", curie=CIM.curie('PMUConfiguration.format'),
                   model_uri=CIMTBL.pMUConfiguration__format, domain=None, range=Optional[str])

slots.pMUConfiguration__frNmr = Slot(uri=CIM['PMUConfiguration.frNmr'], name="pMUConfiguration__frNmr", curie=CIM.curie('PMUConfiguration.frNmr'),
                   model_uri=CIMTBL.pMUConfiguration__frNmr, domain=None, range=Optional[int])

slots.pMUConfiguration__frScale = Slot(uri=CIM['PMUConfiguration.frScale'], name="pMUConfiguration__frScale", curie=CIM.curie('PMUConfiguration.frScale'),
                   model_uri=CIMTBL.pMUConfiguration__frScale, domain=None, range=Optional[str])

slots.pMUConfiguration__grpDly = Slot(uri=CIM['PMUConfiguration.grpDly'], name="pMUConfiguration__grpDly", curie=CIM.curie('PMUConfiguration.grpDly'),
                   model_uri=CIMTBL.pMUConfiguration__grpDly, domain=None, range=Optional[Union[str, XSDTime]])

slots.pMUConfiguration__phNmr = Slot(uri=CIM['PMUConfiguration.phNmr'], name="pMUConfiguration__phNmr", curie=CIM.curie('PMUConfiguration.phNmr'),
                   model_uri=CIMTBL.pMUConfiguration__phNmr, domain=None, range=Optional[int])

slots.pMUConfiguration__phScale = Slot(uri=CIM['PMUConfiguration.phScale'], name="pMUConfiguration__phScale", curie=CIM.curie('PMUConfiguration.phScale'),
                   model_uri=CIMTBL.pMUConfiguration__phScale, domain=None, range=Optional[str])

slots.pMUConfiguration__pmuDataRate = Slot(uri=CIM['PMUConfiguration.pmuDataRate'], name="pMUConfiguration__pmuDataRate", curie=CIM.curie('PMUConfiguration.pmuDataRate'),
                   model_uri=CIMTBL.pMUConfiguration__pmuDataRate, domain=None, range=Optional[int])

slots.pMUConfiguration__streamDataRate = Slot(uri=CIM['PMUConfiguration.streamDataRate'], name="pMUConfiguration__streamDataRate", curie=CIM.curie('PMUConfiguration.streamDataRate'),
                   model_uri=CIMTBL.pMUConfiguration__streamDataRate, domain=None, range=Optional[int])

slots.pMUConfiguration__waitTime = Slot(uri=CIM['PMUConfiguration.waitTime'], name="pMUConfiguration__waitTime", curie=CIM.curie('PMUConfiguration.waitTime'),
                   model_uri=CIMTBL.pMUConfiguration__waitTime, domain=None, range=Optional[Union[str, XSDTime]])

slots.pMUConfiguration__window = Slot(uri=CIM['PMUConfiguration.window'], name="pMUConfiguration__window", curie=CIM.curie('PMUConfiguration.window'),
                   model_uri=CIMTBL.pMUConfiguration__window, domain=None, range=Optional[Union[str, XSDTime]])

slots.pMUConfiguration__PhasorMeasurementUnit = Slot(uri=CIM['PMUConfiguration.PhasorMeasurementUnit'], name="pMUConfiguration__PhasorMeasurementUnit", curie=CIM.curie('PMUConfiguration.PhasorMeasurementUnit'),
                   model_uri=CIMTBL.pMUConfiguration__PhasorMeasurementUnit, domain=None, range=Optional[Union[dict, PhasorMeasurementUnit]])

slots.pMUConfiguration__PMUConfigurationFrame = Slot(uri=CIM['PMUConfiguration.PMUConfigurationFrame'], name="pMUConfiguration__PMUConfigurationFrame", curie=CIM.curie('PMUConfiguration.PMUConfigurationFrame'),
                   model_uri=CIMTBL.pMUConfiguration__PMUConfigurationFrame, domain=None, range=Optional[Union[dict, PMUConfigurationFrame]])

slots.pMUConfigurationFrame__dataRate = Slot(uri=CIM['PMUConfigurationFrame.dataRate'], name="pMUConfigurationFrame__dataRate", curie=CIM.curie('PMUConfigurationFrame.dataRate'),
                   model_uri=CIMTBL.pMUConfigurationFrame__dataRate, domain=None, range=Optional[int])

slots.pMUConfigurationFrame__numPMU = Slot(uri=CIM['PMUConfigurationFrame.numPMU'], name="pMUConfigurationFrame__numPMU", curie=CIM.curie('PMUConfigurationFrame.numPMU'),
                   model_uri=CIMTBL.pMUConfigurationFrame__numPMU, domain=None, range=Optional[int])

slots.pMUConfigurationFrame__pmuConfig = Slot(uri=CIM['PMUConfigurationFrame.pmuConfig'], name="pMUConfigurationFrame__pmuConfig", curie=CIM.curie('PMUConfigurationFrame.pmuConfig'),
                   model_uri=CIMTBL.pMUConfigurationFrame__pmuConfig, domain=None, range=Optional[int])

slots.pMUConfigurationFrame__timeBase = Slot(uri=CIM['PMUConfigurationFrame.timeBase'], name="pMUConfigurationFrame__timeBase", curie=CIM.curie('PMUConfigurationFrame.timeBase'),
                   model_uri=CIMTBL.pMUConfigurationFrame__timeBase, domain=None, range=Optional[int])

slots.pMUStream__PMU = Slot(uri=CIM['PMUStream.PMU'], name="pMUStream__PMU", curie=CIM.curie('PMUStream.PMU'),
                   model_uri=CIMTBL.pMUStream__PMU, domain=None, range=Optional[Union[dict, PhasorMeasurementUnit]])

slots.pMUValueQuality__dataBad = Slot(uri=CIM['PMUValueQuality.dataBad'], name="pMUValueQuality__dataBad", curie=CIM.curie('PMUValueQuality.dataBad'),
                   model_uri=CIMTBL.pMUValueQuality__dataBad, domain=None, range=Optional[Union[bool, Bool]])

slots.pMUValueQuality__dataError = Slot(uri=CIM['PMUValueQuality.dataError'], name="pMUValueQuality__dataError", curie=CIM.curie('PMUValueQuality.dataError'),
                   model_uri=CIMTBL.pMUValueQuality__dataError, domain=None, range=Optional[Union[bool, Bool]])

slots.pMUValueQuality__insertedData = Slot(uri=CIM['PMUValueQuality.insertedData'], name="pMUValueQuality__insertedData", curie=CIM.curie('PMUValueQuality.insertedData'),
                   model_uri=CIMTBL.pMUValueQuality__insertedData, domain=None, range=Optional[Union[bool, Bool]])

slots.pMUValueQuality__localTimeStamp = Slot(uri=CIM['PMUValueQuality.localTimeStamp'], name="pMUValueQuality__localTimeStamp", curie=CIM.curie('PMUValueQuality.localTimeStamp'),
                   model_uri=CIMTBL.pMUValueQuality__localTimeStamp, domain=None, range=Optional[Union[bool, Bool]])

slots.pMUValueQuality__pmuSync = Slot(uri=CIM['PMUValueQuality.pmuSync'], name="pMUValueQuality__pmuSync", curie=CIM.curie('PMUValueQuality.pmuSync'),
                   model_uri=CIMTBL.pMUValueQuality__pmuSync, domain=None, range=Optional[Union[bool, Bool]])

slots.perLengthImpedance__calculatedFrequency = Slot(uri=CIM['PerLengthImpedance.calculatedFrequency'], name="perLengthImpedance__calculatedFrequency", curie=CIM.curie('PerLengthImpedance.calculatedFrequency'),
                   model_uri=CIMTBL.perLengthImpedance__calculatedFrequency, domain=None, range=Optional[float])

slots.perLengthImpedance__calculatedTemperature = Slot(uri=CIM['PerLengthImpedance.calculatedTemperature'], name="perLengthImpedance__calculatedTemperature", curie=CIM.curie('PerLengthImpedance.calculatedTemperature'),
                   model_uri=CIMTBL.perLengthImpedance__calculatedTemperature, domain=None, range=Optional[float])

slots.perLengthImpedance__isUserDefined = Slot(uri=CIM['PerLengthImpedance.isUserDefined'], name="perLengthImpedance__isUserDefined", curie=CIM.curie('PerLengthImpedance.isUserDefined'),
                   model_uri=CIMTBL.perLengthImpedance__isUserDefined, domain=None, range=Optional[Union[bool, Bool]])

slots.perLengthImpedance__rg = Slot(uri=CIM['PerLengthImpedance.rg'], name="perLengthImpedance__rg", curie=CIM.curie('PerLengthImpedance.rg'),
                   model_uri=CIMTBL.perLengthImpedance__rg, domain=None, range=Optional[float])

slots.perLengthImpedance__xg = Slot(uri=CIM['PerLengthImpedance.xg'], name="perLengthImpedance__xg", curie=CIM.curie('PerLengthImpedance.xg'),
                   model_uri=CIMTBL.perLengthImpedance__xg, domain=None, range=Optional[float])

slots.perLengthLineParameter__WireAssemblyInfo = Slot(uri=CIM['PerLengthLineParameter.WireAssemblyInfo'], name="perLengthLineParameter__WireAssemblyInfo", curie=CIM.curie('PerLengthLineParameter.WireAssemblyInfo'),
                   model_uri=CIMTBL.perLengthLineParameter__WireAssemblyInfo, domain=None, range=Optional[Union[dict, WireAssemblyInfo]])

slots.perLengthPhaseImpedance__conductorCount = Slot(uri=CIM['PerLengthPhaseImpedance.conductorCount'], name="perLengthPhaseImpedance__conductorCount", curie=CIM.curie('PerLengthPhaseImpedance.conductorCount'),
                   model_uri=CIMTBL.perLengthPhaseImpedance__conductorCount, domain=None, range=Optional[int])

slots.perLengthSequenceImpedance__b0ch = Slot(uri=CIM['PerLengthSequenceImpedance.b0ch'], name="perLengthSequenceImpedance__b0ch", curie=CIM.curie('PerLengthSequenceImpedance.b0ch'),
                   model_uri=CIMTBL.perLengthSequenceImpedance__b0ch, domain=None, range=Optional[float])

slots.perLengthSequenceImpedance__bch = Slot(uri=CIM['PerLengthSequenceImpedance.bch'], name="perLengthSequenceImpedance__bch", curie=CIM.curie('PerLengthSequenceImpedance.bch'),
                   model_uri=CIMTBL.perLengthSequenceImpedance__bch, domain=None, range=Optional[float])

slots.perLengthSequenceImpedance__g0ch = Slot(uri=CIM['PerLengthSequenceImpedance.g0ch'], name="perLengthSequenceImpedance__g0ch", curie=CIM.curie('PerLengthSequenceImpedance.g0ch'),
                   model_uri=CIMTBL.perLengthSequenceImpedance__g0ch, domain=None, range=Optional[float])

slots.perLengthSequenceImpedance__gch = Slot(uri=CIM['PerLengthSequenceImpedance.gch'], name="perLengthSequenceImpedance__gch", curie=CIM.curie('PerLengthSequenceImpedance.gch'),
                   model_uri=CIMTBL.perLengthSequenceImpedance__gch, domain=None, range=Optional[float])

slots.perLengthSequenceImpedance__r = Slot(uri=CIM['PerLengthSequenceImpedance.r'], name="perLengthSequenceImpedance__r", curie=CIM.curie('PerLengthSequenceImpedance.r'),
                   model_uri=CIMTBL.perLengthSequenceImpedance__r, domain=None, range=Optional[float])

slots.perLengthSequenceImpedance__r0 = Slot(uri=CIM['PerLengthSequenceImpedance.r0'], name="perLengthSequenceImpedance__r0", curie=CIM.curie('PerLengthSequenceImpedance.r0'),
                   model_uri=CIMTBL.perLengthSequenceImpedance__r0, domain=None, range=Optional[float])

slots.perLengthSequenceImpedance__x = Slot(uri=CIM['PerLengthSequenceImpedance.x'], name="perLengthSequenceImpedance__x", curie=CIM.curie('PerLengthSequenceImpedance.x'),
                   model_uri=CIMTBL.perLengthSequenceImpedance__x, domain=None, range=Optional[float])

slots.perLengthSequenceImpedance__x0 = Slot(uri=CIM['PerLengthSequenceImpedance.x0'], name="perLengthSequenceImpedance__x0", curie=CIM.curie('PerLengthSequenceImpedance.x0'),
                   model_uri=CIMTBL.perLengthSequenceImpedance__x0, domain=None, range=Optional[float])

slots.petersenCoil__mode = Slot(uri=CIM['PetersenCoil.mode'], name="petersenCoil__mode", curie=CIM.curie('PetersenCoil.mode'),
                   model_uri=CIMTBL.petersenCoil__mode, domain=None, range=Optional[Union[str, "PetersenCoilModeKind"]])

slots.petersenCoil__nominalU = Slot(uri=CIM['PetersenCoil.nominalU'], name="petersenCoil__nominalU", curie=CIM.curie('PetersenCoil.nominalU'),
                   model_uri=CIMTBL.petersenCoil__nominalU, domain=None, range=Optional[float])

slots.petersenCoil__offsetCurrent = Slot(uri=CIM['PetersenCoil.offsetCurrent'], name="petersenCoil__offsetCurrent", curie=CIM.curie('PetersenCoil.offsetCurrent'),
                   model_uri=CIMTBL.petersenCoil__offsetCurrent, domain=None, range=Optional[float])

slots.petersenCoil__positionCurrent = Slot(uri=CIM['PetersenCoil.positionCurrent'], name="petersenCoil__positionCurrent", curie=CIM.curie('PetersenCoil.positionCurrent'),
                   model_uri=CIMTBL.petersenCoil__positionCurrent, domain=None, range=Optional[float])

slots.petersenCoil__xGroundMax = Slot(uri=CIM['PetersenCoil.xGroundMax'], name="petersenCoil__xGroundMax", curie=CIM.curie('PetersenCoil.xGroundMax'),
                   model_uri=CIMTBL.petersenCoil__xGroundMax, domain=None, range=Optional[float])

slots.petersenCoil__xGroundMin = Slot(uri=CIM['PetersenCoil.xGroundMin'], name="petersenCoil__xGroundMin", curie=CIM.curie('PetersenCoil.xGroundMin'),
                   model_uri=CIMTBL.petersenCoil__xGroundMin, domain=None, range=Optional[float])

slots.petersenCoil__xGroundNominal = Slot(uri=CIM['PetersenCoil.xGroundNominal'], name="petersenCoil__xGroundNominal", curie=CIM.curie('PetersenCoil.xGroundNominal'),
                   model_uri=CIMTBL.petersenCoil__xGroundNominal, domain=None, range=Optional[float])

slots.phaseImpedanceData__b = Slot(uri=CIM['PhaseImpedanceData.b'], name="phaseImpedanceData__b", curie=CIM.curie('PhaseImpedanceData.b'),
                   model_uri=CIMTBL.phaseImpedanceData__b, domain=None, range=Optional[float])

slots.phaseImpedanceData__column = Slot(uri=CIM['PhaseImpedanceData.column'], name="phaseImpedanceData__column", curie=CIM.curie('PhaseImpedanceData.column'),
                   model_uri=CIMTBL.phaseImpedanceData__column, domain=None, range=Optional[int])

slots.phaseImpedanceData__fromPhase = Slot(uri=CIM['PhaseImpedanceData.fromPhase'], name="phaseImpedanceData__fromPhase", curie=CIM.curie('PhaseImpedanceData.fromPhase'),
                   model_uri=CIMTBL.phaseImpedanceData__fromPhase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.phaseImpedanceData__g = Slot(uri=CIM['PhaseImpedanceData.g'], name="phaseImpedanceData__g", curie=CIM.curie('PhaseImpedanceData.g'),
                   model_uri=CIMTBL.phaseImpedanceData__g, domain=None, range=Optional[float])

slots.phaseImpedanceData__r = Slot(uri=CIM['PhaseImpedanceData.r'], name="phaseImpedanceData__r", curie=CIM.curie('PhaseImpedanceData.r'),
                   model_uri=CIMTBL.phaseImpedanceData__r, domain=None, range=Optional[float])

slots.phaseImpedanceData__row = Slot(uri=CIM['PhaseImpedanceData.row'], name="phaseImpedanceData__row", curie=CIM.curie('PhaseImpedanceData.row'),
                   model_uri=CIMTBL.phaseImpedanceData__row, domain=None, range=Optional[int])

slots.phaseImpedanceData__toPhase = Slot(uri=CIM['PhaseImpedanceData.toPhase'], name="phaseImpedanceData__toPhase", curie=CIM.curie('PhaseImpedanceData.toPhase'),
                   model_uri=CIMTBL.phaseImpedanceData__toPhase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.phaseImpedanceData__x = Slot(uri=CIM['PhaseImpedanceData.x'], name="phaseImpedanceData__x", curie=CIM.curie('PhaseImpedanceData.x'),
                   model_uri=CIMTBL.phaseImpedanceData__x, domain=None, range=Optional[float])

slots.phaseImpedanceData__PhaseImpedance = Slot(uri=CIM['PhaseImpedanceData.PhaseImpedance'], name="phaseImpedanceData__PhaseImpedance", curie=CIM.curie('PhaseImpedanceData.PhaseImpedance'),
                   model_uri=CIMTBL.phaseImpedanceData__PhaseImpedance, domain=None, range=Optional[Union[dict, PerLengthPhaseImpedance]])

slots.phaseTapChanger__TransformerEnd = Slot(uri=CIM['PhaseTapChanger.TransformerEnd'], name="phaseTapChanger__TransformerEnd", curie=CIM.curie('PhaseTapChanger.TransformerEnd'),
                   model_uri=CIMTBL.phaseTapChanger__TransformerEnd, domain=None, range=Optional[Union[dict, TransformerEnd]])

slots.phaseTapChangerAsymmetrical__windingConnectionAngle = Slot(uri=CIM['PhaseTapChangerAsymmetrical.windingConnectionAngle'], name="phaseTapChangerAsymmetrical__windingConnectionAngle", curie=CIM.curie('PhaseTapChangerAsymmetrical.windingConnectionAngle'),
                   model_uri=CIMTBL.phaseTapChangerAsymmetrical__windingConnectionAngle, domain=None, range=Optional[float])

slots.phaseTapChangerLinear__stepPhaseShiftIncrement = Slot(uri=CIM['PhaseTapChangerLinear.stepPhaseShiftIncrement'], name="phaseTapChangerLinear__stepPhaseShiftIncrement", curie=CIM.curie('PhaseTapChangerLinear.stepPhaseShiftIncrement'),
                   model_uri=CIMTBL.phaseTapChangerLinear__stepPhaseShiftIncrement, domain=None, range=Optional[float])

slots.phaseTapChangerLinear__xMax = Slot(uri=CIM['PhaseTapChangerLinear.xMax'], name="phaseTapChangerLinear__xMax", curie=CIM.curie('PhaseTapChangerLinear.xMax'),
                   model_uri=CIMTBL.phaseTapChangerLinear__xMax, domain=None, range=Optional[float])

slots.phaseTapChangerNonLinear__voltageStepIncrement = Slot(uri=CIM['PhaseTapChangerNonLinear.voltageStepIncrement'], name="phaseTapChangerNonLinear__voltageStepIncrement", curie=CIM.curie('PhaseTapChangerNonLinear.voltageStepIncrement'),
                   model_uri=CIMTBL.phaseTapChangerNonLinear__voltageStepIncrement, domain=None, range=Optional[float])

slots.phaseTapChangerNonLinear__xMax = Slot(uri=CIM['PhaseTapChangerNonLinear.xMax'], name="phaseTapChangerNonLinear__xMax", curie=CIM.curie('PhaseTapChangerNonLinear.xMax'),
                   model_uri=CIMTBL.phaseTapChangerNonLinear__xMax, domain=None, range=Optional[float])

slots.phaseTapChangerTablePoint__angle = Slot(uri=CIM['PhaseTapChangerTablePoint.angle'], name="phaseTapChangerTablePoint__angle", curie=CIM.curie('PhaseTapChangerTablePoint.angle'),
                   model_uri=CIMTBL.phaseTapChangerTablePoint__angle, domain=None, range=Optional[float])

slots.phaseTapChangerTablePoint__PhaseTapChangerTable = Slot(uri=CIM['PhaseTapChangerTablePoint.PhaseTapChangerTable'], name="phaseTapChangerTablePoint__PhaseTapChangerTable", curie=CIM.curie('PhaseTapChangerTablePoint.PhaseTapChangerTable'),
                   model_uri=CIMTBL.phaseTapChangerTablePoint__PhaseTapChangerTable, domain=None, range=Optional[Union[dict, PhaseTapChangerTable]])

slots.phaseTapChangerTabular__PhaseTapChangerTable = Slot(uri=CIM['PhaseTapChangerTabular.PhaseTapChangerTable'], name="phaseTapChangerTabular__PhaseTapChangerTable", curie=CIM.curie('PhaseTapChangerTabular.PhaseTapChangerTable'),
                   model_uri=CIMTBL.phaseTapChangerTabular__PhaseTapChangerTable, domain=None, range=Optional[Union[dict, PhaseTapChangerTable]])

slots.phasorDataConcentrator__CentralPDC = Slot(uri=CIM['PhasorDataConcentrator.CentralPDC'], name="phasorDataConcentrator__CentralPDC", curie=CIM.curie('PhasorDataConcentrator.CentralPDC'),
                   model_uri=CIMTBL.phasorDataConcentrator__CentralPDC, domain=None, range=Optional[Union[dict, PhasorDataConcentrator]])

slots.phasorMeasurementUnit__timeSourceType = Slot(uri=CIM['PhasorMeasurementUnit.timeSourceType'], name="phasorMeasurementUnit__timeSourceType", curie=CIM.curie('PhasorMeasurementUnit.timeSourceType'),
                   model_uri=CIMTBL.phasorMeasurementUnit__timeSourceType, domain=None, range=Optional[Union[str, "TimeSourceKind"]])

slots.phasorMeasurementUnit__PhasorDataConcentrator = Slot(uri=CIM['PhasorMeasurementUnit.PhasorDataConcentrator'], name="phasorMeasurementUnit__PhasorDataConcentrator", curie=CIM.curie('PhasorMeasurementUnit.PhasorDataConcentrator'),
                   model_uri=CIMTBL.phasorMeasurementUnit__PhasorDataConcentrator, domain=None, range=Optional[Union[dict, PhasorDataConcentrator]])

slots.phasorMeasurementUnit__PMUConfiguration = Slot(uri=CIM['PhasorMeasurementUnit.PMUConfiguration'], name="phasorMeasurementUnit__PMUConfiguration", curie=CIM.curie('PhasorMeasurementUnit.PMUConfiguration'),
                   model_uri=CIMTBL.phasorMeasurementUnit__PMUConfiguration, domain=None, range=Optional[Union[dict, PMUConfiguration]])

slots.phasorMeasurementUnit__PMUStream = Slot(uri=CIM['PhasorMeasurementUnit.PMUStream'], name="phasorMeasurementUnit__PMUStream", curie=CIM.curie('PhasorMeasurementUnit.PMUStream'),
                   model_uri=CIMTBL.phasorMeasurementUnit__PMUStream, domain=None, range=Optional[Union[dict, PMUStream]])

slots.pointOnWaveValue__Analog = Slot(uri=CIM['PointOnWaveValue.Analog'], name="pointOnWaveValue__Analog", curie=CIM.curie('PointOnWaveValue.Analog'),
                   model_uri=CIMTBL.pointOnWaveValue__Analog, domain=None, range=Optional[Union[dict, Analog]])

slots.positionPoint__sequenceNumber = Slot(uri=CIM['PositionPoint.sequenceNumber'], name="positionPoint__sequenceNumber", curie=CIM.curie('PositionPoint.sequenceNumber'),
                   model_uri=CIMTBL.positionPoint__sequenceNumber, domain=None, range=Optional[int])

slots.positionPoint__xPosition = Slot(uri=CIM['PositionPoint.xPosition'], name="positionPoint__xPosition", curie=CIM.curie('PositionPoint.xPosition'),
                   model_uri=CIMTBL.positionPoint__xPosition, domain=None, range=Optional[str])

slots.positionPoint__yPosition = Slot(uri=CIM['PositionPoint.yPosition'], name="positionPoint__yPosition", curie=CIM.curie('PositionPoint.yPosition'),
                   model_uri=CIMTBL.positionPoint__yPosition, domain=None, range=Optional[str])

slots.positionPoint__zPosition = Slot(uri=CIM['PositionPoint.zPosition'], name="positionPoint__zPosition", curie=CIM.curie('PositionPoint.zPosition'),
                   model_uri=CIMTBL.positionPoint__zPosition, domain=None, range=Optional[str])

slots.positionPoint__Location = Slot(uri=CIM['PositionPoint.Location'], name="positionPoint__Location", curie=CIM.curie('PositionPoint.Location'),
                   model_uri=CIMTBL.positionPoint__Location, domain=None, range=Optional[Union[dict, Location]])

slots.positionPoint__RelativeHeight = Slot(uri=CIM['PositionPoint.RelativeHeight'], name="positionPoint__RelativeHeight", curie=CIM.curie('PositionPoint.RelativeHeight'),
                   model_uri=CIMTBL.positionPoint__RelativeHeight, domain=None, range=Optional[Union[dict, RelativeHeight]])

slots.potentialTransformer__nominalRatio = Slot(uri=CIM['PotentialTransformer.nominalRatio'], name="potentialTransformer__nominalRatio", curie=CIM.curie('PotentialTransformer.nominalRatio'),
                   model_uri=CIMTBL.potentialTransformer__nominalRatio, domain=None, range=Optional[float])

slots.potentialTransformer__type = Slot(uri=CIM['PotentialTransformer.type'], name="potentialTransformer__type", curie=CIM.curie('PotentialTransformer.type'),
                   model_uri=CIMTBL.potentialTransformer__type, domain=None, range=Optional[Union[str, "PotentialTransformerKind"]])

slots.powerCutZone__cutLevel1 = Slot(uri=CIM['PowerCutZone.cutLevel1'], name="powerCutZone__cutLevel1", curie=CIM.curie('PowerCutZone.cutLevel1'),
                   model_uri=CIMTBL.powerCutZone__cutLevel1, domain=None, range=Optional[float])

slots.powerCutZone__cutLevel2 = Slot(uri=CIM['PowerCutZone.cutLevel2'], name="powerCutZone__cutLevel2", curie=CIM.curie('PowerCutZone.cutLevel2'),
                   model_uri=CIMTBL.powerCutZone__cutLevel2, domain=None, range=Optional[float])

slots.powerElectricalChemicalUnit__kind = Slot(uri=CIM['PowerElectricalChemicalUnit.kind'], name="powerElectricalChemicalUnit__kind", curie=CIM.curie('PowerElectricalChemicalUnit.kind'),
                   model_uri=CIMTBL.powerElectricalChemicalUnit__kind, domain=None, range=Optional[Union[str, "PowerElectricalChemicalUnitKind"]])

slots.powerElectronicsConnection__inSafeMode = Slot(uri=CIM['PowerElectronicsConnection.inSafeMode'], name="powerElectronicsConnection__inSafeMode", curie=CIM.curie('PowerElectronicsConnection.inSafeMode'),
                   model_uri=CIMTBL.powerElectronicsConnection__inSafeMode, domain=None, range=Optional[Union[bool, Bool]])

slots.powerElectronicsConnection__isGridForming = Slot(uri=CIM['PowerElectronicsConnection.isGridForming'], name="powerElectronicsConnection__isGridForming", curie=CIM.curie('PowerElectronicsConnection.isGridForming'),
                   model_uri=CIMTBL.powerElectronicsConnection__isGridForming, domain=None, range=Optional[Union[bool, Bool]])

slots.powerElectronicsConnection__maxIFault = Slot(uri=CIM['PowerElectronicsConnection.maxIFault'], name="powerElectronicsConnection__maxIFault", curie=CIM.curie('PowerElectronicsConnection.maxIFault'),
                   model_uri=CIMTBL.powerElectronicsConnection__maxIFault, domain=None, range=Optional[float])

slots.powerElectronicsConnection__maxQ = Slot(uri=CIM['PowerElectronicsConnection.maxQ'], name="powerElectronicsConnection__maxQ", curie=CIM.curie('PowerElectronicsConnection.maxQ'),
                   model_uri=CIMTBL.powerElectronicsConnection__maxQ, domain=None, range=Optional[float])

slots.powerElectronicsConnection__minQ = Slot(uri=CIM['PowerElectronicsConnection.minQ'], name="powerElectronicsConnection__minQ", curie=CIM.curie('PowerElectronicsConnection.minQ'),
                   model_uri=CIMTBL.powerElectronicsConnection__minQ, domain=None, range=Optional[float])

slots.powerElectronicsConnection__p = Slot(uri=CIM['PowerElectronicsConnection.p'], name="powerElectronicsConnection__p", curie=CIM.curie('PowerElectronicsConnection.p'),
                   model_uri=CIMTBL.powerElectronicsConnection__p, domain=None, range=Optional[float])

slots.powerElectronicsConnection__q = Slot(uri=CIM['PowerElectronicsConnection.q'], name="powerElectronicsConnection__q", curie=CIM.curie('PowerElectronicsConnection.q'),
                   model_uri=CIMTBL.powerElectronicsConnection__q, domain=None, range=Optional[float])

slots.powerElectronicsConnection__ratedS = Slot(uri=CIM['PowerElectronicsConnection.ratedS'], name="powerElectronicsConnection__ratedS", curie=CIM.curie('PowerElectronicsConnection.ratedS'),
                   model_uri=CIMTBL.powerElectronicsConnection__ratedS, domain=None, range=Optional[float])

slots.powerElectronicsConnection__ratedU = Slot(uri=CIM['PowerElectronicsConnection.ratedU'], name="powerElectronicsConnection__ratedU", curie=CIM.curie('PowerElectronicsConnection.ratedU'),
                   model_uri=CIMTBL.powerElectronicsConnection__ratedU, domain=None, range=Optional[float])

slots.powerElectronicsConnectionPhase__p = Slot(uri=CIM['PowerElectronicsConnectionPhase.p'], name="powerElectronicsConnectionPhase__p", curie=CIM.curie('PowerElectronicsConnectionPhase.p'),
                   model_uri=CIMTBL.powerElectronicsConnectionPhase__p, domain=None, range=Optional[float])

slots.powerElectronicsConnectionPhase__phase = Slot(uri=CIM['PowerElectronicsConnectionPhase.phase'], name="powerElectronicsConnectionPhase__phase", curie=CIM.curie('PowerElectronicsConnectionPhase.phase'),
                   model_uri=CIMTBL.powerElectronicsConnectionPhase__phase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.powerElectronicsConnectionPhase__q = Slot(uri=CIM['PowerElectronicsConnectionPhase.q'], name="powerElectronicsConnectionPhase__q", curie=CIM.curie('PowerElectronicsConnectionPhase.q'),
                   model_uri=CIMTBL.powerElectronicsConnectionPhase__q, domain=None, range=Optional[float])

slots.powerElectronicsConnectionPhase__PowerElectronicsConnection = Slot(uri=CIM['PowerElectronicsConnectionPhase.PowerElectronicsConnection'], name="powerElectronicsConnectionPhase__PowerElectronicsConnection", curie=CIM.curie('PowerElectronicsConnectionPhase.PowerElectronicsConnection'),
                   model_uri=CIMTBL.powerElectronicsConnectionPhase__PowerElectronicsConnection, domain=None, range=Optional[Union[dict, PowerElectronicsConnection]])

slots.powerElectronicsMarineUnit__kind = Slot(uri=CIM['PowerElectronicsMarineUnit.kind'], name="powerElectronicsMarineUnit__kind", curie=CIM.curie('PowerElectronicsMarineUnit.kind'),
                   model_uri=CIMTBL.powerElectronicsMarineUnit__kind, domain=None, range=Optional[Union[str, "MarineUnitKind"]])

slots.powerElectronicsUnit__maxP = Slot(uri=CIM['PowerElectronicsUnit.maxP'], name="powerElectronicsUnit__maxP", curie=CIM.curie('PowerElectronicsUnit.maxP'),
                   model_uri=CIMTBL.powerElectronicsUnit__maxP, domain=None, range=Optional[float])

slots.powerElectronicsUnit__minP = Slot(uri=CIM['PowerElectronicsUnit.minP'], name="powerElectronicsUnit__minP", curie=CIM.curie('PowerElectronicsUnit.minP'),
                   model_uri=CIMTBL.powerElectronicsUnit__minP, domain=None, range=Optional[float])

slots.powerElectronicsUnit__PowerElectronicsConnection = Slot(uri=CIM['PowerElectronicsUnit.PowerElectronicsConnection'], name="powerElectronicsUnit__PowerElectronicsConnection", curie=CIM.curie('PowerElectronicsUnit.PowerElectronicsConnection'),
                   model_uri=CIMTBL.powerElectronicsUnit__PowerElectronicsConnection, domain=None, range=Optional[Union[dict, PowerElectronicsConnection]])

slots.powerElectronicsUnit__PowerElectronicsUnitController = Slot(uri=CIM['PowerElectronicsUnit.PowerElectronicsUnitController'], name="powerElectronicsUnit__PowerElectronicsUnitController", curie=CIM.curie('PowerElectronicsUnit.PowerElectronicsUnitController'),
                   model_uri=CIMTBL.powerElectronicsUnit__PowerElectronicsUnitController, domain=None, range=Optional[Union[dict, PowerElectronicsUnitController]])

slots.powerSystemResource__AssetDatasheet = Slot(uri=CIM['PowerSystemResource.AssetDatasheet'], name="powerSystemResource__AssetDatasheet", curie=CIM.curie('PowerSystemResource.AssetDatasheet'),
                   model_uri=CIMTBL.powerSystemResource__AssetDatasheet, domain=None, range=Optional[Union[dict, AssetInfo]])

slots.powerSystemResource__DesignElement = Slot(uri=CIM['PowerSystemResource.DesignElement'], name="powerSystemResource__DesignElement", curie=CIM.curie('PowerSystemResource.DesignElement'),
                   model_uri=CIMTBL.powerSystemResource__DesignElement, domain=None, range=Optional[Union[dict, DesignElement]])

slots.powerSystemResource__Location = Slot(uri=CIM['PowerSystemResource.Location'], name="powerSystemResource__Location", curie=CIM.curie('PowerSystemResource.Location'),
                   model_uri=CIMTBL.powerSystemResource__Location, domain=None, range=Optional[Union[dict, Location]])

slots.powerSystemResource__OperatedByCompany = Slot(uri=CIM['PowerSystemResource.OperatedByCompany'], name="powerSystemResource__OperatedByCompany", curie=CIM.curie('PowerSystemResource.OperatedByCompany'),
                   model_uri=CIMTBL.powerSystemResource__OperatedByCompany, domain=None, range=Optional[Union[dict, Company]])

slots.powerSystemResource__PSRType = Slot(uri=CIM['PowerSystemResource.PSRType'], name="powerSystemResource__PSRType", curie=CIM.curie('PowerSystemResource.PSRType'),
                   model_uri=CIMTBL.powerSystemResource__PSRType, domain=None, range=Optional[Union[dict, PSRType]])

slots.powerSystemResource__ResourceContainer = Slot(uri=CIM['PowerSystemResource.ResourceContainer'], name="powerSystemResource__ResourceContainer", curie=CIM.curie('PowerSystemResource.ResourceContainer'),
                   model_uri=CIMTBL.powerSystemResource__ResourceContainer, domain=None, range=Optional[Union[dict, ResourceContainer]])

slots.powerTransformer__beforeShCircuitHighestOperatingCurrent = Slot(uri=CIM['PowerTransformer.beforeShCircuitHighestOperatingCurrent'], name="powerTransformer__beforeShCircuitHighestOperatingCurrent", curie=CIM.curie('PowerTransformer.beforeShCircuitHighestOperatingCurrent'),
                   model_uri=CIMTBL.powerTransformer__beforeShCircuitHighestOperatingCurrent, domain=None, range=Optional[float])

slots.powerTransformer__beforeShCircuitHighestOperatingVoltage = Slot(uri=CIM['PowerTransformer.beforeShCircuitHighestOperatingVoltage'], name="powerTransformer__beforeShCircuitHighestOperatingVoltage", curie=CIM.curie('PowerTransformer.beforeShCircuitHighestOperatingVoltage'),
                   model_uri=CIMTBL.powerTransformer__beforeShCircuitHighestOperatingVoltage, domain=None, range=Optional[float])

slots.powerTransformer__beforeShortCircuitAnglePf = Slot(uri=CIM['PowerTransformer.beforeShortCircuitAnglePf'], name="powerTransformer__beforeShortCircuitAnglePf", curie=CIM.curie('PowerTransformer.beforeShortCircuitAnglePf'),
                   model_uri=CIMTBL.powerTransformer__beforeShortCircuitAnglePf, domain=None, range=Optional[float])

slots.powerTransformer__highSideMinOperatingU = Slot(uri=CIM['PowerTransformer.highSideMinOperatingU'], name="powerTransformer__highSideMinOperatingU", curie=CIM.curie('PowerTransformer.highSideMinOperatingU'),
                   model_uri=CIMTBL.powerTransformer__highSideMinOperatingU, domain=None, range=Optional[float])

slots.powerTransformer__isPartOfGeneratorUnit = Slot(uri=CIM['PowerTransformer.isPartOfGeneratorUnit'], name="powerTransformer__isPartOfGeneratorUnit", curie=CIM.curie('PowerTransformer.isPartOfGeneratorUnit'),
                   model_uri=CIMTBL.powerTransformer__isPartOfGeneratorUnit, domain=None, range=Optional[Union[bool, Bool]])

slots.powerTransformer__operationalValuesConsidered = Slot(uri=CIM['PowerTransformer.operationalValuesConsidered'], name="powerTransformer__operationalValuesConsidered", curie=CIM.curie('PowerTransformer.operationalValuesConsidered'),
                   model_uri=CIMTBL.powerTransformer__operationalValuesConsidered, domain=None, range=Optional[Union[bool, Bool]])

slots.powerTransformer__vectorGroup = Slot(uri=CIM['PowerTransformer.vectorGroup'], name="powerTransformer__vectorGroup", curie=CIM.curie('PowerTransformer.vectorGroup'),
                   model_uri=CIMTBL.powerTransformer__vectorGroup, domain=None, range=Optional[str])

slots.powerTransformerEnd__b = Slot(uri=CIM['PowerTransformerEnd.b'], name="powerTransformerEnd__b", curie=CIM.curie('PowerTransformerEnd.b'),
                   model_uri=CIMTBL.powerTransformerEnd__b, domain=None, range=Optional[float])

slots.powerTransformerEnd__b0 = Slot(uri=CIM['PowerTransformerEnd.b0'], name="powerTransformerEnd__b0", curie=CIM.curie('PowerTransformerEnd.b0'),
                   model_uri=CIMTBL.powerTransformerEnd__b0, domain=None, range=Optional[float])

slots.powerTransformerEnd__connectionKind = Slot(uri=CIM['PowerTransformerEnd.connectionKind'], name="powerTransformerEnd__connectionKind", curie=CIM.curie('PowerTransformerEnd.connectionKind'),
                   model_uri=CIMTBL.powerTransformerEnd__connectionKind, domain=None, range=Optional[Union[str, "WindingConnection"]])

slots.powerTransformerEnd__g = Slot(uri=CIM['PowerTransformerEnd.g'], name="powerTransformerEnd__g", curie=CIM.curie('PowerTransformerEnd.g'),
                   model_uri=CIMTBL.powerTransformerEnd__g, domain=None, range=Optional[float])

slots.powerTransformerEnd__g0 = Slot(uri=CIM['PowerTransformerEnd.g0'], name="powerTransformerEnd__g0", curie=CIM.curie('PowerTransformerEnd.g0'),
                   model_uri=CIMTBL.powerTransformerEnd__g0, domain=None, range=Optional[float])

slots.powerTransformerEnd__phaseAngleClock = Slot(uri=CIM['PowerTransformerEnd.phaseAngleClock'], name="powerTransformerEnd__phaseAngleClock", curie=CIM.curie('PowerTransformerEnd.phaseAngleClock'),
                   model_uri=CIMTBL.powerTransformerEnd__phaseAngleClock, domain=None, range=Optional[int])

slots.powerTransformerEnd__r = Slot(uri=CIM['PowerTransformerEnd.r'], name="powerTransformerEnd__r", curie=CIM.curie('PowerTransformerEnd.r'),
                   model_uri=CIMTBL.powerTransformerEnd__r, domain=None, range=Optional[float])

slots.powerTransformerEnd__r0 = Slot(uri=CIM['PowerTransformerEnd.r0'], name="powerTransformerEnd__r0", curie=CIM.curie('PowerTransformerEnd.r0'),
                   model_uri=CIMTBL.powerTransformerEnd__r0, domain=None, range=Optional[float])

slots.powerTransformerEnd__ratedS = Slot(uri=CIM['PowerTransformerEnd.ratedS'], name="powerTransformerEnd__ratedS", curie=CIM.curie('PowerTransformerEnd.ratedS'),
                   model_uri=CIMTBL.powerTransformerEnd__ratedS, domain=None, range=Optional[float])

slots.powerTransformerEnd__ratedU = Slot(uri=CIM['PowerTransformerEnd.ratedU'], name="powerTransformerEnd__ratedU", curie=CIM.curie('PowerTransformerEnd.ratedU'),
                   model_uri=CIMTBL.powerTransformerEnd__ratedU, domain=None, range=Optional[float])

slots.powerTransformerEnd__x = Slot(uri=CIM['PowerTransformerEnd.x'], name="powerTransformerEnd__x", curie=CIM.curie('PowerTransformerEnd.x'),
                   model_uri=CIMTBL.powerTransformerEnd__x, domain=None, range=Optional[float])

slots.powerTransformerEnd__x0 = Slot(uri=CIM['PowerTransformerEnd.x0'], name="powerTransformerEnd__x0", curie=CIM.curie('PowerTransformerEnd.x0'),
                   model_uri=CIMTBL.powerTransformerEnd__x0, domain=None, range=Optional[float])

slots.powerTransformerEnd__PowerTransformer = Slot(uri=CIM['PowerTransformerEnd.PowerTransformer'], name="powerTransformerEnd__PowerTransformer", curie=CIM.curie('PowerTransformerEnd.PowerTransformer'),
                   model_uri=CIMTBL.powerTransformerEnd__PowerTransformer, domain=None, range=Optional[Union[dict, PowerTransformer]])

slots.protectedSwitch__breakingCapacity = Slot(uri=CIM['ProtectedSwitch.breakingCapacity'], name="protectedSwitch__breakingCapacity", curie=CIM.curie('ProtectedSwitch.breakingCapacity'),
                   model_uri=CIMTBL.protectedSwitch__breakingCapacity, domain=None, range=Optional[float])

slots.protectedSwitch__makingCapacity = Slot(uri=CIM['ProtectedSwitch.makingCapacity'], name="protectedSwitch__makingCapacity", curie=CIM.curie('ProtectedSwitch.makingCapacity'),
                   model_uri=CIMTBL.protectedSwitch__makingCapacity, domain=None, range=Optional[float])

slots.ratioTapChanger__stepVoltageIncrement = Slot(uri=CIM['RatioTapChanger.stepVoltageIncrement'], name="ratioTapChanger__stepVoltageIncrement", curie=CIM.curie('RatioTapChanger.stepVoltageIncrement'),
                   model_uri=CIMTBL.ratioTapChanger__stepVoltageIncrement, domain=None, range=Optional[float])

slots.ratioTapChanger__RatioTapChangerTable = Slot(uri=CIM['RatioTapChanger.RatioTapChangerTable'], name="ratioTapChanger__RatioTapChangerTable", curie=CIM.curie('RatioTapChanger.RatioTapChangerTable'),
                   model_uri=CIMTBL.ratioTapChanger__RatioTapChangerTable, domain=None, range=Optional[Union[dict, RatioTapChangerTable]])

slots.ratioTapChanger__TransformerEnd = Slot(uri=CIM['RatioTapChanger.TransformerEnd'], name="ratioTapChanger__TransformerEnd", curie=CIM.curie('RatioTapChanger.TransformerEnd'),
                   model_uri=CIMTBL.ratioTapChanger__TransformerEnd, domain=None, range=Optional[Union[dict, TransformerEnd]])

slots.ratioTapChangerTablePoint__RatioTapChangerTable = Slot(uri=CIM['RatioTapChangerTablePoint.RatioTapChangerTable'], name="ratioTapChangerTablePoint__RatioTapChangerTable", curie=CIM.curie('RatioTapChangerTablePoint.RatioTapChangerTable'),
                   model_uri=CIMTBL.ratioTapChangerTablePoint__RatioTapChangerTable, domain=None, range=Optional[Union[dict, RatioTapChangerTable]])

slots.reactiveCapabilityCurve__coolantTemperature = Slot(uri=CIM['ReactiveCapabilityCurve.coolantTemperature'], name="reactiveCapabilityCurve__coolantTemperature", curie=CIM.curie('ReactiveCapabilityCurve.coolantTemperature'),
                   model_uri=CIMTBL.reactiveCapabilityCurve__coolantTemperature, domain=None, range=Optional[float])

slots.reactiveCapabilityCurve__hydrogenPressure = Slot(uri=CIM['ReactiveCapabilityCurve.hydrogenPressure'], name="reactiveCapabilityCurve__hydrogenPressure", curie=CIM.curie('ReactiveCapabilityCurve.hydrogenPressure'),
                   model_uri=CIMTBL.reactiveCapabilityCurve__hydrogenPressure, domain=None, range=Optional[float])

slots.reactiveCapabilityCurve__referenceVoltage = Slot(uri=CIM['ReactiveCapabilityCurve.referenceVoltage'], name="reactiveCapabilityCurve__referenceVoltage", curie=CIM.curie('ReactiveCapabilityCurve.referenceVoltage'),
                   model_uri=CIMTBL.reactiveCapabilityCurve__referenceVoltage, domain=None, range=Optional[float])

slots.reactiveCapabilityCurve__ExtendedWardEquivalent = Slot(uri=CIM['ReactiveCapabilityCurve.ExtendedWardEquivalent'], name="reactiveCapabilityCurve__ExtendedWardEquivalent", curie=CIM.curie('ReactiveCapabilityCurve.ExtendedWardEquivalent'),
                   model_uri=CIMTBL.reactiveCapabilityCurve__ExtendedWardEquivalent, domain=None, range=Optional[Union[dict, ExtendedWardEquivalent]])

slots.reactiveCapabilityCurve__SynchronousMachine = Slot(uri=CIM['ReactiveCapabilityCurve.SynchronousMachine'], name="reactiveCapabilityCurve__SynchronousMachine", curie=CIM.curie('ReactiveCapabilityCurve.SynchronousMachine'),
                   model_uri=CIMTBL.reactiveCapabilityCurve__SynchronousMachine, domain=None, range=Optional[Union[dict, SynchronousMachine]])

slots.regularIntervalSchedule__endTime = Slot(uri=CIM['RegularIntervalSchedule.endTime'], name="regularIntervalSchedule__endTime", curie=CIM.curie('RegularIntervalSchedule.endTime'),
                   model_uri=CIMTBL.regularIntervalSchedule__endTime, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.regularIntervalSchedule__timeStep = Slot(uri=CIM['RegularIntervalSchedule.timeStep'], name="regularIntervalSchedule__timeStep", curie=CIM.curie('RegularIntervalSchedule.timeStep'),
                   model_uri=CIMTBL.regularIntervalSchedule__timeStep, domain=None, range=Optional[float])

slots.regularTimePoint__sequenceNumber = Slot(uri=CIM['RegularTimePoint.sequenceNumber'], name="regularTimePoint__sequenceNumber", curie=CIM.curie('RegularTimePoint.sequenceNumber'),
                   model_uri=CIMTBL.regularTimePoint__sequenceNumber, domain=None, range=Optional[int])

slots.regularTimePoint__value1 = Slot(uri=CIM['RegularTimePoint.value1'], name="regularTimePoint__value1", curie=CIM.curie('RegularTimePoint.value1'),
                   model_uri=CIMTBL.regularTimePoint__value1, domain=None, range=Optional[float])

slots.regularTimePoint__value2 = Slot(uri=CIM['RegularTimePoint.value2'], name="regularTimePoint__value2", curie=CIM.curie('RegularTimePoint.value2'),
                   model_uri=CIMTBL.regularTimePoint__value2, domain=None, range=Optional[float])

slots.regularTimePoint__value3 = Slot(uri=CIM['RegularTimePoint.value3'], name="regularTimePoint__value3", curie=CIM.curie('RegularTimePoint.value3'),
                   model_uri=CIMTBL.regularTimePoint__value3, domain=None, range=Optional[float])

slots.regularTimePoint__IntervalSchedule = Slot(uri=CIM['RegularTimePoint.IntervalSchedule'], name="regularTimePoint__IntervalSchedule", curie=CIM.curie('RegularTimePoint.IntervalSchedule'),
                   model_uri=CIMTBL.regularTimePoint__IntervalSchedule, domain=None, range=Optional[Union[dict, RegularIntervalSchedule]])

slots.regulatingCondEq__controlEnabled = Slot(uri=CIM['RegulatingCondEq.controlEnabled'], name="regulatingCondEq__controlEnabled", curie=CIM.curie('RegulatingCondEq.controlEnabled'),
                   model_uri=CIMTBL.regulatingCondEq__controlEnabled, domain=None, range=Optional[Union[bool, Bool]])

slots.regulatingCondEq__EquipmentController = Slot(uri=CIM['RegulatingCondEq.EquipmentController'], name="regulatingCondEq__EquipmentController", curie=CIM.curie('RegulatingCondEq.EquipmentController'),
                   model_uri=CIMTBL.regulatingCondEq__EquipmentController, domain=None, range=Optional[Union[dict, EquipmentController]])

slots.regulatingCondEq__RegulatingControl = Slot(uri=CIM['RegulatingCondEq.RegulatingControl'], name="regulatingCondEq__RegulatingControl", curie=CIM.curie('RegulatingCondEq.RegulatingControl'),
                   model_uri=CIMTBL.regulatingCondEq__RegulatingControl, domain=None, range=Optional[Union[dict, RegulatingControl]])

slots.regulatingControl__ctRatio = Slot(uri=CIM['RegulatingControl.ctRatio'], name="regulatingControl__ctRatio", curie=CIM.curie('RegulatingControl.ctRatio'),
                   model_uri=CIMTBL.regulatingControl__ctRatio, domain=None, range=Optional[float])

slots.regulatingControl__discrete = Slot(uri=CIM['RegulatingControl.discrete'], name="regulatingControl__discrete", curie=CIM.curie('RegulatingControl.discrete'),
                   model_uri=CIMTBL.regulatingControl__discrete, domain=None, range=Optional[Union[bool, Bool]])

slots.regulatingControl__enabled = Slot(uri=CIM['RegulatingControl.enabled'], name="regulatingControl__enabled", curie=CIM.curie('RegulatingControl.enabled'),
                   model_uri=CIMTBL.regulatingControl__enabled, domain=None, range=Optional[Union[bool, Bool]])

slots.regulatingControl__maxAllowedTargetValue = Slot(uri=CIM['RegulatingControl.maxAllowedTargetValue'], name="regulatingControl__maxAllowedTargetValue", curie=CIM.curie('RegulatingControl.maxAllowedTargetValue'),
                   model_uri=CIMTBL.regulatingControl__maxAllowedTargetValue, domain=None, range=Optional[float])

slots.regulatingControl__minAllowedTargetValue = Slot(uri=CIM['RegulatingControl.minAllowedTargetValue'], name="regulatingControl__minAllowedTargetValue", curie=CIM.curie('RegulatingControl.minAllowedTargetValue'),
                   model_uri=CIMTBL.regulatingControl__minAllowedTargetValue, domain=None, range=Optional[float])

slots.regulatingControl__mode = Slot(uri=CIM['RegulatingControl.mode'], name="regulatingControl__mode", curie=CIM.curie('RegulatingControl.mode'),
                   model_uri=CIMTBL.regulatingControl__mode, domain=None, range=Optional[Union[str, "RegulatingControlModeKind"]])

slots.regulatingControl__monitoredPhase = Slot(uri=CIM['RegulatingControl.monitoredPhase'], name="regulatingControl__monitoredPhase", curie=CIM.curie('RegulatingControl.monitoredPhase'),
                   model_uri=CIMTBL.regulatingControl__monitoredPhase, domain=None, range=Optional[Union[str, "PhaseCode"]])

slots.regulatingControl__ptRatio = Slot(uri=CIM['RegulatingControl.ptRatio'], name="regulatingControl__ptRatio", curie=CIM.curie('RegulatingControl.ptRatio'),
                   model_uri=CIMTBL.regulatingControl__ptRatio, domain=None, range=Optional[float])

slots.regulatingControl__reverseTargetDeadband = Slot(uri=CIM['RegulatingControl.reverseTargetDeadband'], name="regulatingControl__reverseTargetDeadband", curie=CIM.curie('RegulatingControl.reverseTargetDeadband'),
                   model_uri=CIMTBL.regulatingControl__reverseTargetDeadband, domain=None, range=Optional[float])

slots.regulatingControl__reverseTargetValue = Slot(uri=CIM['RegulatingControl.reverseTargetValue'], name="regulatingControl__reverseTargetValue", curie=CIM.curie('RegulatingControl.reverseTargetValue'),
                   model_uri=CIMTBL.regulatingControl__reverseTargetValue, domain=None, range=Optional[float])

slots.regulatingControl__targetDeadband = Slot(uri=CIM['RegulatingControl.targetDeadband'], name="regulatingControl__targetDeadband", curie=CIM.curie('RegulatingControl.targetDeadband'),
                   model_uri=CIMTBL.regulatingControl__targetDeadband, domain=None, range=Optional[float])

slots.regulatingControl__targetValue = Slot(uri=CIM['RegulatingControl.targetValue'], name="regulatingControl__targetValue", curie=CIM.curie('RegulatingControl.targetValue'),
                   model_uri=CIMTBL.regulatingControl__targetValue, domain=None, range=Optional[float])

slots.regulatingControl__targetValueUnitMultiplier = Slot(uri=CIM['RegulatingControl.targetValueUnitMultiplier'], name="regulatingControl__targetValueUnitMultiplier", curie=CIM.curie('RegulatingControl.targetValueUnitMultiplier'),
                   model_uri=CIMTBL.regulatingControl__targetValueUnitMultiplier, domain=None, range=Optional[Union[str, "UnitMultiplier"]])

slots.regulatingControl__Terminal = Slot(uri=CIM['RegulatingControl.Terminal'], name="regulatingControl__Terminal", curie=CIM.curie('RegulatingControl.Terminal'),
                   model_uri=CIMTBL.regulatingControl__Terminal, domain=None, range=Optional[Union[dict, Terminal]])

slots.regulationSchedule__RegulatingControl = Slot(uri=CIM['RegulationSchedule.RegulatingControl'], name="regulationSchedule__RegulatingControl", curie=CIM.curie('RegulationSchedule.RegulatingControl'),
                   model_uri=CIMTBL.regulationSchedule__RegulatingControl, domain=None, range=Optional[Union[dict, RegulatingControl]])

slots.rotatingMachine__p = Slot(uri=CIM['RotatingMachine.p'], name="rotatingMachine__p", curie=CIM.curie('RotatingMachine.p'),
                   model_uri=CIMTBL.rotatingMachine__p, domain=None, range=Optional[float])

slots.rotatingMachine__q = Slot(uri=CIM['RotatingMachine.q'], name="rotatingMachine__q", curie=CIM.curie('RotatingMachine.q'),
                   model_uri=CIMTBL.rotatingMachine__q, domain=None, range=Optional[float])

slots.rotatingMachine__ratedPowerFactor = Slot(uri=CIM['RotatingMachine.ratedPowerFactor'], name="rotatingMachine__ratedPowerFactor", curie=CIM.curie('RotatingMachine.ratedPowerFactor'),
                   model_uri=CIMTBL.rotatingMachine__ratedPowerFactor, domain=None, range=Optional[float])

slots.rotatingMachine__ratedS = Slot(uri=CIM['RotatingMachine.ratedS'], name="rotatingMachine__ratedS", curie=CIM.curie('RotatingMachine.ratedS'),
                   model_uri=CIMTBL.rotatingMachine__ratedS, domain=None, range=Optional[float])

slots.rotatingMachine__ratedU = Slot(uri=CIM['RotatingMachine.ratedU'], name="rotatingMachine__ratedU", curie=CIM.curie('RotatingMachine.ratedU'),
                   model_uri=CIMTBL.rotatingMachine__ratedU, domain=None, range=Optional[float])

slots.rotatingMachine__GeneratingUnit = Slot(uri=CIM['RotatingMachine.GeneratingUnit'], name="rotatingMachine__GeneratingUnit", curie=CIM.curie('RotatingMachine.GeneratingUnit'),
                   model_uri=CIMTBL.rotatingMachine__GeneratingUnit, domain=None, range=Optional[Union[dict, GeneratingUnit]])

slots.rotatingMachine__HydroPump = Slot(uri=CIM['RotatingMachine.HydroPump'], name="rotatingMachine__HydroPump", curie=CIM.curie('RotatingMachine.HydroPump'),
                   model_uri=CIMTBL.rotatingMachine__HydroPump, domain=None, range=Optional[Union[dict, HydroPump]])

slots.rotatingMachine__RotatingMachinePhase = Slot(uri=CIM['RotatingMachine.RotatingMachinePhase'], name="rotatingMachine__RotatingMachinePhase", curie=CIM.curie('RotatingMachine.RotatingMachinePhase'),
                   model_uri=CIMTBL.rotatingMachine__RotatingMachinePhase, domain=None, range=Optional[Union[dict, RotatingMachinePhase]])

slots.sSSCController__maxInjectionU = Slot(uri=CIM['SSSCController.maxInjectionU'], name="sSSCController__maxInjectionU", curie=CIM.curie('SSSCController.maxInjectionU'),
                   model_uri=CIMTBL.sSSCController__maxInjectionU, domain=None, range=Optional[float])

slots.sSSCController__maxLimitI = Slot(uri=CIM['SSSCController.maxLimitI'], name="sSSCController__maxLimitI", curie=CIM.curie('SSSCController.maxLimitI'),
                   model_uri=CIMTBL.sSSCController__maxLimitI, domain=None, range=Optional[float])

slots.sSSCController__minInjectionU = Slot(uri=CIM['SSSCController.minInjectionU'], name="sSSCController__minInjectionU", curie=CIM.curie('SSSCController.minInjectionU'),
                   model_uri=CIMTBL.sSSCController__minInjectionU, domain=None, range=Optional[float])

slots.sSSCController__minLimitI = Slot(uri=CIM['SSSCController.minLimitI'], name="sSSCController__minLimitI", curie=CIM.curie('SSSCController.minLimitI'),
                   model_uri=CIMTBL.sSSCController__minLimitI, domain=None, range=Optional[float])

slots.sSSCController__mode = Slot(uri=CIM['SSSCController.mode'], name="sSSCController__mode", curie=CIM.curie('SSSCController.mode'),
                   model_uri=CIMTBL.sSSCController__mode, domain=None, range=Optional[Union[str, "SSSCControlModeKind"]])

slots.sSSCController__CurrentDroopOverride = Slot(uri=CIM['SSSCController.CurrentDroopOverride'], name="sSSCController__CurrentDroopOverride", curie=CIM.curie('SSSCController.CurrentDroopOverride'),
                   model_uri=CIMTBL.sSSCController__CurrentDroopOverride, domain=None, range=Optional[Union[dict, CurrentDroopOverride]])

slots.sSSCController__SSSCSimulationSettings = Slot(uri=CIM['SSSCController.SSSCSimulationSettings'], name="sSSCController__SSSCSimulationSettings", curie=CIM.curie('SSSCController.SSSCSimulationSettings'),
                   model_uri=CIMTBL.sSSCController__SSSCSimulationSettings, domain=None, range=Optional[Union[dict, SSSCSimulationSettings]])

slots.sSSCSimulationSettings__mRID = Slot(uri=CIM['SSSCSimulationSettings.mRID'], name="sSSCSimulationSettings__mRID", curie=CIM.curie('SSSCSimulationSettings.mRID'),
                   model_uri=CIMTBL.sSSCSimulationSettings__mRID, domain=None, range=Optional[str])

slots.sSSCSimulationSettings__deltaX = Slot(uri=CIM['SSSCSimulationSettings.deltaX'], name="sSSCSimulationSettings__deltaX", curie=CIM.curie('SSSCSimulationSettings.deltaX'),
                   model_uri=CIMTBL.sSSCSimulationSettings__deltaX, domain=None, range=Optional[float])

slots.sSSCSimulationSettings__isEstimateDLDVSensitive = Slot(uri=CIM['SSSCSimulationSettings.isEstimateDLDVSensitive'], name="sSSCSimulationSettings__isEstimateDLDVSensitive", curie=CIM.curie('SSSCSimulationSettings.isEstimateDLDVSensitive'),
                   model_uri=CIMTBL.sSSCSimulationSettings__isEstimateDLDVSensitive, domain=None, range=Optional[Union[bool, Bool]])

slots.sSSCSimulationSettings__maxCorrectionX = Slot(uri=CIM['SSSCSimulationSettings.maxCorrectionX'], name="sSSCSimulationSettings__maxCorrectionX", curie=CIM.curie('SSSCSimulationSettings.maxCorrectionX'),
                   model_uri=CIMTBL.sSSCSimulationSettings__maxCorrectionX, domain=None, range=Optional[float])

slots.sSSCSimulationSettings__maxIterations = Slot(uri=CIM['SSSCSimulationSettings.maxIterations'], name="sSSCSimulationSettings__maxIterations", curie=CIM.curie('SSSCSimulationSettings.maxIterations'),
                   model_uri=CIMTBL.sSSCSimulationSettings__maxIterations, domain=None, range=Optional[int])

slots.sSSCSimulationSettings__maxMismatch = Slot(uri=CIM['SSSCSimulationSettings.maxMismatch'], name="sSSCSimulationSettings__maxMismatch", curie=CIM.curie('SSSCSimulationSettings.maxMismatch'),
                   model_uri=CIMTBL.sSSCSimulationSettings__maxMismatch, domain=None, range=Optional[float])

slots.season__endDate = Slot(uri=CIM['Season.endDate'], name="season__endDate", curie=CIM.curie('Season.endDate'),
                   model_uri=CIMTBL.season__endDate, domain=None, range=Optional[str])

slots.season__startDate = Slot(uri=CIM['Season.startDate'], name="season__startDate", curie=CIM.curie('Season.startDate'),
                   model_uri=CIMTBL.season__startDate, domain=None, range=Optional[str])

slots.seasonDayTypeSchedule__DayType = Slot(uri=CIM['SeasonDayTypeSchedule.DayType'], name="seasonDayTypeSchedule__DayType", curie=CIM.curie('SeasonDayTypeSchedule.DayType'),
                   model_uri=CIMTBL.seasonDayTypeSchedule__DayType, domain=None, range=Optional[Union[dict, DayType]])

slots.seasonDayTypeSchedule__Season = Slot(uri=CIM['SeasonDayTypeSchedule.Season'], name="seasonDayTypeSchedule__Season", curie=CIM.curie('SeasonDayTypeSchedule.Season'),
                   model_uri=CIMTBL.seasonDayTypeSchedule__Season, domain=None, range=Optional[Union[dict, Season]])

slots.seriesCompensator__r = Slot(uri=CIM['SeriesCompensator.r'], name="seriesCompensator__r", curie=CIM.curie('SeriesCompensator.r'),
                   model_uri=CIMTBL.seriesCompensator__r, domain=None, range=Optional[float])

slots.seriesCompensator__r0 = Slot(uri=CIM['SeriesCompensator.r0'], name="seriesCompensator__r0", curie=CIM.curie('SeriesCompensator.r0'),
                   model_uri=CIMTBL.seriesCompensator__r0, domain=None, range=Optional[float])

slots.seriesCompensator__varistorPresent = Slot(uri=CIM['SeriesCompensator.varistorPresent'], name="seriesCompensator__varistorPresent", curie=CIM.curie('SeriesCompensator.varistorPresent'),
                   model_uri=CIMTBL.seriesCompensator__varistorPresent, domain=None, range=Optional[Union[bool, Bool]])

slots.seriesCompensator__varistorRatedCurrent = Slot(uri=CIM['SeriesCompensator.varistorRatedCurrent'], name="seriesCompensator__varistorRatedCurrent", curie=CIM.curie('SeriesCompensator.varistorRatedCurrent'),
                   model_uri=CIMTBL.seriesCompensator__varistorRatedCurrent, domain=None, range=Optional[float])

slots.seriesCompensator__varistorVoltageThreshold = Slot(uri=CIM['SeriesCompensator.varistorVoltageThreshold'], name="seriesCompensator__varistorVoltageThreshold", curie=CIM.curie('SeriesCompensator.varistorVoltageThreshold'),
                   model_uri=CIMTBL.seriesCompensator__varistorVoltageThreshold, domain=None, range=Optional[float])

slots.seriesCompensator__x = Slot(uri=CIM['SeriesCompensator.x'], name="seriesCompensator__x", curie=CIM.curie('SeriesCompensator.x'),
                   model_uri=CIMTBL.seriesCompensator__x, domain=None, range=Optional[float])

slots.seriesCompensator__x0 = Slot(uri=CIM['SeriesCompensator.x0'], name="seriesCompensator__x0", curie=CIM.curie('SeriesCompensator.x0'),
                   model_uri=CIMTBL.seriesCompensator__x0, domain=None, range=Optional[float])

slots.shortCircuitTest__current = Slot(uri=CIM['ShortCircuitTest.current'], name="shortCircuitTest__current", curie=CIM.curie('ShortCircuitTest.current'),
                   model_uri=CIMTBL.shortCircuitTest__current, domain=None, range=Optional[float])

slots.shortCircuitTest__energisedEndStep = Slot(uri=CIM['ShortCircuitTest.energisedEndStep'], name="shortCircuitTest__energisedEndStep", curie=CIM.curie('ShortCircuitTest.energisedEndStep'),
                   model_uri=CIMTBL.shortCircuitTest__energisedEndStep, domain=None, range=Optional[int])

slots.shortCircuitTest__groundedEndStep = Slot(uri=CIM['ShortCircuitTest.groundedEndStep'], name="shortCircuitTest__groundedEndStep", curie=CIM.curie('ShortCircuitTest.groundedEndStep'),
                   model_uri=CIMTBL.shortCircuitTest__groundedEndStep, domain=None, range=Optional[int])

slots.shortCircuitTest__leakageImpedance = Slot(uri=CIM['ShortCircuitTest.leakageImpedance'], name="shortCircuitTest__leakageImpedance", curie=CIM.curie('ShortCircuitTest.leakageImpedance'),
                   model_uri=CIMTBL.shortCircuitTest__leakageImpedance, domain=None, range=Optional[float])

slots.shortCircuitTest__leakageImpedanceZero = Slot(uri=CIM['ShortCircuitTest.leakageImpedanceZero'], name="shortCircuitTest__leakageImpedanceZero", curie=CIM.curie('ShortCircuitTest.leakageImpedanceZero'),
                   model_uri=CIMTBL.shortCircuitTest__leakageImpedanceZero, domain=None, range=Optional[float])

slots.shortCircuitTest__loss = Slot(uri=CIM['ShortCircuitTest.loss'], name="shortCircuitTest__loss", curie=CIM.curie('ShortCircuitTest.loss'),
                   model_uri=CIMTBL.shortCircuitTest__loss, domain=None, range=Optional[float])

slots.shortCircuitTest__lossZero = Slot(uri=CIM['ShortCircuitTest.lossZero'], name="shortCircuitTest__lossZero", curie=CIM.curie('ShortCircuitTest.lossZero'),
                   model_uri=CIMTBL.shortCircuitTest__lossZero, domain=None, range=Optional[float])

slots.shortCircuitTest__power = Slot(uri=CIM['ShortCircuitTest.power'], name="shortCircuitTest__power", curie=CIM.curie('ShortCircuitTest.power'),
                   model_uri=CIMTBL.shortCircuitTest__power, domain=None, range=Optional[float])

slots.shortCircuitTest__voltage = Slot(uri=CIM['ShortCircuitTest.voltage'], name="shortCircuitTest__voltage", curie=CIM.curie('ShortCircuitTest.voltage'),
                   model_uri=CIMTBL.shortCircuitTest__voltage, domain=None, range=Optional[float])

slots.shortCircuitTest__EnergisedEnd = Slot(uri=CIM['ShortCircuitTest.EnergisedEnd'], name="shortCircuitTest__EnergisedEnd", curie=CIM.curie('ShortCircuitTest.EnergisedEnd'),
                   model_uri=CIMTBL.shortCircuitTest__EnergisedEnd, domain=None, range=Optional[Union[dict, TransformerEndInfo]])

slots.shortCircuitTest__GroundedEnds = Slot(uri=CIM['ShortCircuitTest.GroundedEnds'], name="shortCircuitTest__GroundedEnds", curie=CIM.curie('ShortCircuitTest.GroundedEnds'),
                   model_uri=CIMTBL.shortCircuitTest__GroundedEnds, domain=None, range=Optional[Union[Union[dict, TransformerEndInfo], list[Union[dict, TransformerEndInfo]]]])

slots.shuntCompensator__aVRDelay = Slot(uri=CIM['ShuntCompensator.aVRDelay'], name="shuntCompensator__aVRDelay", curie=CIM.curie('ShuntCompensator.aVRDelay'),
                   model_uri=CIMTBL.shuntCompensator__aVRDelay, domain=None, range=Optional[float])

slots.shuntCompensator__grounded = Slot(uri=CIM['ShuntCompensator.grounded'], name="shuntCompensator__grounded", curie=CIM.curie('ShuntCompensator.grounded'),
                   model_uri=CIMTBL.shuntCompensator__grounded, domain=None, range=Optional[Union[bool, Bool]])

slots.shuntCompensator__maximumSections = Slot(uri=CIM['ShuntCompensator.maximumSections'], name="shuntCompensator__maximumSections", curie=CIM.curie('ShuntCompensator.maximumSections'),
                   model_uri=CIMTBL.shuntCompensator__maximumSections, domain=None, range=Optional[int])

slots.shuntCompensator__nomU = Slot(uri=CIM['ShuntCompensator.nomU'], name="shuntCompensator__nomU", curie=CIM.curie('ShuntCompensator.nomU'),
                   model_uri=CIMTBL.shuntCompensator__nomU, domain=None, range=Optional[float])

slots.shuntCompensator__normalSections = Slot(uri=CIM['ShuntCompensator.normalSections'], name="shuntCompensator__normalSections", curie=CIM.curie('ShuntCompensator.normalSections'),
                   model_uri=CIMTBL.shuntCompensator__normalSections, domain=None, range=Optional[int])

slots.shuntCompensator__phaseConnection = Slot(uri=CIM['ShuntCompensator.phaseConnection'], name="shuntCompensator__phaseConnection", curie=CIM.curie('ShuntCompensator.phaseConnection'),
                   model_uri=CIMTBL.shuntCompensator__phaseConnection, domain=None, range=Optional[Union[str, "PhaseShuntConnectionKind"]])

slots.shuntCompensator__sections = Slot(uri=CIM['ShuntCompensator.sections'], name="shuntCompensator__sections", curie=CIM.curie('ShuntCompensator.sections'),
                   model_uri=CIMTBL.shuntCompensator__sections, domain=None, range=Optional[float])

slots.shuntCompensator__voltageSensitivity = Slot(uri=CIM['ShuntCompensator.voltageSensitivity'], name="shuntCompensator__voltageSensitivity", curie=CIM.curie('ShuntCompensator.voltageSensitivity'),
                   model_uri=CIMTBL.shuntCompensator__voltageSensitivity, domain=None, range=Optional[float])

slots.shuntCompensator__ShuntCompensatorAction = Slot(uri=CIM['ShuntCompensator.ShuntCompensatorAction'], name="shuntCompensator__ShuntCompensatorAction", curie=CIM.curie('ShuntCompensator.ShuntCompensatorAction'),
                   model_uri=CIMTBL.shuntCompensator__ShuntCompensatorAction, domain=None, range=Optional[Union[dict, ShuntCompensatorAction]])

slots.shuntCompensator__ShuntCompensatorDynamics = Slot(uri=CIM['ShuntCompensator.ShuntCompensatorDynamics'], name="shuntCompensator__ShuntCompensatorDynamics", curie=CIM.curie('ShuntCompensator.ShuntCompensatorDynamics'),
                   model_uri=CIMTBL.shuntCompensator__ShuntCompensatorDynamics, domain=None, range=Optional[Union[dict, ShuntCompensatorDynamics]])

slots.shuntCompensator__StaticVarCompensatorSystemDynamics = Slot(uri=CIM['ShuntCompensator.StaticVarCompensatorSystemDynamics'], name="shuntCompensator__StaticVarCompensatorSystemDynamics", curie=CIM.curie('ShuntCompensator.StaticVarCompensatorSystemDynamics'),
                   model_uri=CIMTBL.shuntCompensator__StaticVarCompensatorSystemDynamics, domain=None, range=Optional[Union[dict, StaticVarCompensatorSystemDynamics]])

slots.shuntCompensatorPhase__maximumSections = Slot(uri=CIM['ShuntCompensatorPhase.maximumSections'], name="shuntCompensatorPhase__maximumSections", curie=CIM.curie('ShuntCompensatorPhase.maximumSections'),
                   model_uri=CIMTBL.shuntCompensatorPhase__maximumSections, domain=None, range=Optional[int])

slots.shuntCompensatorPhase__normalSections = Slot(uri=CIM['ShuntCompensatorPhase.normalSections'], name="shuntCompensatorPhase__normalSections", curie=CIM.curie('ShuntCompensatorPhase.normalSections'),
                   model_uri=CIMTBL.shuntCompensatorPhase__normalSections, domain=None, range=Optional[int])

slots.shuntCompensatorPhase__phase = Slot(uri=CIM['ShuntCompensatorPhase.phase'], name="shuntCompensatorPhase__phase", curie=CIM.curie('ShuntCompensatorPhase.phase'),
                   model_uri=CIMTBL.shuntCompensatorPhase__phase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.shuntCompensatorPhase__sections = Slot(uri=CIM['ShuntCompensatorPhase.sections'], name="shuntCompensatorPhase__sections", curie=CIM.curie('ShuntCompensatorPhase.sections'),
                   model_uri=CIMTBL.shuntCompensatorPhase__sections, domain=None, range=Optional[float])

slots.shuntCompensatorPhase__ShuntCompensator = Slot(uri=CIM['ShuntCompensatorPhase.ShuntCompensator'], name="shuntCompensatorPhase__ShuntCompensator", curie=CIM.curie('ShuntCompensatorPhase.ShuntCompensator'),
                   model_uri=CIMTBL.shuntCompensatorPhase__ShuntCompensator, domain=None, range=Optional[Union[dict, ShuntCompensator]])

slots.solarGeneratingUnit__SolarPowerPlant = Slot(uri=CIM['SolarGeneratingUnit.SolarPowerPlant'], name="solarGeneratingUnit__SolarPowerPlant", curie=CIM.curie('SolarGeneratingUnit.SolarPowerPlant'),
                   model_uri=CIMTBL.solarGeneratingUnit__SolarPowerPlant, domain=None, range=Optional[Union[dict, SolarPowerPlant]])

slots.staticVarCompensator__capacitiveRating = Slot(uri=CIM['StaticVarCompensator.capacitiveRating'], name="staticVarCompensator__capacitiveRating", curie=CIM.curie('StaticVarCompensator.capacitiveRating'),
                   model_uri=CIMTBL.staticVarCompensator__capacitiveRating, domain=None, range=Optional[float])

slots.staticVarCompensator__inductiveRating = Slot(uri=CIM['StaticVarCompensator.inductiveRating'], name="staticVarCompensator__inductiveRating", curie=CIM.curie('StaticVarCompensator.inductiveRating'),
                   model_uri=CIMTBL.staticVarCompensator__inductiveRating, domain=None, range=Optional[float])

slots.staticVarCompensator__q = Slot(uri=CIM['StaticVarCompensator.q'], name="staticVarCompensator__q", curie=CIM.curie('StaticVarCompensator.q'),
                   model_uri=CIMTBL.staticVarCompensator__q, domain=None, range=Optional[float])

slots.staticVarCompensator__slope = Slot(uri=CIM['StaticVarCompensator.slope'], name="staticVarCompensator__slope", curie=CIM.curie('StaticVarCompensator.slope'),
                   model_uri=CIMTBL.staticVarCompensator__slope, domain=None, range=Optional[float])

slots.staticVarCompensator__sVCControlMode = Slot(uri=CIM['StaticVarCompensator.sVCControlMode'], name="staticVarCompensator__sVCControlMode", curie=CIM.curie('StaticVarCompensator.sVCControlMode'),
                   model_uri=CIMTBL.staticVarCompensator__sVCControlMode, domain=None, range=Optional[Union[str, "SVCControlMode"]])

slots.staticVarCompensator__voltageSetPoint = Slot(uri=CIM['StaticVarCompensator.voltageSetPoint'], name="staticVarCompensator__voltageSetPoint", curie=CIM.curie('StaticVarCompensator.voltageSetPoint'),
                   model_uri=CIMTBL.staticVarCompensator__voltageSetPoint, domain=None, range=Optional[float])

slots.staticVarCompensator__StaticVarCompensatorDynamics = Slot(uri=CIM['StaticVarCompensator.StaticVarCompensatorDynamics'], name="staticVarCompensator__StaticVarCompensatorDynamics", curie=CIM.curie('StaticVarCompensator.StaticVarCompensatorDynamics'),
                   model_uri=CIMTBL.staticVarCompensator__StaticVarCompensatorDynamics, domain=None, range=Optional[Union[dict, StaticVarCompensatorDynamics]])

slots.stepLimitTablePoint__factor = Slot(uri=CIM['StepLimitTablePoint.factor'], name="stepLimitTablePoint__factor", curie=CIM.curie('StepLimitTablePoint.factor'),
                   model_uri=CIMTBL.stepLimitTablePoint__factor, domain=None, range=Optional[float])

slots.stepLimitTablePoint__step = Slot(uri=CIM['StepLimitTablePoint.step'], name="stepLimitTablePoint__step", curie=CIM.curie('StepLimitTablePoint.step'),
                   model_uri=CIMTBL.stepLimitTablePoint__step, domain=None, range=Optional[int])

slots.stepLimitTablePoint__StepOperationalLimitTable = Slot(uri=CIM['StepLimitTablePoint.StepOperationalLimitTable'], name="stepLimitTablePoint__StepOperationalLimitTable", curie=CIM.curie('StepLimitTablePoint.StepOperationalLimitTable'),
                   model_uri=CIMTBL.stepLimitTablePoint__StepOperationalLimitTable, domain=None, range=Optional[Union[dict, StepOperationalLimitTable]])

slots.stepOperationalLimitTable__TapChanger = Slot(uri=CIM['StepOperationalLimitTable.TapChanger'], name="stepOperationalLimitTable__TapChanger", curie=CIM.curie('StepOperationalLimitTable.TapChanger'),
                   model_uri=CIMTBL.stepOperationalLimitTable__TapChanger, domain=None, range=Optional[Union[dict, TapChanger]])

slots.stringQuantity__multiplier = Slot(uri=CIM['StringQuantity.multiplier'], name="stringQuantity__multiplier", curie=CIM.curie('StringQuantity.multiplier'),
                   model_uri=CIMTBL.stringQuantity__multiplier, domain=None, range=Optional[Union[str, "UnitMultiplier"]])

slots.stringQuantity__unit = Slot(uri=CIM['StringQuantity.unit'], name="stringQuantity__unit", curie=CIM.curie('StringQuantity.unit'),
                   model_uri=CIMTBL.stringQuantity__unit, domain=None, range=Optional[Union[str, "UnitSymbol"]])

slots.stringQuantity__value = Slot(uri=CIM['StringQuantity.value'], name="stringQuantity__value", curie=CIM.curie('StringQuantity.value'),
                   model_uri=CIMTBL.stringQuantity__value, domain=None, range=Optional[str])

slots.subGeographicalRegion__Region = Slot(uri=CIM['SubGeographicalRegion.Region'], name="subGeographicalRegion__Region", curie=CIM.curie('SubGeographicalRegion.Region'),
                   model_uri=CIMTBL.subGeographicalRegion__Region, domain=None, range=Optional[Union[dict, GeographicalRegion]])

slots.subLoadArea__LoadArea = Slot(uri=CIM['SubLoadArea.LoadArea'], name="subLoadArea__LoadArea", curie=CIM.curie('SubLoadArea.LoadArea'),
                   model_uri=CIMTBL.subLoadArea__LoadArea, domain=None, range=Optional[Union[dict, LoadArea]])

slots.substation__NamingFeeder = Slot(uri=CIM['Substation.NamingFeeder'], name="substation__NamingFeeder", curie=CIM.curie('Substation.NamingFeeder'),
                   model_uri=CIMTBL.substation__NamingFeeder, domain=None, range=Optional[Union[dict, Feeder]])

slots.substation__Region = Slot(uri=CIM['Substation.Region'], name="substation__Region", curie=CIM.curie('Substation.Region'),
                   model_uri=CIMTBL.substation__Region, domain=None, range=Optional[Union[dict, SubGeographicalRegion]])

slots.substation__SchedulingArea = Slot(uri=CIM['Substation.SchedulingArea'], name="substation__SchedulingArea", curie=CIM.curie('Substation.SchedulingArea'),
                   model_uri=CIMTBL.substation__SchedulingArea, domain=None, range=Optional[Union[dict, SchedulingArea]])

slots.svDCPowerFlow__p = Slot(uri=CIM['SvDCPowerFlow.p'], name="svDCPowerFlow__p", curie=CIM.curie('SvDCPowerFlow.p'),
                   model_uri=CIMTBL.svDCPowerFlow__p, domain=None, range=Optional[float])

slots.svDCPowerFlow__DCTerminal = Slot(uri=CIM['SvDCPowerFlow.DCTerminal'], name="svDCPowerFlow__DCTerminal", curie=CIM.curie('SvDCPowerFlow.DCTerminal'),
                   model_uri=CIMTBL.svDCPowerFlow__DCTerminal, domain=None, range=Optional[Union[dict, DCTerminal]])

slots.svDCVoltage__v = Slot(uri=CIM['SvDCVoltage.v'], name="svDCVoltage__v", curie=CIM.curie('SvDCVoltage.v'),
                   model_uri=CIMTBL.svDCVoltage__v, domain=None, range=Optional[float])

slots.svDCVoltage__DCTopologicalNode = Slot(uri=CIM['SvDCVoltage.DCTopologicalNode'], name="svDCVoltage__DCTopologicalNode", curie=CIM.curie('SvDCVoltage.DCTopologicalNode'),
                   model_uri=CIMTBL.svDCVoltage__DCTopologicalNode, domain=None, range=Optional[Union[dict, DCTopologicalNode]])

slots.svInjection__phase = Slot(uri=CIM['SvInjection.phase'], name="svInjection__phase", curie=CIM.curie('SvInjection.phase'),
                   model_uri=CIMTBL.svInjection__phase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.svInjection__pInjection = Slot(uri=CIM['SvInjection.pInjection'], name="svInjection__pInjection", curie=CIM.curie('SvInjection.pInjection'),
                   model_uri=CIMTBL.svInjection__pInjection, domain=None, range=Optional[float])

slots.svInjection__qInjection = Slot(uri=CIM['SvInjection.qInjection'], name="svInjection__qInjection", curie=CIM.curie('SvInjection.qInjection'),
                   model_uri=CIMTBL.svInjection__qInjection, domain=None, range=Optional[float])

slots.svInjection__TopologicalNode = Slot(uri=CIM['SvInjection.TopologicalNode'], name="svInjection__TopologicalNode", curie=CIM.curie('SvInjection.TopologicalNode'),
                   model_uri=CIMTBL.svInjection__TopologicalNode, domain=None, range=Optional[Union[dict, TopologicalNode]])

slots.svPowerFlow__p = Slot(uri=CIM['SvPowerFlow.p'], name="svPowerFlow__p", curie=CIM.curie('SvPowerFlow.p'),
                   model_uri=CIMTBL.svPowerFlow__p, domain=None, range=Optional[float])

slots.svPowerFlow__phase = Slot(uri=CIM['SvPowerFlow.phase'], name="svPowerFlow__phase", curie=CIM.curie('SvPowerFlow.phase'),
                   model_uri=CIMTBL.svPowerFlow__phase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.svPowerFlow__q = Slot(uri=CIM['SvPowerFlow.q'], name="svPowerFlow__q", curie=CIM.curie('SvPowerFlow.q'),
                   model_uri=CIMTBL.svPowerFlow__q, domain=None, range=Optional[float])

slots.svPowerFlow__Terminal = Slot(uri=CIM['SvPowerFlow.Terminal'], name="svPowerFlow__Terminal", curie=CIM.curie('SvPowerFlow.Terminal'),
                   model_uri=CIMTBL.svPowerFlow__Terminal, domain=None, range=Optional[Union[dict, Terminal]])

slots.svShuntCompensatorSections__phase = Slot(uri=CIM['SvShuntCompensatorSections.phase'], name="svShuntCompensatorSections__phase", curie=CIM.curie('SvShuntCompensatorSections.phase'),
                   model_uri=CIMTBL.svShuntCompensatorSections__phase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.svShuntCompensatorSections__sections = Slot(uri=CIM['SvShuntCompensatorSections.sections'], name="svShuntCompensatorSections__sections", curie=CIM.curie('SvShuntCompensatorSections.sections'),
                   model_uri=CIMTBL.svShuntCompensatorSections__sections, domain=None, range=Optional[float])

slots.svShuntCompensatorSections__ShuntCompensator = Slot(uri=CIM['SvShuntCompensatorSections.ShuntCompensator'], name="svShuntCompensatorSections__ShuntCompensator", curie=CIM.curie('SvShuntCompensatorSections.ShuntCompensator'),
                   model_uri=CIMTBL.svShuntCompensatorSections__ShuntCompensator, domain=None, range=Optional[Union[dict, ShuntCompensator]])

slots.svStatus__inService = Slot(uri=CIM['SvStatus.inService'], name="svStatus__inService", curie=CIM.curie('SvStatus.inService'),
                   model_uri=CIMTBL.svStatus__inService, domain=None, range=Optional[Union[bool, Bool]])

slots.svStatus__phase = Slot(uri=CIM['SvStatus.phase'], name="svStatus__phase", curie=CIM.curie('SvStatus.phase'),
                   model_uri=CIMTBL.svStatus__phase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.svStatus__ConductingEquipment = Slot(uri=CIM['SvStatus.ConductingEquipment'], name="svStatus__ConductingEquipment", curie=CIM.curie('SvStatus.ConductingEquipment'),
                   model_uri=CIMTBL.svStatus__ConductingEquipment, domain=None, range=Optional[Union[dict, ConductingEquipment]])

slots.svSwitch__open = Slot(uri=CIM['SvSwitch.open'], name="svSwitch__open", curie=CIM.curie('SvSwitch.open'),
                   model_uri=CIMTBL.svSwitch__open, domain=None, range=Optional[Union[bool, Bool]])

slots.svSwitch__phase = Slot(uri=CIM['SvSwitch.phase'], name="svSwitch__phase", curie=CIM.curie('SvSwitch.phase'),
                   model_uri=CIMTBL.svSwitch__phase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.svSwitch__Switch = Slot(uri=CIM['SvSwitch.Switch'], name="svSwitch__Switch", curie=CIM.curie('SvSwitch.Switch'),
                   model_uri=CIMTBL.svSwitch__Switch, domain=None, range=Optional[Union[dict, Switch]])

slots.svTapStep__position = Slot(uri=CIM['SvTapStep.position'], name="svTapStep__position", curie=CIM.curie('SvTapStep.position'),
                   model_uri=CIMTBL.svTapStep__position, domain=None, range=Optional[float])

slots.svTapStep__TapChanger = Slot(uri=CIM['SvTapStep.TapChanger'], name="svTapStep__TapChanger", curie=CIM.curie('SvTapStep.TapChanger'),
                   model_uri=CIMTBL.svTapStep__TapChanger, domain=None, range=Optional[Union[dict, TapChanger]])

slots.svVoltage__angle = Slot(uri=CIM['SvVoltage.angle'], name="svVoltage__angle", curie=CIM.curie('SvVoltage.angle'),
                   model_uri=CIMTBL.svVoltage__angle, domain=None, range=Optional[float])

slots.svVoltage__phase = Slot(uri=CIM['SvVoltage.phase'], name="svVoltage__phase", curie=CIM.curie('SvVoltage.phase'),
                   model_uri=CIMTBL.svVoltage__phase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.svVoltage__v = Slot(uri=CIM['SvVoltage.v'], name="svVoltage__v", curie=CIM.curie('SvVoltage.v'),
                   model_uri=CIMTBL.svVoltage__v, domain=None, range=Optional[float])

slots.svVoltage__TopologicalNode = Slot(uri=CIM['SvVoltage.TopologicalNode'], name="svVoltage__TopologicalNode", curie=CIM.curie('SvVoltage.TopologicalNode'),
                   model_uri=CIMTBL.svVoltage__TopologicalNode, domain=None, range=Optional[Union[dict, TopologicalNode]])

slots.switch__locked = Slot(uri=CIM['Switch.locked'], name="switch__locked", curie=CIM.curie('Switch.locked'),
                   model_uri=CIMTBL.switch__locked, domain=None, range=Optional[Union[bool, Bool]])

slots.switch__normalOpen = Slot(uri=CIM['Switch.normalOpen'], name="switch__normalOpen", curie=CIM.curie('Switch.normalOpen'),
                   model_uri=CIMTBL.switch__normalOpen, domain=None, range=Optional[Union[bool, Bool]])

slots.switch__open = Slot(uri=CIM['Switch.open'], name="switch__open", curie=CIM.curie('Switch.open'),
                   model_uri=CIMTBL.switch__open, domain=None, range=Optional[Union[bool, Bool]])

slots.switch__ratedCurrent = Slot(uri=CIM['Switch.ratedCurrent'], name="switch__ratedCurrent", curie=CIM.curie('Switch.ratedCurrent'),
                   model_uri=CIMTBL.switch__ratedCurrent, domain=None, range=Optional[float])

slots.switch__retained = Slot(uri=CIM['Switch.retained'], name="switch__retained", curie=CIM.curie('Switch.retained'),
                   model_uri=CIMTBL.switch__retained, domain=None, range=Optional[Union[bool, Bool]])

slots.switch__topologicalUsageType = Slot(uri=CIM['Switch.topologicalUsageType'], name="switch__topologicalUsageType", curie=CIM.curie('Switch.topologicalUsageType'),
                   model_uri=CIMTBL.switch__topologicalUsageType, domain=None, range=Optional[Union[str, "TopologicalUsageKind"]])

slots.switch__CompositeSwitch = Slot(uri=CIM['Switch.CompositeSwitch'], name="switch__CompositeSwitch", curie=CIM.curie('Switch.CompositeSwitch'),
                   model_uri=CIMTBL.switch__CompositeSwitch, domain=None, range=Optional[Union[dict, CompositeSwitch]])

slots.switch__SwitchAction = Slot(uri=CIM['Switch.SwitchAction'], name="switch__SwitchAction", curie=CIM.curie('Switch.SwitchAction'),
                   model_uri=CIMTBL.switch__SwitchAction, domain=None, range=Optional[Union[dict, SwitchAction]])

slots.switchPhase__closed = Slot(uri=CIM['SwitchPhase.closed'], name="switchPhase__closed", curie=CIM.curie('SwitchPhase.closed'),
                   model_uri=CIMTBL.switchPhase__closed, domain=None, range=Optional[Union[bool, Bool]])

slots.switchPhase__normalOpen = Slot(uri=CIM['SwitchPhase.normalOpen'], name="switchPhase__normalOpen", curie=CIM.curie('SwitchPhase.normalOpen'),
                   model_uri=CIMTBL.switchPhase__normalOpen, domain=None, range=Optional[Union[bool, Bool]])

slots.switchPhase__open = Slot(uri=CIM['SwitchPhase.open'], name="switchPhase__open", curie=CIM.curie('SwitchPhase.open'),
                   model_uri=CIMTBL.switchPhase__open, domain=None, range=Optional[Union[bool, Bool]])

slots.switchPhase__phaseSide1 = Slot(uri=CIM['SwitchPhase.phaseSide1'], name="switchPhase__phaseSide1", curie=CIM.curie('SwitchPhase.phaseSide1'),
                   model_uri=CIMTBL.switchPhase__phaseSide1, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.switchPhase__phaseSide2 = Slot(uri=CIM['SwitchPhase.phaseSide2'], name="switchPhase__phaseSide2", curie=CIM.curie('SwitchPhase.phaseSide2'),
                   model_uri=CIMTBL.switchPhase__phaseSide2, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.switchPhase__ratedCurrent = Slot(uri=CIM['SwitchPhase.ratedCurrent'], name="switchPhase__ratedCurrent", curie=CIM.curie('SwitchPhase.ratedCurrent'),
                   model_uri=CIMTBL.switchPhase__ratedCurrent, domain=None, range=Optional[float])

slots.switchPhase__Switch = Slot(uri=CIM['SwitchPhase.Switch'], name="switchPhase__Switch", curie=CIM.curie('SwitchPhase.Switch'),
                   model_uri=CIMTBL.switchPhase__Switch, domain=None, range=Optional[Union[dict, Switch]])

slots.switchSchedule__Switch = Slot(uri=CIM['SwitchSchedule.Switch'], name="switchSchedule__Switch", curie=CIM.curie('SwitchSchedule.Switch'),
                   model_uri=CIMTBL.switchSchedule__Switch, domain=None, range=Optional[Union[dict, Switch]])

slots.synchronousMachine__aVRToManualLag = Slot(uri=CIM['SynchronousMachine.aVRToManualLag'], name="synchronousMachine__aVRToManualLag", curie=CIM.curie('SynchronousMachine.aVRToManualLag'),
                   model_uri=CIMTBL.synchronousMachine__aVRToManualLag, domain=None, range=Optional[float])

slots.synchronousMachine__aVRToManualLead = Slot(uri=CIM['SynchronousMachine.aVRToManualLead'], name="synchronousMachine__aVRToManualLead", curie=CIM.curie('SynchronousMachine.aVRToManualLead'),
                   model_uri=CIMTBL.synchronousMachine__aVRToManualLead, domain=None, range=Optional[float])

slots.synchronousMachine__baseQ = Slot(uri=CIM['SynchronousMachine.baseQ'], name="synchronousMachine__baseQ", curie=CIM.curie('SynchronousMachine.baseQ'),
                   model_uri=CIMTBL.synchronousMachine__baseQ, domain=None, range=Optional[float])

slots.synchronousMachine__condenserP = Slot(uri=CIM['SynchronousMachine.condenserP'], name="synchronousMachine__condenserP", curie=CIM.curie('SynchronousMachine.condenserP'),
                   model_uri=CIMTBL.synchronousMachine__condenserP, domain=None, range=Optional[float])

slots.synchronousMachine__coolantCondition = Slot(uri=CIM['SynchronousMachine.coolantCondition'], name="synchronousMachine__coolantCondition", curie=CIM.curie('SynchronousMachine.coolantCondition'),
                   model_uri=CIMTBL.synchronousMachine__coolantCondition, domain=None, range=Optional[float])

slots.synchronousMachine__coolantType = Slot(uri=CIM['SynchronousMachine.coolantType'], name="synchronousMachine__coolantType", curie=CIM.curie('SynchronousMachine.coolantType'),
                   model_uri=CIMTBL.synchronousMachine__coolantType, domain=None, range=Optional[Union[str, "CoolantType"]])

slots.synchronousMachine__earthing = Slot(uri=CIM['SynchronousMachine.earthing'], name="synchronousMachine__earthing", curie=CIM.curie('SynchronousMachine.earthing'),
                   model_uri=CIMTBL.synchronousMachine__earthing, domain=None, range=Optional[Union[bool, Bool]])

slots.synchronousMachine__earthingStarPointR = Slot(uri=CIM['SynchronousMachine.earthingStarPointR'], name="synchronousMachine__earthingStarPointR", curie=CIM.curie('SynchronousMachine.earthingStarPointR'),
                   model_uri=CIMTBL.synchronousMachine__earthingStarPointR, domain=None, range=Optional[float])

slots.synchronousMachine__earthingStarPointX = Slot(uri=CIM['SynchronousMachine.earthingStarPointX'], name="synchronousMachine__earthingStarPointX", curie=CIM.curie('SynchronousMachine.earthingStarPointX'),
                   model_uri=CIMTBL.synchronousMachine__earthingStarPointX, domain=None, range=Optional[float])

slots.synchronousMachine__ikk = Slot(uri=CIM['SynchronousMachine.ikk'], name="synchronousMachine__ikk", curie=CIM.curie('SynchronousMachine.ikk'),
                   model_uri=CIMTBL.synchronousMachine__ikk, domain=None, range=Optional[float])

slots.synchronousMachine__manualToAVR = Slot(uri=CIM['SynchronousMachine.manualToAVR'], name="synchronousMachine__manualToAVR", curie=CIM.curie('SynchronousMachine.manualToAVR'),
                   model_uri=CIMTBL.synchronousMachine__manualToAVR, domain=None, range=Optional[float])

slots.synchronousMachine__maxQ = Slot(uri=CIM['SynchronousMachine.maxQ'], name="synchronousMachine__maxQ", curie=CIM.curie('SynchronousMachine.maxQ'),
                   model_uri=CIMTBL.synchronousMachine__maxQ, domain=None, range=Optional[float])

slots.synchronousMachine__maxU = Slot(uri=CIM['SynchronousMachine.maxU'], name="synchronousMachine__maxU", curie=CIM.curie('SynchronousMachine.maxU'),
                   model_uri=CIMTBL.synchronousMachine__maxU, domain=None, range=Optional[float])

slots.synchronousMachine__minQ = Slot(uri=CIM['SynchronousMachine.minQ'], name="synchronousMachine__minQ", curie=CIM.curie('SynchronousMachine.minQ'),
                   model_uri=CIMTBL.synchronousMachine__minQ, domain=None, range=Optional[float])

slots.synchronousMachine__minU = Slot(uri=CIM['SynchronousMachine.minU'], name="synchronousMachine__minU", curie=CIM.curie('SynchronousMachine.minU'),
                   model_uri=CIMTBL.synchronousMachine__minU, domain=None, range=Optional[float])

slots.synchronousMachine__mu = Slot(uri=CIM['SynchronousMachine.mu'], name="synchronousMachine__mu", curie=CIM.curie('SynchronousMachine.mu'),
                   model_uri=CIMTBL.synchronousMachine__mu, domain=None, range=Optional[float])

slots.synchronousMachine__operatingMode = Slot(uri=CIM['SynchronousMachine.operatingMode'], name="synchronousMachine__operatingMode", curie=CIM.curie('SynchronousMachine.operatingMode'),
                   model_uri=CIMTBL.synchronousMachine__operatingMode, domain=None, range=Optional[Union[str, "SynchronousMachineOperatingMode"]])

slots.synchronousMachine__qPercent = Slot(uri=CIM['SynchronousMachine.qPercent'], name="synchronousMachine__qPercent", curie=CIM.curie('SynchronousMachine.qPercent'),
                   model_uri=CIMTBL.synchronousMachine__qPercent, domain=None, range=Optional[float])

slots.synchronousMachine__r = Slot(uri=CIM['SynchronousMachine.r'], name="synchronousMachine__r", curie=CIM.curie('SynchronousMachine.r'),
                   model_uri=CIMTBL.synchronousMachine__r, domain=None, range=Optional[float])

slots.synchronousMachine__r0 = Slot(uri=CIM['SynchronousMachine.r0'], name="synchronousMachine__r0", curie=CIM.curie('SynchronousMachine.r0'),
                   model_uri=CIMTBL.synchronousMachine__r0, domain=None, range=Optional[float])

slots.synchronousMachine__r2 = Slot(uri=CIM['SynchronousMachine.r2'], name="synchronousMachine__r2", curie=CIM.curie('SynchronousMachine.r2'),
                   model_uri=CIMTBL.synchronousMachine__r2, domain=None, range=Optional[float])

slots.synchronousMachine__referencePriority = Slot(uri=CIM['SynchronousMachine.referencePriority'], name="synchronousMachine__referencePriority", curie=CIM.curie('SynchronousMachine.referencePriority'),
                   model_uri=CIMTBL.synchronousMachine__referencePriority, domain=None, range=Optional[int])

slots.synchronousMachine__satDirectSubtransX = Slot(uri=CIM['SynchronousMachine.satDirectSubtransX'], name="synchronousMachine__satDirectSubtransX", curie=CIM.curie('SynchronousMachine.satDirectSubtransX'),
                   model_uri=CIMTBL.synchronousMachine__satDirectSubtransX, domain=None, range=Optional[float])

slots.synchronousMachine__satDirectSyncX = Slot(uri=CIM['SynchronousMachine.satDirectSyncX'], name="synchronousMachine__satDirectSyncX", curie=CIM.curie('SynchronousMachine.satDirectSyncX'),
                   model_uri=CIMTBL.synchronousMachine__satDirectSyncX, domain=None, range=Optional[float])

slots.synchronousMachine__satDirectTransX = Slot(uri=CIM['SynchronousMachine.satDirectTransX'], name="synchronousMachine__satDirectTransX", curie=CIM.curie('SynchronousMachine.satDirectTransX'),
                   model_uri=CIMTBL.synchronousMachine__satDirectTransX, domain=None, range=Optional[float])

slots.synchronousMachine__shortCircuitRotorType = Slot(uri=CIM['SynchronousMachine.shortCircuitRotorType'], name="synchronousMachine__shortCircuitRotorType", curie=CIM.curie('SynchronousMachine.shortCircuitRotorType'),
                   model_uri=CIMTBL.synchronousMachine__shortCircuitRotorType, domain=None, range=Optional[Union[str, "ShortCircuitRotorKind"]])

slots.synchronousMachine__type = Slot(uri=CIM['SynchronousMachine.type'], name="synchronousMachine__type", curie=CIM.curie('SynchronousMachine.type'),
                   model_uri=CIMTBL.synchronousMachine__type, domain=None, range=Optional[Union[str, "SynchronousMachineKind"]])

slots.synchronousMachine__voltageRegulationRange = Slot(uri=CIM['SynchronousMachine.voltageRegulationRange'], name="synchronousMachine__voltageRegulationRange", curie=CIM.curie('SynchronousMachine.voltageRegulationRange'),
                   model_uri=CIMTBL.synchronousMachine__voltageRegulationRange, domain=None, range=Optional[float])

slots.synchronousMachine__x0 = Slot(uri=CIM['SynchronousMachine.x0'], name="synchronousMachine__x0", curie=CIM.curie('SynchronousMachine.x0'),
                   model_uri=CIMTBL.synchronousMachine__x0, domain=None, range=Optional[float])

slots.synchronousMachine__x2 = Slot(uri=CIM['SynchronousMachine.x2'], name="synchronousMachine__x2", curie=CIM.curie('SynchronousMachine.x2'),
                   model_uri=CIMTBL.synchronousMachine__x2, domain=None, range=Optional[float])

slots.synchronousMachine__InitialReactiveCapabilityCurve = Slot(uri=CIM['SynchronousMachine.InitialReactiveCapabilityCurve'], name="synchronousMachine__InitialReactiveCapabilityCurve", curie=CIM.curie('SynchronousMachine.InitialReactiveCapabilityCurve'),
                   model_uri=CIMTBL.synchronousMachine__InitialReactiveCapabilityCurve, domain=None, range=Optional[Union[dict, ReactiveCapabilityCurve]])

slots.synchronousMachine__SynchronousMachineDynamics = Slot(uri=CIM['SynchronousMachine.SynchronousMachineDynamics'], name="synchronousMachine__SynchronousMachineDynamics", curie=CIM.curie('SynchronousMachine.SynchronousMachineDynamics'),
                   model_uri=CIMTBL.synchronousMachine__SynchronousMachineDynamics, domain=None, range=Optional[Union[dict, SynchronousMachineDynamics]])

slots.synchrophaserFrame__chk = Slot(uri=CIM['SynchrophaserFrame.chk'], name="synchrophaserFrame__chk", curie=CIM.curie('SynchrophaserFrame.chk'),
                   model_uri=CIMTBL.synchrophaserFrame__chk, domain=None, range=Optional[int])

slots.synchrophaserFrame__fracsec = Slot(uri=CIM['SynchrophaserFrame.fracsec'], name="synchrophaserFrame__fracsec", curie=CIM.curie('SynchrophaserFrame.fracsec'),
                   model_uri=CIMTBL.synchrophaserFrame__fracsec, domain=None, range=Optional[int])

slots.synchrophaserFrame__framesize = Slot(uri=CIM['SynchrophaserFrame.framesize'], name="synchrophaserFrame__framesize", curie=CIM.curie('SynchrophaserFrame.framesize'),
                   model_uri=CIMTBL.synchrophaserFrame__framesize, domain=None, range=Optional[int])

slots.synchrophaserFrame__leapByte = Slot(uri=CIM['SynchrophaserFrame.leapByte'], name="synchrophaserFrame__leapByte", curie=CIM.curie('SynchrophaserFrame.leapByte'),
                   model_uri=CIMTBL.synchrophaserFrame__leapByte, domain=None, range=Optional[float])

slots.synchrophaserFrame__soc = Slot(uri=CIM['SynchrophaserFrame.soc'], name="synchrophaserFrame__soc", curie=CIM.curie('SynchrophaserFrame.soc'),
                   model_uri=CIMTBL.synchrophaserFrame__soc, domain=None, range=Optional[Union[str, XSDTime]])

slots.synchrophaserFrame__streamId = Slot(uri=CIM['SynchrophaserFrame.streamId'], name="synchrophaserFrame__streamId", curie=CIM.curie('SynchrophaserFrame.streamId'),
                   model_uri=CIMTBL.synchrophaserFrame__streamId, domain=None, range=Optional[int])

slots.synchrophaserFrame__sync = Slot(uri=CIM['SynchrophaserFrame.sync'], name="synchrophaserFrame__sync", curie=CIM.curie('SynchrophaserFrame.sync'),
                   model_uri=CIMTBL.synchrophaserFrame__sync, domain=None, range=Optional[str])

slots.tCSCCompensationPoint__mRID = Slot(uri=CIM['TCSCCompensationPoint.mRID'], name="tCSCCompensationPoint__mRID", curie=CIM.curie('TCSCCompensationPoint.mRID'),
                   model_uri=CIMTBL.tCSCCompensationPoint__mRID, domain=None, range=Optional[str])

slots.tCSCCompensationPoint__compensationZ = Slot(uri=CIM['TCSCCompensationPoint.compensationZ'], name="tCSCCompensationPoint__compensationZ", curie=CIM.curie('TCSCCompensationPoint.compensationZ'),
                   model_uri=CIMTBL.tCSCCompensationPoint__compensationZ, domain=None, range=Optional[float])

slots.tCSCCompensationPoint__section = Slot(uri=CIM['TCSCCompensationPoint.section'], name="tCSCCompensationPoint__section", curie=CIM.curie('TCSCCompensationPoint.section'),
                   model_uri=CIMTBL.tCSCCompensationPoint__section, domain=None, range=Optional[int])

slots.tCSCCompensationPoint__ThyristorControlledSeriesCompensator = Slot(uri=CIM['TCSCCompensationPoint.ThyristorControlledSeriesCompensator'], name="tCSCCompensationPoint__ThyristorControlledSeriesCompensator", curie=CIM.curie('TCSCCompensationPoint.ThyristorControlledSeriesCompensator'),
                   model_uri=CIMTBL.tCSCCompensationPoint__ThyristorControlledSeriesCompensator, domain=None, range=Optional[Union[dict, ThyristorControlledSeriesCompensator]])

slots.tapChanger__controlEnabled = Slot(uri=CIM['TapChanger.controlEnabled'], name="tapChanger__controlEnabled", curie=CIM.curie('TapChanger.controlEnabled'),
                   model_uri=CIMTBL.tapChanger__controlEnabled, domain=None, range=Optional[Union[bool, Bool]])

slots.tapChanger__ctRating = Slot(uri=CIM['TapChanger.ctRating'], name="tapChanger__ctRating", curie=CIM.curie('TapChanger.ctRating'),
                   model_uri=CIMTBL.tapChanger__ctRating, domain=None, range=Optional[float])

slots.tapChanger__ctRatio = Slot(uri=CIM['TapChanger.ctRatio'], name="tapChanger__ctRatio", curie=CIM.curie('TapChanger.ctRatio'),
                   model_uri=CIMTBL.tapChanger__ctRatio, domain=None, range=Optional[float])

slots.tapChanger__highStep = Slot(uri=CIM['TapChanger.highStep'], name="tapChanger__highStep", curie=CIM.curie('TapChanger.highStep'),
                   model_uri=CIMTBL.tapChanger__highStep, domain=None, range=Optional[int])

slots.tapChanger__initialDelay = Slot(uri=CIM['TapChanger.initialDelay'], name="tapChanger__initialDelay", curie=CIM.curie('TapChanger.initialDelay'),
                   model_uri=CIMTBL.tapChanger__initialDelay, domain=None, range=Optional[float])

slots.tapChanger__lowStep = Slot(uri=CIM['TapChanger.lowStep'], name="tapChanger__lowStep", curie=CIM.curie('TapChanger.lowStep'),
                   model_uri=CIMTBL.tapChanger__lowStep, domain=None, range=Optional[int])

slots.tapChanger__ltcFlag = Slot(uri=CIM['TapChanger.ltcFlag'], name="tapChanger__ltcFlag", curie=CIM.curie('TapChanger.ltcFlag'),
                   model_uri=CIMTBL.tapChanger__ltcFlag, domain=None, range=Optional[Union[bool, Bool]])

slots.tapChanger__neutralStep = Slot(uri=CIM['TapChanger.neutralStep'], name="tapChanger__neutralStep", curie=CIM.curie('TapChanger.neutralStep'),
                   model_uri=CIMTBL.tapChanger__neutralStep, domain=None, range=Optional[int])

slots.tapChanger__neutralU = Slot(uri=CIM['TapChanger.neutralU'], name="tapChanger__neutralU", curie=CIM.curie('TapChanger.neutralU'),
                   model_uri=CIMTBL.tapChanger__neutralU, domain=None, range=Optional[float])

slots.tapChanger__normalStep = Slot(uri=CIM['TapChanger.normalStep'], name="tapChanger__normalStep", curie=CIM.curie('TapChanger.normalStep'),
                   model_uri=CIMTBL.tapChanger__normalStep, domain=None, range=Optional[int])

slots.tapChanger__ptPhase = Slot(uri=CIM['TapChanger.ptPhase'], name="tapChanger__ptPhase", curie=CIM.curie('TapChanger.ptPhase'),
                   model_uri=CIMTBL.tapChanger__ptPhase, domain=None, range=Optional[Union[str, "PhaseCode"]])

slots.tapChanger__ptRatio = Slot(uri=CIM['TapChanger.ptRatio'], name="tapChanger__ptRatio", curie=CIM.curie('TapChanger.ptRatio'),
                   model_uri=CIMTBL.tapChanger__ptRatio, domain=None, range=Optional[float])

slots.tapChanger__step = Slot(uri=CIM['TapChanger.step'], name="tapChanger__step", curie=CIM.curie('TapChanger.step'),
                   model_uri=CIMTBL.tapChanger__step, domain=None, range=Optional[float])

slots.tapChanger__subsequentDelay = Slot(uri=CIM['TapChanger.subsequentDelay'], name="tapChanger__subsequentDelay", curie=CIM.curie('TapChanger.subsequentDelay'),
                   model_uri=CIMTBL.tapChanger__subsequentDelay, domain=None, range=Optional[float])

slots.tapChanger__SvTapStep = Slot(uri=CIM['TapChanger.SvTapStep'], name="tapChanger__SvTapStep", curie=CIM.curie('TapChanger.SvTapStep'),
                   model_uri=CIMTBL.tapChanger__SvTapStep, domain=None, range=Optional[Union[dict, SvTapStep]])

slots.tapChanger__TapChangeController = Slot(uri=CIM['TapChanger.TapChangeController'], name="tapChanger__TapChangeController", curie=CIM.curie('TapChanger.TapChangeController'),
                   model_uri=CIMTBL.tapChanger__TapChangeController, domain=None, range=Optional[Union[dict, TapChangerController]])

slots.tapChanger__TapChangerControl = Slot(uri=CIM['TapChanger.TapChangerControl'], name="tapChanger__TapChangerControl", curie=CIM.curie('TapChanger.TapChangerControl'),
                   model_uri=CIMTBL.tapChanger__TapChangerControl, domain=None, range=Optional[Union[dict, TapChangerControl]])

slots.tapChangerControl__lineDropCompensation = Slot(uri=CIM['TapChangerControl.lineDropCompensation'], name="tapChangerControl__lineDropCompensation", curie=CIM.curie('TapChangerControl.lineDropCompensation'),
                   model_uri=CIMTBL.tapChangerControl__lineDropCompensation, domain=None, range=Optional[Union[bool, Bool]])

slots.tapChangerControl__lineDropR = Slot(uri=CIM['TapChangerControl.lineDropR'], name="tapChangerControl__lineDropR", curie=CIM.curie('TapChangerControl.lineDropR'),
                   model_uri=CIMTBL.tapChangerControl__lineDropR, domain=None, range=Optional[float])

slots.tapChangerControl__lineDropX = Slot(uri=CIM['TapChangerControl.lineDropX'], name="tapChangerControl__lineDropX", curie=CIM.curie('TapChangerControl.lineDropX'),
                   model_uri=CIMTBL.tapChangerControl__lineDropX, domain=None, range=Optional[float])

slots.tapChangerControl__maxLimitVoltage = Slot(uri=CIM['TapChangerControl.maxLimitVoltage'], name="tapChangerControl__maxLimitVoltage", curie=CIM.curie('TapChangerControl.maxLimitVoltage'),
                   model_uri=CIMTBL.tapChangerControl__maxLimitVoltage, domain=None, range=Optional[float])

slots.tapChangerControl__minLimitVoltage = Slot(uri=CIM['TapChangerControl.minLimitVoltage'], name="tapChangerControl__minLimitVoltage", curie=CIM.curie('TapChangerControl.minLimitVoltage'),
                   model_uri=CIMTBL.tapChangerControl__minLimitVoltage, domain=None, range=Optional[float])

slots.tapChangerControl__reverseLineDropR = Slot(uri=CIM['TapChangerControl.reverseLineDropR'], name="tapChangerControl__reverseLineDropR", curie=CIM.curie('TapChangerControl.reverseLineDropR'),
                   model_uri=CIMTBL.tapChangerControl__reverseLineDropR, domain=None, range=Optional[float])

slots.tapChangerControl__reverseLineDropX = Slot(uri=CIM['TapChangerControl.reverseLineDropX'], name="tapChangerControl__reverseLineDropX", curie=CIM.curie('TapChangerControl.reverseLineDropX'),
                   model_uri=CIMTBL.tapChangerControl__reverseLineDropX, domain=None, range=Optional[float])

slots.tapChangerControl__reverseToNeutral = Slot(uri=CIM['TapChangerControl.reverseToNeutral'], name="tapChangerControl__reverseToNeutral", curie=CIM.curie('TapChangerControl.reverseToNeutral'),
                   model_uri=CIMTBL.tapChangerControl__reverseToNeutral, domain=None, range=Optional[Union[bool, Bool]])

slots.tapChangerControl__reversible = Slot(uri=CIM['TapChangerControl.reversible'], name="tapChangerControl__reversible", curie=CIM.curie('TapChangerControl.reversible'),
                   model_uri=CIMTBL.tapChangerControl__reversible, domain=None, range=Optional[Union[bool, Bool]])

slots.tapChangerControl__reversingDelay = Slot(uri=CIM['TapChangerControl.reversingDelay'], name="tapChangerControl__reversingDelay", curie=CIM.curie('TapChangerControl.reversingDelay'),
                   model_uri=CIMTBL.tapChangerControl__reversingDelay, domain=None, range=Optional[float])

slots.tapChangerControl__reversingPowerThreshold = Slot(uri=CIM['TapChangerControl.reversingPowerThreshold'], name="tapChangerControl__reversingPowerThreshold", curie=CIM.curie('TapChangerControl.reversingPowerThreshold'),
                   model_uri=CIMTBL.tapChangerControl__reversingPowerThreshold, domain=None, range=Optional[float])

slots.tapChangerInfo__bil = Slot(uri=CIM['TapChangerInfo.bil'], name="tapChangerInfo__bil", curie=CIM.curie('TapChangerInfo.bil'),
                   model_uri=CIMTBL.tapChangerInfo__bil, domain=None, range=Optional[float])

slots.tapChangerInfo__ctRating = Slot(uri=CIM['TapChangerInfo.ctRating'], name="tapChangerInfo__ctRating", curie=CIM.curie('TapChangerInfo.ctRating'),
                   model_uri=CIMTBL.tapChangerInfo__ctRating, domain=None, range=Optional[float])

slots.tapChangerInfo__ctRatio = Slot(uri=CIM['TapChangerInfo.ctRatio'], name="tapChangerInfo__ctRatio", curie=CIM.curie('TapChangerInfo.ctRatio'),
                   model_uri=CIMTBL.tapChangerInfo__ctRatio, domain=None, range=Optional[float])

slots.tapChangerInfo__frequency = Slot(uri=CIM['TapChangerInfo.frequency'], name="tapChangerInfo__frequency", curie=CIM.curie('TapChangerInfo.frequency'),
                   model_uri=CIMTBL.tapChangerInfo__frequency, domain=None, range=Optional[float])

slots.tapChangerInfo__highStep = Slot(uri=CIM['TapChangerInfo.highStep'], name="tapChangerInfo__highStep", curie=CIM.curie('TapChangerInfo.highStep'),
                   model_uri=CIMTBL.tapChangerInfo__highStep, domain=None, range=Optional[int])

slots.tapChangerInfo__isTcul = Slot(uri=CIM['TapChangerInfo.isTcul'], name="tapChangerInfo__isTcul", curie=CIM.curie('TapChangerInfo.isTcul'),
                   model_uri=CIMTBL.tapChangerInfo__isTcul, domain=None, range=Optional[Union[bool, Bool]])

slots.tapChangerInfo__lowStep = Slot(uri=CIM['TapChangerInfo.lowStep'], name="tapChangerInfo__lowStep", curie=CIM.curie('TapChangerInfo.lowStep'),
                   model_uri=CIMTBL.tapChangerInfo__lowStep, domain=None, range=Optional[int])

slots.tapChangerInfo__neutralStep = Slot(uri=CIM['TapChangerInfo.neutralStep'], name="tapChangerInfo__neutralStep", curie=CIM.curie('TapChangerInfo.neutralStep'),
                   model_uri=CIMTBL.tapChangerInfo__neutralStep, domain=None, range=Optional[int])

slots.tapChangerInfo__neutralU = Slot(uri=CIM['TapChangerInfo.neutralU'], name="tapChangerInfo__neutralU", curie=CIM.curie('TapChangerInfo.neutralU'),
                   model_uri=CIMTBL.tapChangerInfo__neutralU, domain=None, range=Optional[float])

slots.tapChangerInfo__ptRatio = Slot(uri=CIM['TapChangerInfo.ptRatio'], name="tapChangerInfo__ptRatio", curie=CIM.curie('TapChangerInfo.ptRatio'),
                   model_uri=CIMTBL.tapChangerInfo__ptRatio, domain=None, range=Optional[float])

slots.tapChangerInfo__ratedApparentPower = Slot(uri=CIM['TapChangerInfo.ratedApparentPower'], name="tapChangerInfo__ratedApparentPower", curie=CIM.curie('TapChangerInfo.ratedApparentPower'),
                   model_uri=CIMTBL.tapChangerInfo__ratedApparentPower, domain=None, range=Optional[float])

slots.tapChangerInfo__stepPhaseIncrement = Slot(uri=CIM['TapChangerInfo.stepPhaseIncrement'], name="tapChangerInfo__stepPhaseIncrement", curie=CIM.curie('TapChangerInfo.stepPhaseIncrement'),
                   model_uri=CIMTBL.tapChangerInfo__stepPhaseIncrement, domain=None, range=Optional[float])

slots.tapChangerInfo__stepReactiveIncrement = Slot(uri=CIM['TapChangerInfo.stepReactiveIncrement'], name="tapChangerInfo__stepReactiveIncrement", curie=CIM.curie('TapChangerInfo.stepReactiveIncrement'),
                   model_uri=CIMTBL.tapChangerInfo__stepReactiveIncrement, domain=None, range=Optional[float])

slots.tapChangerInfo__stepVoltageIncrement = Slot(uri=CIM['TapChangerInfo.stepVoltageIncrement'], name="tapChangerInfo__stepVoltageIncrement", curie=CIM.curie('TapChangerInfo.stepVoltageIncrement'),
                   model_uri=CIMTBL.tapChangerInfo__stepVoltageIncrement, domain=None, range=Optional[float])

slots.tapChangerTablePoint__b = Slot(uri=CIM['TapChangerTablePoint.b'], name="tapChangerTablePoint__b", curie=CIM.curie('TapChangerTablePoint.b'),
                   model_uri=CIMTBL.tapChangerTablePoint__b, domain=None, range=Optional[float])

slots.tapChangerTablePoint__g = Slot(uri=CIM['TapChangerTablePoint.g'], name="tapChangerTablePoint__g", curie=CIM.curie('TapChangerTablePoint.g'),
                   model_uri=CIMTBL.tapChangerTablePoint__g, domain=None, range=Optional[float])

slots.tapChangerTablePoint__r = Slot(uri=CIM['TapChangerTablePoint.r'], name="tapChangerTablePoint__r", curie=CIM.curie('TapChangerTablePoint.r'),
                   model_uri=CIMTBL.tapChangerTablePoint__r, domain=None, range=Optional[float])

slots.tapChangerTablePoint__ratio = Slot(uri=CIM['TapChangerTablePoint.ratio'], name="tapChangerTablePoint__ratio", curie=CIM.curie('TapChangerTablePoint.ratio'),
                   model_uri=CIMTBL.tapChangerTablePoint__ratio, domain=None, range=Optional[float])

slots.tapChangerTablePoint__step = Slot(uri=CIM['TapChangerTablePoint.step'], name="tapChangerTablePoint__step", curie=CIM.curie('TapChangerTablePoint.step'),
                   model_uri=CIMTBL.tapChangerTablePoint__step, domain=None, range=Optional[int])

slots.tapChangerTablePoint__x = Slot(uri=CIM['TapChangerTablePoint.x'], name="tapChangerTablePoint__x", curie=CIM.curie('TapChangerTablePoint.x'),
                   model_uri=CIMTBL.tapChangerTablePoint__x, domain=None, range=Optional[float])

slots.tapSchedule__TapChanger = Slot(uri=CIM['TapSchedule.TapChanger'], name="tapSchedule__TapChanger", curie=CIM.curie('TapSchedule.TapChanger'),
                   model_uri=CIMTBL.tapSchedule__TapChanger, domain=None, range=Optional[Union[dict, TapChanger]])

slots.tapeShieldCableInfo__tapeLap = Slot(uri=CIM['TapeShieldCableInfo.tapeLap'], name="tapeShieldCableInfo__tapeLap", curie=CIM.curie('TapeShieldCableInfo.tapeLap'),
                   model_uri=CIMTBL.tapeShieldCableInfo__tapeLap, domain=None, range=Optional[float])

slots.tapeShieldCableInfo__tapeThickness = Slot(uri=CIM['TapeShieldCableInfo.tapeThickness'], name="tapeShieldCableInfo__tapeThickness", curie=CIM.curie('TapeShieldCableInfo.tapeThickness'),
                   model_uri=CIMTBL.tapeShieldCableInfo__tapeThickness, domain=None, range=Optional[float])

slots.terminal__phases = Slot(uri=CIM['Terminal.phases'], name="terminal__phases", curie=CIM.curie('Terminal.phases'),
                   model_uri=CIMTBL.terminal__phases, domain=None, range=Optional[Union[str, "PhaseCode"]])

slots.terminal__BoundedConnectivityArea = Slot(uri=CIM['Terminal.BoundedConnectivityArea'], name="terminal__BoundedConnectivityArea", curie=CIM.curie('Terminal.BoundedConnectivityArea'),
                   model_uri=CIMTBL.terminal__BoundedConnectivityArea, domain=None, range=Optional[Union[dict, ConnectivityArea]])

slots.terminal__BoundedContainer = Slot(uri=CIM['Terminal.BoundedContainer'], name="terminal__BoundedContainer", curie=CIM.curie('Terminal.BoundedContainer'),
                   model_uri=CIMTBL.terminal__BoundedContainer, domain=None, range=Optional[Union[dict, ResourceContainer]])

slots.terminal__Bushing = Slot(uri=CIM['Terminal.Bushing'], name="terminal__Bushing", curie=CIM.curie('Terminal.Bushing'),
                   model_uri=CIMTBL.terminal__Bushing, domain=None, range=Optional[Union[dict, Bushing]])

slots.terminal__ConductingEquipment = Slot(uri=CIM['Terminal.ConductingEquipment'], name="terminal__ConductingEquipment", curie=CIM.curie('Terminal.ConductingEquipment'),
                   model_uri=CIMTBL.terminal__ConductingEquipment, domain=None, range=Optional[Union[dict, ConductingEquipment]])

slots.terminal__ConnectivityNode = Slot(uri=CIM['Terminal.ConnectivityNode'], name="terminal__ConnectivityNode", curie=CIM.curie('Terminal.ConnectivityNode'),
                   model_uri=CIMTBL.terminal__ConnectivityNode, domain=None, range=Optional[Union[dict, ConnectivityNode]])

slots.terminal__NormalHeadFeeder = Slot(uri=CIM['Terminal.NormalHeadFeeder'], name="terminal__NormalHeadFeeder", curie=CIM.curie('Terminal.NormalHeadFeeder'),
                   model_uri=CIMTBL.terminal__NormalHeadFeeder, domain=None, range=Optional[Union[dict, Feeder]])

slots.terminal__StateShortCircuitResult = Slot(uri=CIM['Terminal.StateShortCircuitResult'], name="terminal__StateShortCircuitResult", curie=CIM.curie('Terminal.StateShortCircuitResult'),
                   model_uri=CIMTBL.terminal__StateShortCircuitResult, domain=None, range=Optional[Union[dict, StateShortCircuitResult]])

slots.terminal__TopologicalNode = Slot(uri=CIM['Terminal.TopologicalNode'], name="terminal__TopologicalNode", curie=CIM.curie('Terminal.TopologicalNode'),
                   model_uri=CIMTBL.terminal__TopologicalNode, domain=None, range=Optional[Union[dict, TopologicalNode]])

slots.terminal__UsagePoint = Slot(uri=CIM['Terminal.UsagePoint'], name="terminal__UsagePoint", curie=CIM.curie('Terminal.UsagePoint'),
                   model_uri=CIMTBL.terminal__UsagePoint, domain=None, range=Optional[Union[dict, UsagePoint]])

slots.thyristorControlledSeriesCompensator__compensationZ = Slot(uri=CIM['ThyristorControlledSeriesCompensator.compensationZ'], name="thyristorControlledSeriesCompensator__compensationZ", curie=CIM.curie('ThyristorControlledSeriesCompensator.compensationZ'),
                   model_uri=CIMTBL.thyristorControlledSeriesCompensator__compensationZ, domain=None, range=Optional[float])

slots.thyristorControlledSeriesCompensator__flexibleCapacitiveZ = Slot(uri=CIM['ThyristorControlledSeriesCompensator.flexibleCapacitiveZ'], name="thyristorControlledSeriesCompensator__flexibleCapacitiveZ", curie=CIM.curie('ThyristorControlledSeriesCompensator.flexibleCapacitiveZ'),
                   model_uri=CIMTBL.thyristorControlledSeriesCompensator__flexibleCapacitiveZ, domain=None, range=Optional[float])

slots.thyristorControlledSeriesCompensator__flexibleInductiveZ = Slot(uri=CIM['ThyristorControlledSeriesCompensator.flexibleInductiveZ'], name="thyristorControlledSeriesCompensator__flexibleInductiveZ", curie=CIM.curie('ThyristorControlledSeriesCompensator.flexibleInductiveZ'),
                   model_uri=CIMTBL.thyristorControlledSeriesCompensator__flexibleInductiveZ, domain=None, range=Optional[float])

slots.thyristorControlledSeriesCompensator__minI = Slot(uri=CIM['ThyristorControlledSeriesCompensator.minI'], name="thyristorControlledSeriesCompensator__minI", curie=CIM.curie('ThyristorControlledSeriesCompensator.minI'),
                   model_uri=CIMTBL.thyristorControlledSeriesCompensator__minI, domain=None, range=Optional[float])

slots.thyristorControlledSeriesCompensator__reconnectionI = Slot(uri=CIM['ThyristorControlledSeriesCompensator.reconnectionI'], name="thyristorControlledSeriesCompensator__reconnectionI", curie=CIM.curie('ThyristorControlledSeriesCompensator.reconnectionI'),
                   model_uri=CIMTBL.thyristorControlledSeriesCompensator__reconnectionI, domain=None, range=Optional[float])

slots.tieFlow__positiveFlowIn = Slot(uri=CIM['TieFlow.positiveFlowIn'], name="tieFlow__positiveFlowIn", curie=CIM.curie('TieFlow.positiveFlowIn'),
                   model_uri=CIMTBL.tieFlow__positiveFlowIn, domain=None, range=Optional[Union[bool, Bool]])

slots.tieFlow__ControlArea = Slot(uri=CIM['TieFlow.ControlArea'], name="tieFlow__ControlArea", curie=CIM.curie('TieFlow.ControlArea'),
                   model_uri=CIMTBL.tieFlow__ControlArea, domain=None, range=Optional[Union[dict, ControlArea]])

slots.tieFlow__Terminal = Slot(uri=CIM['TieFlow.Terminal'], name="tieFlow__Terminal", curie=CIM.curie('TieFlow.Terminal'),
                   model_uri=CIMTBL.tieFlow__Terminal, domain=None, range=Optional[Union[dict, Terminal]])

slots.tieFlow__TieCorridor = Slot(uri=CIM['TieFlow.TieCorridor'], name="tieFlow__TieCorridor", curie=CIM.curie('TieFlow.TieCorridor'),
                   model_uri=CIMTBL.tieFlow__TieCorridor, domain=None, range=Optional[Union[dict, TieCorridor]])

slots.timeInterval__end = Slot(uri=CIM['TimeInterval.end'], name="timeInterval__end", curie=CIM.curie('TimeInterval.end'),
                   model_uri=CIMTBL.timeInterval__end, domain=None, range=Optional[Union[str, XSDTime]])

slots.timeInterval__start = Slot(uri=CIM['TimeInterval.start'], name="timeInterval__start", curie=CIM.curie('TimeInterval.start'),
                   model_uri=CIMTBL.timeInterval__start, domain=None, range=Optional[Union[str, XSDTime]])

slots.topologicalArea__topologyType = Slot(uri=CIM['TopologicalArea.topologyType'], name="topologicalArea__topologyType", curie=CIM.curie('TopologicalArea.topologyType'),
                   model_uri=CIMTBL.topologicalArea__topologyType, domain=None, range=Optional[Union[str, "TopologicalAreaKind"]])

slots.topologicalArea__TopologicalIsland = Slot(uri=CIM['TopologicalArea.TopologicalIsland'], name="topologicalArea__TopologicalIsland", curie=CIM.curie('TopologicalArea.TopologicalIsland'),
                   model_uri=CIMTBL.topologicalArea__TopologicalIsland, domain=None, range=Optional[Union[dict, TopologicalIsland]])

slots.topologicalIsland__AngleRefTopologicalNode = Slot(uri=CIM['TopologicalIsland.AngleRefTopologicalNode'], name="topologicalIsland__AngleRefTopologicalNode", curie=CIM.curie('TopologicalIsland.AngleRefTopologicalNode'),
                   model_uri=CIMTBL.topologicalIsland__AngleRefTopologicalNode, domain=None, range=Optional[Union[dict, TopologicalNode]])

slots.topologicalNode__busName = Slot(uri=CIM['TopologicalNode.busName'], name="topologicalNode__busName", curie=CIM.curie('TopologicalNode.busName'),
                   model_uri=CIMTBL.topologicalNode__busName, domain=None, range=Optional[str])

slots.topologicalNode__busNumber = Slot(uri=CIM['TopologicalNode.busNumber'], name="topologicalNode__busNumber", curie=CIM.curie('TopologicalNode.busNumber'),
                   model_uri=CIMTBL.topologicalNode__busNumber, domain=None, range=Optional[int])

slots.topologicalNode__pInjection = Slot(uri=CIM['TopologicalNode.pInjection'], name="topologicalNode__pInjection", curie=CIM.curie('TopologicalNode.pInjection'),
                   model_uri=CIMTBL.topologicalNode__pInjection, domain=None, range=Optional[float])

slots.topologicalNode__qInjection = Slot(uri=CIM['TopologicalNode.qInjection'], name="topologicalNode__qInjection", curie=CIM.curie('TopologicalNode.qInjection'),
                   model_uri=CIMTBL.topologicalNode__qInjection, domain=None, range=Optional[float])

slots.topologicalNode__AngleRefTopologicalIsland = Slot(uri=CIM['TopologicalNode.AngleRefTopologicalIsland'], name="topologicalNode__AngleRefTopologicalIsland", curie=CIM.curie('TopologicalNode.AngleRefTopologicalIsland'),
                   model_uri=CIMTBL.topologicalNode__AngleRefTopologicalIsland, domain=None, range=Optional[Union[dict, TopologicalIsland]])

slots.topologicalNode__BaseVoltage = Slot(uri=CIM['TopologicalNode.BaseVoltage'], name="topologicalNode__BaseVoltage", curie=CIM.curie('TopologicalNode.BaseVoltage'),
                   model_uri=CIMTBL.topologicalNode__BaseVoltage, domain=None, range=Optional[Union[dict, BaseVoltage]])

slots.topologicalNode__ConnectivityNodeContainer = Slot(uri=CIM['TopologicalNode.ConnectivityNodeContainer'], name="topologicalNode__ConnectivityNodeContainer", curie=CIM.curie('TopologicalNode.ConnectivityNodeContainer'),
                   model_uri=CIMTBL.topologicalNode__ConnectivityNodeContainer, domain=None, range=Optional[Union[dict, ConnectivityNodeContainer]])

slots.topologicalNode__ReportingGroup = Slot(uri=CIM['TopologicalNode.ReportingGroup'], name="topologicalNode__ReportingGroup", curie=CIM.curie('TopologicalNode.ReportingGroup'),
                   model_uri=CIMTBL.topologicalNode__ReportingGroup, domain=None, range=Optional[Union[dict, ReportingGroup]])

slots.topologicalNode__StateShortCircuitResult = Slot(uri=CIM['TopologicalNode.StateShortCircuitResult'], name="topologicalNode__StateShortCircuitResult", curie=CIM.curie('TopologicalNode.StateShortCircuitResult'),
                   model_uri=CIMTBL.topologicalNode__StateShortCircuitResult, domain=None, range=Optional[Union[dict, StateShortCircuitResult]])

slots.topologicalNode__TopologicalIsland = Slot(uri=CIM['TopologicalNode.TopologicalIsland'], name="topologicalNode__TopologicalIsland", curie=CIM.curie('TopologicalNode.TopologicalIsland'),
                   model_uri=CIMTBL.topologicalNode__TopologicalIsland, domain=None, range=Optional[Union[dict, TopologicalIsland]])

slots.transformerCoreAdmittance__b = Slot(uri=CIM['TransformerCoreAdmittance.b'], name="transformerCoreAdmittance__b", curie=CIM.curie('TransformerCoreAdmittance.b'),
                   model_uri=CIMTBL.transformerCoreAdmittance__b, domain=None, range=Optional[float])

slots.transformerCoreAdmittance__b0 = Slot(uri=CIM['TransformerCoreAdmittance.b0'], name="transformerCoreAdmittance__b0", curie=CIM.curie('TransformerCoreAdmittance.b0'),
                   model_uri=CIMTBL.transformerCoreAdmittance__b0, domain=None, range=Optional[float])

slots.transformerCoreAdmittance__g = Slot(uri=CIM['TransformerCoreAdmittance.g'], name="transformerCoreAdmittance__g", curie=CIM.curie('TransformerCoreAdmittance.g'),
                   model_uri=CIMTBL.transformerCoreAdmittance__g, domain=None, range=Optional[float])

slots.transformerCoreAdmittance__g0 = Slot(uri=CIM['TransformerCoreAdmittance.g0'], name="transformerCoreAdmittance__g0", curie=CIM.curie('TransformerCoreAdmittance.g0'),
                   model_uri=CIMTBL.transformerCoreAdmittance__g0, domain=None, range=Optional[float])

slots.transformerCoreAdmittance__TransformerEndInfo = Slot(uri=CIM['TransformerCoreAdmittance.TransformerEndInfo'], name="transformerCoreAdmittance__TransformerEndInfo", curie=CIM.curie('TransformerCoreAdmittance.TransformerEndInfo'),
                   model_uri=CIMTBL.transformerCoreAdmittance__TransformerEndInfo, domain=None, range=Optional[Union[dict, TransformerEndInfo]])

slots.transformerEnd__bmagSat = Slot(uri=CIM['TransformerEnd.bmagSat'], name="transformerEnd__bmagSat", curie=CIM.curie('TransformerEnd.bmagSat'),
                   model_uri=CIMTBL.transformerEnd__bmagSat, domain=None, range=Optional[float])

slots.transformerEnd__endNumber = Slot(uri=CIM['TransformerEnd.endNumber'], name="transformerEnd__endNumber", curie=CIM.curie('TransformerEnd.endNumber'),
                   model_uri=CIMTBL.transformerEnd__endNumber, domain=None, range=Optional[int])

slots.transformerEnd__grounded = Slot(uri=CIM['TransformerEnd.grounded'], name="transformerEnd__grounded", curie=CIM.curie('TransformerEnd.grounded'),
                   model_uri=CIMTBL.transformerEnd__grounded, domain=None, range=Optional[Union[bool, Bool]])

slots.transformerEnd__magBaseU = Slot(uri=CIM['TransformerEnd.magBaseU'], name="transformerEnd__magBaseU", curie=CIM.curie('TransformerEnd.magBaseU'),
                   model_uri=CIMTBL.transformerEnd__magBaseU, domain=None, range=Optional[float])

slots.transformerEnd__magSatFlux = Slot(uri=CIM['TransformerEnd.magSatFlux'], name="transformerEnd__magSatFlux", curie=CIM.curie('TransformerEnd.magSatFlux'),
                   model_uri=CIMTBL.transformerEnd__magSatFlux, domain=None, range=Optional[float])

slots.transformerEnd__rground = Slot(uri=CIM['TransformerEnd.rground'], name="transformerEnd__rground", curie=CIM.curie('TransformerEnd.rground'),
                   model_uri=CIMTBL.transformerEnd__rground, domain=None, range=Optional[float])

slots.transformerEnd__xground = Slot(uri=CIM['TransformerEnd.xground'], name="transformerEnd__xground", curie=CIM.curie('TransformerEnd.xground'),
                   model_uri=CIMTBL.transformerEnd__xground, domain=None, range=Optional[float])

slots.transformerEnd__AdditionalRatioTapChanger = Slot(uri=CIM['TransformerEnd.AdditionalRatioTapChanger'], name="transformerEnd__AdditionalRatioTapChanger", curie=CIM.curie('TransformerEnd.AdditionalRatioTapChanger'),
                   model_uri=CIMTBL.transformerEnd__AdditionalRatioTapChanger, domain=None, range=Optional[Union[dict, RatioTapChanger]])

slots.transformerEnd__BaseVoltage = Slot(uri=CIM['TransformerEnd.BaseVoltage'], name="transformerEnd__BaseVoltage", curie=CIM.curie('TransformerEnd.BaseVoltage'),
                   model_uri=CIMTBL.transformerEnd__BaseVoltage, domain=None, range=Optional[Union[dict, BaseVoltage]])

slots.transformerEnd__CoreAdmittance = Slot(uri=CIM['TransformerEnd.CoreAdmittance'], name="transformerEnd__CoreAdmittance", curie=CIM.curie('TransformerEnd.CoreAdmittance'),
                   model_uri=CIMTBL.transformerEnd__CoreAdmittance, domain=None, range=Optional[Union[dict, TransformerCoreAdmittance]])

slots.transformerEnd__PhaseTapChanger = Slot(uri=CIM['TransformerEnd.PhaseTapChanger'], name="transformerEnd__PhaseTapChanger", curie=CIM.curie('TransformerEnd.PhaseTapChanger'),
                   model_uri=CIMTBL.transformerEnd__PhaseTapChanger, domain=None, range=Optional[Union[dict, PhaseTapChanger]])

slots.transformerEnd__RatioTapChanger = Slot(uri=CIM['TransformerEnd.RatioTapChanger'], name="transformerEnd__RatioTapChanger", curie=CIM.curie('TransformerEnd.RatioTapChanger'),
                   model_uri=CIMTBL.transformerEnd__RatioTapChanger, domain=None, range=Optional[Union[dict, RatioTapChanger]])

slots.transformerEnd__StarImpedance = Slot(uri=CIM['TransformerEnd.StarImpedance'], name="transformerEnd__StarImpedance", curie=CIM.curie('TransformerEnd.StarImpedance'),
                   model_uri=CIMTBL.transformerEnd__StarImpedance, domain=None, range=Optional[Union[dict, TransformerStarImpedance]])

slots.transformerEnd__Terminal = Slot(uri=CIM['TransformerEnd.Terminal'], name="transformerEnd__Terminal", curie=CIM.curie('TransformerEnd.Terminal'),
                   model_uri=CIMTBL.transformerEnd__Terminal, domain=None, range=Optional[Union[dict, Terminal]])

slots.transformerEndInfo__connectionKind = Slot(uri=CIM['TransformerEndInfo.connectionKind'], name="transformerEndInfo__connectionKind", curie=CIM.curie('TransformerEndInfo.connectionKind'),
                   model_uri=CIMTBL.transformerEndInfo__connectionKind, domain=None, range=Optional[Union[str, "WindingConnection"]])

slots.transformerEndInfo__emergencyS = Slot(uri=CIM['TransformerEndInfo.emergencyS'], name="transformerEndInfo__emergencyS", curie=CIM.curie('TransformerEndInfo.emergencyS'),
                   model_uri=CIMTBL.transformerEndInfo__emergencyS, domain=None, range=Optional[float])

slots.transformerEndInfo__endNumber = Slot(uri=CIM['TransformerEndInfo.endNumber'], name="transformerEndInfo__endNumber", curie=CIM.curie('TransformerEndInfo.endNumber'),
                   model_uri=CIMTBL.transformerEndInfo__endNumber, domain=None, range=Optional[int])

slots.transformerEndInfo__insulationU = Slot(uri=CIM['TransformerEndInfo.insulationU'], name="transformerEndInfo__insulationU", curie=CIM.curie('TransformerEndInfo.insulationU'),
                   model_uri=CIMTBL.transformerEndInfo__insulationU, domain=None, range=Optional[float])

slots.transformerEndInfo__phaseAngleClock = Slot(uri=CIM['TransformerEndInfo.phaseAngleClock'], name="transformerEndInfo__phaseAngleClock", curie=CIM.curie('TransformerEndInfo.phaseAngleClock'),
                   model_uri=CIMTBL.transformerEndInfo__phaseAngleClock, domain=None, range=Optional[int])

slots.transformerEndInfo__r = Slot(uri=CIM['TransformerEndInfo.r'], name="transformerEndInfo__r", curie=CIM.curie('TransformerEndInfo.r'),
                   model_uri=CIMTBL.transformerEndInfo__r, domain=None, range=Optional[float])

slots.transformerEndInfo__ratedS = Slot(uri=CIM['TransformerEndInfo.ratedS'], name="transformerEndInfo__ratedS", curie=CIM.curie('TransformerEndInfo.ratedS'),
                   model_uri=CIMTBL.transformerEndInfo__ratedS, domain=None, range=Optional[float])

slots.transformerEndInfo__shortTermS = Slot(uri=CIM['TransformerEndInfo.shortTermS'], name="transformerEndInfo__shortTermS", curie=CIM.curie('TransformerEndInfo.shortTermS'),
                   model_uri=CIMTBL.transformerEndInfo__shortTermS, domain=None, range=Optional[float])

slots.transformerEndInfo__CoreAdmittance = Slot(uri=CIM['TransformerEndInfo.CoreAdmittance'], name="transformerEndInfo__CoreAdmittance", curie=CIM.curie('TransformerEndInfo.CoreAdmittance'),
                   model_uri=CIMTBL.transformerEndInfo__CoreAdmittance, domain=None, range=Optional[Union[dict, TransformerCoreAdmittance]])

slots.transformerEndInfo__TransformerStarImpedance = Slot(uri=CIM['TransformerEndInfo.TransformerStarImpedance'], name="transformerEndInfo__TransformerStarImpedance", curie=CIM.curie('TransformerEndInfo.TransformerStarImpedance'),
                   model_uri=CIMTBL.transformerEndInfo__TransformerStarImpedance, domain=None, range=Optional[Union[dict, TransformerStarImpedance]])

slots.transformerEndInfo__TransformerTankInfo = Slot(uri=CIM['TransformerEndInfo.TransformerTankInfo'], name="transformerEndInfo__TransformerTankInfo", curie=CIM.curie('TransformerEndInfo.TransformerTankInfo'),
                   model_uri=CIMTBL.transformerEndInfo__TransformerTankInfo, domain=None, range=Optional[Union[dict, TransformerTankInfo]])

slots.transformerMeshImpedance__r = Slot(uri=CIM['TransformerMeshImpedance.r'], name="transformerMeshImpedance__r", curie=CIM.curie('TransformerMeshImpedance.r'),
                   model_uri=CIMTBL.transformerMeshImpedance__r, domain=None, range=Optional[float])

slots.transformerMeshImpedance__r0 = Slot(uri=CIM['TransformerMeshImpedance.r0'], name="transformerMeshImpedance__r0", curie=CIM.curie('TransformerMeshImpedance.r0'),
                   model_uri=CIMTBL.transformerMeshImpedance__r0, domain=None, range=Optional[float])

slots.transformerMeshImpedance__x = Slot(uri=CIM['TransformerMeshImpedance.x'], name="transformerMeshImpedance__x", curie=CIM.curie('TransformerMeshImpedance.x'),
                   model_uri=CIMTBL.transformerMeshImpedance__x, domain=None, range=Optional[float])

slots.transformerMeshImpedance__x0 = Slot(uri=CIM['TransformerMeshImpedance.x0'], name="transformerMeshImpedance__x0", curie=CIM.curie('TransformerMeshImpedance.x0'),
                   model_uri=CIMTBL.transformerMeshImpedance__x0, domain=None, range=Optional[float])

slots.transformerMeshImpedance__FromTransformerEnd = Slot(uri=CIM['TransformerMeshImpedance.FromTransformerEnd'], name="transformerMeshImpedance__FromTransformerEnd", curie=CIM.curie('TransformerMeshImpedance.FromTransformerEnd'),
                   model_uri=CIMTBL.transformerMeshImpedance__FromTransformerEnd, domain=None, range=Optional[Union[dict, TransformerEnd]])

slots.transformerMeshImpedance__FromTransformerEndInfo = Slot(uri=CIM['TransformerMeshImpedance.FromTransformerEndInfo'], name="transformerMeshImpedance__FromTransformerEndInfo", curie=CIM.curie('TransformerMeshImpedance.FromTransformerEndInfo'),
                   model_uri=CIMTBL.transformerMeshImpedance__FromTransformerEndInfo, domain=None, range=Optional[Union[dict, TransformerEndInfo]])

slots.transformerMeshImpedance__ToTransformerEnd = Slot(uri=CIM['TransformerMeshImpedance.ToTransformerEnd'], name="transformerMeshImpedance__ToTransformerEnd", curie=CIM.curie('TransformerMeshImpedance.ToTransformerEnd'),
                   model_uri=CIMTBL.transformerMeshImpedance__ToTransformerEnd, domain=None, range=Optional[Union[Union[dict, TransformerEnd], list[Union[dict, TransformerEnd]]]])

slots.transformerMeshImpedance__ToTransformerEndInfos = Slot(uri=CIM['TransformerMeshImpedance.ToTransformerEndInfos'], name="transformerMeshImpedance__ToTransformerEndInfos", curie=CIM.curie('TransformerMeshImpedance.ToTransformerEndInfos'),
                   model_uri=CIMTBL.transformerMeshImpedance__ToTransformerEndInfos, domain=None, range=Optional[Union[Union[dict, TransformerEndInfo], list[Union[dict, TransformerEndInfo]]]])

slots.transformerStarImpedance__r = Slot(uri=CIM['TransformerStarImpedance.r'], name="transformerStarImpedance__r", curie=CIM.curie('TransformerStarImpedance.r'),
                   model_uri=CIMTBL.transformerStarImpedance__r, domain=None, range=Optional[float])

slots.transformerStarImpedance__r0 = Slot(uri=CIM['TransformerStarImpedance.r0'], name="transformerStarImpedance__r0", curie=CIM.curie('TransformerStarImpedance.r0'),
                   model_uri=CIMTBL.transformerStarImpedance__r0, domain=None, range=Optional[float])

slots.transformerStarImpedance__x = Slot(uri=CIM['TransformerStarImpedance.x'], name="transformerStarImpedance__x", curie=CIM.curie('TransformerStarImpedance.x'),
                   model_uri=CIMTBL.transformerStarImpedance__x, domain=None, range=Optional[float])

slots.transformerStarImpedance__x0 = Slot(uri=CIM['TransformerStarImpedance.x0'], name="transformerStarImpedance__x0", curie=CIM.curie('TransformerStarImpedance.x0'),
                   model_uri=CIMTBL.transformerStarImpedance__x0, domain=None, range=Optional[float])

slots.transformerStarImpedance__TransformerEndInfo = Slot(uri=CIM['TransformerStarImpedance.TransformerEndInfo'], name="transformerStarImpedance__TransformerEndInfo", curie=CIM.curie('TransformerStarImpedance.TransformerEndInfo'),
                   model_uri=CIMTBL.transformerStarImpedance__TransformerEndInfo, domain=None, range=Optional[Union[dict, TransformerEndInfo]])

slots.transformerTank__PowerTransformer = Slot(uri=CIM['TransformerTank.PowerTransformer'], name="transformerTank__PowerTransformer", curie=CIM.curie('TransformerTank.PowerTransformer'),
                   model_uri=CIMTBL.transformerTank__PowerTransformer, domain=None, range=Optional[Union[dict, PowerTransformer]])

slots.transformerTank__TransformerTankInfo = Slot(uri=CIM['TransformerTank.TransformerTankInfo'], name="transformerTank__TransformerTankInfo", curie=CIM.curie('TransformerTank.TransformerTankInfo'),
                   model_uri=CIMTBL.transformerTank__TransformerTankInfo, domain=None, range=Optional[Union[dict, TransformerTankInfo]])

slots.transformerTankEnd__phases = Slot(uri=CIM['TransformerTankEnd.phases'], name="transformerTankEnd__phases", curie=CIM.curie('TransformerTankEnd.phases'),
                   model_uri=CIMTBL.transformerTankEnd__phases, domain=None, range=Optional[Union[str, "PhaseCode"]])

slots.transformerTankEnd__TransformerTank = Slot(uri=CIM['TransformerTankEnd.TransformerTank'], name="transformerTankEnd__TransformerTank", curie=CIM.curie('TransformerTankEnd.TransformerTank'),
                   model_uri=CIMTBL.transformerTankEnd__TransformerTank, domain=None, range=Optional[Union[dict, TransformerTank]])

slots.transformerTankInfo__PowerTransformerInfo = Slot(uri=CIM['TransformerTankInfo.PowerTransformerInfo'], name="transformerTankInfo__PowerTransformerInfo", curie=CIM.curie('TransformerTankInfo.PowerTransformerInfo'),
                   model_uri=CIMTBL.transformerTankInfo__PowerTransformerInfo, domain=None, range=Optional[Union[dict, PowerTransformerInfo]])

slots.vehicleInfo__make = Slot(uri=CIM['VehicleInfo.make'], name="vehicleInfo__make", curie=CIM.curie('VehicleInfo.make'),
                   model_uri=CIMTBL.vehicleInfo__make, domain=None, range=Optional[str])

slots.vehicleInfo__model = Slot(uri=CIM['VehicleInfo.model'], name="vehicleInfo__model", curie=CIM.curie('VehicleInfo.model'),
                   model_uri=CIMTBL.vehicleInfo__model, domain=None, range=Optional[str])

slots.vehicleInfo__vehicleType = Slot(uri=CIM['VehicleInfo.vehicleType'], name="vehicleInfo__vehicleType", curie=CIM.curie('VehicleInfo.vehicleType'),
                   model_uri=CIMTBL.vehicleInfo__vehicleType, domain=None, range=Optional[str])

slots.vehicleInfo__year = Slot(uri=CIM['VehicleInfo.year'], name="vehicleInfo__year", curie=CIM.curie('VehicleInfo.year'),
                   model_uri=CIMTBL.vehicleInfo__year, domain=None, range=Optional[str])

slots.voltageAngleLimit__isFlowToRefTerminal = Slot(uri=CIM['VoltageAngleLimit.isFlowToRefTerminal'], name="voltageAngleLimit__isFlowToRefTerminal", curie=CIM.curie('VoltageAngleLimit.isFlowToRefTerminal'),
                   model_uri=CIMTBL.voltageAngleLimit__isFlowToRefTerminal, domain=None, range=Optional[Union[bool, Bool]])

slots.voltageAngleLimit__normalValue = Slot(uri=CIM['VoltageAngleLimit.normalValue'], name="voltageAngleLimit__normalValue", curie=CIM.curie('VoltageAngleLimit.normalValue'),
                   model_uri=CIMTBL.voltageAngleLimit__normalValue, domain=None, range=Optional[float])

slots.voltageAngleLimit__value = Slot(uri=CIM['VoltageAngleLimit.value'], name="voltageAngleLimit__value", curie=CIM.curie('VoltageAngleLimit.value'),
                   model_uri=CIMTBL.voltageAngleLimit__value, domain=None, range=Optional[float])

slots.voltageAngleLimit__AngleReferenceTerminal = Slot(uri=CIM['VoltageAngleLimit.AngleReferenceTerminal'], name="voltageAngleLimit__AngleReferenceTerminal", curie=CIM.curie('VoltageAngleLimit.AngleReferenceTerminal'),
                   model_uri=CIMTBL.voltageAngleLimit__AngleReferenceTerminal, domain=None, range=Optional[Union[dict, Terminal]])

slots.voltageControlZone__BusbarSection = Slot(uri=CIM['VoltageControlZone.BusbarSection'], name="voltageControlZone__BusbarSection", curie=CIM.curie('VoltageControlZone.BusbarSection'),
                   model_uri=CIMTBL.voltageControlZone__BusbarSection, domain=None, range=Optional[Union[dict, BusbarSection]])

slots.voltageControlZone__RegulationSchedule = Slot(uri=CIM['VoltageControlZone.RegulationSchedule'], name="voltageControlZone__RegulationSchedule", curie=CIM.curie('VoltageControlZone.RegulationSchedule'),
                   model_uri=CIMTBL.voltageControlZone__RegulationSchedule, domain=None, range=Optional[Union[dict, RegulationSchedule]])

slots.voltageInjectionControlFunction__targetValue = Slot(uri=CIM['VoltageInjectionControlFunction.targetValue'], name="voltageInjectionControlFunction__targetValue", curie=CIM.curie('VoltageInjectionControlFunction.targetValue'),
                   model_uri=CIMTBL.voltageInjectionControlFunction__targetValue, domain=None, range=Optional[float])

slots.voltageLevel__highVoltageLimit = Slot(uri=CIM['VoltageLevel.highVoltageLimit'], name="voltageLevel__highVoltageLimit", curie=CIM.curie('VoltageLevel.highVoltageLimit'),
                   model_uri=CIMTBL.voltageLevel__highVoltageLimit, domain=None, range=Optional[float])

slots.voltageLevel__lowVoltageLimit = Slot(uri=CIM['VoltageLevel.lowVoltageLimit'], name="voltageLevel__lowVoltageLimit", curie=CIM.curie('VoltageLevel.lowVoltageLimit'),
                   model_uri=CIMTBL.voltageLevel__lowVoltageLimit, domain=None, range=Optional[float])

slots.voltageLevel__BaseVoltage = Slot(uri=CIM['VoltageLevel.BaseVoltage'], name="voltageLevel__BaseVoltage", curie=CIM.curie('VoltageLevel.BaseVoltage'),
                   model_uri=CIMTBL.voltageLevel__BaseVoltage, domain=None, range=Optional[Union[dict, BaseVoltage]])

slots.voltageLevel__Substation = Slot(uri=CIM['VoltageLevel.Substation'], name="voltageLevel__Substation", curie=CIM.curie('VoltageLevel.Substation'),
                   model_uri=CIMTBL.voltageLevel__Substation, domain=None, range=Optional[Union[dict, Substation]])

slots.voltageLimit__normalValue = Slot(uri=CIM['VoltageLimit.normalValue'], name="voltageLimit__normalValue", curie=CIM.curie('VoltageLimit.normalValue'),
                   model_uri=CIMTBL.voltageLimit__normalValue, domain=None, range=Optional[float])

slots.voltageLimit__value = Slot(uri=CIM['VoltageLimit.value'], name="voltageLimit__value", curie=CIM.curie('VoltageLimit.value'),
                   model_uri=CIMTBL.voltageLimit__value, domain=None, range=Optional[float])

slots.windGeneratingUnit__windGenUnitType = Slot(uri=CIM['WindGeneratingUnit.windGenUnitType'], name="windGeneratingUnit__windGenUnitType", curie=CIM.curie('WindGeneratingUnit.windGenUnitType'),
                   model_uri=CIMTBL.windGeneratingUnit__windGenUnitType, domain=None, range=Optional[Union[str, "WindGenUnitKind"]])

slots.windGeneratingUnit__WindPowerPlant = Slot(uri=CIM['WindGeneratingUnit.WindPowerPlant'], name="windGeneratingUnit__WindPowerPlant", curie=CIM.curie('WindGeneratingUnit.WindPowerPlant'),
                   model_uri=CIMTBL.windGeneratingUnit__WindPowerPlant, domain=None, range=Optional[Union[dict, WindPowerPlant]])

slots.wireInfo__constructionKind = Slot(uri=CIM['WireInfo.constructionKind'], name="wireInfo__constructionKind", curie=CIM.curie('WireInfo.constructionKind'),
                   model_uri=CIMTBL.wireInfo__constructionKind, domain=None, range=Optional[Union[str, "WireMaterialKind"]])

slots.wireInfo__coreRadius = Slot(uri=CIM['WireInfo.coreRadius'], name="wireInfo__coreRadius", curie=CIM.curie('WireInfo.coreRadius'),
                   model_uri=CIMTBL.wireInfo__coreRadius, domain=None, range=Optional[float])

slots.wireInfo__coreStrandCount = Slot(uri=CIM['WireInfo.coreStrandCount'], name="wireInfo__coreStrandCount", curie=CIM.curie('WireInfo.coreStrandCount'),
                   model_uri=CIMTBL.wireInfo__coreStrandCount, domain=None, range=Optional[int])

slots.wireInfo__coreStrandRadius = Slot(uri=CIM['WireInfo.coreStrandRadius'], name="wireInfo__coreStrandRadius", curie=CIM.curie('WireInfo.coreStrandRadius'),
                   model_uri=CIMTBL.wireInfo__coreStrandRadius, domain=None, range=Optional[float])

slots.wireInfo__gmr = Slot(uri=CIM['WireInfo.gmr'], name="wireInfo__gmr", curie=CIM.curie('WireInfo.gmr'),
                   model_uri=CIMTBL.wireInfo__gmr, domain=None, range=Optional[float])

slots.wireInfo__insulated = Slot(uri=CIM['WireInfo.insulated'], name="wireInfo__insulated", curie=CIM.curie('WireInfo.insulated'),
                   model_uri=CIMTBL.wireInfo__insulated, domain=None, range=Optional[Union[bool, Bool]])

slots.wireInfo__insulationMaterial = Slot(uri=CIM['WireInfo.insulationMaterial'], name="wireInfo__insulationMaterial", curie=CIM.curie('WireInfo.insulationMaterial'),
                   model_uri=CIMTBL.wireInfo__insulationMaterial, domain=None, range=Optional[Union[str, "WireInsulationKind"]])

slots.wireInfo__insulationThickness = Slot(uri=CIM['WireInfo.insulationThickness'], name="wireInfo__insulationThickness", curie=CIM.curie('WireInfo.insulationThickness'),
                   model_uri=CIMTBL.wireInfo__insulationThickness, domain=None, range=Optional[float])

slots.wireInfo__radius = Slot(uri=CIM['WireInfo.radius'], name="wireInfo__radius", curie=CIM.curie('WireInfo.radius'),
                   model_uri=CIMTBL.wireInfo__radius, domain=None, range=Optional[float])

slots.wireInfo__ratedStrength = Slot(uri=CIM['WireInfo.ratedStrength'], name="wireInfo__ratedStrength", curie=CIM.curie('WireInfo.ratedStrength'),
                   model_uri=CIMTBL.wireInfo__ratedStrength, domain=None, range=Optional[float])

slots.wireInfo__sizeDescription = Slot(uri=CIM['WireInfo.sizeDescription'], name="wireInfo__sizeDescription", curie=CIM.curie('WireInfo.sizeDescription'),
                   model_uri=CIMTBL.wireInfo__sizeDescription, domain=None, range=Optional[str])

slots.wireInfo__strandCount = Slot(uri=CIM['WireInfo.strandCount'], name="wireInfo__strandCount", curie=CIM.curie('WireInfo.strandCount'),
                   model_uri=CIMTBL.wireInfo__strandCount, domain=None, range=Optional[int])

slots.wireInfo__strandRadius = Slot(uri=CIM['WireInfo.strandRadius'], name="wireInfo__strandRadius", curie=CIM.curie('WireInfo.strandRadius'),
                   model_uri=CIMTBL.wireInfo__strandRadius, domain=None, range=Optional[float])

slots.wirePhaseInfo__phaseInfo = Slot(uri=CIM['WirePhaseInfo.phaseInfo'], name="wirePhaseInfo__phaseInfo", curie=CIM.curie('WirePhaseInfo.phaseInfo'),
                   model_uri=CIMTBL.wirePhaseInfo__phaseInfo, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.wirePhaseInfo__WireAssemblyInfo = Slot(uri=CIM['WirePhaseInfo.WireAssemblyInfo'], name="wirePhaseInfo__WireAssemblyInfo", curie=CIM.curie('WirePhaseInfo.WireAssemblyInfo'),
                   model_uri=CIMTBL.wirePhaseInfo__WireAssemblyInfo, domain=None, range=Optional[Union[dict, WireAssemblyInfo]])

slots.wirePhaseInfo__WireInfo = Slot(uri=CIM['WirePhaseInfo.WireInfo'], name="wirePhaseInfo__WireInfo", curie=CIM.curie('WirePhaseInfo.WireInfo'),
                   model_uri=CIMTBL.wirePhaseInfo__WireInfo, domain=None, range=Optional[Union[dict, WireInfo]])

slots.wirePhaseInfo__WirePosition = Slot(uri=CIM['WirePhaseInfo.WirePosition'], name="wirePhaseInfo__WirePosition", curie=CIM.curie('WirePhaseInfo.WirePosition'),
                   model_uri=CIMTBL.wirePhaseInfo__WirePosition, domain=None, range=Optional[Union[dict, WirePosition]])

slots.wirePosition__phase = Slot(uri=CIM['WirePosition.phase'], name="wirePosition__phase", curie=CIM.curie('WirePosition.phase'),
                   model_uri=CIMTBL.wirePosition__phase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.wirePosition__sequenceNumber = Slot(uri=CIM['WirePosition.sequenceNumber'], name="wirePosition__sequenceNumber", curie=CIM.curie('WirePosition.sequenceNumber'),
                   model_uri=CIMTBL.wirePosition__sequenceNumber, domain=None, range=Optional[int])

slots.wirePosition__xCoord = Slot(uri=CIM['WirePosition.xCoord'], name="wirePosition__xCoord", curie=CIM.curie('WirePosition.xCoord'),
                   model_uri=CIMTBL.wirePosition__xCoord, domain=None, range=Optional[float])

slots.wirePosition__yCoord = Slot(uri=CIM['WirePosition.yCoord'], name="wirePosition__yCoord", curie=CIM.curie('WirePosition.yCoord'),
                   model_uri=CIMTBL.wirePosition__yCoord, domain=None, range=Optional[float])

slots.wirePosition__WireSpacingInfo = Slot(uri=CIM['WirePosition.WireSpacingInfo'], name="wirePosition__WireSpacingInfo", curie=CIM.curie('WirePosition.WireSpacingInfo'),
                   model_uri=CIMTBL.wirePosition__WireSpacingInfo, domain=None, range=Optional[Union[dict, WireSpacingInfo]])

slots.wireSegmentPhase__phase = Slot(uri=CIM['WireSegmentPhase.phase'], name="wireSegmentPhase__phase", curie=CIM.curie('WireSegmentPhase.phase'),
                   model_uri=CIMTBL.wireSegmentPhase__phase, domain=None, range=Optional[Union[str, "SinglePhaseKind"]])

slots.wireSegmentPhase__sequenceNumber = Slot(uri=CIM['WireSegmentPhase.sequenceNumber'], name="wireSegmentPhase__sequenceNumber", curie=CIM.curie('WireSegmentPhase.sequenceNumber'),
                   model_uri=CIMTBL.wireSegmentPhase__sequenceNumber, domain=None, range=Optional[int])

slots.wireSegmentPhase__WireSegment = Slot(uri=CIM['WireSegmentPhase.WireSegment'], name="wireSegmentPhase__WireSegment", curie=CIM.curie('WireSegmentPhase.WireSegment'),
                   model_uri=CIMTBL.wireSegmentPhase__WireSegment, domain=None, range=Optional[Union[dict, WireSegment]])

slots.wireSpacingInfo__isCable = Slot(uri=CIM['WireSpacingInfo.isCable'], name="wireSpacingInfo__isCable", curie=CIM.curie('WireSpacingInfo.isCable'),
                   model_uri=CIMTBL.wireSpacingInfo__isCable, domain=None, range=Optional[Union[bool, Bool]])

slots.wireSpacingInfo__phaseWireCount = Slot(uri=CIM['WireSpacingInfo.phaseWireCount'], name="wireSpacingInfo__phaseWireCount", curie=CIM.curie('WireSpacingInfo.phaseWireCount'),
                   model_uri=CIMTBL.wireSpacingInfo__phaseWireCount, domain=None, range=Optional[int])

slots.wireSpacingInfo__phaseWireSpacing = Slot(uri=CIM['WireSpacingInfo.phaseWireSpacing'], name="wireSpacingInfo__phaseWireSpacing", curie=CIM.curie('WireSpacingInfo.phaseWireSpacing'),
                   model_uri=CIMTBL.wireSpacingInfo__phaseWireSpacing, domain=None, range=Optional[float])

slots.wireSpacingInfo__usage = Slot(uri=CIM['WireSpacingInfo.usage'], name="wireSpacingInfo__usage", curie=CIM.curie('WireSpacingInfo.usage'),
                   model_uri=CIMTBL.wireSpacingInfo__usage, domain=None, range=Optional[Union[str, "WireUsageKind"]])

slots.wireSpacingInfo__DuctBank = Slot(uri=CIM['WireSpacingInfo.DuctBank'], name="wireSpacingInfo__DuctBank", curie=CIM.curie('WireSpacingInfo.DuctBank'),
                   model_uri=CIMTBL.wireSpacingInfo__DuctBank, domain=None, range=Optional[Union[dict, DuctBank]])

slots.twoNodeMixin__node1 = Slot(uri=CIMTBL.node1, name="twoNodeMixin__node1", curie=CIMTBL.curie('node1'),
                   model_uri=CIMTBL.twoNodeMixin__node1, domain=None, range=Optional[str])

slots.twoNodeMixin__node2 = Slot(uri=CIMTBL.node2, name="twoNodeMixin__node2", curie=CIMTBL.curie('node2'),
                   model_uri=CIMTBL.twoNodeMixin__node2, domain=None, range=Optional[str])

slots.twoBusMixin__bus1 = Slot(uri=CIMTBL.bus1, name="twoBusMixin__bus1", curie=CIMTBL.curie('bus1'),
                   model_uri=CIMTBL.twoBusMixin__bus1, domain=None, range=Optional[str])

slots.twoBusMixin__bus2 = Slot(uri=CIMTBL.bus2, name="twoBusMixin__bus2", curie=CIMTBL.curie('bus2'),
                   model_uri=CIMTBL.twoBusMixin__bus2, domain=None, range=Optional[str])

slots.oneNodeMixin__node = Slot(uri=CIMTBL.node, name="oneNodeMixin__node", curie=CIMTBL.curie('node'),
                   model_uri=CIMTBL.oneNodeMixin__node, domain=None, range=Optional[str])

slots.phasesMixin__phases = Slot(uri=CIMTBL.phases, name="phasesMixin__phases", curie=CIMTBL.curie('phases'),
                   model_uri=CIMTBL.phasesMixin__phases, domain=None, range=Optional[str])

slots.templateRefMixin__Template = Slot(uri=CIMTBL.Template, name="templateRefMixin__Template", curie=CIMTBL.curie('Template'),
                   model_uri=CIMTBL.templateRefMixin__Template, domain=None, range=Optional[str])

