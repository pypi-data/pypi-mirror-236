"""Apply partial to a whole library."""
from inspect import getfullargspec
from functools import partial
from types import ModuleType, SimpleNamespace
from typing import Any, Type

from cachetools import cached
from numba.core.registry import CPUDispatcher

from .search import get_all_functions, get_all_submodules


def partial_functions_in_module(
    module: ModuleType, arg: str, value: Any
) -> SimpleNamespace:
    """
    Apply partial to fix a keyword arg on every function in module.
    Args:
        module: Module to be partialed.
        arg: Name of arg to fix.
        value: Value to set arg to.

    Returns:
        A namespace with the same functions as module, but with the arg fixed.
    """
    partialled_module = SimpleNamespace()

    for name, func in get_all_functions(module):
        setattr(partialled_module, name, partial(func, **{arg: value}))

    return partialled_module


def partial_module(module: ModuleType, arg: str, value: Any) -> SimpleNamespace:
    """
    Recursively go through modules and partial all functions.

    Args:
        module: Module to be partialed.
        arg: Name of arg to fix.
        value: Value to set arg to.

    Returns:
        A namespace with the same functions as module, but with the arg fixed.
    """
    # Partial functions in this module and set attribute.
    partialled_module = partial_functions_in_module(module, arg, value)

    # Loop over submodules and resursively add partialed functions.
    submodules = get_all_submodules(module)

    for name, sub in submodules:
        setattr(partialled_module, name, partial_module(sub, arg, value))

    return partialled_module


def partial_functions_in_module_by_type(
    module: ModuleType, type_to_fix: Type, value: Any
) -> SimpleNamespace:
    """
    Apply partial to all function inputs of the given type.
    Args:
        module: Module to be partialed.
        type_to_fix: Type of args you want to replace.
        value: Value to set arg to.

    Returns:
        A namespace with the same functions as module, but with the arg fixed.
    """
    partialled_module = SimpleNamespace()

    for name, func in get_all_functions(module):
        try:
            # Handle numba'd functions.
            if isinstance(func, CPUDispatcher):
                args = getfullargspec(func.py_func).annotations
            else:
                args = getfullargspec(func).annotations
        except TypeError:
            # Cannot get type information, so just add to partialled module and continue.
            setattr(partialled_module, name, func)
            continue

        # This is the return value, not an input.
        if "return" in args:
            args.pop("return")

        setattr(
            partialled_module,
            name,
            partial(
                func, **{name: value for name in args if args[name] is type_to_fix}
            ),
        )

    return partialled_module


@cached(cache={}, key=lambda module, x, y: hash(module))
def partial_module_by_type(
    module: ModuleType, type_to_fix: Type, value: Any
) -> SimpleNamespace:
    """
    Recursively go through modules and partial all functions.

    Args:
        module: Module to be partialed.
        type_to_fix: Name of arg to fix.
        value: Value to set arg to.

    Returns:
        A namespace with the same functions as module, but with the arg fixed.
    """
    # Partial functions in this module and set attribute.
    partialled_module = partial_functions_in_module_by_type(module, type_to_fix, value)

    # Loop over submodules and resursively add partialed functions.
    submodules = get_all_submodules(module)

    for name, sub in submodules:
        setattr(
            partialled_module, name, partial_module_by_type(sub, type_to_fix, value)
        )

    return partialled_module
