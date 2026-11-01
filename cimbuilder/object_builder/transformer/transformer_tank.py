import cimprofiles.cim18.cim18v17.connectivity_unbalanced as CN
import cimprofiles.cim18.cim18v17.construction as CONST
import cimprofiles.cim18.cim18v17.electrical_balanced as EL_UNBAL
import cimprofiles.cim18.cim18v17.regulating_control as REG

from cimbuilder.builders.base import ObjectBuilder
from cimtables import graph_write

class TransformerTankBuilder(ObjectBuilder):
    cim_class_name = 'TransformerTank'

    def add_lug(self, *, TransformerTank:object, designation:str,) -> CONST.TransformerLug:
        """
        Incomplete/WIP - do not rely on this method. It builds a
        TransformerLug but never sets `designation` on it, never associates
        it with `TransformerTank`, never adds it to the graph, and has no
        return statement (so it always returns None despite its `->
        CONST.TransformerLug` annotation). Also note `TransformerTank` is
        documented as the parameter name but is actually expected to be a
        live object (its `.name` is read directly, not resolved by mRID) -
        and `name={TransformerTank.name}` builds a one-element Python set
        literal, not the string `TransformerTank.name` itself, so even that
        one write is almost certainly a bug.
        * TransformerTank: intended to be a live TransformerTank object (not
          an mRID string).
        * designation: intended to be a plain string - high side is
          H1,H2,H3, low-side is X1,X2,X3 for xfmr over 200kVA and 8660V;
          smaller transformers use additive polarity X3,X2,X1. Currently
          unused by the method body.
        """

        lug = self.cim.TransformerLug(name={TransformerTank.name})