"""HOSHI reader implementation (PEP8 module name: hoshi_reader).

Copied from original HoshiReader implementation; module filename uses
lowercase with underscore to follow PEP8 module naming.
"""

from pathlib import Path
import logging
import re
import os

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from pandas.api.types import is_integer_dtype, is_float_dtype, is_string_dtype

# Constants
G_GRAV = 6.67428e-8  # in cm^3/g/s^2
R_SUN = 6.9566e10  # in cm
M_SUN = 1.9891e33  # in g
L_SUN = 3.839e33  # in erg/


def _clean_series_and_cast(s: pd.Series, dtype):
    """Clean a string Series (remove commas, fix Fortran 'D' exponents and missing 'E')
    then cast to the requested dtype and return a numpy array.

    This mirrors the cleaning done in `_coerce_dtypes` so single-column reads behave
    the same as full-DataFrame coercion.
    """
    missing_vals = {"": np.nan, "NaN": np.nan, "nan": np.nan, "---": np.nan, "NA": np.nan, "N/A": np.nan}

    s_clean = s.astype(str).str.strip()
    s_clean = s_clean.replace(missing_vals)
    s_clean = s_clean.str.replace(",", "", regex=True)
    s_clean = s_clean.str.replace(r"[dD]", "E", regex=True)
    s_clean = s_clean.str.replace(
        r"(?P<mant>[+-]?(?:\d+\.\d*|\d*\.\d+|\d+))(?P<exp>[+-]\d{1,3})$",
        r"\g<mant>E\g<exp>",
        regex=True,
    )

    converted = pd.to_numeric(s_clean, errors="coerce")

    if dtype in (float, "float", "float64"):
        return converted.astype("float64").to_numpy()
    elif dtype in (int, "int", "int64"):
        # Follow _coerce_dtypes behavior: use nullable Int64 if there are NaNs
        if converted.isna().any():
            return converted.astype("Int64").to_numpy()
        else:
            return converted.astype("int64").to_numpy()
    else:
        return s_clean.where(s_clean.notna(), "").to_numpy()


def coerce_dtypes(df: pd.DataFrame, dtype=float, min_convert_frac: float = 0.99) -> pd.DataFrame:
    """Clean and coerce a DataFrame's columns to appropriate dtypes.

    This is the module-level version of the former class method. It applies the same
    cleaning rules (strip, remove commas, fix 'D' exponents and missing 'E',
    coerce to numeric) and returns a DataFrame with columns cast to numeric types
    where the fraction of convertible entries meets ``min_convert_frac``.

    Args:
        df: DataFrame with raw string columns to coerce.
        dtype: preferred numeric dtype for floats/ints.
        min_convert_frac: minimum fraction of non-empty entries that must be
            convertible to consider the column numeric.
    """
    int_cols = ["stg", "jcma", "nmlo", "ndv"]
    missing_vals = {"": np.nan, "NaN": np.nan, "nan": np.nan, "---": np.nan, "NA": np.nan, "N/A": np.nan}

    df_out = df.copy()
    for col in df_out.columns:
        s = df_out[col]
        s_clean = s.astype(str).str.strip()
        s_clean = s_clean.replace(missing_vals)
        s_clean = s_clean.str.replace(",", "", regex=True)
        s_clean = s_clean.str.replace(r"[dD]", "E", regex=True)
        s_clean = s_clean.str.replace(
            r"(?P<mant>[+-]?(?:\d+\.\d*|\d*\.\d+|\d+))(?P<exp>[+-]\d{1,3})$",
            r"\g<mant>E\g<exp>",
            regex=True,
        )

        non_empty_mask = s_clean.notna()
        n_non_empty = int(non_empty_mask.sum())
        if n_non_empty == 0:
            df_out[col] = pd.Series([np.nan] * len(df_out), index=df_out.index)
            continue

        converted = pd.to_numeric(s_clean, errors="coerce")
        n_converted = int((~converted[non_empty_mask].isna()).sum())
        frac = n_converted / n_non_empty

        if frac >= min_convert_frac:
            if col in int_cols:
                if converted.isna().any():
                    df_out[col] = converted.astype("Int64")
                else:
                    df_out[col] = converted.astype("int64")
            else:
                if dtype in (int, "int", "int64") and not converted.isna().any():
                    df_out[col] = converted.astype("int64")
                else:
                    df_out[col] = converted.astype("float64")
        else:
            df_out[col] = s_clean.where(s_clean.notna(), "")

    return df_out


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

