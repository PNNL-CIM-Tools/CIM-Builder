import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
from cimtables import Qty, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class BaseVoltageBuilder(ObjectBuilder):
    cim_class_name = "BaseVoltage"

    def add_connectivity(
        self, base_volt: CN.BaseVoltage, *, nominalVoltage: float | Qty
    ) -> CN.BaseVoltage:

        graph_write.set_attr(base_volt, CN, "nominalVoltage", nominalVoltage)

        return base_volt

class BaseFrequencyBuilder(ObjectBuilder):
    cim_class_name = "BaseFrequency"

    def add_connectivity(
        self, base_freq: CN.BaseFrequency, *, frequency: float | Qty = 60
    ) -> CN.BaseFrequency:

        graph_write.set_attr(base_freq, CN, "frequency", frequency)

        return base_freq

class BasePowerBuilder(ObjectBuilder):
    cim_class_name = "BasePower"

    def add_connectivity(
        self, base_power: CN.BasePower, *, basePower: float | Qty
    ) -> CN.BasePower:

        graph_write.set_attr(base_power, CN, "basePower", basePower)

        return base_power