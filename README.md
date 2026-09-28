# Jupyter Notebooks and Tests

This repository contains tests and notebooks created for further developments and understanding.
## Installation and startup


```bash
git clone https://gitlab.cern.ch/flight-simulator/machine-interfaces.git
git clone https://gitlab.cern.ch/flight-simulator/response-matrix.git
git clone https://gitlab.cern.ch/flight-simulator/jupyter-notebooks.git
cd jupyter-notebooks
poetry update rf-track --lock
poetry install --extras atf2
poetry run jupyter lab
```

Keep these repositories in the same parent directory; Poetry uses their local editable packages. The selected extra installs only that machine adapter and its dependencies. Available machine extras: `clear`, `atf2`, `facet2`, `esrf`; combine them with `--extras "clear atf2"` when needed.

For the GUI and emittance examples, use `poetry install --extras "atf2 gui-experiments emittance-analysis"`.

The optional `gui-experiments` and `emittance-analysis` extras also require the corresponding application repositories beside this repository: `system-identification`, `beam-based-alignment`, `atf2-knobs` and `emittance-measurement`. Poetry resolves optional dependencies when updating the lock file, so keep those sibling checkouts available for `poetry lock` as well.
