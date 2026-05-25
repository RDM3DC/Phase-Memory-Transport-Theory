"""
Toy coupled Adaptive Curvature Flow Network / PMT solver.

This is a 1D finite-difference version of the four-field loop:

    dG/dt     = alpha*|I| - mu*G + lambda*|grad(kappa)| + sigma*M
    dkappa/dt = eta*div(G grad(kappa)) - beta*kappa
    dtheta/dt = omega + gamma*div(G_eff grad(theta))
    dM/dt     = xi*(dtheta/dt)^2 - rho*M

Run:
    python examples/acfn_pmt_coupled_solver.py
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

try:
    from .minimal_pmt_sim import divergence_flux_1d, stable_explicit_dt
except ImportError:
    from minimal_pmt_sim import divergence_flux_1d, stable_explicit_dt


@dataclass(frozen=True)
class CoupledPMTParameters:
    n: int = 160
    steps: int = 1000
    dt: float = 0.0005
    length: float = 1.0
    omega: float = 0.6
    gamma: float = 0.01
    xi: float = 0.4
    rho: float = 0.08
    memory_feedback: float = 0.35
    alpha: float = 0.22
    mu: float = 0.25
    curvature_gain: float = 0.08
    eta: float = 0.006
    beta: float = 0.3
    intensity_center: float = 0.34
    intensity_width: float = 0.035


def centered_gradient_1d(field: np.ndarray, dx: float) -> np.ndarray:
    """Centered periodic gradient."""
    return (np.roll(field, -1) - np.roll(field, 1)) / (2.0 * dx)


def initial_fields(params: CoupledPMTParameters) -> dict[str, np.ndarray]:
    """Create smooth initial fields for a coupled ACFN/PMT toy run."""
    coordinate = np.linspace(0.0, params.length, params.n, endpoint=False)
    phase = 0.2 * np.sin(2.0 * np.pi * coordinate)
    phase += 0.45 * np.exp(-((coordinate - 0.32) ** 2) / 0.003)
    memory = np.zeros_like(coordinate)
    conductance = np.full_like(coordinate, 0.75)
    curvature = 0.18 * np.sin(4.0 * np.pi * coordinate)
    intensity = np.exp(-((coordinate - params.intensity_center) ** 2) / params.intensity_width)

    return {
        "x": coordinate,
        "theta": phase,
        "memory": memory,
        "conductance": conductance,
        "curvature": curvature,
        "intensity": intensity,
    }


def summarize_coupled_state(fields: dict[str, np.ndarray], length: float) -> dict[str, float | bool]:
    """Return stability and persistence diagnostics for the coupled run."""
    theta = fields["theta"]
    memory = fields["memory"]
    conductance = fields["conductance"]
    curvature = fields["curvature"]
    dx = length / len(theta)
    epsilon = float(np.finfo(float).eps)
    memory_mean = float(memory.mean())
    conductance_mean = float(conductance.mean())

    finite = bool(
        np.all(np.isfinite(theta))
        and np.all(np.isfinite(memory))
        and np.all(np.isfinite(conductance))
        and np.all(np.isfinite(curvature))
    )

    return {
        "finite": finite,
        "memory_min": float(memory.min()),
        "memory_max": float(memory.max()),
        "memory_mean": memory_mean,
        "memory_charge": float(np.sum(memory) * dx),
        "memory_contrast": float(memory.max() / max(memory_mean, epsilon)),
        "conductance_min": float(conductance.min()),
        "conductance_max": float(conductance.max()),
        "conductance_mean": conductance_mean,
        "conductance_contrast": float(conductance.max() / max(conductance_mean, epsilon)),
        "phase_roughness": float(np.mean(centered_gradient_1d(theta, dx) ** 2)),
        "curvature_energy": float(np.mean(curvature**2)),
    }


def run_coupled_solver(
    params: CoupledPMTParameters | None = None,
) -> tuple[dict[str, np.ndarray], dict[str, float | bool]]:
    """Run the coupled ACFN/PMT finite-difference toy solver."""
    params = params or CoupledPMTParameters()
    fields = initial_fields(params)
    dx = params.length / params.n

    theta = fields["theta"]
    memory = fields["memory"]
    conductance = fields["conductance"]
    curvature = fields["curvature"]
    intensity = fields["intensity"]

    for _ in range(params.steps):
        remaining_dt = params.dt

        while remaining_dt > 0.0:
            g_eff = conductance * (1.0 + params.memory_feedback * memory)
            phase_dt = stable_explicit_dt(dx, params.gamma, g_eff)
            curvature_dt = stable_explicit_dt(dx, params.eta, conductance)
            sub_dt = min(remaining_dt, phase_dt, curvature_dt)

            theta_t = params.omega + params.gamma * divergence_flux_1d(g_eff, theta, dx)
            memory_t = params.xi * theta_t**2 - params.rho * memory
            curvature_t = params.eta * divergence_flux_1d(conductance, curvature, dx) - params.beta * curvature
            conductance_t = (
                params.alpha * np.abs(intensity)
                - params.mu * conductance
                + params.curvature_gain * np.abs(centered_gradient_1d(curvature, dx))
                + params.memory_feedback * memory
            )

            theta = theta + sub_dt * theta_t
            memory = np.maximum(0.0, memory + sub_dt * memory_t)
            curvature = curvature + sub_dt * curvature_t
            conductance = np.maximum(0.0, conductance + sub_dt * conductance_t)
            remaining_dt -= sub_dt

    fields["theta"] = theta
    fields["memory"] = memory
    fields["conductance"] = conductance
    fields["curvature"] = curvature
    fields["g_eff"] = conductance * (1.0 + params.memory_feedback * memory)

    return fields, summarize_coupled_state(fields, params.length)


if __name__ == "__main__":
    final_fields, metrics = run_coupled_solver()

    print("Coupled ACFN/PMT solver complete")
    for metric_name, metric_value in metrics.items():
        if isinstance(metric_value, bool):
            print(f"{metric_name}: {metric_value}")
        else:
            print(f"{metric_name}: {metric_value:.8f}")