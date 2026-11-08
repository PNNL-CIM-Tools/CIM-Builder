# EL_BAL.PhaseTapChangerTable(Point) pending profile rebuild, drop this import once it lands
from __future__ import annotations

import cimprofiles.cim18.cim18v17.electrical_balanced as EL_BAL
from cimtables import graph_write
from cimtables.units import Qty

from cimbuilder.object_builder.object_builder import ObjectBuilder


class PhaseTapChangerTableBuilder(ObjectBuilder):
    """
    Builder for the table of angle, ratio and impedance per step used by PhaseTapChangerTabular.
    Builder functions to be called in the following order:
    * create() - instantiate the PhaseTapChangerTable
    * add_table_point() - add one point for every step
    """

    cim_class_name = "PhaseTapChangerTable"

    def add_table_point(
        self,
        table: EL_BAL.PhaseTapChangerTable,
        *,
        step: int,
        angle: float | Qty,
        ratio: float | None = None,
        r: float | None = None,
        x: float | None = None,
        b: float | None = None,
        g: float | None = None,
    ) -> tuple[EL_BAL.PhaseTapChangerTable, EL_BAL.PhaseTapChangerTablePoint]:
        """
        Adds the values for one step of the table
        * step: integer, tap step of this point
        * angle: phase shift at this step, float in degrees or Qty('deg')
        * ratio: voltage ratio at this step relative to the neutral step, float (e.g. 1.0)
        * r: resistance change from the neutral step, float in percentage
        * x: reactance change from the neutral step, float in percentage
        * b: susceptance change from the neutral step, float in percentage
        * g: conductance change from the neutral step, float in percentage
        """
        el_bal: EL_BAL = self.cim  # type: ignore
        point = el_bal.PhaseTapChangerTablePoint()  # no mRID on this class
        point.uuid(mRID=f"{table.mRID}_step_{step}")
        graph_write.set_attr(point, EL_BAL, "step", step)
        graph_write.set_attr(point, EL_BAL, "angle", angle)
        graph_write.set_attr(point, EL_BAL, "ratio", ratio)
        graph_write.set_attr(point, EL_BAL, "r", r)
        graph_write.set_attr(point, EL_BAL, "x", x)
        graph_write.set_attr(point, EL_BAL, "b", b)
        graph_write.set_attr(point, EL_BAL, "g", g)
        graph_write.set_assc(point, EL_BAL, "PhaseTapChangerTable", table)
        graph_write.add_to_graph(self.network, point)
        return table, point
