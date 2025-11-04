#!/usr/bin/env bash
# FileNameConvention.sh - generate and parse compact parameter filenames
#
# Implements the same conventions as FileNameConvention.py:
# - Labels: mass->M, metallicity->Z, angular_velocity->O, initial_helium_abundance->Y
# - Exponent offset +10 applied to the value before formatting
# - Format: <Label><TwoDigitExponent>F<MantissaWithDAsDecimal>
#   e.g. M09F8d50 for mass=0.85

set -eo pipefail

progname=$(basename "$0")

usage() {
  cat <<EOF
Usage: $progname <command> [options]

Commands:
  gen --mass <val> --metallicity <val> --angular-velocity <val> --helium <val>
      Generate a filename fragment for provided parameters. Use any subset of options.

  parse <name>
      Parse a generated name and print key=value pairs.

Examples:
  $progname gen --mass 0.85 --helium 0.28
  $progname parse M09F8d50_Y10F2d80

EOF
}

is_upper_single_char() {
  local s=$1
  [[ ${#s} -eq 1 && $s =~ [A-Z] ]]
}

map_label() {
  local label=$1
  case "$label" in
    mass|m|M) echo M ;;
    metallicity|z|Z) echo Z ;;
    "angular velocity"|angular-velocity|angular_velocity|o|O) echo O ;;
    "initial helium abundance"|helium|y|Y) echo Y ;;
    *)
      if is_upper_single_char "$label"; then
        echo "$label"
      else
        echo "" >&2
        return 1
      fi
      ;;
  esac
}

format_fragment() {
  # args: label value
  local label=$1
  local val=$2
  if [[ -z "$label" ]]; then
    echo "Missing label" >&2
    return 1
  fi
  if [[ -z "${val:-}" ]]; then
    echo ""
    return 0
  fi

  # apply exponent offset +10
  # compute scaled value = val * 10**10
  # Use awk for floating point arithmetic and formatting
  local scaled
  scaled=$(awk -v v="$val" 'BEGIN{printf "%0.12e", v * (10**10)}')
  # scaled like 8.500000000000e+00
  # split into mantissa and exponent
  local mantissa exp
  mantissa=$(echo "$scaled" | awk -F'e' '{print $1}')
  exp=$(echo "$scaled" | awk -F'e' '{print $2+0}')
  # mantissa format: keep two decimal places when converting to sd (like python {:.2e})
  # We'll reformat mantissa to have 2 decimal places in scientific notation's mantissa
  local sstr
  sstr=$(awk -v v="$val" 'BEGIN{v=v*(10**10); printf "%0.2e", v}')
  mantissa=$(echo "$sstr" | awk -F'e' '{print $1}')
  exp=$(echo "$sstr" | awk -F'e' '{print $2+0}')

  # Replace decimal point with 'd' in mantissa
  local sd
  sd=${mantissa/./d}

  # Format exponent as two digits (positive only expected)
  if (( exp < 0 )); then
    echo "Negative exponent after offset not expected" >&2
    return 1
  fi
  exp_str=$(printf "%02d" "$exp")

  echo "${label}${exp_str}F${sd}"
}

cmd_generate() {
  local mass=; local metallicity=; local angvel=; local helium=; other_list=()
  # parse options
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --mass) mass=$2; shift 2 ;;
      --metallicity) metallicity=$2; shift 2 ;;
      --angular-velocity|--angular_velocity|--angvel) angvel=$2; shift 2 ;;
      --helium|--initial-helium|--initial_helium|--initial-helium-abundance) helium=$2; shift 2 ;;
      --other)
        # format: --other KEY=VALUE
        other_list+=("$2")
        shift 2 ;;
      -h|--help) usage; exit 0 ;;
      *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
    esac
  done

  # Safely compute number of --other entries without triggering set -u on unset arrays
  other_list_len=0
  if [ "${other_list+set}" = "set" ]; then
    for _kv in "${other_list[@]}"; do
      other_list_len=$((other_list_len+1))
    done
  fi
  if [[ -z "$mass" && -z "$metallicity" && -z "$angvel" && -z "$helium" && $other_list_len -eq 0 ]]; then
    echo "At least one quantity must be provided." >&2
    exit 1
  fi

  local parts=()
  if [[ -n "$mass" ]]; then
    lab=$(map_label mass) || exit 1
    parts+=("$(format_fragment "$lab" "$mass")")
  fi
  if [[ -n "$metallicity" ]]; then
    lab=$(map_label metallicity) || exit 1
    parts+=("$(format_fragment "$lab" "$metallicity")")
  fi
  if [[ -n "$angvel" ]]; then
    lab=$(map_label "angular velocity") || exit 1
    parts+=("$(format_fragment "$lab" "$angvel")")
  fi
  if [[ -n "$helium" ]]; then
    lab=$(map_label "initial helium abundance") || exit 1
    parts+=("$(format_fragment "$lab" "$helium")")
  fi
  for kv in "${other_list[@]}"; do
    IFS='=' read -r k v <<< "$kv"
    lab=$(map_label "$k") || lab="$k"
    parts+=("$(format_fragment "$lab" "$v")")
  done

  # filter empty
  local out=()
  for p in "${parts[@]}"; do
    if [[ -n "$p" ]]; then out+=("$p"); fi
  done

  IFS=_; echo "${out[*]}"; IFS=' '
}

parse_component() {
  local comp=$1
  # Expect at least 4 chars: LDDF...
  if [[ ${#comp} -lt 4 ]]; then
    echo "Invalid component: $comp" >&2; return 1
  fi
  local label=${comp:0:1}
  local exp_str=${comp:1:2}
  local fchar=${comp:3:1}
  if [[ "$fchar" != "F" ]]; then
    echo "Invalid component format (missing F): $comp" >&2; return 1
  fi
  local mantissa_str=${comp:4}
  # replace d with .
  local mantissa=${mantissa_str//d/.}
  # compute exponent back: exponent = int(exp_str) - 10
  local exponent=$((10#${exp_str} - 10))
  # compute value = mantissa * 10**exponent
  # use awk for float math
  local value
  value=$(awk -v m="$mantissa" -v e="$exponent" 'BEGIN{printf "%g", m * (10**e)}')

  case "$label" in
    M) echo "mass=$value" ;;
    Z) echo "metallicity=$value" ;;
    O) echo "angular_velocity=$value" ;;
    Y) echo "initial_helium_abundance=$value" ;;
    *)
      if is_upper_single_char "$label"; then
        echo "${label}=$value"
      else
        echo "Unrecognized label: $label" >&2; return 1
      fi
      ;;
  esac
}

cmd_parse() {
  if [[ $# -ne 1 ]]; then
    usage; exit 1
  fi
  local name=$1
  IFS='_' read -ra comps <<< "$name"
  for c in "${comps[@]}"; do
    parse_component "$c"
  done
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

cmd=$1; shift
case "$cmd" in
  gen) cmd_generate "$@" ;;
  parse) cmd_parse "$@" ;;
  -h|--help) usage ;;
  *) echo "Unknown command: $cmd" >&2; usage; exit 1 ;;
esac
