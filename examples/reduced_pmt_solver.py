"""
Reduced Phase-Memory Transport Theory (PMT) solver.

This solves a finite-dimensional phase-memory feedback model:

    dM/dt     = xi*Omega^2 - rho*M
    dG_eff/dt = a*M - b*G_eff

The equilibrium is:

    M* = xi*Omega^2/rho
    G_eff* = a*xi*Omega^2/(b*rho)

The equilibrium is stable when:

    rho > 0 and b > 0

Run:
    python examples/reduced_pmt_solver.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReducedPMTParameters:
    omega_activity: float = 1.4
    xi: float = 0.6
    rho: float = 0.8
    conductance_gain: float = 0.7
    conductance_decay: float = 0.5
    dt: float = 0.002
    steps: int = 10000
    initial_memory: float = 0.0
    initial_g_eff: float = 0.1


def equilibrium(p: ReducedPMTParameters) -> dict[str, float | bool]:
    exists = p.rho > 0.0 and p.conductance_decay > 0.0
    if not exists:
        return {"exists": False, "M_star": 0.0, "G_eff_star": 0.0}

    m_star = p.xi * p.omega_activity**2 / p.rho
    g_star = p.conductance_gain * m_star / p.conductance_decay
    return {"exists": True, "M_star": m_star, "G_eff_star": g_star}


def stability_condition(p: ReducedPMTParameters) -> dict[str, float | bool]:
    eigen_memory = -p.rho
    eigen_conductance = -p.conductance_decay
    return {
        "eigen_memory": eigen_memory,
        "eigen_conductance": eigen_conductance,
        "stable": eigen_memory < 0.0 and eigen_conductance < 0.0,
    }


def run_solver(params: ReducedPMTParameters | None = None) -> dict[str, float | bool]:
    p = params or ReducedPMTParameters()

    memory = max(0.0, p.initial_memory)
    g_eff = max(0.0, p.initial_g_eff)

    max_memory = memory
    max_g_eff = g_eff

    for _ in range(p.steps):
        dm = p.xi * p.omega_activity**2 - p.rho * memory
        dg = p.conductance_gain * memory - p.conductance_decay * g_eff

        memory = max(0.0, memory + p.dt * dm)
        g_eff = max(0.0, g_eff + p.dt * dg)

        max_memory = max(max_memory, memory)
        max_g_eff = max(max_g_eff, g_eff)

    eq = equilibrium(p)
    stable = stability_condition(p)

    m_star = float(eq["M_star"])
    g_star = float(eq["G_eff_star"])
    distance_to_equilibrium = ((memory - m_star) ** 2 + (g_eff - g_star) ** 2) ** 0.5

    # PMT-to-EPM seed metric placeholder:
    # if v*M > V0 + u*kappa, PMT memory can seed EPM.
    v = 1.0
    v0 = 0.4
    u = 0.3
    kappa = 0.2
    epm_seed_margin = v * memory - (v0 + u * kappa)

    return {
        **eq,
        **stable,
        "final_memory": memory,
        "final_g_eff": g_eff,
        "max_memory": max_memory,
        "max_g_eff": max_g_eff,
        "distance_to_equilibrium": distance_to_equilibrium,
        "epm_seed_margin_demo": epm_seed_margin,
        "epm_seed_condition_met_demo": epm_seed_margin > 0.0,
    }


if __name__ == "__main__":
    result = run_solver()
    print("Reduced PMT solver complete")
    for key, value in result.items():
        if isinstance(value, bool):
            print(f"{key}: {value}")
        else:
            print(f"{key}: {value:.8f}")
