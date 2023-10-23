"""Functions to get the contents of a library."""
from functools import lru_cache
from types import ModuleType, FunctionType
from typing import Callable


def _is_hidden(object_name: str) -> bool:
    return object_name.startswith("_")


def _has_module_attr(module: ModuleType, attribute_name: str) -> bool:
    return (
        hasattr(getattr(module, attribute_name), "__module__")
        and getattr(module, attribute_name).__module__ is not None
    )


def _is_in_submodule(module: ModuleType, attribute_name: str) -> bool:
    # Returns true is the module of the attribute is a submodule of module.
    # (This can return false when module imports a function, rather than creating it.
    return getattr(module, attribute_name).__module__.startswith(module.__name__)


@lru_cache
def get_all_functions(
    module: ModuleType,
) -> tuple[tuple[str, FunctionType], ...]:
    """
    Returns every function in the module.

    Args:
        module: Get functions from this module.

    Returns:
        All the function in the module.
    """
    return tuple(
        (f, getattr(module, f))
        for f in dir(module)
        # Don't include hidden functions/modules
        if not _is_hidden(f)
        # Only include callables
        and isinstance(getattr(module, f), Callable)
        and (
            # If the callable has a module, it must be a submodule.
            # Include also if it has no module.
            not _has_module_attr(module, f)
            or _is_in_submodule(module, f)
        )
    )


@lru_cache
def get_all_submodules(
    module: ModuleType,
) -> tuple[tuple[str, ModuleType], ...]:
    """
    Returns every function in the module.

    Args:
        module: Get functions from this module.

    Returns:
        All the function in the module.
    """
    return tuple(
        (f, getattr(module, f))
        for f in dir(module)
        # No hidden modules.
        if not f.startswith("_")
        # Must be module type.
        and isinstance(getattr(module, f), ModuleType)
        # Must be a submodule (i.e. not an imported external module).
        and getattr(module, f).__name__.startswith(module.__name__)
        # Must not be the module itself.
        and module != getattr(module, f)
    )
