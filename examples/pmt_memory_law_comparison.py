"""
Compare PMT memory-write laws on the same 1D phase transport initial state.

Run:
    python examples/pmt_memory_law_comparison.py

Outputs:
    figures/memory_law_comparison.csv
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

try:
    from .minimal_pmt_sim import MemoryLaw, run_simulation, summarize_fields
except ImportError:
    from minimal_pmt_sim import MemoryLaw, run_simulation, summarize_fields


MEMORY_LAWS: tuple[MemoryLaw, ...] = ("phase_rate_squared", "gradient_squared", "mixed")
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "figures" / "memory_law_comparison.csv"


def compare_memory_laws(n: int = 192, steps: int = 1200) -> list[dict[str, Any]]:
    """Run each memory-write law and return comparable summary rows."""
    rows: list[dict[str, Any]] = []

    for memory_law in MEMORY_LAWS:
        theta, memory, g_eff = run_simulation(n=n, steps=steps, memory_law=memory_law)
        summary = summarize_fields(theta, memory, g_eff)
        rows.append({"memory_law": memory_law, **summary})

    return rows


def write_csv(rows: list[dict[str, Any]], output_path: Path = DEFAULT_OUTPUT) -> Path:
    """Write comparison rows as a CSV artifact."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return output_path


def format_row(row: dict[str, Any]) -> str:
    """Format one memory-law comparison row for console output."""
    return (
        f"{row['memory_law']:>20} | "
        f"memory_mean={row['memory_mean']:.6f} | "
        f"memory_max={row['memory_max']:.6f} | "
        f"contrast={row['memory_contrast']:.6f} | "
        f"finite={row['finite']}"
    )


if __name__ == "__main__":
    comparison_rows = compare_memory_laws()
    comparison_path = write_csv(comparison_rows)

    print("PMT memory-law comparison complete")
    for comparison_row in comparison_rows:
        print(format_row(comparison_row))
    print(f"wrote: {comparison_path}")