"""hoshi_reader package: export reader classes at package level.

This lets users import the classes with either:

    from hoshi_workflow.hoshi_reader import HoshiModel

The implementation lives in `hoshi_workflow.hoshi_reader.hoshi_reader`.
"""

from .hoshi_reader import (
    HoshiModel,
    HoshiHistory,
    HoshiHistoryCombined,
    HoshiProfile,
    HoshiNucNetwork,
    # some search functions
    find_nearest,
    find_all_within,
    find_first_greater,
    find_first_less,
    # some reader functions 
    get_var_from_block,

)  # noqa: F401

__all__ = [
    "HoshiModel",
    "HoshiHistory",
    "HoshiHistoryCombined",
    "HoshiProfile",
    "HoshiNucNetwork",
    "find_nearest",
    "find_all_within",
    "find_first_greater",
    "find_first_less",
    "get_var_from_block",
]
