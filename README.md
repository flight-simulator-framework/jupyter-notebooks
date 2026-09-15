# Jupyter Notebooks and Tests

This repository contains tests and notebooks created for further developments and understanding.
## Installation and startup

Use Python 3.11 or newer and Poetry 2 or newer.

```bash
git clone https://gitlab.cern.ch/flight-simulator/jupyter-notebooks.git
cd jupyter-notebooks
poetry install
poetry run jupyter lab
```

Poetry downloads and installs the required Python dependencies automatically.

For the GUI and emittance examples, use `poetry install --extras "gui-experiments emittance-analysis"`.

Open a notebook from `Jupyter Notebooks` and select the Python kernel from this environment. Measurement-analysis notebooks require the corresponding recorded datasets; set their input paths to your own data.
