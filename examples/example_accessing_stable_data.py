"""
Example: Accessing Solar Stable Isotopes Data

This example demonstrates how to access the stable.txt data file
from anywhere using hoshi_workflow.data module.
"""

# %%
# Import the data access functions
from hoshi_workflow.data import (
    get_stable_isotopes_path, 
    load_stable_isotopes
)
import pandas as pd
import numpy as np

# %%
# Method 1: Get the file path and read it yourself
print("Method 1: Get file path")
print("-" * 50)

stable_path = get_stable_isotopes_path()
print(f"stable.txt is located at:\n{stable_path}\n")

# Read the file
with open(stable_path, 'r') as f:
    # Read first 10 lines
    for i, line in enumerate(f):
        if i >= 10:
            break
        print(line.rstrip())

# %%
# Method 2: Load parsed data directly
print("\n\nMethod 2: Load parsed data")
print("-" * 50)

isotopes = load_stable_isotopes()
data = isotopes['data']
path = isotopes['path']

print(f"Loaded from: {path}")
print(f"Total isotopes: {len(data)}\n")

# Display first 10 isotopes
print("First 10 isotopes:")
print(f"{'Element':<8} {'A':<4} {'Z':<4} {'Abundance':>15}")
print("-" * 40)
for A, Z, elem, abund in data[:10]:
    print(f"{elem:<8} {A:<4} {Z:<4} {abund:>15.3e}")

# %%
# Method 3: Load into pandas DataFrame
print("\n\nMethod 3: Pandas DataFrame")
print("-" * 50)

# Read directly into DataFrame
df = pd.read_csv(
    stable_path,
    sep=r'\s+',
    names=['A', 'Z', 'Element', 'Abundance'],
    comment='#'
)

# Remove 'end' marker and any rows with nan
df = df[df['Element'] != 'end'].copy()
df = df.dropna()

# Convert abundance strings to float (handle Fortran notation)
df['Abundance'] = df['Abundance'].astype(str).str.replace('d', 'e', case=False)
df['Abundance'] = pd.to_numeric(df['Abundance'], errors='coerce')
df = df.dropna()  # Remove any remaining NaN values

# Convert A and Z to integers
df['A'] = df['A'].astype(int)
df['Z'] = df['Z'].astype(int)

print(f"DataFrame shape: {df.shape}")
print(f"\nFirst 10 rows:")
print(df.head(10))

# %%
# Example Analysis: Most abundant isotopes
print("\n\nMost abundant isotopes:")
print("-" * 50)

top_10 = df.nlargest(10, 'Abundance')
print(top_10.to_string(index=False))

# %%
# Example Analysis: Count isotopes per element
print("\n\nNumber of stable isotopes per element:")
print("-" * 50)

isotope_counts = df.groupby('Element').size().sort_values(ascending=False)
print(f"\nTop 10 elements with most stable isotopes:")
print(isotope_counts.head(10))

# %%
# Example: Create a lookup dictionary
print("\n\nCreate lookup dictionary:")
print("-" * 50)

isotope_dict = {
    f"{elem}-{A}": abundance 
    for A, Z, elem, abundance in data
}

# Look up specific isotopes
examples = ['H-1', 'He-4', 'C-12', 'O-16', 'Fe-56']
print("\nAbundances of common isotopes:")
for iso in examples:
    if iso in isotope_dict:
        print(f"{iso:<8}: {isotope_dict[iso]:.3e}")
    else:
        print(f"{iso:<8}: Not found")

# %%
print("\n✓ All examples completed successfully!")
print("\nYou can now use these methods in your own code,")
print("and the data file will always be accessible regardless")
print("of where you run your script from.")