def find_nearest(arr: np.ndarray, x: float, *, descending: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """Return the index and value nearest to ``x`` in ``arr``.

    Simpler, unified API: always returns ``(indices, values)`` where both are numpy arrays.
    For a single nearest element the returned arrays have length 1. The function expects the
    input to be sorted (ascending by default). Set ``descending=True`` for descending arrays.

    Args:
        arr: 1-D array-like sorted array.
        x: Target value.
        descending: If True, treat ``arr`` as sorted in descending order.

    Raises:
        ValueError: if ``arr`` is empty or no index can be determined.
    """
    a = np.asarray(arr)
    if a.size == 0:
        raise ValueError("find_nearest: empty input array")

    if descending:
        a_proc = a[::-1]
        pos = np.searchsorted(a_proc, x, side="left")
        candidates = []
        if pos - 1 >= 0:
            candidates.append(pos - 1)
        if pos < a_proc.size:
            candidates.append(pos)
        if not candidates:
            raise ValueError("find_nearest: index not found")
        best = min(candidates, key=lambda i: abs(a_proc[i] - x))
        idx = int(a.size - 1 - best)
        return np.array([idx], dtype=int), np.array([float(a[idx])], dtype=float)
    else:
        pos = np.searchsorted(a, x, side="left")
        candidates = []
        if pos - 1 >= 0:
            candidates.append(pos - 1)
        if pos < a.size:
            candidates.append(pos)
        if not candidates:
            raise ValueError("find_nearest: index not found")
        best = min(candidates, key=lambda i: abs(a[i] - x))
        idx = int(best)
        return np.array([idx], dtype=int), np.array([float(a[idx])], dtype=float)


def find_all_within(arr: np.ndarray, x: float, *, tol: float = 1e-3, descending: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """Return all indices and values within ``tol`` of ``x``.

    Returns ``(indices, values)``. Indices are ordered according to the array direction: for
    ascending arrays indices increase, for descending arrays they decrease.

    Args:
        arr: 1-D array-like.
        x: Target value.
        tol: Absolute tolerance.
        descending: If True, treat ``arr`` as sorted in descending order.

    Raises:
        ValueError: if input empty or no matches found.
    """
    a = np.asarray(arr)
    if a.size == 0:
        raise ValueError("find_all_within: empty input array")

    idxs = np.where(np.abs(a - x) <= float(tol))[0]
    if idxs.size == 0:
        raise ValueError("find_all_within: index not found")

    if descending:
        ordered = np.sort(idxs)[::-1]
    else:
        ordered = np.sort(idxs)

    return ordered.astype(int), a[ordered]


def find_first_greater(arr: np.ndarray, x: float, *, descending: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """Return the first index and value greater than ``x`` as arrays of length 1.

    Uses ``np.searchsorted`` for efficiency. For descending arrays the index is mapped back to
    the original array ordering.

    Args:
        arr: 1-D array-like sorted array.
        x: Threshold value.
        descending: If True, treat ``arr`` as sorted descending.

    Raises:
        ValueError: if input empty or no value greater than ``x`` exists.
    """
    a = np.asarray(arr)
    if a.size == 0:
        raise ValueError("find_first_greater: empty input array")

    if descending:
        a_rev = a[::-1]
        pos = np.searchsorted(a_rev, x, side="right")
        if pos >= a_rev.size:
            raise ValueError("find_first_greater: index not found")
        idx = int(a.size - 1 - pos)
        return np.array([idx], dtype=int), np.array([float(a[idx])], dtype=float)
    else:
        pos = np.searchsorted(a, x, side="right")
        if pos >= a.size:
            raise ValueError("find_first_greater: index not found")
        return np.array([int(pos)], dtype=int), np.array([float(a[pos])], dtype=float)


def find_first_less(arr: np.ndarray, x: float, *, descending: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """Return the first index and value less than ``x``.

    This helper is primarily intended for descending arrays. It reuses
    ``find_first_greater`` by negating the data: for any array ``a``,
    ``a[i] < x`` is equivalent to ``(-a)[i] > -x``. For descending arrays
    negating yields an ascending array so we call ``find_first_greater`` on
    ``-a`` with ``descending=False`` and map the result back to the original
    values/indices.

    For ascending arrays the function finds the first element less than ``x``
    by using ``np.searchsorted`` and returning the element at position
    ``pos-1`` (if exists).

    Args:
        arr: 1-D array-like sorted array.
        x: Threshold value.
        descending: If True (default), treat ``arr`` as sorted descending.

    Raises:
        ValueError: if input empty or no value less than ``x`` exists.
    """
    a = np.asarray(arr)
    if a.size == 0:
        raise ValueError("find_first_less: empty input array")

    if descending:
        # negate array and target, call existing function on ascending data
        idxs, _ = find_first_greater(-a, -x, descending=False)
        if idxs.size == 0:
            raise ValueError("find_first_less: index not found")
        return idxs, a[idxs]
    else:
        # ascending array: first element less than x is at pos-1
        pos = np.searchsorted(a, x, side="left")
        if pos == 0:
            raise ValueError("find_first_less: index not found")
        idx = int(pos - 1)
        return np.array([idx], dtype=int), np.array([float(a[idx])], dtype=float)

def get_var_from_block(file_path, target_block_idx, target_var_idx):
    """
    Parses a multi-block data file to extract a specific variable.
    
    The file structure is assumed to be:
    - Block Header: An integer N indicating the number of following data lines.
    - Block Body: N lines of data (variables).
    
    Comments (starting with #) and empty lines are ignored.

    :param file_path: Path to the input file.
    :param target_block_idx: The index of the target block (1-based).
    :param target_var_idx: The index of the variable within the target block (1-based).
    :return: The string content of the target line, or an error message if not found.
    """
    
    current_block_count = 0  # Counter for the blocks encountered so far
    lines_left_in_block = 0  # Number of data lines remaining in the current block
    current_var_count = 0    # Counter for variables within the current block
    
    found_target_block = False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # 1. Data Cleaning: Remove comments (#) and surrounding whitespace
                content = line.split('#')[0].strip()
                
                # 2. Skip empty lines
                if not content:
                    continue

                # --- State Machine Logic ---
                
                if lines_left_in_block > 0:
                    # [State A: Reading data within a block]
                    # Note: Even if 'content' is a number here, it is treated as data, 
                    # not a new block header.
                    
                    if found_target_block:
                        current_var_count += 1
                        # Check if this is the requested variable
                        if current_var_count == target_var_idx:
                            return content 
                    
                    # Decrement the remaining line count for the current block
                    lines_left_in_block -= 1
                    
                else:
                    # [State B: Searching for a new block Header]
                    # We expect an integer defining the size of the next block.
                    
                    if content.isdigit():
                        # New block header found
                        current_block_count += 1
                        lines_left_in_block = int(content) # Set expected data lines
                        current_var_count = 0 # Reset variable counter for the new block
                        
                        # Check if this is the target block
                        if current_block_count == target_block_idx:
                            found_target_block = True
                            
                            # Boundary Check: If the block size is smaller than the requested index
                            if target_var_idx > lines_left_in_block:
                                return f"Error: Target block has only {lines_left_in_block} lines; cannot fetch line {target_var_idx}."
                                
                            # Special Case: Empty block (size 0)
                            if lines_left_in_block == 0:
                                found_target_block = False

        return "Target not found (End of file or index out of bounds)"

    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

class HoshiModel:
    def __init__(self, work_dir):
        self.work_dir = Path(work_dir)
        self.summary_dir = self.work_dir / "summary"
        self.writestr_dir = self.work_dir / "writestr"
        self.HOSHI_DIR = os.getenv("HOSHI_DIR")
        self.check_dir()

    def check_dir(self):
        if not self.summary_dir.exists():
            logging.info("No summary directory found")
        if not self.writestr_dir.exists():
            logging.info("No writestr directory found")
        if not self.work_dir.exists():
            logging.error("env HOSHI_DIR not found")


class HoshiHistory(HoshiModel):

    def __init__(self, path: str | Path):
        p = Path(path)
        # Determine model work directory and data_path, then initialize base
        if p.is_dir():
            if str(path).endswith("summary") or p.name == "summary":
                work_dir = p.parent
                data_path = p / "summary.txt"
            else:
                work_dir = p
                data_path = p / "summary" / "summary.txt"
        elif p.is_file() and str(path).endswith("summary.txt"):
            work_dir = p.parent.parent
            data_path = p
        else:
            raise ValueError(
                "Invalid path provided. Path should be either a directory or a summary.txt file."
            )

        # initialize HoshiModel to set work_dir, summary_dir, writestr_dir
        super().__init__(work_dir)
        self.data_path = data_path
        self.var_names = self._get_var_names()

    def _get_var_names(self) -> list:
        with open(self.data_path, "r") as file:
            for line in file:
                if line.startswith("#"):
                    header_line = line
                    break

        cleaned_header = header_line.replace("#", "")
        cleaned_header = re.sub(r"\d+:", " ", cleaned_header)
        variable_names = cleaned_header.split()

        return variable_names

# ...existing code...
    def _coerce_dtypes(self, df: pd.DataFrame, dtype=float, min_convert_frac: float = 0.99) -> pd.DataFrame:
        """
        将读取到的 DataFrame 列转换为合适的数值/字符串类型，并作为类内部可复用方法。
        - 清洗：strip、去千分位逗号、把常见占位符视为缺失。
        - 如果非空条目中 >= min_convert_frac 可以转为数值，则把列转换为数值（其余置为 NaN）。
        - 对指定的 int 列使用 pandas 可空整型 Int64（如果存在 NaN）。
        """
        # Thin wrapper to the module-level coerce_dtypes for backward compatibility
        return coerce_dtypes(df, dtype=dtype, min_convert_frac=min_convert_frac)
# ...existing code...

    def _find_run_headers(self) -> list:
        headers = []
        with open(self.data_path, "r") as f:
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

        with open(self.data_path, "r") as f:
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
            self.data_path,
            comment="#",
            sep=r"\s+",
            engine="python",
            header=None,
            names=var_names,
            skiprows=data_start,
            nrows=nrows,
            dtype=str,
            na_values=["", "NaN", "nan"],
            keep_default_na=True,
        )

        df = self._coerce_dtypes(df, dtype=dtype)
        return df
    
    def _generate_combined_data(
        self,
        save_flag: bool = False,
        start_stg: int = 1,
        ) -> pd.DataFrame:
        
        idx_run = self.count_runs()
        df_combined = self.read_run(idx_run)
        stg_list = df_combined['stg'].to_numpy(dtype=int)
        end_idx = stg_list[0] - 1
        logging.info(f"End index of the last run: {end_idx}")

        idx_run -= 1
        while idx_run > 0 and end_idx > 0:
            idx_run -= 1
            df = self.read_run(idx_run)
            stg = df['stg'].to_numpy(dtype=int)
            if not end_idx in stg:
                logging.warning(f"End index {end_idx} not found in run {idx_run}, skipping it.")
                continue
            else:
                logging.info(f"Found end index {end_idx} in run {idx_run}.")
                cut_idx = np.where(stg == end_idx)[0][0]
                df_cut = df.iloc[:cut_idx+2]
                df_combined = pd.concat([df_cut, df_combined], ignore_index=True)
                logging.info(f"Combined DataFrame now has {len(df_combined)} rows.")
                stg_list = df_combined['stg'].to_numpy(dtype=int)
                if stg_list[0] == start_stg:
                    logging.info("Reached the beginning of the data.")
                    break
                else:
                    end_idx = stg_list[0] - 1
        if idx_run == 0:
            logging.info(f"Processed all runs. The beginning of the combined data is stg {stg_list[0]}.")
                
        check_list = np.arange(stg_list[0], stg_list[-1]+1, dtype=int)
        missing_stages = set(check_list) - set(stg_list)
        if missing_stages:
            logging.warning(f"Missing stages: {sorted(missing_stages)}")
        else:
            logging.info(f"No missing stages, data is continuous from {stg_list[0]} to {stg_list[-1]}.")
        
        if save_flag:
            save_path = self.data_path.parent / "summary_combined.txt"
            
            fmt_list = []
            header_fmt_list = []
            # Determine format for each column based on its dtype
            for c in df_combined.columns:
                col = df_combined[c]
                if is_integer_dtype(col.dtype):
                    fmt_list.append('%7d')
                    header_fmt_list.append('%7s')
                    df_combined[c] = col.astype('int64')
                elif is_float_dtype(col.dtype):
                    fmt_list.append('%15.6e')
                    header_fmt_list.append('%15s')
                    df_combined[c] = col.astype('float64')
                else:
                    fmt_list.append('%s')
                    header_fmt_list.append('%s')
                    df_combined[c] = col.astype(str)
            
            header_line = ' '.join(fmt % name for fmt, name in zip(header_fmt_list, df_combined.columns))

            with open(save_path, "w") as f:
                f.write(header_line + "\n")
                np.savetxt(f, df_combined.to_numpy(), fmt=fmt_list)
                    
            logging.info(f"Combined data saved to {save_path}")
        
        return self._coerce_dtypes(df_combined, dtype=float)
        

class HoshiHistoryCombined(HoshiHistory):
    def __init__(
        self, 
        path: str | Path, 
        save_flag: bool = False,
        quick: bool = False,
        ):
        super().__init__(path)
        new_path = self.data_path.parent / "summary_combined.txt"
        self.quick_mode = quick
        self.data_path = new_path
        if not new_path.exists():
            logging.info("Generating combined summary data ...")
            self.data_path = new_path.parent / "summary.txt"
            self.dataframe = self._generate_combined_data(save_flag=save_flag)
            if save_flag:
                self.data_path = new_path
                logging.info(f"Combined summary data file created at {self.data_path}")
        else:
            if not quick:
                logging.info("Loading existing combined summary data from file.")
                self.dataframe = pd.read_csv(
                    self.data_path,
                    comment="#",
                    sep=r"\s+",
                    engine="python",
                    header=0,
                    names=self.var_names,
                    dtype=str,
                    na_values=["", "NaN", "nan"],
                    keep_default_na=True,
                )
                self.dataframe = self._coerce_dtypes(self.dataframe, dtype=float)
            else:
                logging.info("Quick mode: skipping loading of combined summary data. To access data, use data() method which reads from file directly.")
                self.dataframe = None
        
    def data(self, var_name: str, dtype=float) -> np.ndarray:
        if var_name not in self.var_names:
            logging.error(f"Variable name '{var_name}' not found in the combined data.")
            return np.array([])
        
        if self.quick_mode or self.dataframe is None:
            df = pd.read_csv(
                self.data_path,
                sep=r"\s+",
                engine="python",
                header=0,
                usecols=[var_name],
                dtype=str,
                na_values=["", "NaN", "nan"],
                keep_default_na=True,
            )
            return _clean_series_and_cast(df[var_name], dtype)
        else:
            col_data = self.dataframe[var_name]
            if dtype in (float, "float", "float64"):
                return col_data.astype(float).to_numpy()
            elif dtype in (int, "int", "int64"):
                return col_data.astype(int).to_numpy()
            else:
                return col_data.to_numpy()


class HoshiProfile(HoshiModel):
    def __init__(
        self, 
        path: str, 
        str_num: int,
        quick: bool = False,
        ):
        p = Path(path)
        target = f"str{str_num:05d}.txt"
        # Determine work_dir and profile data_path
        if p.is_file() and str(path).endswith(target):
            # path is the profile file inside work_dir/writestr/strXXXXX.txt
            work_dir = p.parent.parent
            data_path = p
        elif str(path).endswith("writestr"):
            # path is the writestr directory
            work_dir = p.parent
            data_path = p / target
        elif p.is_dir() and (p / "evol").exists():
            # path is the model/work directory
            work_dir = p
            data_path = p / "writestr" / target
        else:
            logging.error(
                "Invalid path provided. Path should be either a directory or a profile file."
            )
            return

        # initialize base to set work_dir and related dirs
        super().__init__(work_dir)
        self.data_path = data_path
        self.var_names = self._get_var_names()
        self.quick_mode = quick
        if not quick:
            df = pd.read_csv(
                self.data_path,
                comment="#",
                sep=r"\s+",
                engine="python",
                header=0,
                names=self.var_names,
                dtype=str,
                na_values=["", "NaN", "nan"],
                keep_default_na=True,
            )
            self.dataframe = coerce_dtypes(df, dtype=float)
        else:
            self.dataframe = None
            logging.info("Quick mode: skipping loading of profile data. To access data, use data() method which reads from file directly.")
            return

    def _get_var_names(self) -> list:
        with open(self.data_path, "r") as file:
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

        if self.quick_mode or self.dataframe is None:
            df = pd.read_csv(
                self.data_path,
                sep=r"\s+",
                engine="python",
                header=0,
                usecols=[var_name],
                dtype=str,
                na_values=["", "NaN", "nan"],
                keep_default_na=True,
            )
            return _clean_series_and_cast(df[var_name], dtype)
        else:
            col_data = self.dataframe[var_name]
            if dtype in (float, "float", "float64"):
                return col_data.astype(float).to_numpy()
            elif dtype in (int, "int", "int64"):
                return col_data.astype(int).to_numpy()
            else:
                return col_data.to_numpy()

class HoshiNucNetwork(HoshiModel):
    def __init__(
        self,
        work_dir: str | Path,
        ):
        super().__init__(work_dir)
        p = get_var_from_block(
            file_path=self.work_dir / "param" / "files.data",
            target_block_idx=1,
            target_var_idx=3,
        )
        p = Path(p)
        if not p.is_absolute():
            p = self.HOSHI_DIR / p
        if not p.exists():
            logging.error(f"Nuclear network file not found at {p}")
            return
        self.network_path = p
        # parse network file into a dictionary mapping isotope name -> properties
        self.nuc_dic = self._parse_network_file()
        self.nuc_list = list(self.nuc_dic.keys())

    def _parse_network_file(self) -> dict:
        """Parse the nuclear network file and return a dict of nuclide properties.

        The expected file format (example lines):
          1  300
             2     1     n       1.000   0   1   0.5     8.071  awns

        Notes:
        - The file often contains leading line/index columns; we skip the first 6
          characters of each line before splitting the meaningful fields.
        - The first non-empty line gives the total number of nuclides (we attempt
          to parse it but do not require it to be exact).
        - For each nuclide line we read: name, mass_number, Z, N, spin, mass_excess, label
        - Returns a dict keyed by the nuclide name (string) with values being
          dictionaries containing parsed numeric values.
        """
        nuclides = {}
        try:
            with open(self.network_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            logging.error(f"Failed to read nuclear network file {self.network_path}: {e}")
            return nuclides

        # find first non-empty line and try to parse total count (optional)
        total_expected = None
        for i, line in enumerate(lines):
            s = line.strip()
            if not s:
                continue
            # skip leading 6 chars if present
            body = line[6:].strip() if len(line) > 6 else line.strip()
            if not body:
                continue
            parts = body.split()
            # if first meaningful line contains a single integer, take it as total
            if total_expected is None:
                try:
                    # sometimes the first meaningful token is total count
                    total_expected = int(parts[0])
                except Exception:
                    # fallback: try second token
                    if len(parts) > 1:
                        try:
                            total_expected = int(parts[1])
                        except Exception:
                            total_expected = None
                # continue to parse subsequent lines
                continue

        # parse nuclide lines
        for line in lines:
            if not line.strip():
                continue
            body = line[6:].strip() if len(line) > 6 else line.strip()
            if not body:
                continue
            parts = body.split()
            # skip lines that look like a header containing only a count
            if len(parts) < 2:
                continue
            # If this line is just the total count, skip
            try:
                if len(parts) == 1 and int(parts[0]) == total_expected:
                    continue
            except Exception:
                pass

            # Expect at least 7 columns after skipping indices: name, mass, Z, N, spin, mass_excess, label
            if len(parts) < 7:
                # not enough columns; skip or warn
                logging.debug(f"Skipping unparsable network line: '{body}'")
                continue

            name = parts[0]
            # mass number may be provided as float-like (e.g. '12.000')
            try:
                mass_number = int(float(parts[1]))
            except Exception:
                mass_number = None
            try:
                Z = int(float(parts[2]))
            except Exception:
                Z = None
            try:
                N = int(float(parts[3]))
            except Exception:
                N = None
            try:
                spin = float(parts[4])
            except Exception:
                spin = None
            try:
                mass_excess = float(parts[5])
            except Exception:
                mass_excess = None
            label = " ".join(parts[6:]) if len(parts) > 6 else ""

            nuclides[name] = {
                "mass_number": mass_number,
                "Z": Z,
                "N": N,
                "spin": spin,
                "mass_excess": mass_excess,
                "label": label,
            }

        if total_expected is not None and total_expected != len(nuclides):
            logging.debug(f"Parsed {len(nuclides)} nuclides, expected {total_expected} (from file header)")

        return nuclides


# class HoshiCxdata(HoshiModel):
#     def __init__(
#         self, 
#         path: str, 
#         str_num: int,
#         ):
#         p = Path(path)
#         target = f"cxdat{str_num:05d}.txt"
#         # Determine work_dir and profile data_path
#         if p.is_file() and str(path).endswith(target):
#             # path is the profile file inside work_dir/cxdata/cxdatXXXXX.txt
#             work_dir = p.parent.parent
#             data_path = p
#         elif str(path).endswith("cxdata"):
#             # path is the cxdata directory
#             work_dir = p.parent
#             data_path = p / target
#         elif p.is_dir() and (p / "evol").exists():
#             # path is the model/work directory
#             work_dir = p
#             data_path = p / "cxdata" / target
#         else:
#             logging.error(
#                 "Invalid path provided. Path should be either a directory or a profile file."
#             )
#             return
        
#         # initialize base to set work_dir and related dirs
#         super().__init__(work_dir)
#         self.data_path = data_path
        
