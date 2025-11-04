"""HOSHI reader implementation (PEP8 module name: hoshi_reader).

Copied from original HoshiReader implementation; module filename uses
lowercase with underscore to follow PEP8 module naming.
"""

from pathlib import Path
import logging
import re

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

# Constants
G_GRAV = 6.67428e-8  # in cm^3/g/s^2
R_SUN = 6.9566e10  # in cm
M_SUN = 1.9891e33  # in g
L_SUN = 3.839e33  # in erg/


def set_plot_xtickers(
    ax: plt.Axes,
    x_interval: float,
    x_minorTicks_num: int,
    major_tick_length: float = 6,
    minor_tick_length: float = 3,
):
    ax.tick_params(
        axis="both",
        which="major",
        direction="in",
        length=major_tick_length,
        top=True,
        bottom=True,
    )
    ax.tick_params(
        axis="both",
        which="minor",
        direction="in",
        length=minor_tick_length,
        top=True,
        bottom=True,
    )

    ax.xaxis.set_major_locator(ticker.MultipleLocator(x_interval))
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(x_minorTicks_num))


def set_plot_ytickers(
    ax: plt.Axes,
    y_interval: float,
    y_minorTicks_num: int,
    major_tick_length: float = 6,
    minor_tick_length: float = 3,
):
    ax.tick_params(
        axis="both",
        which="major",
        direction="in",
        length=major_tick_length,
        left=True,
        right=True,
    )
    ax.tick_params(
        axis="both",
        which="minor",
        direction="in",
        length=minor_tick_length,
        left=True,
        right=True,
    )

    ax.yaxis.set_major_locator(ticker.MultipleLocator(y_interval))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(y_minorTicks_num))


class HoshiModel:
    def __init__(self, work_dir):
        self.work_dir = Path(work_dir)
        self.summary_dir = self.work_dir / "summary"
        self.writestr_dir = self.work_dir / "writestr"
        self.check_dir()

    def check_dir(self):
        if not self.summary_dir.exists():
            logging.info("No summary directory found")
        if not self.writestr_dir.exists():
            logging.info("No writestr directory found")


class HoshiHistory(HoshiModel):
    var_names = []

    def __init__(self, path):
        p = Path(path)
        if p.is_dir():
            if str(path).endswith("summary") or p.name == "summary":
                self.path = p / "summary.txt"
            else:
                self.path = p / "summary" / "summary.txt"
        elif p.is_file() and str(path).endswith("summary.txt"):
            self.path = p
        else:
            raise ValueError(
                "Invalid path provided. Path should be either a directory or a summary.txt file."
            )

        self.var_names = self._get_var_names()

    def _get_var_names(self) -> list:
        with open(self.path, "r") as file:
            for line in file:
                if line.startswith("#"):
                    header_line = line
                    break

        cleaned_header = header_line.replace("#", "")
        cleaned_header = re.sub(r"\d+:", " ", cleaned_header)
        variable_names = cleaned_header.split()

        return variable_names

    def _find_run_headers(self) -> list:
        headers = []
        with open(self.path, "r") as f:
            for idx, line in enumerate(f):
                if line.startswith("#"):
                    headers.append((line.rstrip("\n"), idx))
        return headers

    def count_runs(self) -> int:
        return len(self._find_run_headers())

    def list_runs(self) -> list:
        headers = self._find_run_headers()
        runs = []
        if not headers:
            return runs

        with open(self.path, "r") as f:
            all_lines = f.readlines()
        total_lines = len(all_lines)

        for i, (header, start_idx) in enumerate(headers):
            if i + 1 < len(headers):
                end_idx = headers[i + 1][1] - 1
            else:
                end_idx = total_lines - 1

            cleaned_header = header.replace("#", "")
            cleaned_header = re.sub(r"\d+:", " ", cleaned_header)
            var_names = cleaned_header.split()

            runs.append(
                {
                    "index": i + 1,
                    "header": header,
                    "start_line": start_idx,
                    "end_line": end_idx,
                    "var_names": var_names,
                }
            )

        return runs

    def read_run(self, run_index: int = -1, dtype=float) -> pd.DataFrame:
        runs = self.list_runs()
        if not runs:
            logging.error("No runs (header lines) found in summary file.")
            return pd.DataFrame()

        if run_index < 0:
            sel = runs[run_index]
        else:
            if run_index < 1 or run_index > len(runs):
                logging.error(
                    f"run_index out of range. Must be between 1 and {len(runs)}"
                )
                return pd.DataFrame()
            sel = runs[run_index - 1]

        var_names = sel["var_names"]
        data_start = sel["start_line"] + 1
        data_end = sel["end_line"]
        nrows = data_end - data_start + 1
        if nrows <= 0:
            return pd.DataFrame(columns=var_names)

        df = pd.read_csv(
            self.path,
            comment="#",
            delim_whitespace=True,
            header=None,
            names=var_names,
            skiprows=data_start,
            nrows=nrows,
            dtype=str,
            na_values=["", "NaN", "nan"],
            keep_default_na=True,
        )

        for col in df.columns:
            col_series = df[col]
            non_empty_mask = col_series.notna() & (col_series.str.strip() != "")
            if not non_empty_mask.any():
                continue

            converted = pd.to_numeric(col_series, errors="coerce")

            if not converted[non_empty_mask].isna().any():
                try:
                    if dtype in (float, "float", "float64"):
                        df[col] = converted.astype(float)
                    elif dtype in (int, "int", "int64"):
                        df[col] = converted.astype("Int64")
                    else:
                        df[col] = converted
                except Exception:
                    df[col] = converted
            else:
                df[col] = col_series.astype(str).str.strip()

        return df

    def data(self, var_name: str, dtype=float) -> np.ndarray:
        if var_name not in self.var_names:
            logging.error(f"Variable name '{var_name}' not found in the file.")
            return np.array([])

        col_index = self.var_names.index(var_name)

        df = pd.read_csv(
            self.path,
            comment="#",
            delim_whitespace=True,
            header=None,
            usecols=[col_index],
            dtype=dtype,
        )
        return df.iloc[:, 0].values


class HoshiProfile(HoshiModel):
    def __init__(self, path: str, str_num: int):
        p = Path(path)
        target = f"str{str_num:05d}.txt"
        if p.is_file() and str(path).endswith(target):
            self.path = p
        elif str(path).endswith("writestr"):
            self.path = p / target
        elif p.is_dir() and (p / "evol").exists():
            self.path = p / "writestr" / target
        else:
            logging.error(
                "Invalid path provided. Path should be either a directory or a profile file."
            )
            return

        self.var_names = self._get_var_names()

    def _get_var_names(self) -> list:
        with open(self.path, "r") as file:
            for _ in range(2):
                next(file)
            header_line = next(file)

        cleaned_header = header_line.replace("#", "")
        cleaned_header = re.sub(r"\d+:", " ", cleaned_header)
        variable_names = cleaned_header.split()

        return variable_names

    def data(self, var_name: str, dtype=float) -> np.ndarray:
        if var_name not in self.var_names:
            logging.error(f"Variable name '{var_name}' not found in the file.")
            return np.array([])

        col_index = self.var_names.index(var_name)

        df = pd.read_csv(
            self.path,
            comment="#",
            delim_whitespace=True,
            header=None,
            usecols=[col_index],
            skiprows=2,
            dtype=dtype,
        )
        return df.iloc[:, 0].values
