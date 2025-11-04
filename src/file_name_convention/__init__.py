"""Compatibility shim for `file_name_convention`.

This module delegates to `hoshi_workflow.file_name_convention` so existing
imports like `import file_name_convention` continue to work while the
real implementation lives under the `hoshi_workflow` namespace.
"""

from hoshi_workflow.file_name_convention import *  # type: ignore

__all__ = [name for name in dir() if not name.startswith("_")]
