from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
from machine_interfaces.Backend.State import State
from response_matrix.Response import Response
from response_matrix.ResponseMatrix_DFS_WFS import ResponseMatrix_DFS_WFS


class Beamline:
    def __init__(self, seed=42, noise_mm=0.002, nsamples=32):
        self.rng = np.random.default_rng(seed)
        self.noise_mm = noise_mm
        self.nsamples = nsamples
        self.s_correctors = np.array([0.0, 2.0, 4.0])
        self.s_bpms = np.array([0.5, 1.5, 3.0, 4.5, 6.0])
        self.hcorrectors = ["HC1", "HC2", "HC3"]
        self.vcorrectors = ["VC1", "VC2", "VC3"]
        self.correctors = self.hcorrectors + self.vcorrectors
        self.bpms = [f"BPM{i + 1}" for i in range(len(self.s_bpms))]
        drift = np.maximum(self.s_bpms[:, None] - self.s_correctors, 0.0)
        self.R = np.block([[drift, 0.04 * drift], [0.03 * drift, drift]])
        self.settings = np.zeros(6)
        self.error = np.array([0.08, -0.12, 0.06, -0.06, 0.09, -0.03])
        self.offset = self.R @ self.error
        self.sequence = ["HC1", "VC1", "BPM1", "BPM2", "HC2", "VC2", "BPM3", "HC3", "VC3", "BPM4", "BPM5"]
        self.screens = ["SCREEN1"]
        screen_drift = np.maximum(7.0 - self.s_correctors, 0.0)
        self.R_screen = np.block([[screen_drift, 0.04 * screen_drift], [0.03 * screen_drift, screen_drift]])
        self.energy = 1.0

    def get_name(self):
        return "Tutorial linear beamline"

    def get_correctors(self, names=None):
        names = self.correctors if names is None else list(names)
        indices = [self.correctors.index(name) for name in names]
        return {"names": names, "bdes": self.settings[indices].copy(), "bact": self.settings[indices].copy()}

    def set_correctors(self, names, values):
        names, values = list(names), np.asarray(values, dtype=float)
        if values.shape != (len(names),) or not np.all(np.isfinite(values)):
            raise ValueError("Provide one finite setting per corrector")
        indices = [self.correctors.index(name) for name in names]
        self.settings[indices] = values

    def get_bpms(self, names=None):
        names = self.bpms if names is None else list(names)
        indices = [self.bpms.index(name) for name in names]
        mean = (self.offset + self.R @ self.settings) / self.energy
        shots = mean + self.rng.normal(0.0, self.noise_mm, (self.nsamples, mean.size))
        n = len(self.bpms)
        return {"names": names, "x": shots[:, indices], "y": shots[:, n + np.array(indices)], "tmit": np.ones((self.nsamples, len(indices)))}

    def get_screens(self, names=None):
        names = self.screens if names is None else list(names)
        centre = self.R_screen @ (self.error + self.settings) / self.energy
        x, y = self.rng.normal(centre, [0.5, 0.3], (20000, 2)).T
        image, hedges, vedges = np.histogram2d(x, y, bins=(120, 80), range=[[-3.0, 3.0], [-2.0, 2.0]])
        n = len(names)
        return {"names": names, "x": np.full(n, x.mean()), "y": np.full(n, y.mean()), "sigx": np.full(n, x.std()),
                "sigy": np.full(n, y.std()), "images": [image] * n, "hedges": [hedges] * n, "vedges": [vedges] * n}

    def change_energy(self):
        self.energy = 0.9
        return self.energy - 1.0

    def reset_energy(self):
        self.energy = 1.0

    def get_state(self):
        return State(correctors=self.get_correctors(), bpms=self.get_bpms(), sequence=self.sequence,
                     hcorrectors_names=self.hcorrectors, vcorrectors_names=self.vcorrectors,
                     timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc))


