from __future__ import annotations

import unittest

from examples.acfn_pmt_coupled_solver import CoupledPMTParameters, run_coupled_solver
from examples.minimal_pmt_sim import run_simulation, summarize_fields
from examples.pmt_2d_channel_sim import PMT2DParameters, run_channel_simulation_2d
from examples.pmt_memory_law_comparison import compare_memory_laws
from examples.reduced_pmt_solver import ReducedPMTParameters, run_solver


class PMTExampleTests(unittest.TestCase):
    def test_minimal_simulation_returns_finite_fields(self) -> None:
        theta, memory, g_eff = run_simulation(n=96, steps=300)
        summary = summarize_fields(theta, memory, g_eff)

        self.assertTrue(summary["finite"])
        self.assertGreaterEqual(summary["memory_min"], 0.0)
        self.assertGreater(summary["memory_contrast"], 1.0)

    def test_memory_law_comparison_runs_all_laws(self) -> None:
        rows = compare_memory_laws(n=80, steps=180)

        self.assertEqual(len(rows), 3)
        for row in rows:
            self.assertTrue(row["finite"])
            self.assertGreaterEqual(row["memory_min"], 0.0)

    def test_reduced_solver_converges_to_stable_equilibrium(self) -> None:
        result = run_solver(ReducedPMTParameters(steps=4000))

        self.assertTrue(result["stable"])
        self.assertLess(result["distance_to_equilibrium"], 0.1)

    def test_coupled_acfn_pmt_solver_returns_finite_state(self) -> None:
        _, metrics = run_coupled_solver(CoupledPMTParameters(n=64, steps=160))

        self.assertTrue(metrics["finite"])
        self.assertGreaterEqual(metrics["memory_min"], 0.0)
        self.assertGreaterEqual(metrics["conductance_min"], 0.0)

    def test_2d_channel_simulation_returns_finite_state(self) -> None:
        _, metrics = run_channel_simulation_2d(PMT2DParameters(n_x=32, n_y=24, steps=80))

        self.assertTrue(metrics["finite"])
        self.assertGreaterEqual(metrics["memory_min"], 0.0)
        self.assertGreater(metrics["memory_contrast"], 1.0)


if __name__ == "__main__":
    unittest.main()