# analog-sims

Transistor-level circuit simulations with open-source tools, to check
circuit ideas from ECEN720 (e.g. phase interpolators) against real device
models.

- Simulator: ngspice (batch mode), `brew install ngspice`
- PDK: SkyWater SKY130 (`sky130_fd_pr` primitives), via volare

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install volare numpy matplotlib
.venv/bin/volare enable --pdk sky130 -l sky130_fd_pr c6d73a35f524070e85faff4a6a9eef49553ebc2b
ln -s ~/.volare/sky130A pdk
```

`.spiceinit` is the PDK's ngspice init (HSPICE compatibility, KLU). Netlists
include the models with `.lib "pdk/libs.tech/ngspice/sky130.lib.spice" tt`,
so run ngspice from the repo root. `tools/spice.py` does that and reads the
`wrdata` output.

## Sims

| Directory | What |
|---|---|
| `sims/inverter` | Hello world: inverter VTC and transient; FO4 delay (59.7 ps, tt 1.8 V 27 C) |

Run a sim's plot script from the repo root, e.g.
`.venv/bin/python sims/inverter/plot.py`.

Devices wider than the model bins are split into fingers (`nf`), keeping
the per-finger width inside the binned range.
