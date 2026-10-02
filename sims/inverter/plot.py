"""Inverter hello world and FO4 delay, SKY130 tt 1.8 V.

Run from the repo root: .venv/bin/python sims/inverter/plot.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import spice  # noqa: E402

HERE = Path("sims/inverter")


def main() -> None:
    spice.run(HERE / "vtc.cir")
    out = spice.run(HERE / "fo4.cir")
    meas = {line.split()[0]: float(line.split()[2]) for line in out.splitlines()
            if line.split() and line.split()[0] in ("tphl", "tplh", "tf3", "tr3")}
    fo4 = (meas["tphl"] + meas["tplh"]) / 2

    vtc, tran, chain = (spice.read(HERE / f) for f in ("vtc.dat", "tran.dat", "fo4.dat"))
    fig, (ax_vtc, ax_tran, ax_fo4) = plt.subplots(1, 3, figsize=(13, 3.6))

    ax_vtc.plot(vtc["v(in)"], vtc["v(out)"])
    ax_vtc.plot([0, 1.8], [0, 1.8], "k:", lw=0.8)
    ax_vtc.set_xlabel("Vin (V)")
    ax_vtc.set_ylabel("Vout (V)")
    ax_vtc.set_title("DC transfer, Wn/Wp = 1/2 um")

    t = tran["time"] * 1e12
    ax_tran.plot(t, tran["v(in)"], label="in")
    ax_tran.plot(t, tran["v(out)"], label="out (5 fF)")
    ax_tran.set_xlabel("time (ps)")
    ax_tran.set_ylabel("V")
    ax_tran.set_title("Transient")
    ax_tran.legend()

    t = chain["time"] * 1e12
    for node in ("n2", "n3", "n4"):
        ax_fo4.plot(t, chain[f"v({node})"], label=node)
    ax_fo4.axhline(0.9, color="k", lw=0.5, ls=":")
    ax_fo4.set_xlim(2250, 2500)
    ax_fo4.set_xlabel("time (ps)")
    ax_fo4.set_title(f"FO4 chain: stage n2 -> n3, FO4 = {fo4 * 1e12:.1f} ps")
    ax_fo4.legend()

    for ax in (ax_vtc, ax_tran, ax_fo4):
        ax.grid(True)
    fig.tight_layout()
    fig.savefig(HERE / "inverter.png", dpi=110)
    print({k: f"{v * 1e12:.1f} ps" for k, v in meas.items()}, f"FO4 {fo4 * 1e12:.1f} ps")


if __name__ == "__main__":
    main()
