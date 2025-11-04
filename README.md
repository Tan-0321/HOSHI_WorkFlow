# HOSHI_WorkFlow
Python utilities for HOSHI workflows: reading outputs, naming conventions,
and helpers for building initial models.

Quick start — install and import
```
pip install -e .
```

Import example after installation:

```python
from hoshi_workflow.file_name_convention import generate_name
from hoshi_workflow.hoshi_reader import HoshiHistory

name = generate_name(mass=1.0)
```
