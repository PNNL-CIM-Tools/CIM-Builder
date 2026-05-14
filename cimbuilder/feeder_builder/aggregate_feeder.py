"""Deprecated — use cimbuilder.composite_builder.aggregate_feeder instead."""
import warnings as _warnings

from cimbuilder.composite_builder.aggregate_feeder import new_aggregate_feeder as _new_aggregate_feeder


def new_aggregate_feeder(*args, **kwargs):
    _warnings.warn(
        "cimbuilder.feeder_builder.aggregate_feeder is deprecated. "
        "Use cimbuilder.composite_builder.aggregate_feeder instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return _new_aggregate_feeder(*args, **kwargs)
