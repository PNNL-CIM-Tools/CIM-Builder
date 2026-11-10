import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.protection import UnderFrequencyProtectionFunctionBlockBuilder


def test_add_protection(network, container):
    builder = UnderFrequencyProtectionFunctionBlockBuilder(network, container)
    ufls = builder.create(mRID="ufls_59_3_brk_1", name="ufls_59.3")

    builder.add_protection(ufls, operateValue=Qty(59.3, "Hz"))

    assert type(ufls).__name__ == "UnderFrequencyProtectionFunctionBlock"
    assert float(ufls.operateValue.to("Hz")) == pytest.approx(59.3)
