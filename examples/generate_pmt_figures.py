"""
Generate lightweight PMT figure artifacts without external plotting libraries.

Run:
    python examples/generate_pmt_figures.py

Outputs:
    figures/pmt_1d_fields.csv
    figures/pmt_1d_fields.svg
"""

from __future__ import annotations

import csv
import html
from pathlib import Path

import numpy as np

try:
    from .minimal_pmt_sim import run_simulation
except ImportError:
    from minimal_pmt_sim import run_simulation


REPO_ROOT = Path(__file__).resolve().parents[1]
FIGURE_DIR = REPO_ROOT / "figures"
FIELD_COLORS = {
    "theta": "#245c8f",
    "memory": "#b6532f",
    "G_eff": "#557a3a",
}


def normalized_polyline(values: np.ndarray, left: float, right: float, top: float, bottom: float) -> str:
    """Convert a 1D series into SVG polyline points inside a panel."""
    value_min = float(np.min(values))
    value_max = float(np.max(values))
    value_span = value_max - value_min
    x_positions = np.linspace(left, right, len(values))

    if value_span <= np.finfo(float).eps:
        y_positions = np.full_like(x_positions, (top + bottom) / 2.0)
    else:
        normalized_values = (values - value_min) / value_span
        y_positions = bottom - normalized_values * (bottom - top)

    return " ".join(
        f"{x_position:.2f},{y_position:.2f}"
        for x_position, y_position in zip(x_positions, y_positions, strict=True)
    )


def write_fields_csv(output_path: Path, coordinate: np.ndarray, theta: np.ndarray, memory: np.ndarray, g_eff: np.ndarray) -> Path:
    """Write the final 1D field snapshot as CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["x", "theta", "memory", "G_eff"])
        for coordinate_value, theta_value, memory_value, conductance_value in zip(
            coordinate,
            theta,
            memory,
            g_eff,
            strict=True,
        ):
            writer.writerow([coordinate_value, theta_value, memory_value, conductance_value])

    return output_path


def write_fields_svg(output_path: Path, theta: np.ndarray, memory: np.ndarray, g_eff: np.ndarray) -> Path:
    """Write a three-panel SVG of theta, memory, and effective conductance."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    width = 960
    height = 640
    left = 90.0
    right = 910.0
    panel_height = 130.0
    panel_gap = 70.0
    first_top = 90.0
    fields = (("theta", theta), ("memory", memory), ("G_eff", g_eff))

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">',
        '<rect width="100%" height="100%" fill="#f8f5ef"/>',
        '<text x="90" y="48" font-family="Georgia, serif" font-size="30" fill="#1f2b2d">PMT 1D field snapshot</text>',
        '<text x="90" y="72" font-family="Verdana, sans-serif" font-size="13" fill="#5c6465">stable diffusive transport with memory-reinforced conductance</text>',
    ]

    for panel_index, (field_name, values) in enumerate(fields):
        top = first_top + panel_index * (panel_height + panel_gap)
        bottom = top + panel_height
        color = FIELD_COLORS[field_name]
        escaped_name = html.escape(field_name)
        polyline = normalized_polyline(values, left, right, top, bottom)
        value_min = float(np.min(values))
        value_max = float(np.max(values))

        elements.extend(
            [
                f'<text x="36" y="{(top + bottom) / 2.0:.2f}" font-family="Verdana, sans-serif" font-size="16" fill="#263436">{escaped_name}</text>',
                f'<line x1="{left}" y1="{bottom:.2f}" x2="{right}" y2="{bottom:.2f}" stroke="#c9c0b4" stroke-width="1"/>',
                f'<line x1="{left}" y1="{top:.2f}" x2="{left}" y2="{bottom:.2f}" stroke="#c9c0b4" stroke-width="1"/>',
                f'<polyline points="{polyline}" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
                f'<text x="{right - 160:.2f}" y="{top - 12:.2f}" font-family="Verdana, sans-serif" font-size="12" fill="#5c6465">min {value_min:.4f} / max {value_max:.4f}</text>',
            ]
        )

    elements.append("</svg>")
    output_path.write_text("\n".join(elements), encoding="utf-8")
    return output_path


def generate_figures() -> dict[str, Path]:
    """Run the 1D PMT model and write CSV/SVG artifacts."""
    theta, memory, g_eff = run_simulation()
    coordinate = np.linspace(0.0, 1.0, len(theta), endpoint=False)

    field_csv = write_fields_csv(FIGURE_DIR / "pmt_1d_fields.csv", coordinate, theta, memory, g_eff)
    field_svg = write_fields_svg(FIGURE_DIR / "pmt_1d_fields.svg", theta, memory, g_eff)

    return {"field_csv": field_csv, "field_svg": field_svg}


if __name__ == "__main__":
    figure_paths = generate_figures()
    print("PMT figure generation complete")
    for artifact_name, artifact_path in figure_paths.items():
        print(f"{artifact_name}: {artifact_path}")