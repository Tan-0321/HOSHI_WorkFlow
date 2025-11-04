"""Utilities to run and modify HOSHI model directories.

This module provides a small wrapper around a HOSHI model directory
containing an `evol` executable and the `param/files.henyey` file.

The implementation focuses on safer file operations (backups, atomic
replace) and clearer logging.
"""

import argparse
import logging
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Union

import FileNameConvention as fnc
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


class HoshiModel:
    """Represents a HOSHI model directory containing an `evol` executable."""

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

        This function does NOT mutate `new_params` and supports `dry_run`
        (no write) and `backup` (create `.bak` before replacing).
        """
        input_file = self.DIR / "param" / "files.henyey"
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        # validate provided keys (but work on a local copy so we don't
        # mutate the caller's dict). We'll pop from `pending` as we apply
        # replacements and check at the end that all requested keys were
        # actually applied to the file.
        for key in new_params.keys():
            if key not in self.henyey_params:
                raise KeyError(
                    f"Key '{key}' not found in Henyey parameters. Available keys: {list(self.henyey_params.keys())}"
                )

        pending = new_params.copy()
        keys_prev = list(self.henyey_params.keys())
        out_lines = []
        idx = 0

        text = input_file.read_text(encoding="utf-8")
        for raw_line in text.splitlines():
            line = raw_line.rstrip("\n")
            stripped = line.strip()
            if stripped and not (stripped.startswith("*") or stripped.startswith("#")):
                # split into left (value) and right (comment) on the first ':'
                if ":" in line:
                    left, right = line.split(":", 1)
                    comment = ":" + right
                else:
                    left = line
                    comment = ""

                if idx < len(keys_prev):
                    key = keys_prev[idx]
                    idx += 1
                    # use pending (a local copy) and pop when we consume a key
                    if key in pending:
                        new_val = str(pending.pop(key))
                        # preserve leading whitespace from the original left-hand side
                        leading_ws = left[: len(left) - len(left.lstrip())]
                        new_line = f"{leading_ws}{new_val}\t\t\t{comment}".rstrip()
                        logger.debug("Replacing key %s -> %s", key, new_val)
                        out_lines.append(new_line)
                        continue
                out_lines.append(line)
            else:
                out_lines.append(line)

        new_content = "\n".join(out_lines) + "\n"

        if dry_run:
            logger.info("Dry run: new content prepared for %s", input_file)
            return

        # create a backup if requested
        if backup:
            bak_path = input_file.with_suffix(input_file.suffix + ".bak")
            shutil.copy2(input_file, bak_path)
            logger.info("Backup created: %s", bak_path)

        # atomic write: create temp file in same dir then replace
        tmp_dir = str(input_file.parent)
        with tempfile.NamedTemporaryFile(
            "w", delete=False, dir=tmp_dir, encoding="utf-8"
        ) as tf:
            tf.write(new_content)
            tmp_path = Path(tf.name)

        tmp_path.replace(input_file)
        logger.info("Updated Henyey file written: %s", input_file)
        # If any pending keys remain, they could not be applied because the
        # file contains fewer variable lines than expected. Report this to
        # the caller so they can adjust inputs or the files.henyey layout.
        if pending:
            missing = list(pending.keys())
            logger.warning(
                "Some new_params were not applied (no matching lines): %s", missing
            )
            raise KeyError(f"The following parameters were not applied: {missing}")

        self.henyey_params = self._read_henyey_params()
        return None

    def fake_run(self) -> None:
        logger.info("Running fake simulation with current parameters:")
        mass = self.henyey_params.get("new_mass").replace("d", "e")
        z_rel = self.henyey_params.get("relative_metallicity").replace("d", "e")
        new_name = (
            fnc.generate_name(
                mass=float(mass) if mass is not None else None,
                metallicity=float(z_rel) if z_rel is not None else None,
            )
            + ".fake"
        )
        with open(self.DIR / "strdata" / new_name, "a") as f:
            f.write(
                f"Fake simulation with mass={mass}, relative_metallicity={z_rel}, output name={new_name}\n"
            )

    def make_initial_model(
        self,
        initial_structure_file: str,
        target_relative_metallicity: float,
        target_mass: float,
    ) -> None:
        input_structure_file = str(initial_structure_file).strip()
        if self.henyey_params["input_structure_file"] != input_structure_file:
            logger.info("Updating input_structure_file to %s", input_structure_file)
        val_dict = fnc.parse_name(input_structure_file)
        mass = val_dict.get("mass")
        z_rel = val_dict.get("metallicity")
        if mass is None or z_rel is None:
            raise ValueError(
                f"Could not parse mass or metallicity from filename {input_structure_file}"
            )
        mass = float(mass)
        z_rel = float(z_rel)
        loop_num = np.log10(abs(max(target_relative_metallicity, 1e-5) / z_rel))
        if int(loop_num) == loop_num:
            extra_loop = 0
        else:
            extra_loop = 1
        if target_relative_metallicity < 1e-5:
            extra_loop += 1
        loop_num = int(abs(loop_num)) + extra_loop

        self.modify_input_henyey(
            {
                "FLAG_change_mass": "1",
                "new_mass": str(target_mass),
            }
        )
        if self.henyey_params["NAME_OUT"] != "e":
            self.modify_input_henyey(
                {
                    "NAME_OUT": "e",
                }
            )

        present_z_rel = z_rel
        present_input_structure_file = input_structure_file
        while loop_num > 0:
            logger.info("Making initial model, %d loops left...", loop_num)
            if loop_num == 1:
                new_z_rel = target_relative_metallicity
            else:
                new_z_rel = present_z_rel * np.power(
                    10, np.sign(target_relative_metallicity - present_z_rel)
                )
            present_z_rel = new_z_rel
            loop_num -= 1

            output_structure_file = fnc.generate_name(
                mass=target_mass,
                metallicity=new_z_rel,
            )
            self.modify_input_henyey(
                {
                    "input_structure_file": present_input_structure_file,
                    "output_structure_file": output_structure_file,
                    "relative_metallicity": str(new_z_rel),
                }
            )

            exit_code = self.run()
            if exit_code != 0:
                logger.error(
                    "Faile to make input initial structure data with parameters: mass = %d, Z_rel = %d ",
                    target_mass,
                    new_z_rel,
                )
                return None
            present_input_structure_file = output_structure_file

        return None
