"""Compatibility shim for `HOSHI_reader`.

Delegates to `hoshi_workflow.HOSHI_reader` so both
`from HOSHI_reader import HoshiHistory` and
`from hoshi_workflow.HOSHI_reader import HoshiHistory` work.
"""

from hoshi_workflow.hoshi_reader import HoshiHistory, HoshiProfile, HoshiModel  # type: ignore

__all__ = ["HoshiModel", "HoshiHistory", "HoshiProfile"]
