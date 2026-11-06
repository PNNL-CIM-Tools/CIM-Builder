import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
from cimtables import Qty, graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder


class BaseVoltageBuilder(ObjectBuilder):
    cim_class_name = "BaseVoltage"

    def create(
        self,
        *,
        mRID: str | None = None,
        name: str | None = None,
        identifier: str | None = None,
        description: str | None = None,
        nominalVoltage: float | Qty,
    ) -> CN.BaseVoltage:
        base_volt: CN.BaseVoltage = super().create(
            mRID=mRID, name=name, identifier=identifier, description=description
        )  # type:ignore
        graph_write.set_attr(base_volt, CN, "nominalVoltage", nominalVoltage)

        return base_volt


class BaseFrequencyBuilder(ObjectBuilder):
    cim_class_name = "BaseFrequency"

    def create(
        self,
        *,
        mRID: str | None = None,
        name: str | None = None,
        identifier: str | None = None,
        description: str | None = None,
        frequency: float | Qty = 60,
    ) -> CN.BaseFrequency:
        base_freq: CN.BaseFrequency = super().create(
            mRID=mRID, name=name, identifier=identifier, description=description
        )  # type:ignore
        graph_write.set_attr(base_freq, CN, "frequency", frequency)

        return base_freq


class BasePowerBuilder(ObjectBuilder):
    cim_class_name = "BasePower"

    def add_connectivity(
        self, base_power: CN.BasePower, *, basePower: float | Qty
    ) -> CN.BasePower:

        graph_write.set_attr(base_power, CN, "basePower", basePower)

        return base_power
