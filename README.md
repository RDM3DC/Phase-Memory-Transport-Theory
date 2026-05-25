# Phase-Memory Transport Theory (PMT)

**Standalone repository for Arm 7 of the expanded Canonical Core framework.**

PMT studies how phase can behave as a history-bearing transport medium in adaptive systems.

The central loop is:

```text
phase → memory → adaptation → geometry → future phase
```

This repository is connected to the Canonical Core stack:

```text
1. ARP/AIN                               → adaptation engine
2. Adaptive-π Geometry                   → adaptive phase-period geometry
3. Curve Memory / CMA                    → path and derivative memory
4. Phase-Lift / PR-Root / PROs           → branch-aware phase operators
5. QPS-GR Mapping                        → strain / clock / visibility engineering layer
6. Adaptive Curvature Flow Networks      → dynamic geometry
7. Phase-Memory Transport Theory         → adaptive phase-memory transport
8. Emergent Phase Matter                 → stable phase-memory structures
9. Adaptive Conservation and Symmetry    → adaptive invariants and laws
```

---

## Core Idea

Earlier arms define:

- adaptive conductance `G`
- adaptive geometry / curvature `κ`
- curve memory `M`
- resolved phase `θ`
- phase lifting through `⧉`

PMT adds a transport layer where phase evolution writes memory, and memory changes future transport.

In plain language:

```text
phase does not just move through the system;
it changes the system that future phase moves through.
```

---

## Minimal PMT Equations

A compact PMT model is:

```text
∂θ/∂t = ω − γ ∇·(G ∇θ)
```

```text
∂M/∂t = ξ(∂θ/∂t)² − ρM
```

```text
G_eff = G(1 + σM)
```

where:

| Symbol | Meaning |
|---|---|
| `θ` | phase field |
| `M` | memory density |
| `G` | adaptive conductance / transport capacity |
| `G_eff` | memory-modified effective conductance |
| `ω` | intrinsic phase frequency |
| `γ` | phase transport strength |
| `ξ` | memory creation rate |
| `ρ` | memory decay rate |
| `σ` | memory feedback strength |

---

## Four-Field Coupled Form

When coupled to Adaptive Curvature Flow Networks, PMT becomes part of a four-field adaptive system:

```text
dG/dt = α|I| − μG + λ|∇κ| + σM

∂κ/∂t = η ∇·(G ∇κ) − βκ

∂θ/∂t = ω − γ ∇·(G ∇θ)

∂M/∂t = ξ(∂θ/∂t)² − ρM
```

with recurring state variables:

```text
G  → adaptation
κ  → geometry
θ  → phase
M  → memory
```

---

## Repository Structure

```text
Phase-Memory-Transport-Theory/
├── README.md
├── papers/
│   └── phase-memory-transport-theory.md
├── docs/
│   ├── notation.md
│   └── roadmap.md
└── examples/
    └── minimal_pmt_sim.py
```

---

## Canonical Relationship

PMT is Paper 07 in the expanded Canonical Core framework:

- Canonical Core website: https://rdm3dc.github.io/canonical-core/
- Canonical Core repo: https://github.com/RDM3DC/canonical-core

The standalone purpose of this repository is to develop PMT into:

- equations
- simulations
- visualizations
- tests
- implementation prototypes
- future experimental / engineering examples

---

## Status

**Version:** 0.1.0-draft  
**Status:** Early standalone scaffold  
**Canonical role:** Arm 7 — adaptive phase-memory transport

---

## License

Text and theory notes: CC BY 4.0 unless otherwise stated.  
Code examples: MIT-style permissive use unless otherwise stated.
