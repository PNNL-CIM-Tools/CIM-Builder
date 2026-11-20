from datetime import datetime, timedelta, timezone

import pyarrow as pa
import pytest
from cimtables.units import Qty

from cimbuilder.object_builder.inverter import PhotoVoltaicUnitBuilder
from cimbuilder.object_builder.load import EnergyConsumerBuilder
from cimbuilder.object_builder.schedule import (
    TIME_POINT_SCHEMA,
    EnergyConnectionScheduleBuilder,
)

HOURS = [datetime(2020, 1, 1) + timedelta(hours=h) for h in range(3)]


def _schedule(network, container):
    consumer = EnergyConsumerBuilder(network=network, container=container).create(mRID="ld_1", name="1")
    builder = EnergyConnectionScheduleBuilder(network=network, container=container)
    schedule = builder.create(mRID="ld_1_pq", name="ls1")
    builder.add_schedule(schedule, EnergyConnection=consumer.mRID, timeSeriesKind="schedule",
                         interpolationKind="previous", actionMethod="yearly")
    return builder, schedule, consumer


def test_add_schedule_links_the_consumer_and_sets_the_kinds(network, container):
    _, schedule, consumer = _schedule(network, container)
    assert schedule.EnergyConnection is consumer
    assert schedule in consumer.EnergyConnectionSchedule
    assert schedule.timeSeriesKind.value == "schedule"
    assert schedule.interpolationKind.value == "previous"
    assert schedule.actionMethod == "yearly"


def test_add_schedule_raises_on_an_unknown_connection(network, container):
    builder = EnergyConnectionScheduleBuilder(network=network, container=container)
    schedule = builder.create(mRID="orphan")
    with pytest.raises(ValueError, match="EnergyConnection 'ld_x' not found"):
        builder.add_schedule(schedule, EnergyConnection="ld_x")


def test_time_points_are_rows_in_si_not_graph_objects(network, container):
    builder, schedule, _ = _schedule(network, container)
    objects_before = sum(len(objects) for objects in network.graph.values())

    table = builder.time_points(schedule, times=list(reversed(HOURS)), p=[3.0, 2.0, 1.0], q=[0.3, 0.2, 0.1],
                                p_unit="kW", q_unit="kVAr")

    assert sum(len(objects) for objects in network.graph.values()) == objects_before
    assert table.schema.equals(TIME_POINT_SCHEMA, check_metadata=True)
    assert table.column("EnergyConnectionSchedule").to_pylist() == [schedule.uri()] * 3
    assert [t.replace(tzinfo=None) for t in table.column("atTime").to_pylist()] == HOURS  # sorted, naive = UTC
    assert table.column("p").to_pylist() == [1000.0, 2000.0, 3000.0]
    assert table.column("q").to_pylist() == pytest.approx([100.0, 200.0, 300.0])


def test_time_points_with_only_p_leave_q_null_and_convert_zones_to_utc(network, container):
    builder, schedule, _ = _schedule(network, container)
    central = timezone(timedelta(hours=-6))
    table = builder.time_points(schedule, times=[datetime(2020, 1, 1, tzinfo=central)], p=[5.0])
    assert table.column("q").to_pylist() == [None]
    assert table.column("atTime").to_pylist()[0] == datetime(2020, 1, 1, 6, tzinfo=timezone.utc)


def test_tables_of_several_schedules_concatenate(network, container):
    builder, schedule, consumer = _schedule(network, container)
    other = builder.create(mRID="ld_1_q")
    builder.add_schedule(other, EnergyConnection=consumer.mRID)
    table = pa.concat_tables([builder.time_points(schedule, times=HOURS, p=[1, 2, 3]),
                              builder.time_points(other, times=HOURS[:1], q=[4])]).unify_dictionaries()
    assert table.num_rows == 4
    assert set(table.column("EnergyConnectionSchedule").to_pylist()) == {schedule.uri(), other.uri()}


@pytest.mark.parametrize("kwargs, match", [
    ({"times": HOURS}, "need p, q or both"),
    ({"times": HOURS, "p": [1.0, 2.0]}, "3 times but 2 p values"),
    ({"times": [HOURS[0], HOURS[0]], "p": [1.0, 2.0]}, "repeated times"),
])
def test_time_points_raise(network, container, kwargs, match):
    builder, schedule, _ = _schedule(network, container)
    with pytest.raises(ValueError, match=match):
        builder.time_points(schedule, **kwargs)


def test_photovoltaic_unit_add_ssh_sets_irradiance(network, container):
    builder = PhotoVoltaicUnitBuilder(network=network, container=container)
    unit = builder.create(mRID="pv_1_unit")
    builder.add_ssh(unit, p=Qty(-4, "kW"), irradiance=Qty(0.8, "kW/m^2"), inService=True)
    assert unit.irradiance.to("W/m^2") == pytest.approx(800.0)
    assert unit.inService is True
