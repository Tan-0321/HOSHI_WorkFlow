import logging
import re

import numpy as np
import pandas as pd

# regular expression to parse isotope labels.
# all isotope labels used in following are expected to be in the form "ElementSymbolMassNumber",
# e.g., "H1", "He4", "C12", "Fe56".
_iso_re = re.compile(r"^\s*([A-Za-z]{1,2})\s*(\d+)\s*$")
clean = lambda s: re.sub(r"\s+", "", str(s))  # delete（space/tab/newline）


class Nomoto2013Yields:
    """Class to handle the yields data from Nomoto 2013.
    Args:
        file_path (str): Path to the yields data file(tsv).
        mass (int | float | str): Mass of the stellar model,
        e.g., 15 or "15.0" for 15 Msun.

    Attributes:
        E_explosion (float): Explosion energy in 1e51 erg.
        M_remnant (float): Remnant mass in Msun.
        mass (float): Mass of the stellar model in Msun.
        yields (dict): Dictionary of isotope yields with keys as isotope names,
            (e.g., 'H1', 'He4'), and values as yields in Msun.
    """

    E_explosion: float = 0.0  # in 1e51 erg
    M_remnant: float = 0.0  # in Msun
    mass: float = 0.0  # in Msun
    yields: dict[str, float] = None

    def __init__(self, file_path: str, mass: int | float | str):
        # isinstance accepts a tuple for multiple types
        if isinstance(mass, (float, int)):
            mass_str = f"{mass:.1f}"
        elif isinstance(mass, str):
            mass_str = mass
        else:
            raise ValueError("mass must be int, float or str")

        df = pd.read_csv(
            file_path,
            sep="\t",  # tab-separated, for tsv files
            skiprows=2,  # skip first two rows, blank row and "Z=..."
            header=0,  # use the mass row as column headers
        )

        # mass values may be repeated, with different explosion energies
        # in nomoto2013, e.g., 140.0 appears twice
        matching_cols = [col for col in df.columns if col.startswith(mass_str)]
        if len(matching_cols) > 1:
            logging.warning(
                "multiple columns match '%s': %s. Using the first one.",
                mass_str,
                matching_cols,
            )
        elif len(matching_cols) == 0:
            raise ValueError(
                f"Error: no columns match '{mass_str}' in dataframe columns {df.columns.tolist()}"
            )

        yields_data = df[matching_cols[0]].values
        iso_names = df.iloc[2:, 0].values  # skip E_explosion, M_remnant rows

        self.E_explosion = yields_data[0]  # in 1e51 erg
        self.M_remnant = yields_data[1]  # in Msun
        self.mass = float(mass)

        yields_data = yields_data[2:]  # skip E_explosion, M_remnant entries
        self.yields = {
            clean(iso_names[i]): yields_data[i] for i in range(len(yields_data))
        }
        return None


class InitialComposition:
    """Class to handle the initial composition of isotopes in a star.
    Args:
        data_source (str | dict): Path to the composition data file, or a dictionary
            of isotope mass fractions.
        normalization_error (float): Tolerance for normalization check. Default is 1e-2.

    Attributes:
        composition (dict): Dictionary of isotope mass fractions with keys as isotope names,
            (e.g., 'H1', 'He4'), and values as mass fractions.
        num_isotope (int): Number of isotopes in the composition.
        X (float): Hydrogen mass fraction.
        Y (float): Helium mass fraction.
        Z (float): Metal mass fraction.

    Note:
        To create an instance from a file, the file should have the format
        as same as "ZSOLAR.DAT.KOBAYASHI". The file format is:
            H     1  0.735224E+00
            H     2  0.294096E-04
            He    3  0.311643E-04
            ......
        To create an instance from a dictionary, the dictionary should have
        keys as isotope names (e.g., 'H1', 'He4') and values as mass fractions.

    Functions:
        _from_file(path): Load composition from a file.
        check_normalization(): Check and normalize the composition to sum to 1.
        _compute_xyz(): Compute X, Y, Z from the composition.
        save_to_file(path, ref_abd_path): Save the composition to a file in the
            format of ref_abd_path (usually "ZSOLAR.DAT.KOBAYASHI").

    """

    num_isotope: int
    X: float
    Y: float
    Z: float
    composition: dict

    def __init__(
        self,
        data_source: str | dict[str, float],
        normalization_error: float = 1e-2,
    ):
        if isinstance(data_source, str):
            self._from_file(data_source)
        elif isinstance(data_source, dict):
            self.composition = data_source.copy()
        else:
            raise ValueError("data_source must be a file path or a dictionary.")
        # compute X, Y, Z on initialization
        self.X = None
        self.Y = None
        self.Z = None
        self.total = None
        self.norm_error = normalization_error
        if self.composition is not None:
            self.num_isotope = len(self.composition)
            self.check_normalization()
            self._compute_xyz()
        else:
            logging.warning("composition is None; X, Y, Z not computed.")

    def _from_file(self, path: str):
        # reading from a file like "ZSOLAR.DAT.KOBAYASHI"
        data = np.loadtxt(path, dtype=str)
        name = np.array([s.ljust(2).strip() for s in data[:, 0]])  # isotope name
        mass_number = data[:, 1].astype(int)  # mass number
        mass_fraction = data[:, 2].astype(float)  # mass fraction
        comp = {n + str(mass_number[i]): mass_fraction[i] for i, n in enumerate(name)}
        self.composition = comp
        self.num_isotope = len(comp)
        return None

    def check_normalization(self):
        total_raw = sum(self.composition.values())
        if abs(total_raw - 1.0) > self.norm_error:
            logging.warning(
                "raw isotope sum = %.6e (expected ~1). Normalizing.", total_raw
            )
            for iso_name, val in self.composition.items():
                try:
                    v = float(val) / total_raw
                    self.composition[iso_name] = v
                except Exception:
                    continue
        return None

    def _compute_xyz(self):
        X = 0.0
        Y = 0.0
        total_raw = 0.0
        for iso_label, val in self.composition.items():
            try:
                v = float(val)
            except Exception:
                continue
            total_raw += v
            m = _iso_re.match(str(iso_label))
            # isotope label may have unexpected format, (HE4, he4, He4)
            # so we use regex to parse it
            if m:
                elem = m.group(1).upper()
                if elem == "H":
                    X += v
                elif elem == "HE":
                    Y += v

        Z = 1.0 - X - Y

        self.X = float(X)
        self.Y = float(Y)
        self.Z = float(Z)
        return None

    def save_to_file(self, path: str, ref_abd_path: str):
        """Save the composition to a file in the format of ref_abd_path.
        ref_file usually is "ZSOLAR.DAT.KOBAYASHI".
        Only save the intersection of sets of isotopes in self.composition and ref_abd.composition.
        The isotopes not in self.composition will be set to 0.0 in the output file.
        """
        ref_abd = InitialComposition(ref_abd_path)
        # build output composition using the reference isotopes;
        # fill with values from self.composition (or 0.0 if missing)
        comp = {
            iso_name: float(self.composition.get(iso_name, 0.0))
            for iso_name in ref_abd.composition.keys()
        }
        with open(path, "w") as f:
            for iso_name, val in comp.items():
                m = _iso_re.match(str(iso_name))
                if m:
                    elem = m.group(1).ljust(2)
                    mass_num = int(m.group(2))
                    f.write(f"{elem} {mass_num:4d} {val:.6e}\n")
        return None
