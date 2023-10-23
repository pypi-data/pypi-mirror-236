"""Partial a whole library."""
from currywrap.partial import (
    partial_functions_in_module,
    partial_module,
    partial_functions_in_module_by_type,
    partial_module_by_type,
)
from currywrap import search

__all__ = [
    "partial_module",
    "partial_module_by_type",
    "partial_functions_in_module_by_type",
    "partial_functions_in_module",
    "search",
]
