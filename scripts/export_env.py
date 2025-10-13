#!/usr/bin/env python3
"""
export_env.py

Read a .env file and print shell `export KEY='value'` lines. Intended usage:

  # Dry-run (safe): show keys present but mask values
  python3 scripts/export_env.py

  # To load into current shell (zsh/bash):
  eval "$(python3 scripts/export_env.py --apply)"

This avoids sourcing the .env directly in the shell (which fails when values
contain unquoted spaces) and provides safe quoting.
"""
import argparse
import os
import shlex
import sys


def parse_env_file(path):
    pairs = []
    if not os.path.exists(path):
        return pairs

    with open(path, "r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            idx = line.find("=")
            key = line[:idx].strip()
            val = line[idx+1:]
            # Remove optional surrounding quotes
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            pairs.append((key, val))
    return pairs


def shell_export_line(key, val):
    # Use shlex.quote to make safe single-quoted shell value
    return f"export {key}={shlex.quote(val)}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", default=".env", help="Path to the .env file")
    parser.add_argument("--apply", action="store_true", help="Print full export lines (suitable for eval)")
    parser.add_argument("--dry-run", action="store_true", help="Alias for not --apply (shows masked values)")
    args = parser.parse_args()

    pairs = parse_env_file(args.env_file)
    if not pairs:
        print(f"# No variables found in {args.env_file}", file=sys.stderr)
        return

    # Default behaviour: masked dry-run unless --apply is specified
    apply_mode = args.apply

    for key, val in pairs:
        if not apply_mode:
            # Print a masked indicator for safety
            print(f"# {key}=***")
        else:
            print(shell_export_line(key, val))


if __name__ == "__main__":
    main()