class Linac:
    def __init__(self, seed=5, ncells=12, drift=2.0, k1l=0.6, wake=0.02, error_mm=0.1, noise_mm=0.0):
        self.rng = np.random.default_rng(seed)
        self.drift, self.wake, self.noise_mm = drift, wake, noise_mm
        self.s = drift * np.arange(1, ncells + 1)
        self.k = k1l * (-1.0) ** np.arange(ncells)
        self.quad_offset, self.bpm_offset, self.cavity_offset = self.rng.normal(0.0, error_mm, (3, ncells))
        self.settings = np.zeros(ncells)
        self.movers = np.zeros(ncells)

    def trajectory(self, settings=None, movers=None, delta=0.0, charge=1.0):
        settings = self.settings if settings is None else settings
        movers = self.movers if movers is None else movers
        x, xp, path = 0.0, 0.0, []
        for k, q, a, kick in zip(self.k, self.quad_offset + movers, self.cavity_offset, settings):
            xp += kick / (1.0 + delta) + self.wake * charge * (x - a)
            x += self.drift * xp
            path.append(x)
            xp -= k * (x - q) / (1.0 + delta)
        return np.array(path)

    def bpms(self, **beam):
        return self.trajectory(**beam) - self.bpm_offset + self.rng.normal(0.0, self.noise_mm, self.s.size)

    def response(self, step=0.05, actuator="settings", **beam):
        initial = getattr(self, actuator)
        columns = []
        for j in range(initial.size):
            plus, minus = initial.copy(), initial.copy()
            plus[j] += step
            minus[j] -= step
            columns.append((self.trajectory(**{actuator: plus}, **beam) - self.trajectory(**{actuator: minus}, **beam)) / (2 * step))
        return np.column_stack(columns)


def orbit_vector(machine):
    orbit = machine.get_state().get_orbit()
    return np.concatenate([orbit["x"], orbit["y"]])


def acquire_pairs(machine, directory, kick=0.15, cycles=1):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    initial = machine.settings.copy()
    try:
        for cycle in range(cycles):
            for j, name in enumerate(machine.correctors):
                for tag, sign in (("p", 1), ("m", -1)):
                    values = initial.copy()
                    values[j] += sign * kick
                    machine.set_correctors(machine.correctors, values)
                    machine.get_state().save(filename=str(directory / f"DATA_{name}_{tag}{cycle:04d}.pkl"))
                machine.set_correctors(machine.correctors, initial)
    finally:
        machine.set_correctors(machine.correctors, initial)
    return directory


def reconstruct_response(machine, directory):
    result = ResponseMatrix_DFS_WFS()._compute_response_matrix_from_directory(
        str(directory), machine.correctors, machine.bpms, triangular=True)
    response = Response()
    (response.Rxx, response.Ryy, response.Rxy, response.Ryx, response.Bx, response.By,
     response.hcorrs, response.vcorrs, response.bpms) = result
    return response


def measured_response(machine, kick=0.15):
    with TemporaryDirectory(prefix="flight-tutorial-") as directory:
        acquire_pairs(machine, directory, kick=kick)
        return reconstruct_response(machine, directory)


def response_block(response):
    return np.block([[response.Rxx, response.Rxy], [response.Ryx, response.Ryy]])


def beam_matrix(emittance=2e-6, beta=4.0, alpha=0.8):
    return emittance * np.array([[beta, -alpha], [-alpha, (1.0 + alpha**2) / beta]])


def transport(k, drift=2.0):
    return np.array([[1.0 - drift * k, drift], [-k, 1.0]])


def scan_sizes(k, covariance, drift=2.0):
    r1, r2 = 1.0 - drift * np.asarray(k), drift
    return np.sqrt(r1**2 * covariance[0, 0] + 2.0 * r1 * r2 * covariance[0, 1] + r2**2 * covariance[1, 1])


def gaussian_signal(points, center, widths, amplitude=0.8):
    points, center, widths = map(np.asarray, (points, center, widths))
    return amplitude * np.exp(-0.5 * np.sum(((points - center) / widths)**2, axis=-1))
