# Jupyter Notebooks and Tests

This repository contains tests and notebooks created for further developments and understanding.
## Installation and startup

For a local installation, use Python 3.11 or newer and keep the repositories in one directory:

```bash
git clone https://gitlab.cern.ch/flight-simulator/machine-interfaces.git
git clone https://gitlab.cern.ch/flight-simulator/response-matrix.git
git clone https://gitlab.cern.ch/flight-simulator/jupyter-notebooks.git
python3 -m venv venv
source venv/bin/activate
pip install -e machine-interfaces -e machine-interfaces/backends/atf2 -e response-matrix -e jupyter-notebooks
cd jupyter-notebooks
jupyter lab
```

Replace `atf2` with `esrf` or `facet2` for another machine. The CLEAR control-system packages are available only from the CERN Acc-Py index; elsewhere, install only the CLEAR simulation:

```bash
pip install rf-track cpymad
pip install --no-deps -e machine-interfaces/backends/clear
```

Editable installs pick up `git pull` changes without reinstalling.

For the GUI and emittance examples, also clone `system-identification`, `beam-based-alignment`, `atf2-knobs` and `emittance-measurement` into the same directory and add them to `pip install -e`.
