# Examples — dependencies, installation, and project layout

This file provides an overview for the `examples/` directory. It lists
project dependencies, shows two common installation options (installing into
the current environment or creating a new virtual environment), and outlines
the repository layout so you know which subpackages to look at when running
examples or developing further.

1) Main dependencies
---------------------
- Python >= 3.10 (required by `pyproject.toml`)
- Runtime dependencies (from `pyproject.toml` `dependencies`):
  - numpy
  - pandas
  - matplotlib
  - scipy

Optional / development dependencies (useful for tests, formatting and static
analysis; see `requirements-dev.txt` or `pyproject.toml` under
`[project.optional-dependencies].dev`):
  - pytest
  - ruff
  - black
  - isort
  - mypy
  - pre-commit
  - coverage

2) Installation (two common approaches)
---------------------------------------
Run the following commands from the repository root. Examples assume a Unix
shell (bash/zsh).

- Install into the currently active Python environment (editable install):

```bash
pip install -e .
```

  This installs the package in "editable" mode so changes to source files are
  immediately visible in the environment.

- Create and use a new virtual environment (recommended to avoid polluting
  your global environment):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Optional: install development dependencies:

```bash
pip install -r requirements-dev.txt
# or using the optional extras (if supported): pip install .[dev]
```

3) How to run examples
-----------------------
After installation, run example scripts under `examples/`. For instance:

```bash
python examples/quickstart/run_quickstart.py
```

If an example requires additional data, the example directory will include a
small sample or a download helper. Large datasets are not committed to the
repository.

4) Repository layout (brief)
----------------------------
This project uses the `src/` layout. The main subpackages and their roles are:

- `src/file_name_convention/` (accessible as `hoshi_workflow.file_name_convention`)
  - Purpose: Utilities to generate and parse compact file-name fragments used
    for model identifiers (e.g., `generate_name`, `parse_name`).
  - Import example:

```python
from hoshi_workflow.file_name_convention import generate_name, parse_name
```
  - Key file: `FileNameConvention.py`.

- `src/make_initial_models/`
  - Purpose: Tools to operate on HOSHI model directories, including
    `HoshiModelDir` which safely edits `param/files.henyey`, runs the `evol`
    executable, and helps construct initial models.
  - Key file: `MakeInitialModels.py`.

- `src/HOSHI_reader/` (accessible as `hoshi_workflow.hoshi_reader`)
  - Purpose: Classes to read HOSHI outputs (history/profile/model) for
    downstream analysis and plotting.
  - Import example:

```python
from hoshi_workflow.hoshi_reader import HoshiModel, HoshiHistory, HoshiProfile
```

- `src/initial_composition/`
  - Purpose: Data and helpers for initial chemical composition and yield
    tables used when creating models.

- `simulations/`
  - Purpose: Example simulation directories and scripts. These are useful as
    references but are not part of the installed library.

5) Notes and recommendations
----------------------------
- Keep examples small and reproducible: use small sample data or scripts that
  create a minimal model layout so users can run examples without a full
  HOSHI install.
- Consider adding a lightweight CI job that runs at least one example script
  to prevent examples from becoming stale when the code changes.

If you'd like, I can also add a short "Examples / Quick start" section to the
project root `README.md` linking to this file. Let me know and I will submit
the update.
