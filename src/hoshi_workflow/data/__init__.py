"""Data resource access module for hoshi_workflow.

This module provides safe access to package data files like solar abundance
tables (e.g., stable.txt) regardless of where the package is installed.
"""

from pathlib import Path
from typing import Union
import sys

__all__ = ["get_data_path", "get_stable_isotopes_path", "load_stable_isotopes"]


def get_data_path() -> Path:
    """Get the absolute path to the data directory in the installed package.
    
    Returns:
        Path: Absolute path to the data directory.
        
    Raises:
        FileNotFoundError: If the data directory cannot be found.
    """
    # Use __file__ to locate this module's directory, then find data directory
    this_dir = Path(__file__).resolve().parent
    
    if not this_dir.exists():
        raise FileNotFoundError(
            f"Cannot locate hoshi_workflow data directory at {this_dir}"
        )
    
    return this_dir


def get_stable_isotopes_path() -> Path:
    """Get the absolute path to the stable isotopes data file (stable.txt).
    
    This file contains solar abundance data for stable isotopes in the format:
    A  Z  Element  Abundance
    
    Returns:
        Path: Absolute path to stable.txt
        
    Raises:
        FileNotFoundError: If the stable.txt file cannot be found.
        
    Example:
        >>> from hoshi_workflow.data import get_stable_isotopes_path
        >>> stable_path = get_stable_isotopes_path()
        >>> with open(stable_path) as f:
        ...     data = f.read()
    """
    data_dir = get_data_path()
    stable_path = data_dir / "solar" / "stable.txt"
    
    if not stable_path.exists():
        raise FileNotFoundError(
            f"stable.txt not found at {stable_path}. "
            "This file should be included with the hoshi_workflow package."
        )
    
    return stable_path


def load_stable_isotopes() -> dict:
    """Load stable isotopes data from stable.txt into a structured dictionary.
    
    Returns:
        dict: Dictionary with keys:
            - 'data': list of tuples (A, Z, element, abundance)
            - 'path': Path object pointing to the source file
            
    Example:
        >>> from hoshi_workflow.data import load_stable_isotopes
        >>> isotopes = load_stable_isotopes()
        >>> for A, Z, elem, abund in isotopes['data'][:5]:
        ...     print(f"{elem}-{A}: {abund}")
    """
    import numpy as np
    
    stable_path = get_stable_isotopes_path()
    data = []
    
    with open(stable_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and end marker
            if not line or line.startswith('end'):
                continue
            
            parts = line.split()
            if len(parts) >= 4:
                try:
                    A = int(parts[0])           # Mass number
                    Z = int(parts[1])           # Atomic number
                    element = parts[2]          # Element symbol
                    # Handle scientific notation like 2.79d+10
                    abundance_str = parts[3].replace('d', 'e').replace('D', 'e')
                    abundance = float(abundance_str)
                    data.append((A, Z, element, abundance))
                except (ValueError, IndexError):
                    # Skip lines that don't parse correctly
                    continue
    
    return {
        'data': data,
        'path': stable_path
    }


# Convenience function for backward compatibility with old code
def get_solar_stable_path() -> Path:
    """Alias for get_stable_isotopes_path() for backward compatibility.
    
    Returns:
        Path: Absolute path to stable.txt
    """
    return get_stable_isotopes_path()
