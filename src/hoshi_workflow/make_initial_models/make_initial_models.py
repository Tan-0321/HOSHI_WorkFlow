"""Utilities to run and modify HOSHI model directories.

This module provides a small wrapper around a HOSHI model directory
containing an `evol` executable and the `param/files.henyey` file.

The implementation focuses on safer file operations (backups, atomic
replace) and clearer logging.
"""

import logging
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Union

from hoshi_workflow.file_name_convention import generate_name, parse_name
import numpy as np

logger = logging.getLogger(__name__)
# Best practice for libraries: attach a NullHandler so that importing this
# module does not configure the root logger or produce "No handler" warnings.
logger.addHandler(logging.NullHandler())


def enable_logging(
    level: int = logging.INFO,
    *,
    handler: logging.Handler | None = None,
    fmt: str | None = None,
    force: bool = False,
) -> None:
    """Enable logging for this module.

    This configures a StreamHandler on the module logger (not the root
    logger) so library users can opt-in to seeing log messages. By default
    a simple StreamHandler is created. Callers may provide a custom
    handler. Repeated calls do not add duplicate handlers unless
    ``force=True``.

    Args:
        level: logging level (e.g., logging.INFO).
        handler: optional custom logging.Handler to attach.
        fmt: optional format string for the handler.
        force: if True, remove existing handlers and reconfigure.
    """
    global logger
    if force:
        for h in list(logger.handlers):
            logger.removeHandler(h)

    if handler is None:
        handler = logging.StreamHandler()

    if fmt is None:
        fmt = "%(asctime)s %(levelname)s %(name)s: %(message)s"

    handler.setFormatter(logging.Formatter(fmt))
    handler.setLevel(level)

    # avoid adding duplicate handlers
    if not force and any(
        type(h) is type(handler) and h.level == handler.level for h in logger.handlers
    ):
        logger.debug("Logging already enabled for module %s", __name__)
        logger.setLevel(level)
        return

    logger.addHandler(handler)
    logger.setLevel(level)
    # When we configure the module logger we typically don't want propagation
    # to the root logger (avoid duplicate messages)
    logger.propagate = False


def disable_logging() -> None:
    """Remove handlers attached by enable_logging and restore NullHandler."""
    global logger
    for h in list(logger.handlers):
        logger.removeHandler(h)
    logger.addHandler(logging.NullHandler())
    logger.propagate = True
    logger.setLevel(logging.WARNING)
    logger.debug("Module logging disabled")


LOGGING_ENABLED = True


