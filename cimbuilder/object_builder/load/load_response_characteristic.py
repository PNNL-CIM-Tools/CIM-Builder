import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
from cimtables import graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class LoadResponseCharacteristicBuilder(ObjectBuilder):
    """
    Builder for the voltage dependence of loads (ZIP or exponential), shared by every
    EnergyConsumer with the same response. Builder functions to be called in the following order:
    * create() - instantiate the LoadResponseCharacteristic, e.g. zip_constant_pq
    * add_electrical() - ZIP fractions or voltage exponents
    Link loads with EnergyConsumerBuilder.add_electrical(LoadResponse=...)
    """

    cim_class_name = "LoadResponseCharacteristic"

    def add_electrical(
        self,
        response: EL_BAL.LoadResponseCharacteristic,
        *,
        exponentModel: bool,
        pConstantImpedance: float | None = None,
        pConstantCurrent: float | None = None,
        pConstantPower: float | None = None,
        qConstantImpedance: float | None = None,
        qConstantCurrent: float | None = None,
        qConstantPower: float | None = None,
        pVoltageExponent: float | None = None,
        qVoltageExponent: float | None = None,
    ) -> EL_BAL.LoadResponseCharacteristic:
        """
        Adds ZIP fractions (exponentModel=False) or voltage exponents (exponentModel=True)
        * exponentModel: boolean, the exponents are used if true, the ZIP fractions if false
        * pConstantImpedance: fraction of active power that is constant impedance, float (e.g. 0.4)
        * pConstantCurrent: fraction of active power that is constant current, float
        * pConstantPower: fraction of active power that is constant power, float
        * qConstantImpedance: fraction of reactive power that is constant impedance, float
        * qConstantCurrent: fraction of reactive power that is constant current, float
        * qConstantPower: fraction of reactive power that is constant power, float
        * pVoltageExponent: exponent of the active power voltage dependence, float
        * qVoltageExponent: exponent of the reactive power voltage dependence, float
        The p and q fractions each sum to 1
        """
        graph_write.set_attr(response, EL_BAL, "exponentModel", exponentModel)
        graph_write.set_attr(response, EL_BAL, "pConstantImpedance", pConstantImpedance)
        graph_write.set_attr(response, EL_BAL, "pConstantCurrent", pConstantCurrent)
        graph_write.set_attr(response, EL_BAL, "pConstantPower", pConstantPower)
        graph_write.set_attr(response, EL_BAL, "qConstantImpedance", qConstantImpedance)
        graph_write.set_attr(response, EL_BAL, "qConstantCurrent", qConstantCurrent)
        graph_write.set_attr(response, EL_BAL, "qConstantPower", qConstantPower)
        graph_write.set_attr(response, EL_BAL, "pVoltageExponent", pVoltageExponent)
        graph_write.set_attr(response, EL_BAL, "qVoltageExponent", qVoltageExponent)
        return response
