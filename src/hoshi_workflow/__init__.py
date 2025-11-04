"""hoshi_workflow package aggregator.

This module provides a thin aggregation layer so users can import
submodules under the `hoshi_workflow` namespace while keeping the
existing top-level packages available for backward compatibility.

It intentionally performs safe imports and avoids hard failures at
import time if optional subpackages are missing.
"""
from importlib import import_module

__all__ = []

_subpackages = [
    "file_name_convention",
    "hoshi_reader",
    "initial_composition",
    "make_initial_models",
]

for _mod in _subpackages:
    try:
        # Prefer importing as a submodule of this package, fall back to top-level.
        try:
            mod = import_module(f"hoshi_workflow.{_mod}")
        except Exception:
            mod = import_module(_mod)

        globals()[_mod] = mod
        __all__.append(_mod)
    except Exception:
        # ignore import errors here to keep import-time robust
        pass

# Provide a few convenient re-exports for common APIs when available.
try:
    _fnc = globals().get("file_name_convention")
    if _fnc is not None:
        generate_name = _fnc.generate_name
        parse_name = _fnc.parse_name
        __all__.extend(["generate_name", "parse_name"])
except Exception:
    pass
