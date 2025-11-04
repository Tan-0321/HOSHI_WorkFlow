# initial_composition — FileNameConvention (Bash)

This repository contains a small utility script that mirrors the behavior of `FileNameConvention.py` but implemented in portable Bash.

## Script

`FileNameConvention.sh` — generate and parse compact parameter filename fragments.

Conventions implemented:
- Labels: mass -> `M`, metallicity -> `Z`, angular_velocity -> `O`, initial helium abundance (helium) -> `Y`.
- Exponent offset of `+10` applied before formatting.
- Fragment format: `<Label><TwoDigitExponent>F<MantissaWithDAsDecimal>` (decimal point replaced by `d`).

Examples:

Generate a name fragment from parameters:

```bash
./FileNameConvention.sh generate --mass 0.85 --helium 0.28
# Example output: M09F8d50_Y09F2d80
```

Parse a generated fragment back to numeric values:

```bash
./FileNameConvention.sh parse M09F8d50_Y09F2d80
# Output:
# mass=0.85
# initial_helium_abundance=0.28
```

More examples:

- Small metallicity (tests exponent formatting):

```bash
./FileNameConvention.sh generate --metallicity 1e-5
# Example output: Z05F1d00
```

- Angular velocity:

```bash
./FileNameConvention.sh generate --angular-velocity 0.5
# Example output: O09F5d00
```

- Using `--other KEY=VALUE` for an extra single-letter label (e.g. label 'A'):

```bash
./FileNameConvention.sh generate --other A=3.2
# Example output: A10F3d20
```

- Combined generate and parse (round-trip):

```bash
# generate
NAME=$(./FileNameConvention.sh generate --mass 1.25 --metallicity 0.002 --helium 0.27)
echo "$NAME"
# parse
./FileNameConvention.sh parse "$NAME"
```
