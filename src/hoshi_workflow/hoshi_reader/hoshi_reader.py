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
from pandas.api.types import is_integer_dtype, is_float_dtype, is_string_dtype

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

    def __init__(self, path: str | Path):
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

# ...existing code...
    def _coerce_dtypes(self, df: pd.DataFrame, dtype=float, min_convert_frac: float = 0.99) -> pd.DataFrame:
        """
        将读取到的 DataFrame 列转换为合适的数值/字符串类型，并作为类内部可复用方法。
        - 清洗：strip、去千分位逗号、把常见占位符视为缺失。
        - 如果非空条目中 >= min_convert_frac 可以转为数值，则把列转换为数值（其余置为 NaN）。
        - 对指定的 int 列使用 pandas 可空整型 Int64（如果存在 NaN）。
        """
        int_cols = ['stg', 'jcma', 'nmlo', 'ndv']
        # 常见占位符映射为缺失
        missing_vals = {"": np.nan, "NaN": np.nan, "nan": np.nan, "---": np.nan, "NA": np.nan, "N/A": np.nan}

        for col in df.columns:
            s = df[col]

            # 统一为字符串再清洗（安全），但保留原有 NA 为 np.nan
            s_clean = s.astype(str).str.strip()
            # 把像 "nan"、""、"---" 等视为缺失
            s_clean = s_clean.replace(missing_vals)
            # 去掉千分位逗号
            s_clean = s_clean.str.replace(",", "", regex=True)

            # 标记非空条目（清洗后）
            non_empty_mask = s_clean.notna()
            n_non_empty = int(non_empty_mask.sum())
            if n_non_empty == 0:
                # 全为空，设为全 NaN（float 类型）
                df[col] = pd.Series([np.nan] * len(df), index=df.index)
                continue

            converted = pd.to_numeric(s_clean, errors="coerce")
            n_converted = int((~converted[non_empty_mask].isna()).sum())
            frac = n_converted / n_non_empty

            if frac >= min_convert_frac:
                # 接受数值列（其余为 NaN）
                if col in int_cols:
                    # 如果存在 NaN，使用可空 Int64；否则用 int64
                    if converted.isna().any():
                        df[col] = converted.astype("Int64")
                    else:
                        df[col] = converted.astype("int64")
                else:
                    # 根据 dtype 参数选择 float 或 int
                    if dtype in (int, "int", "int64") and not converted.isna().any():
                        df[col] = converted.astype("int64")
                    else:
                        df[col] = converted.astype("float64")
            else:
                # 不满足转换比例，保留清洗后的字符串（空值设为 "" 保持 object）
                df[col] = s_clean.where(s_clean.notna(), "")
        return df
# ...existing code...

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
        ) -> pd.DataFrame:
        
        idx_run = self.count_runs()
        df_combined = self.read_run(idx_run)
        stg = df_combined['stg'].to_numpy(dtype=int)
        end_idx = stg[0] - 1
        logging.info(f"End index of the last run: {end_idx}")

        while idx_run > 0:
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
                if stg_list[0] == 1:
                    logging.info("Reached the beginning of the data.")
                    break
                else:
                    end_idx = stg_list[0] - 1
                
        check_list = np.arange(stg_list[0], stg_list[-1]+1, dtype=int)
        missing_stages = set(check_list) - set(stg_list)
        if missing_stages:
            logging.warning(f"Missing stages: {sorted(missing_stages)}")
        else:
            logging.info(f"No missing stages, data is continuous from {stg_list[0]} to {stg_list[-1]}.")
        
        if save_flag:
            save_path = self.path.parent / "summary_combined.txt"
            
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
        new_path = self.path.parent / "summary_combined.txt"
        self.quick_mode = quick
        self.path = new_path
        if not new_path.exists():
            if save_flag:
                logging.info("Generating combined summary data and saving to file.")
                
            self.dataframe = self._generate_combined_data(save_flag=save_flag)
        else:
            if not quick:
                logging.info("Loading existing combined summary data from file.")
                self.dataframe = pd.read_csv(
                    self.path,
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
                self.path, 
                sep=r'\s+', 
                engine="python",
                header=0, 
                usecols=[var_name], 
                dtype=dtype
            )
            return df[var_name].values
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
        self.quick_mode = quick
        if not quick:
            self.dataframe = pd.read_csv(
                self.path,
                comment="#",
                sep=r"\s+",
                engine="python",
                header=0,
                names=self.var_names,
                dtype=str,
                na_values=["", "NaN", "nan"],
                keep_default_na=True,
            )
        else:
            self.dataframe = None
            logging.info("Quick mode: skipping loading of profile data. To access data, use data() method which reads from file directly.")
            return

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

        if self.quick_mode or self.dataframe is None:
            df = pd.read_csv(
                self.path, 
                sep=r'\s+', 
                engine="python",
                header=0, 
                usecols=[var_name], 
                dtype=dtype
            )
            return df[var_name].values
        else:
            col_data = self.dataframe[var_name]
            if dtype in (float, "float", "float64"):
                return col_data.astype(float).to_numpy()
            elif dtype in (int, "int", "int64"):
                return col_data.astype(int).to_numpy()
            else:
                return col_data.to_numpy()

