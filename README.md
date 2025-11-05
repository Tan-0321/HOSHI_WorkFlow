# HOSHI_WorkFlow

Python utilities for working with HOSHI simulations:
- reading outputs (`hoshi_reader`)
- naming conventions (`file_name_convention`)
- preparing initial chemical composition (`initial_composition`)
- making initial models (`make_initial_models`)
- ... more tools to be developed

[![CI](https://img.shields.io/badge/ci-pending-lightgrey)]() [![PyPI](https://img.shields.io/badge/pypi-not%20published-lightgrey)]() [![License](https://img.shields.io/badge/license-MIT-blue)]()

## Compatibility & Requirements
- Python >= 3.10
- See `pyproject.toml` (runtime deps) and `requirements-dev.txt` (dev deps) for Python package dependencies.
- Some examples require the HOSHI executable or a specific directory layout; use `fake_run` / `dry_run` for tests without the binary.

## Installation
Developer install (recommended):
```bash
git clone <repo-url>
cd HOSHI_WorkFlow
pip install -e .
```

Or install from source distribution:
```bash
pip install .
```

## Quick Start
Example usage:
```python
from hoshi_workflow.file_name_convention import generate_name

name = generate_name(mass=1.0)
print(name)
```

## Examples
Example notebooks and scripts are under `examples/`. Many notebooks use `fake_run` or `dry_run` so they can run without the HOSHI executable. 



## Development & Testing
To run the local test suite, use the following command:  
Note: Currently, the test suite only includes basic import checks.
```bash
pytest -q
```
Install development tooling (optional):
```bash
pip install -r requirements-dev.txt
# or configure pre-commit / black / flake8 as preferred
```


## License
This project is provided under the MIT License. Replace with the correct license if different.


