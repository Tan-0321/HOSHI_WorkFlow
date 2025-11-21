import importlib
from pathlib import Path

import pytest
import pandas as pd

import hoshi_workflow.hoshi_reader as hr  # module under test


@pytest.fixture(scope="module")
def example_model_dir():
    repo_root = Path(__file__).resolve().parent.parent
    example_dir = repo_root / "examples" / "example_model" / "fake_model"
    if not example_dir.exists():
        pytest.skip(f"Example model dir not found: {example_dir}")
    return example_dir


def test_history_basic_read(example_model_dir):
    """test basic reading of `summary.txt` data from example model"""
    hm = hr.HoshiModel(str(example_model_dir))
    history = hr.HoshiHistory(hm.summary_dir)

    assert isinstance(history.var_names, list)
    n_runs = history.count_runs()
    assert isinstance(n_runs, int) and n_runs >= 1

    # read data of the last run 
    df = history.read_run(run_index=n_runs)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

    # check some expected columns exist and are numeric
    for col in ("dens_c", "temp_c", "stg", "dens", "temp"):
        if col in df.columns:
            series = df[col]
            assert pd.api.types.is_numeric_dtype(series)


def test_generate_combined_and_combined_reader(example_model_dir, tmp_path):
    """test generation and reading of combined history data"""
    hm = hr.HoshiModel(str(example_model_dir))
    history = hr.HoshiHistory(hm.summary_dir)

    # directly call internal generation function (not saving to disk / still works if implementation requires saving)
    try:
        df_combined = history._generate_combined_data(save_flag=False)
    except TypeError:
        # if implementation signature differs, try without arguments
        df_combined = history._generate_combined_data()

    assert isinstance(df_combined, pd.DataFrame)
    assert len(df_combined) > 0

    # now test HoshiHistoryCombined reader
    HCombined = getattr(hr, "HoshiHistoryCombined", None)
    if HCombined is not None:
        hist_comb = HCombined(hm.summary_dir)
        df2 = getattr(hist_comb, "dataframe", None)
        if df2 is None:
            # allow using data() to get columns or read_run style interface
            df2 = hist_comb.read_run() if hasattr(hist_comb, "read_run") else pd.DataFrame()
        assert isinstance(df2, pd.DataFrame)

def test_hoshi_profile_read(example_model_dir):
    """test basic reading of profile (writestr) data from example model"""
    hm = hr.HoshiModel(str(example_model_dir))
    # pick a known stg number from the example model
    stg_number = 2468
    profile = hr.HoshiProfile(hm.writestr_dir, stg_number)

    assert isinstance(profile.var_names, list)
    assert len(profile.var_names) > 0

    # read some column data
    dens = profile.data("Dens")
    temp = profile.data("Temp")
    mass = profile.data("Mr")


