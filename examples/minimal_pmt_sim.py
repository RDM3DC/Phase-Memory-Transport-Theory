"""
Minimal Phase-Memory Transport Theory simulation.

This is a toy 1D finite-difference model for:

    ∂θ/∂t = ω - γ ∇·(G_eff ∇θ)
    ∂M/∂t = ξ(∂θ/∂t)^2 - ρM
    G_eff = G(1 + σM)

Run:
    python examples/minimal_pmt_sim.py

Outputs:
    final theta and memory summaries printed to console.
"""

from __future__ import annotations

import numpy as np


def laplacian_1d(u: np.ndarray, dx: float) -> np.ndarray:
    """Periodic 1D Laplacian."""
    return (np.roll(u, -1) - 2.0 * u + np.roll(u, 1)) / (dx * dx)


def divergence_flux_1d(g: np.ndarray, theta: np.ndarray, dx: float) -> np.ndarray:
    """Approximate div(g grad(theta)) with periodic boundaries."""
    grad_theta_forward = (np.roll(theta, -1) - theta) / dx
    flux_forward = g * grad_theta_forward
    return (flux_forward - np.roll(flux_forward, 1)) / dx


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
        g_eff = g_base * (1.0 + sigma * memory)

        # PMT phase transport.
        theta_t = omega - gamma * divergence_flux_1d(g_eff, theta, dx)

        # PMT memory writing.
        memory_t = xi * theta_t**2 - rho * memory

        theta = theta + dt * theta_t
        memory = np.maximum(0.0, memory + dt * memory_t)

    g_eff = g_base * (1.0 + sigma * memory)
    return theta, memory, g_eff


if __name__ == "__main__":
    theta, memory, g_eff = run_simulation()

    print("PMT minimal simulation complete")
    print(f"theta:  min={theta.min(): .6f}, max={theta.max(): .6f}, mean={theta.mean(): .6f}")
    print(f"memory: min={memory.min(): .6f}, max={memory.max(): .6f}, mean={memory.mean(): .6f}")
    print(f"G_eff:  min={g_eff.min(): .6f}, max={g_eff.max(): .6f}, mean={g_eff.mean(): .6f}")
