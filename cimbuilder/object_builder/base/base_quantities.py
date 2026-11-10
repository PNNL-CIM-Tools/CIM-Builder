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

    def create(
        self,
        *,
        mRID: str | None = None,
        name: str | None = None,
        identifier: str | None = None,
        description: str | None = None,
        basePower: float | Qty,
    ) -> CN.BasePower:
        """
        Adds the system base that every later pu/percent value with base='system' converts against
        * basePower: system base apparent power, float in VA or Qty('MVA')
        Sets network.base_power, so create it before any per-unit values
        """
        cn: CN = self.cim  # type:ignore
        if identifier is not None:
            raise ValueError("BasePower is an IdentifiedObject: pass mRID, not identifier")
        # basePower must be set before the graph add, which reads it into network.base_power
        base_power = cn.BasePower(mRID=mRID, name=name, description=description)
        graph_write.set_attr(base_power, CN, "basePower", basePower)
        graph_write.add_to_graph(self.network, base_power)
        return base_power
