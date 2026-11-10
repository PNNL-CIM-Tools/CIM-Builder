import cimprofiles.cim18.cim18v17 as cim

from cimbuilder.object_builder.line import WireConfigurationBuilder, XYSpacingBuilder


def test_wire_configuration_add_electrical_per_length_impedance(network, container):
    builder = WireConfigurationBuilder(network=network, container=container)
    config = builder.create(mRID="wc1")
    pli = cim.PerLengthSequenceImpedance(mRID="pli1")
    network.add_to_graph(pli)

    builder.add_electrical(config, PerLengthImpedance="pli1")
    assert config.PerLengthImpedance is pli


def test_wire_configuration_add_electrical_earth_resistivity(network, container):
    builder = WireConfigurationBuilder(network=network, container=container)
    config = builder.create(mRID="wc1")
    er = cim.EarthResistivity(mRID="er1")
    network.add_to_graph(er)

    builder.add_electrical(config, EarthResistivity="er1")

    assert config.EarthResistivity is er
    assert config.PerLengthImpedance is None


def test_wire_configuration_create_construction(network, container):
    xy_builder = XYSpacingBuilder(network=network, container=container)
    spacing = xy_builder.create(mRID="xy1")

    builder = WireConfigurationBuilder(network=network, container=container)
    config = builder.create(mRID="wc1", numberOfPhases=3, WireSpacing=spacing.mRID)
    assert config.numberOfPhases == 3
    assert config.WireSpacing is spacing


def test_wire_configuration_add_wire_sequence_configuration(network, container):
    builder = WireConfigurationBuilder(network=network, container=container)
    config = builder.create(mRID="wc_601")
    wire = cim.OverheadWireInfo(mRID="wire_556500_26_7")
    network.add_to_graph(wire)

    _, wire_sequence = builder.add_wire_sequence_configuration(config, sequenceNumber=2, WireInfo=wire.mRID)
    assert wire_sequence.mRID == "wc_601_2"
    assert wire_sequence.sequenceNumber == 2
    assert wire_sequence.WireInfo is wire
    assert config.WireSequence == [wire_sequence]
