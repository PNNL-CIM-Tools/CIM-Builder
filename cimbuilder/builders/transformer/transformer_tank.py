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
        Adds transformer lug with
        * designation: high side is H1,H2,H3, low-side is X1,X2,X3 for xfmr over 200kVA and 8660V.
        smaller transformers use additive polarity X3,X2,X1
        """
        
        lug = self.cim.TransformerLug(name={TransformerTank.name})