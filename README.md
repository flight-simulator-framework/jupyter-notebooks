# Jupyter Notebooks and Tests

This repository contains tests and notebooks created for further developments and understanding.

## Start with a tutorial

The [application tutorials](tutorials/README.md) introduce every application and its main variants with short examples, equations and plots. They run without opening a GUI or connecting to a machine. Start with [Machine Interface](tutorials/00_MachineInterface.ipynb), or go directly to [Orbit Bump](tutorials/03_OrbitBump.ipynb) or [Emittance Measurement](tutorials/05_EmittanceMeasurement.ipynb).

The [tutorial guide](tutorials/README.md) lists the short interface examples: dispersion, screen images, BPM orbit readings and saving measurements. Existing research and accelerator notebooks are in [`examples`](examples).

## Development

Development, issues and pull requests are hosted on [GitHub](https://github.com/flight-simulator-framework/jupyter-notebooks). The [CERN GitLab repository](https://gitlab.cern.ch/flight-simulator/jupyter-notebooks) receives updates from GitHub through a pull mirror.

## Installation and startup

To run all tutorials, use Python 3.11 or newer. From a directory where you want to keep the repositories, clone any that are missing. The commands below clone from GitHub; to clone from CERN GitLab instead, replace `https://github.com/flight-simulator-framework/` with `https://gitlab.cern.ch/flight-simulator/`:

```bash
git clone https://github.com/flight-simulator-framework/machine-interfaces.git
git clone https://github.com/flight-simulator-framework/response-matrix.git
git clone https://github.com/flight-simulator-framework/jupyter-notebooks.git
git clone https://github.com/flight-simulator-framework/emittance-measurement.git
```

Then, from the shared parent directory:

```bash
python3 -m venv .venv-tutorials
source .venv-tutorials/bin/activate
python -m pip install -e machine-interfaces -e response-matrix -e emittance-measurement -e jupyter-notebooks
python -m pip install rf-track cpymad
python -m pip install --no-deps -e machine-interfaces/backends/clear
python -m ipykernel install --sys-prefix --name flight-tutorials --display-name "Flight tutorials"
cd jupyter-notebooks/tutorials
jupyter lab
```

Open a notebook, select **Kernel → Change Kernel → Flight tutorials**, then use **Run → Run All Cells**. Run the cells from the top. The tutorials use simulation and do not require a machine connection.

Dependencies are declared in `pyproject.toml`; no separate `requirements.txt` is needed. The CLEAR simulation is installed separately because its real-machine control packages are available only from the CERN Acc-Py index. Editable installs pick up source changes without reinstalling.

For research notebooks using ATF2, ESRF or FACET-II, install the corresponding backend with `python -m pip install -e machine-interfaces/backends/atf2` (replace `atf2` as needed), from the shared parent directory. For ATF2, also build the magnet current–strength conversion library with `make -C machine-interfaces/backends/atf2/machine_interfaces_atf2/libmagnet libmagnet.so CFLAG=-fPIC`, which requires `gcc`, `gfortran` and `make`. For GUI examples, also clone and install the relevant application repositories.
