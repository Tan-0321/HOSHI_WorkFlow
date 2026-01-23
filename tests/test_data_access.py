"""Test script to verify data resource access functionality."""

import sys
from pathlib import Path

def test_imports():
    """Test that the data module can be imported."""
    try:
        from hoshi_workflow.data import (
            get_data_path,
            get_stable_isotopes_path,
            load_stable_isotopes,
            get_solar_stable_path
        )
        print("✓ Successfully imported all functions from hoshi_workflow.data")
        return True
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        return False


def test_get_path():
    """Test getting the stable isotopes file path."""
    try:
        from hoshi_workflow.data import get_stable_isotopes_path
        path = get_stable_isotopes_path()
        print(f"✓ Found stable.txt at: {path}")
        
        if not path.exists():
            print(f"✗ File does not exist at {path}")
            return False
        
        print(f"✓ File exists and is accessible")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_load_data():
    """Test loading and parsing stable isotopes data."""
    try:
        from hoshi_workflow.data import load_stable_isotopes
        isotopes = load_stable_isotopes()
        
        if 'data' not in isotopes or 'path' not in isotopes:
            print("✗ Loaded data missing required keys")
            return False
        
        data = isotopes['data']
        path = isotopes['path']
        
        print(f"✓ Loaded {len(data)} stable isotopes from {path}")
        
        # Check first few entries
        if len(data) >= 3:
            print("\nFirst 3 isotopes:")
            for i, (A, Z, elem, abund) in enumerate(data[:3], 1):
                print(f"  {i}. {elem}-{A} (Z={Z}): {abund:.2e}")
        
        # Verify data structure
        A, Z, elem, abund = data[0]
        if not isinstance(A, int):
            print(f"✗ Mass number should be int, got {type(A)}")
            return False
        if not isinstance(Z, int):
            print(f"✗ Atomic number should be int, got {type(Z)}")
            return False
        if not isinstance(elem, str):
            print(f"✗ Element should be str, got {type(elem)}")
            return False
        if not isinstance(abund, float):
            print(f"✗ Abundance should be float, got {type(abund)}")
            return False
        
        print("✓ Data structure is correct")
        return True
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_content():
    """Test reading file content directly."""
    try:
        from hoshi_workflow.data import get_stable_isotopes_path
        path = get_stable_isotopes_path()
        
        with open(path, 'r') as f:
            lines = f.readlines()
        
        if len(lines) == 0:
            print("✗ File is empty")
            return False
        
        print(f"✓ File contains {len(lines)} lines")
        
        # Check for expected format
        first_line = lines[0].strip()
        parts = first_line.split()
        if len(parts) >= 4:
            print(f"✓ First line format looks correct: {first_line}")
        else:
            print(f"⚠ First line might have unexpected format: {first_line}")
        
        return True
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("Testing hoshi_workflow.data module")
    print("="*60)
    print()
    
    tests = [
        ("Import test", test_imports),
        ("Path access test", test_get_path),
        ("Data loading test", test_load_data),
        ("File content test", test_file_content),
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n{name}:")
        print("-" * 40)
        result = test_func()
        results.append((name, result))
        print()
    
    print("="*60)
    print("Test Summary")
    print("="*60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
