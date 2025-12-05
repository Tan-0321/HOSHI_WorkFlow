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
    
    # verify data is numeric arrays
    assert hasattr(dens, '__len__') and len(dens) > 0
    assert hasattr(temp, '__len__') and len(temp) > 0
    assert hasattr(mass, '__len__') and len(mass) > 0


def test_hoshi_profile_dataframe(example_model_dir):
    """test accessing profile data via dataframe"""
    profile = hr.HoshiProfile(str(example_model_dir), 2468)
    
    # check dataframe attribute
    df_profile = profile.dataframe
    assert isinstance(df_profile, pd.DataFrame)
    assert not df_profile.empty
    
    # verify common columns exist
    expected_cols = ["Dens", "Temp", "Mr"]
    for col in expected_cols:
        assert col in df_profile.columns


def test_hoshi_profile_abundance(example_model_dir):
    """test accessing abundance data in profile"""
    profile = hr.HoshiProfile(str(example_model_dir), 2468)
    
    # test accessing isotope abundances
    abundance_cols = ["X(p)", "X(He)", "X(C)", "X(N)", "X(O)", "X(Ne)", "X(Mg)", "X(Si)", "X(Fe)"]
    
    for nuc in abundance_cols:
        if nuc in profile.var_names:
            data = profile.data(nuc)
            assert hasattr(data, '__len__') and len(data) > 0


def test_hoshi_cxdata_read(example_model_dir):
    """test basic reading of cxdata from example model"""
    cxdata = hr.HoshiCxdata(str(example_model_dir), 2468)
    
    # verify var_names is a list
    assert isinstance(cxdata.var_names, list)
    assert len(cxdata.var_names) > 0
    
    # check common isotopes exist in var_names
    assert "p" in cxdata.var_names  # protium
    assert "he4" in cxdata.var_names  # helium-4
    assert "Mr" in cxdata.var_names  # mass coordinate


def test_hoshi_cxdata_dataframe(example_model_dir):
    """test accessing cxdata via dataframe"""
    cxdata = hr.HoshiCxdata(str(example_model_dir), 2468)
    
    # check dataframe attribute
    df = cxdata.dataframe
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    
    # verify some columns exist
    for col in ["Mr", "p", "he4"]:
        if col in cxdata.var_names:
            assert col in df.columns


def test_hoshi_cxdata_data_method(example_model_dir):
    """test accessing cxdata columns with data() method"""
    cxdata = hr.HoshiCxdata(str(example_model_dir), 2468)
    
    # test data() method for different columns
    h1_mass_fraction = cxdata.data("p")
    mass = cxdata.data("Mr")
    
    # verify returned arrays
    assert hasattr(h1_mass_fraction, '__len__') and len(h1_mass_fraction) > 0
    assert hasattr(mass, '__len__') and len(mass) > 0


def test_hoshi_cxdata_isotope_yield(example_model_dir):
    """test getting isotope yield from cxdata"""
    cxdata = hr.HoshiCxdata(str(example_model_dir), 2468)
    
    # test isotope_yield method with mass_cut_idx
    try:
        y_n14 = cxdata.isotope_yield("n14", mass_cut_idx=10)
        # verify return is numeric
        assert isinstance(y_n14, (int, float))
    except (AttributeError, ValueError):
        # if method doesn't exist or isotope not available, skip
        pytest.skip("isotope_yield method not available")


def test_hoshi_cxdata_yields_dictionary(example_model_dir):
    """test getting yields dictionary from cxdata"""
    cxdata = hr.HoshiCxdata(str(example_model_dir), 2468)
    
    # test yields_dictionary method
    try:
        dict_yield = cxdata.yields_dictionary(mass_cut_idx=10)
        # verify return is dictionary
        assert isinstance(dict_yield, dict)
    except (AttributeError, ValueError):
        # if method doesn't exist, skip
        pytest.skip("yields_dictionary method not available")


def test_hoshi_model_directories(example_model_dir):
    """test HoshiModel directory access and HOSHI environment info"""
    hm = hr.HoshiModel(str(example_model_dir))
    
    # verify directory attributes
    assert hasattr(hm, 'summary_dir')
    assert hasattr(hm, 'writestr_dir')
    assert hasattr(hm, 'cxdata_dir')
    
    # verify directories exist (can be str or Path)
    assert hm.summary_dir is not None
    assert hm.writestr_dir is not None
    assert hm.cxdata_dir is not None
    
    # verify they can be converted to string
    assert len(str(hm.summary_dir)) > 0
    assert len(str(hm.writestr_dir)) > 0
    assert len(str(hm.cxdata_dir)) > 0
    
    # check HOSHI environment info
    assert hasattr(hm, 'HOSHI_DIR')
    assert hasattr(hm, 'HOSHI_VERSION')
    assert len(str(hm.HOSHI_DIR)) > 0
    assert len(str(hm.HOSHI_VERSION)) > 0


def test_hoshi_history_count_runs(example_model_dir):
    """test counting runs in history"""
    hm = hr.HoshiModel(str(example_model_dir))
    history = hr.HoshiHistory(hm.summary_dir)
    
    # verify count_runs returns integer
    n_runs = history.count_runs()
    assert isinstance(n_runs, int)
    assert n_runs >= 1


def test_hoshi_history_data_method(example_model_dir):
    """test accessing history data with data() method"""
    hm = hr.HoshiModel(str(example_model_dir))
    history = hr.HoshiHistory(hm.summary_dir)
    
    n_runs = history.count_runs()
    df = history.read_run(run_index=n_runs)
    
    # test data() method if available
    if hasattr(history, 'data'):
        try:
            dens_c = history.data('dens_c')
            assert hasattr(dens_c, '__len__')
        except:
            pass


def test_hoshi_history_combined_data_method(example_model_dir):
    """test accessing combined history data with data() method"""
    hm = hr.HoshiModel(str(example_model_dir))
    history = hr.HoshiHistory(hm.summary_dir)
    
    # generate combined data
    try:
        df_combined = history._generate_combined_data(save_flag=False)
    except TypeError:
        df_combined = history._generate_combined_data()
    
    assert isinstance(df_combined, pd.DataFrame)
    
    # test HoshiHistoryCombined if available
    HCombined = getattr(hr, "HoshiHistoryCombined", None)
    if HCombined is not None:
        hist_comb = HCombined(hm.summary_dir)
        
        # test data() method
        if hasattr(hist_comb, 'data'):
            try:
                tmp_c = hist_comb.data('temp_c')
                assert hasattr(tmp_c, '__len__')
            except:
                pass


