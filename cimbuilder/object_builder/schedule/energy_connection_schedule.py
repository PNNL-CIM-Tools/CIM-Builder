"""EnergyConnectionSchedule (nc_schedule): p/q over time for one EnergyConnection.

The schedule itself is a graph object, serialized in the CIM XML. Its time points are not: `time_points` returns
them as rows of a pyarrow table in `TIME_POINT_SCHEMA`, one row per instant, keyed by the schedule's uri(). A
year of hourly points on every load of a feeder is millions of points, too many for one graph object each (CIM issue
#7963, "Serialization of High-Volume Data").
"""

from collections.abc import Sequence
from datetime import datetime

import cimprofiles.cim18.cim18v17.nc_schedule as NC
import pyarrow as pa
import pyarrow.compute as pc
from cimprofiles.units.units import ureg
from cimtables import graph_write

from cimbuilder.object_builder.object_builder import ObjectBuilder

mRID = str

#: The TimePoint class the rows stand for.
TIME_POINT_CLASS = "EnergyConnectionTimePoint"

#: One row per point: the schedule's uri(), the UTC instant the value takes effect, p and q in SI (load sign
#: convention). p or q is null when the schedule carries only the other.
TIME_POINT_SCHEMA = pa.schema(
    [
        pa.field("EnergyConnectionSchedule", pa.dictionary(pa.int32(), pa.string()), nullable=False),
        pa.field("atTime", pa.timestamp("us", tz="UTC"), nullable=False),
        pa.field("p", pa.float64(), metadata={"unit": "W"}),
        pa.field("q", pa.float64(), metadata={"unit": "VAr"}),
    ],
    metadata={"cim:profile": "cim18v17", "cim:class": TIME_POINT_CLASS},
)


class EnergyConnectionScheduleBuilder(ObjectBuilder):
    cim_class_name = "EnergyConnectionSchedule"

    def add_schedule(
        self,
        schedule: NC.EnergyConnectionSchedule,
        *,
        EnergyConnection: mRID,
        timeSeriesKind: str | None = None,
        interpolationKind: str | None = None,
        actionMethod: str | None = None,
    ) -> NC.EnergyConnectionSchedule:
        """
        Links the schedule to its equipment and says how to read its points.
        * EnergyConnection: mRID of the EnergyConsumer, EnergySource, PowerElectronicsConnection or RotatingMachine
        * timeSeriesKind: BaseTimeSeriesKind, "actual" | "forecast" | "hindcast" | "schedule"
        * interpolationKind: TimeSeriesInterpolationKind between points, "previous" (a value holds until the next
          point) | "linear" | "next" | "none" | "zero"
        * actionMethod: free text telling apart several schedules of the same kind on one EnergyConnection
        """
        nc: NC = self.cim  # type: ignore
        graph_write.set_attr(schedule, NC, "timeSeriesKind", self._enum("BaseTimeSeriesKind", timeSeriesKind))
        graph_write.set_attr(
            schedule, NC, "interpolationKind", self._enum("TimeSeriesInterpolationKind", interpolationKind)
        )
        graph_write.set_attr(schedule, NC, "actionMethod", actionMethod)
        graph_write.set_assc_from_mrid(
            network=self.network,
            source_object=schedule,
            profile_part=NC,
            association_name="EnergyConnection",
            target_class=nc.EnergyConnection,
            target_mRID=EnergyConnection,
        )
        return schedule

    def time_points(
        self,
        schedule: NC.EnergyConnectionSchedule,
        *,
        times: Sequence[datetime],
        p: Sequence[float] | None = None,
        q: Sequence[float] | None = None,
        p_unit: str = "W",
        q_unit: str = "VAr",
    ) -> pa.Table:
        """
        The schedule's points as rows in TIME_POINT_SCHEMA, sorted by time. Nothing is added to the graph: the
        caller keeps the table (concatenate the tables of several schedules with pyarrow.concat_tables).
        * times: when each value takes effect, datetimes (or a numpy datetime64 array); naive times are taken as UTC
        * p: active power at each time, in p_unit ("W" | "kW" | "MW")
        * q: reactive power at each time, in q_unit ("VAr" | "kVAr" | "MVAr")
        Raises on no values, a length mismatch or a repeated time (a point has no identity besides its time).
        """
        if p is None and q is None:
            raise ValueError(f"{schedule.mRID!r}: time points need p, q or both")
        instants = pa.array(times, type=TIME_POINT_SCHEMA.field("atTime").type)
        columns = {"p": _column(p, p_unit, "W", len(instants)), "q": _column(q, q_unit, "VAr", len(instants))}
        for name, values in columns.items():
            if len(values) != len(instants):
                raise ValueError(f"{schedule.mRID!r}: {len(instants)} times but {len(values)} {name} values")
        if len(pc.unique(instants)) != len(instants):
            raise ValueError(f"{schedule.mRID!r}: repeated times")
        uri = pa.array([schedule.uri()] * len(instants), type=pa.string()).dictionary_encode()
        table = pa.table({"EnergyConnectionSchedule": uri, "atTime": instants, **columns}, schema=TIME_POINT_SCHEMA)
        return table.sort_by("atTime")


def _column(values, unit: str, si_unit: str, length: int) -> pa.Array:
    """`values` in `unit` as a float64 column in `si_unit`, scaled by the profile unit registry's factor from `unit`
    to `si_unit` (the power units are all linear); no values is a column of nulls."""
    if values is None:
        return pa.nulls(length, pa.float64())
    factor = ureg.Quantity(1.0, unit).to(si_unit).magnitude
    return pc.multiply(pa.array(values, type=pa.float64()), factor)
