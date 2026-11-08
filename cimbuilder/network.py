"""The network shell every builder writes into, built from scratch with no source file."""

import os

import cimprofiles.cim18.cim18v17 as cim
from cimgraph.core import set_model_scope
from cimgraph.core.env_vars import get_cim_profile
from cimgraph.models import FeederModel
from cimtables import graph_write
from cimtables.units import Qty

from cimbuilder.object_builder.base import BaseFrequencyBuilder

mRID = str


def new_feeder_model(
    *,
    authority: str,
    model: str,
    Feeder: mRID,
    name: str | None = None,
    frequency: float | Qty = 60,
) -> FeederModel:
    """
    Creates an empty cim18v17 FeederModel, the same setup cimtables.load_model does for a .cimtbl file
    * authority: model authority URI, seeds every UUID (e.g. https://github.com/NREL-Distribution-Suites/grid-data-models)
    * model: model name, unique per model under the authority (e.g. the GDM system name)
    * Feeder: mRID of the model's Feeder, e.g. fdr_<name>. With several feeders it is the graph's
      container only, add the others with FeederBuilder and give each piece of equipment its own EquipmentContainer
    * name: human-readable name of the Feeder
    * frequency: system frequency of the BaseFrequency base_freq, float in Hz or Qty('Hz')
    Sets the process-wide CIM profile and model scope, so call it before creating any object
    """
    os.environ["CIMG_CIM_PROFILE"] = "cim18v17"
    get_cim_profile.cache_clear()
    set_model_scope(authority, model)

    feeder = cim.Feeder(mRID=Feeder, name=name)
    network = FeederModel(container=feeder, connection=None, distributed=False)
    # FeederModel does not add its own container to the graph
    graph_write.add_to_graph(network, feeder)
    BaseFrequencyBuilder(network=network, container=feeder).create(
        mRID="base_freq", frequency=frequency
    )
    return network
