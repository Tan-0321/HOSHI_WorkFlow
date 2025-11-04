"""Compatibility wrapper: delegate to `hoshi_workflow.HOSHI_reader.HoshiReader`.

This file previously contained the implementation. It is kept as a thin
wrapper to maintain backwards compatibility for direct imports.
"""

from hoshi_workflow.hoshi_reader.hoshi_reader import *  # type: ignore
