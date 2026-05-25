"""
Minimal Phase-Memory Transport Theory simulation.

This is a toy 1D finite-difference model for:

    ∂θ/∂t = ω + γ ∇·(G_eff ∇θ)
    ∂M/∂t = ξ(∂θ/∂t)^2 - ρM
    G_eff = G(1 + σM)

Run:
    python examples/minimal_pmt_sim.py

Outputs:
    final theta, memory, conductance, and channel summaries printed to console.
"""

from __future__ import annotations

from typing import Literal

import numpy as np


MemoryLaw = Literal["phase_rate_squared", "gradient_squared", "mixed"]


def laplacian_1d(u: np.ndarray, dx: float) -> np.ndarray:
    """Periodic 1D Laplacian."""
    return (np.roll(u, -1) - 2.0 * u + np.roll(u, 1)) / (dx * dx)


def divergence_flux_1d(g: np.ndarray, theta: np.ndarray, dx: float) -> np.ndarray:
    """Approximate div(g grad(theta)) with periodic boundaries."""
    grad_theta_forward = (np.roll(theta, -1) - theta) / dx
    flux_forward = g * grad_theta_forward
    return (flux_forward - np.roll(flux_forward, 1)) / dx


def gradient_squared_1d(theta: np.ndarray, dx: float) -> np.ndarray:
    """Centered |grad(theta)|^2 with periodic boundaries."""
    grad_theta = (np.roll(theta, -1) - np.roll(theta, 1)) / (2.0 * dx)
    return grad_theta**2


def memory_source_1d(memory_law: MemoryLaw, theta_t: np.ndarray, theta: np.ndarray, dx: float) -> np.ndarray:
    """Evaluate a PMT memory-write source term."""
    phase_rate_source = theta_t**2

    if memory_law == "phase_rate_squared":
        return phase_rate_source
    if memory_law == "gradient_squared":
        return gradient_squared_1d(theta, dx)
    if memory_law == "mixed":
        return 0.5 * (phase_rate_source + gradient_squared_1d(theta, dx))

    raise ValueError(f"Unknown memory law: {memory_law}")


def stable_explicit_dt(dx: float, gamma: float, g_eff: np.ndarray, safety: float = 0.2) -> float:
    """Return a conservative explicit diffusion time step."""
    max_transport = gamma * float(np.max(g_eff))
    if max_transport <= 0.0:
        return np.inf
    return safety * dx * dx / (2.0 * max_transport)


def run_simulation(
    n: int = 256,
    steps: int = 2000,
    dt: float = 0.0005,
    length: float = 1.0,
    omega: float = 1.0,
    gamma: float = 0.02,
    xi: float = 0.5,
    rho: float = 0.05,
    sigma: float = 0.5,
    memory_law: MemoryLaw = "phase_rate_squared",
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Run a minimal PMT toy simulation."""
    x = np.linspace(0.0, length, n, endpoint=False)
    dx = length / n

    # Initial phase: smooth wave plus a localized phase bump.
    theta = 0.25 * np.sin(2.0 * np.pi * x)
    theta += 0.75 * np.exp(-((x - 0.35) ** 2) / 0.002)

    # Base conductance and memory.
    g_base = np.ones_like(x)
    memory = np.zeros_like(x)

    for _ in range(steps):
        remaining_dt = dt

        while remaining_dt > 0.0:
            g_eff = g_base * (1.0 + sigma * memory)
            sub_dt = min(remaining_dt, stable_explicit_dt(dx, gamma, g_eff))

            # PMT phase transport.
            theta_t = omega + gamma * divergence_flux_1d(g_eff, theta, dx)

            # PMT memory writing.
            memory_t = xi * memory_source_1d(memory_law, theta_t, theta, dx) - rho * memory

            theta = theta + sub_dt * theta_t
            memory = np.maximum(0.0, memory + sub_dt * memory_t)
            remaining_dt -= sub_dt

    g_eff = g_base * (1.0 + sigma * memory)
    return theta, memory, g_eff


def summarize_fields(theta: np.ndarray, memory: np.ndarray, g_eff: np.ndarray) -> dict[str, float | bool]:
    """Return finite-run and channel-contrast diagnostics."""
    finite = bool(
        np.all(np.isfinite(theta))
        and np.all(np.isfinite(memory))
        and np.all(np.isfinite(g_eff))
    )
    memory_mean = float(memory.mean())
    g_eff_mean = float(g_eff.mean())
    epsilon = float(np.finfo(float).eps)

    return {
        "finite": finite,
        "theta_min": float(theta.min()),
        "theta_max": float(theta.max()),
        "theta_mean": float(theta.mean()),
        "memory_min": float(memory.min()),
        "memory_max": float(memory.max()),
        "memory_mean": memory_mean,
        "memory_contrast": float(memory.max() / max(memory_mean, epsilon)),
        "g_eff_min": float(g_eff.min()),
        "g_eff_max": float(g_eff.max()),
        "g_eff_mean": g_eff_mean,
        "conductance_gain_mean": float(g_eff_mean - 1.0),
    }


if __name__ == "__main__":
    theta, memory, g_eff = run_simulation()
    summary = summarize_fields(theta, memory, g_eff)

    print("PMT minimal simulation complete")
    print(
        f"theta:  min={summary['theta_min']: .6f}, "
        f"max={summary['theta_max']: .6f}, mean={summary['theta_mean']: .6f}"
    )
    print(
        f"memory: min={summary['memory_min']: .6f}, "
        f"max={summary['memory_max']: .6f}, mean={summary['memory_mean']: .6f}, "
        f"contrast={summary['memory_contrast']: .6f}"
    )
    print(
        f"G_eff:  min={summary['g_eff_min']: .6f}, "
        f"max={summary['g_eff_max']: .6f}, mean={summary['g_eff_mean']: .6f}"
    )
