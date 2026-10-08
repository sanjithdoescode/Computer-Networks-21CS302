#!/usr/bin/env python3
"""
scripts/build_figures.py
Master figure builder and validator for Computer Networks exam preparation repository.
"""

import sys
import os
import argparse
import subprocess

def run_generator(script_path):
    print(f"\n==========================================")
    print(f"Running Generator: {script_path}")
    print(f"==========================================")
    if not os.path.exists(script_path):
        print(f"Generator {script_path} not found yet!")
        return False
    res = subprocess.run([sys.executable, script_path], check=False)
    return res.returncode == 0

def verify_unit_figures(unit_dir):
    fig_dir = os.path.join(unit_dir, "figures")
    if not os.path.exists(fig_dir):
        print(f"No figures directory for {unit_dir}")
        return 0, 0
    svgs = [f for f in os.listdir(fig_dir) if f.endswith(".svg")]
    valid = 0
    for s in svgs:
        p = os.path.join(fig_dir, s)
        if os.path.getsize(p) > 100:
            valid += 1
        else:
            print(f"Warning: Suspiciously small/empty SVG: {p}")
    print(f"[{unit_dir}] {valid}/{len(svgs)} valid SVG figures.")
    return valid, len(svgs)

def main():
    parser = argparse.ArgumentParser(description="Build and verify publication figures across all units")
    parser.add_argument("--unit", choices=["1", "2", "3", "4", "5", "all"], default="all", help="Target unit to build")
    parser.add_argument("--verify-only", action="store_true", help="Only verify existing figures without building")
    args = parser.parse_args()

    units = ["1", "2", "3", "4", "5"] if args.unit == "all" else [args.unit]
    
    if not args.verify_only:
        for u in units:
            gen_script = f"scripts/figures/generate_unit{u}.py"
            if os.path.exists(gen_script):
                success = run_generator(gen_script)
                if not success:
                    print(f"Failed to generate figures for Unit {u}")
                    sys.exit(1)

    print("\n================ Verification Summary ================")
    total_valid = 0
    total_count = 0
    for u in units:
        v, c = verify_unit_figures(f"UNIT - {u}")
        total_valid += v
        total_count += c
    print(f"\nTotal Valid Figures: {total_valid} / {total_count}")

if __name__ == "__main__":
    main()
