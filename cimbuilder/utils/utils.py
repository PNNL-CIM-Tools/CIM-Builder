"""Deprecated compatibility shims for pre-rewrite imports.

New code should import from ``cimbuilder.utils.terminal`` and
``cimbuilder.utils.base_voltage`` directly.  This module is removed in Phase 7.
"""
from __future__ import annotations

from cimbuilder.utils.base_voltage import get_or_create_base_voltage as _get_or_create_base_voltage
from cimbuilder.utils.terminal import terminal_to_node

__all__ = ["terminal_to_node", "get_base_voltage"]


def get_base_voltage(network, base_voltage):
    """Deprecated alias for ``get_or_create_base_voltage``."""
    return _get_or_create_base_voltage(network, base_voltage)