class HoshiModelDir:
    """Represents a HOSHI model directory containing an `evol` executable.
    
    """

    DIR = None
    PROGRAM_EXEC = None
    henyey_params = None

    def __init__(self, model_dir):
        self.DIR = Path(model_dir)
        self.PROGRAM_EXEC = self.DIR / "evol"
        if not self.DIR.exists():
            raise FileNotFoundError(f"Model directory not found: {self.DIR}")
        if not self.PROGRAM_EXEC.exists():
            raise FileNotFoundError(f"Executable not found: {self.PROGRAM_EXEC}")
        self.henyey_params = self._read_henyey_params()

    def run(self, log_file: Union[Path, str, None] = None, check: bool = False) -> int:
        """Run the `evol` program and capture output to log_file.

        Args:
            log_file: path to write output. If None, a timestamped .log file
                will be created inside the model directory.
            check: if True, raise CalledProcessError on non-zero exit code.

        Returns:
            The subprocess return code.
        """
        if log_file is None:
            s = datetime.now().strftime("%y_%m%d_%H%M")
            log_file = self.DIR / f"run_{s}.log"
        else:
            log_file = Path(log_file)
            if not log_file.is_absolute():
                # relative paths are created relative to the model dir
                log_file = self.DIR / log_file

        logger.info(
            "Running '%s' in %s, logging output to %s",
            self.PROGRAM_EXEC.name,
            self.DIR,
            log_file,
        )
        with open(log_file, "wb") as f:
            # Run the executable and capture both stdout and stderr.
            # Run in the model directory to ensure relative paths behave as expected.
            proc = subprocess.run(
                [str(self.PROGRAM_EXEC)],
                stdout=f,
                stderr=subprocess.STDOUT,
                cwd=str(self.DIR),
            )
        logger.info("Process finished with return code %d", proc.returncode)

        if check and proc.returncode != 0:
            # Re-raise as CalledProcessError for callers who want an exception
            raise subprocess.CalledProcessError(proc.returncode, str(self.PROGRAM_EXEC))

        return proc.returncode

    def _read_henyey_params(self) -> dict:
        """Read and return parameters from the self.DIR/param/files.henyey file.

        Returns:
            A dictionary of parameter names and their values.
        """
        input_file = self.DIR / "param" / "files.henyey"
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        params = {
            "input_structure_dir": None,
            "output_summary_dir": None,
            "input_structure_file": None,
            "output_structure_file": None,
            "NAME_IN": None,
            "NAME_OUT": None,
            "NSTG_max": None,
            "MAXQTY": None,
            "FLAG_reduce_D_and_Li": None,
            "relative_metallicity": None,
            "FLAG_change_mass": None,
            "new_mass": None,
        }
        values = []
        with open(input_file, "r") as f:
            for line in f:
                line = line.strip()
                line = line.split(":", 1)[0].strip()
                if line and not (line.startswith("*") or line.startswith("#")):
                    values.append(line)
        # print(values)

        keys = list(params.keys())
        for i, key in enumerate(keys):
            if i < len(values):
                params[key] = values[i]
        # parts = params['MAXQTY'].split()
        # if len(parts) == 2:
        #     params['MAXQTY'] = (parts[0], parts[1])
        return params

    def modify_input_henyey(
        self, new_params: Dict[str, str], *, dry_run: bool = False, backup: bool = True
    ) -> None:
        """Modify `param/files.henyey` using `new_params`.

        Matches parameters positionally: non-empty non-comment lines are
        assigned in order to known keys (same behavior as original code).
        """
        input_file = self.DIR / "param" / "files.henyey"
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        with open(input_file, "r") as f:
            lines = f.readlines()

        cleaned = []
        for line in lines:
            s = line.strip()
            if s and not (s.startswith("*") or s.startswith("#")):
                cleaned.append(s.split(":", 1)[0].strip())

        keys = [
            "input_structure_dir",
            "output_summary_dir",
            "input_structure_file",
            "output_structure_file",
            "NAME_IN",
            "NAME_OUT",
            "NSTG_max",
            "MAXQTY",
            "FLAG_reduce_D_and_Li",
            "relative_metallicity",
            "FLAG_change_mass",
            "new_mass",
        ]

        updated = {}
        for i, key in enumerate(keys):
            old = None
            if i < len(cleaned):
                old = cleaned[i]
            updated[key] = new_params.get(key, old)

        # Compose new file contents by walking original lines and replacing
        # the positional parameters while preserving comments and structure.
        out_lines = []
        data_idx = 0
        for line in lines:
            s = line.strip()
            if s and not (s.startswith("*") or s.startswith("#")):
                key = keys[data_idx]
                val = updated.get(key, "")
                out_lines.append(f"{val}\n")
                data_idx += 1
            else:
                out_lines.append(line)

        if backup:
            backup_file = input_file.with_suffix(input_file.suffix + ".bak")
            shutil.copy2(input_file, backup_file)
            logger.debug("Backed up %s to %s", input_file, backup_file)

        if dry_run:
            logger.info("Dry run: new file would be:\n%s", "".join(out_lines))
            return

        # Write atomically
        fd, tmp_path = tempfile.mkstemp(dir=str(input_file.parent))
        with open(fd, "w") as f:
            f.writelines(out_lines)
        shutil.move(tmp_path, input_file)
        logger.info("Updated %s", input_file)
