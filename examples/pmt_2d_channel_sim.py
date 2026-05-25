"""
Toy 2D Phase-Memory Transport channel simulation.

Run:
    python examples/pmt_2d_channel_sim.py

Outputs:
    figures/pmt_2d_memory.pgm
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMAGE = REPO_ROOT / "figures" / "pmt_2d_memory.pgm"


@dataclass(frozen=True)
class PMT2DParameters:
    n_x: int = 72
    n_y: int = 48
    steps: int = 600
    dt: float = 0.0003
    length_x: float = 1.0
    length_y: float = 0.75
    omega: float = 0.8
    gamma: float = 0.006
    xi: float = 0.35
    rho: float = 0.06
    sigma: float = 0.4


def divergence_flux_2d(conductance: np.ndarray, theta: np.ndarray, dx: float, dy: float) -> np.ndarray:
    """Approximate div(G grad(theta)) on a periodic 2D grid."""
    grad_x_forward = (np.roll(theta, -1, axis=1) - theta) / dx
    grad_y_forward = (np.roll(theta, -1, axis=0) - theta) / dy
    flux_x = conductance * grad_x_forward
    flux_y = conductance * grad_y_forward
    div_x = (flux_x - np.roll(flux_x, 1, axis=1)) / dx
    div_y = (flux_y - np.roll(flux_y, 1, axis=0)) / dy
    return div_x + div_y


def stable_explicit_dt_2d(dx: float, dy: float, gamma: float, conductance: np.ndarray, safety: float = 0.18) -> float:
    """Return a conservative explicit 2D diffusion time step."""
    max_transport = gamma * float(np.max(conductance))
    if max_transport <= 0.0:
        return np.inf
    return safety * min(dx, dy) ** 2 / (4.0 * max_transport)


def initial_fields_2d(params: PMT2DParameters) -> dict[str, np.ndarray]:
    """Create a seeded 2D phase field and base conductance channel."""
    x_coordinate = np.linspace(0.0, params.length_x, params.n_x, endpoint=False)
    y_coordinate = np.linspace(0.0, params.length_y, params.n_y, endpoint=False)
    coordinate_x, coordinate_y = np.meshgrid(x_coordinate, y_coordinate)
    normalized_y = coordinate_y / params.length_y

    theta = 0.18 * np.sin(2.0 * np.pi * coordinate_x / params.length_x)
    theta += 0.45 * np.exp(-(((coordinate_x - 0.25) ** 2) / 0.012 + ((normalized_y - 0.48) ** 2) / 0.018))
    theta -= 0.30 * np.exp(-(((coordinate_x - 0.72) ** 2) / 0.018 + ((normalized_y - 0.54) ** 2) / 0.026))
    memory = np.zeros_like(theta)
    base_conductance = 0.78 + 0.18 * np.exp(-((normalized_y - 0.5) ** 2) / 0.03)

    return {
        "x": coordinate_x,
        "y": coordinate_y,
        "theta": theta,
        "memory": memory,
        "base_conductance": base_conductance,
    }


def summarize_channel(fields: dict[str, np.ndarray]) -> dict[str, float | bool]:
    """Return finite-run and channel-formation diagnostics."""
    theta = fields["theta"]
    memory = fields["memory"]
    g_eff = fields["g_eff"]
    memory_mean = float(memory.mean())
    memory_std = float(memory.std())
    epsilon = float(np.finfo(float).eps)
    channel_mask = memory > memory_mean + memory_std

    finite = bool(
        np.all(np.isfinite(theta))
        and np.all(np.isfinite(memory))
        and np.all(np.isfinite(g_eff))
    )

    return {
        "finite": finite,
        "memory_min": float(memory.min()),
        "memory_max": float(memory.max()),
        "memory_mean": memory_mean,
        "memory_contrast": float(memory.max() / max(memory_mean, epsilon)),
        "channel_fraction": float(np.mean(channel_mask)),
        "g_eff_min": float(g_eff.min()),
        "g_eff_max": float(g_eff.max()),
        "theta_variance": float(np.var(theta)),
    }


def run_channel_simulation_2d(
    params: PMT2DParameters | None = None,
) -> tuple[dict[str, np.ndarray], dict[str, float | bool]]:
    """Run the toy 2D PMT channel simulation."""
    params = params or PMT2DParameters()
    fields = initial_fields_2d(params)
    dx = params.length_x / params.n_x
    dy = params.length_y / params.n_y

    theta = fields["theta"]
    memory = fields["memory"]
    base_conductance = fields["base_conductance"]

    for _ in range(params.steps):
        remaining_dt = params.dt

        while remaining_dt > 0.0:
            g_eff = base_conductance * (1.0 + params.sigma * memory)
            sub_dt = min(remaining_dt, stable_explicit_dt_2d(dx, dy, params.gamma, g_eff))
            theta_t = params.omega + params.gamma * divergence_flux_2d(g_eff, theta, dx, dy)
            memory_t = params.xi * theta_t**2 - params.rho * memory

            theta = theta + sub_dt * theta_t
            memory = np.maximum(0.0, memory + sub_dt * memory_t)
            remaining_dt -= sub_dt

    fields["theta"] = theta
    fields["memory"] = memory
    fields["g_eff"] = base_conductance * (1.0 + params.sigma * memory)

    return fields, summarize_channel(fields)


def write_memory_pgm(memory: np.ndarray, output_path: Path = DEFAULT_IMAGE) -> Path:
    """Write the final memory field as an ASCII PGM image."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    memory_min = float(memory.min())
    memory_max = float(memory.max())
    value_span = memory_max - memory_min

    if value_span <= np.finfo(float).eps:
        scaled = np.zeros_like(memory, dtype=np.uint8)
    else:
        scaled = np.round(255.0 * (memory - memory_min) / value_span).astype(np.uint8)

    rows = [" ".join(str(int(pixel_value)) for pixel_value in scaled_row) for scaled_row in scaled]
    output_path.write_text(
        "\n".join(["P2", f"{memory.shape[1]} {memory.shape[0]}", "255", *rows]),
        encoding="ascii",
    )
    return output_path


if __name__ == "__main__":
    final_fields, metrics = run_channel_simulation_2d()
    image_path = write_memory_pgm(final_fields["memory"])

    print("PMT 2D channel simulation complete")
    for metric_name, metric_value in metrics.items():
        if isinstance(metric_value, bool):
            print(f"{metric_name}: {metric_value}")
        else:
            print(f"{metric_name}: {metric_value:.8f}")
    print(f"wrote: {image_path}")