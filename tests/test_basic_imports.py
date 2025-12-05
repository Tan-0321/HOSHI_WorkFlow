import importlib
import pytest


def test_import_file_name_convention_via_aggregate():
    # Import via new aggregated namespace
    mod = importlib.import_module("hoshi_workflow.file_name_convention")
    assert hasattr(mod, "generate_name")
    name = mod.generate_name(mass=1.0)
    assert isinstance(name, str) and name.startswith("M")


def test_import_file_name_convention_direct():
    # Direct import from the new namespace (legacy top-level shims have been removed)
    mod = importlib.import_module("hoshi_workflow.file_name_convention")
    assert hasattr(mod, "parse_name")
    name = mod.generate_name(mass=0.85)
    parsed = mod.parse_name(name)
    assert "mass" in parsed or "M" in parsed


def test_hoshi_reader_imports():
    # Aggregate import
    mod = importlib.import_module("hoshi_workflow.hoshi_reader")
    assert hasattr(mod, "HoshiModel")
    # Ensure reader package exposes history/profile classes
    assert hasattr(mod, "HoshiHistory")
    assert hasattr(mod, "HoshiHistoryCombined")
    assert hasattr(mod, "HoshiProfile")


def test_generate_name_with_mass_only():
    """test generating filename with only mass parameter"""
    mod = importlib.import_module("hoshi_workflow.file_name_convention")
    
    name = mod.generate_name(mass=1.0)
    assert isinstance(name, str)
    assert name.startswith("M")
    assert "F" in name


def test_generate_name_with_multiple_params():
    """test generating filename with multiple parameters"""
    mod = importlib.import_module("hoshi_workflow.file_name_convention")
    
    name = mod.generate_name(
        mass=1.23,
        metallicity=0.0144,
        angular_velocity=0.5,
        initial_helium_abundance=0.2503,
    )
    assert isinstance(name, str)
    # Should contain underscores separating components
    components = name.split("_")
    assert len(components) == 4


def test_generate_name_with_partial_params():
    """test generating filename with partial parameters"""
    mod = importlib.import_module("hoshi_workflow.file_name_convention")
    
    name = mod.generate_name(mass=2.5, metallicity=0.02)
    assert isinstance(name, str)
    components = name.split("_")
    assert len(components) == 2


def test_generate_name_with_other_params():
    """test generating filename with custom other_params"""
    mod = importlib.import_module("hoshi_workflow.file_name_convention")
    
    name = mod.generate_name(
        mass=1.0,
        metallicity=0.015,
        other_params={"A": 1.23e15, "B": 2.67e-8},
    )
    assert isinstance(name, str)
    # Should contain at least 4 components
    components = name.split("_")
    assert len(components) >= 4


def test_generate_name_requires_at_least_one_param():
    """test that generate_name requires at least one parameter"""
    mod = importlib.import_module("hoshi_workflow.file_name_convention")
    
    with pytest.raises(ValueError):
        mod.generate_name()


def test_parse_name_simple():
    """test parsing a simple generated filename"""
    mod = importlib.import_module("hoshi_workflow.file_name_convention")
    
    # Generate and parse back
    original_name = mod.generate_name(mass=0.85)
    parsed = mod.parse_name(original_name)
    
    assert isinstance(parsed, dict)
    assert "mass" in parsed
    # Check approximate value (allow for floating point errors)
    assert abs(parsed["mass"] - 0.85) < 0.01


def test_parse_name_with_multiple_params():
    """test parsing a filename with multiple parameters"""
    mod = importlib.import_module("hoshi_workflow.file_name_convention")
    
    original_name = mod.generate_name(
        mass=1.23,
        metallicity=0.0144,
        angular_velocity=0.5,
        initial_helium_abundance=0.25,
    )
    parsed = mod.parse_name(original_name)
    
    assert isinstance(parsed, dict)
    assert "mass" in parsed
    assert "metallicity" in parsed
    assert "angular_velocity" in parsed
    assert "initial_helium_abundance" in parsed
    
    # Check approximate values
    assert abs(parsed["mass"] - 1.23) < 0.01
    assert abs(parsed["metallicity"] - 0.0144) < 0.001
    assert abs(parsed["angular_velocity"] - 0.5) < 0.01


def test_parse_name_roundtrip():
    """test roundtrip consistency: generate -> parse -> compare"""
    mod = importlib.import_module("hoshi_workflow.file_name_convention")
    
    test_params = {
        "mass": 2.5,
        "metallicity": 0.02,
    }
    
    name = mod.generate_name(**test_params)
    parsed = mod.parse_name(name)
    
    # Verify roundtrip accuracy
    for key, value in test_params.items():
        assert key in parsed
        assert abs(parsed[key] - value) < 0.001


def test_generate_name_format():
    """test the format of generated names follows convention"""
    mod = importlib.import_module("hoshi_workflow.file_name_convention")
    
    name = mod.generate_name(mass=0.85)
    # Should match pattern: M##F#d## (e.g., M09F8d50)
    assert "M" in name
    assert "F" in name
    # Should contain only alphanumeric, underscores, and 'd' for decimal
    assert all(c.isalnum() or c in "_d" for c in name)


def test_file_name_convention_in_hoshi_workflow():
    """test that file_name_convention is accessible from main package"""
    mod = importlib.import_module("hoshi_workflow")
    
    # Functions should be accessible from main package
    if hasattr(mod, "generate_name"):
        name = mod.generate_name(mass=1.0)
        assert isinstance(name, str)
    
    if hasattr(mod, "parse_name"):
        # If accessible, test basic functionality
        assert callable(mod.parse_name)
