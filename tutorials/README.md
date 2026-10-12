# Flight Simulator tutorials

These tutorials serve as a base to understand our tools within Flight Simulator framework and show how to write easily your own applications.

## Setup

From their shared parent directory:

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

## Choose a tutorial

| Notebook | Application or component | What you will see |
|---|---|---|
| [00 · Machine Interface](00_MachineInterface.ipynb) | Shared machine-interface layer | Overview of interface methods |
| [00a · Machine Interface - Measure Dispersion](00a_DispersionMeasurement.ipynb) | Shared machine-interface layer | Shows how to write example scripts, e.g. to measure dispersion |
| [00b · Machine Interface - Get Screen Image](00b_GetScreenImage.ipynb) | Shared machine-interface layer | Shows how to write example scripts, e.g. to get the screen image|
| [00c · Read Orbit](00c_ReadOrbit.ipynb) | Shared machine-interface layer, `State.py` | Read BPM shots, average them and plot the orbit with uncertainty |
| [01 · System Identification](01_SystemIdentification.ipynb) | `SysID_GUI.py` | Positive/negative excitation, uncertainties and real `State` snapshots |
| [02 · Response Matrix](02_ResponseMatrix.ipynb) | `ComputeResponseMatrix_GUI.py`, `ComputeResponseMatrix_rnd_GUI.py` | Application reconstruction, coupling, singular values, export and random-excitation regression |
| [03 · Orbit Bump](03_OrbitBump.ipynb) | `BumpsApplication_GUI.py` | Target, prediction, limited settings and measured closure |
| [04 · Beam-Based Alignment](04_BeamBasedAlignment.ipynb) | `BBA_GUI.py` | Weighted orbit/DFS/WFS objective and iterative correction |
| [05 · Emittance Measurement](05_EmittanceMeasurement.ipynb) | `Emittance_Measurement_GUI.py` | Actual linear-optics fit, scan curve, emittance, Twiss parameters and phase-space ellipse |
