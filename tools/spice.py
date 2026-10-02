"""Run an ngspice netlist in batch mode from the repo root (so .spiceinit and
the pdk/ link resolve) and read the columns it wrote with wrdata.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def run(netlist: str | Path) -> str:
    """ngspice -b on `netlist`; returns its stdout, raises on failure."""
    result = subprocess.run(
        ["ngspice", "-b", str(netlist)], cwd=ROOT, capture_output=True, text=True
    )
    if result.returncode != 0 or "Error" in result.stdout + result.stderr:
        raise RuntimeError(f"ngspice failed on {netlist}:\n{result.stdout}\n{result.stderr}")
    return result.stdout


def read(path: str | Path) -> dict[str, np.ndarray]:
    """A wrdata file written with wr_singlescale and wr_vecnames: one column
    per vector, the first being the sweep or time axis.
    """
    path = ROOT / path
    names = path.read_text().splitlines()[0].split()
    data = np.loadtxt(path, skiprows=1, ndmin=2)
    return {name: data[:, i] for i, name in enumerate(names)}
