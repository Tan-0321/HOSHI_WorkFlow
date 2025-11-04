# -*- coding: utf-8 -*-
"""
Created on Fri Jan 3rd

@author: Bingyang Tan
"""

import logging
from pathlib import Path
import re

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import scipy as sp

# NOTE: library modules must not configure the root logger on import.
# logging.basicConfig(...) has been removed to avoid side effects when this
# package is imported by other applications. Use the module-level
# `enable_logging()` (or configure the root logger) from an entry script.

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
    # 设置刻度线
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

    return None


def set_plot_ytickers(
    ax: plt.Axes,
    y_interval: float,
    y_minorTicks_num: int,
    major_tick_length: float = 6,
    minor_tick_length: float = 3,
):
    # 设置刻度线

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

    return None


class HoshiModel:
    def __init__(self, work_dir):
        self.work_dir = Path(work_dir)
        self.summary_dir = self.work_dir / "summary"
        self.writestr_dir = self.work_dir / "writestr"
        self.check_dir()

    def check_dir(self):
        if not self.summary_dir.exists():
            # os.makedirs(self.summary_dir)
            logging.info("No summary directory found")
        if not self.writestr_dir.exists():
            # os.makedirs(self.writestr_dir)
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
        # Return variable names from the first header found in the file
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
        """
        Scan the summary file and return a list of tuples (header_line_str, header_line_index).
        header_line_index is the 0-based line number where the header (starting with '#') appears.
        """
        headers = []
        with open(self.path, "r") as f:
            for idx, line in enumerate(f):
                if line.startswith("#"):
                    headers.append((line.rstrip("\n"), idx))
        return headers

    def count_runs(self) -> int:
        """Return how many runs (header blocks) are present in the summary file."""
        return len(self._find_run_headers())

    def list_runs(self) -> list:
        """Return a list of run metadata dicts: {index(1-based), header, start_line, end_line, var_names}.

        end_line is inclusive (0-based). If a run goes to EOF, end_line is the last line index.
        """
        headers = self._find_run_headers()
        runs = []
        if not headers:
            return runs

        # read total lines once to determine end boundaries
        with open(self.path, "r") as f:
            all_lines = f.readlines()
        total_lines = len(all_lines)

        for i, (header, start_idx) in enumerate(headers):
            if i + 1 < len(headers):
                end_idx = headers[i + 1][1] - 1
            else:
                end_idx = total_lines - 1

            # parse variable names from header
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
        """
        Read a specific run block from the summary file and return it as a pandas DataFrame.

        run_index: 1-based index of the run to read. Negative values follow Python convention (e.g. -1 -> last run).
        Returns an empty DataFrame if the run has no data lines.
        """
        runs = self.list_runs()
        if not runs:
            logging.error("No runs (header lines) found in summary file.")
            return pd.DataFrame()

        # convert run_index to 0-based
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
        data_start = sel["start_line"] + 1  # data begins after the header line
        data_end = sel["end_line"]
        nrows = data_end - data_start + 1
        if nrows <= 0:
            # empty run
            return pd.DataFrame(columns=var_names)

        # Read as strings first to avoid hard failures when some columns contain
        # non-numeric tokens (e.g. '6.670-321'). After reading, attempt to convert
        # each column to numeric. If conversion fails for any non-empty value,
        # keep that column as string.
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

        # Try to coerce columns to numeric where possible
        for col in df.columns:
            col_series = df[col]
            # mask of non-empty (non-NA and not just whitespace) entries
            non_empty_mask = col_series.notna() & (col_series.str.strip() != "")
            if not non_empty_mask.any():
                # column entirely empty -> leave as is
                continue

            # attempt conversion
            converted = pd.to_numeric(col_series, errors="coerce")

            # if all non-empty entries were successfully converted (no NaN),
            # use numeric dtype. Otherwise keep as original string values.
            if not converted[non_empty_mask].isna().any():
                # cast to requested dtype if it's a numeric type
                try:
                    if dtype in (float, "float", "float64"):
                        df[col] = converted.astype(float)
                    elif dtype in (int, "int", "int64"):
                        df[col] = converted.astype("Int64")
                    else:
                        # default: assign converted numeric
                        df[col] = converted
                except Exception:
                    # fallback: assign converted without strict astype
                    df[col] = converted
            else:
                # keep as string (strip whitespace)
                df[col] = col_series.astype(str).str.strip()

        return df

    def data(self, var_name: str, dtype=float) -> np.ndarray:
        if var_name not in self.var_names:
            logging.error(f"Variable name '{var_name}' not found in the file.")
            return np.array([])  # 返回一个空的 numpy 数组

        # 获取变量名在 var_names 中的索引
        col_index = self.var_names.index(var_name)

        # 使用 pandas 读取指定列的数据
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
            # jump the first two lines
            for _ in range(2):
                next(file)
            # get the line with variable names
            header_line = next(file)

        cleaned_header = header_line.replace("#", "")
        cleaned_header = re.sub(r"\d+:", " ", cleaned_header)
        variable_names = cleaned_header.split()

        return variable_names

    def data(self, var_name: str, dtype=float) -> np.ndarray:
        if var_name not in self.var_names:
            logging.error(f"Variable name '{var_name}' not found in the file.")
            return np.array([])  # 返回一个空的 numpy 数组

        # 获取变量名在 var_names 中的索引
        col_index = self.var_names.index(var_name)

        # 使用 pandas 读取指定列的数据
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
