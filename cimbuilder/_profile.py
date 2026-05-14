"""Runtime CIM profile access with IDE type support.

Every builder uses ``get_cim()`` to obtain the active CIM profile module at
runtime.  The active profile is chosen by ``cimgraph.databases.get_cim_profile()``,
which honors the ``CIMG_CIM_PROFILE`` environment variable.

The ``TYPE_CHECKING`` import below lets Pylance / mypy resolve ``cim.Breaker``,
``cim.Terminal``, etc. against the canonical profile (``cimhub_2026``) without
forcing a runtime dependency on it — that import is invisible at runtime.

Profile-scoped builders (dynamics, split-profile distribution) import their
own profile module under ``TYPE_CHECKING`` at the top of their own file, and
may call ``get_cim()`` if they happen to target the common profile, or use
their own local alias otherwise.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

from cimgraph.databases import get_cim_profile

if TYPE_CHECKING:
    import cimgraph.data_profile.cimhub_2026 as cim  # noqa: F401


def get_cim() -> "cim":
    """Return the active CIM profile module.

    Runtime lookup goes through ``cimgraph.databases.get_cim_profile()``,
    which reads the ``CIMG_CIM_PROFILE`` environment variable.  The function
    signature is annotated as returning ``"cim"`` (the TYPE_CHECKING alias)
    so that type-checkers resolve attribute access (``cim.Breaker``, etc.)
    against the cimhub_2026 profile while the actual module returned at
    runtime is whichever profile the environment selects.
    """
    _, cim_module = get_cim_profile()
    return cim_module
