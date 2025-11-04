import importlib


def test_import_file_name_convention_via_aggregate():
    # Import via new aggregated namespace
    mod = importlib.import_module("hoshi_workflow.file_name_convention")
    assert hasattr(mod, "generate_name")
    name = mod.generate_name(mass=1.0)
    assert isinstance(name, str) and name.startswith("M")


def test_import_file_name_convention_via_shim():
    # Import via legacy top-level shim
    mod = importlib.import_module("file_name_convention")
    assert hasattr(mod, "parse_name")
    name = mod.generate_name(mass=0.85)
    parsed = mod.parse_name(name)
    assert "mass" in parsed or "M" in parsed


def test_hoshi_reader_imports():
    # Aggregate import
    mod = importlib.import_module("hoshi_workflow.hoshi_reader")
    assert hasattr(mod, "HoshiModel")

    # Legacy shim
    mod2 = importlib.import_module("HOSHI_reader")
    assert hasattr(mod2, "HoshiHistory")
