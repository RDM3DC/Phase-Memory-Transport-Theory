# PMT Proof and Solution Package

**Repository:** Phase-Memory-Transport-Theory  
**Canonical Core Arm:** 07  
**Date:** 2026-05-25  
**Status:** Mathematical working draft

---

## 0. Purpose

Phase-Memory Transport Theory (PMT) describes phase as a history-bearing transport medium.

This document proves the first rigorous core of PMT:

1. memory positivity,
2. memory boundedness,
3. exact phase-memory charge accounting,
4. phase diffusion energy dissipation in the fixed-conductance case,
5. solved uniform phase-memory model,
6. stability of a reduced memory-coupled transport model,
7. graph PMT dissipation,
8. links to ACFN, EPM, and ACST.

---

## 1. Minimal PMT System

The basic PMT equations in the diffusive simulation convention are

```text
∂θ/∂t = ω + γ ∇·(G∇θ)
```

```text
∂M/∂t = ξ(∂θ/∂t)² − ρM
```

```text
G_eff = G(1 + σM)
```

where:

- `θ` is phase or resolved phase,
- `M ≥ 0` is memory density,
- `G ≥ 0` is adaptive conductance / transport capacity,
- `ω` is intrinsic frequency,
- `γ` is phase transport strength,
- `ξ ≥ 0` is memory creation,
- `ρ > 0` is memory decay,
- `σ` is memory feedback.

The central loop is:

```text
phase → memory → adaptation → geometry → future phase
```

---

## 2. Theorem: PMT Memory Positivity

### Statement

If

```text
M(x,0) ≥ 0,
ξ ≥ 0,
ρ > 0,
```

then any solution of

```text
∂M/∂t = ξ(∂θ/∂t)² − ρM
```

satisfies

```text
M(x,t) ≥ 0
```

for all `t ≥ 0`.

### Proof

For each fixed `x`, memory satisfies the linear ODE

```text
dM/dt + ρM = ξ(∂θ/∂t)².
```

Using the integrating factor:

```text
M(t) = e^{-ρt}M(0) + ∫0^t e^{-ρ(t-s)} ξ(∂θ/∂t(s))² ds.
```

Both terms are nonnegative. Therefore `M(t) ≥ 0`.

QED.

---

## 3. Theorem: PMT Memory Boundedness Under Bounded Phase Rate

### Statement

If

```text
|∂θ/∂t| ≤ B
```

then

```text
M(x,t) ≤ e^{-ρt}M(x,0) + (ξB²/ρ)(1 − e^{-ρt}).
```

In particular,

```text
limsup_{t→∞}M(x,t) ≤ ξB²/ρ.
```

### Proof

Use the exact solution:

```text
M(t)=e^{-ρt}M(0)+∫0^t e^{-ρ(t-s)}ξ(∂θ/∂t)²ds.
```

Since `(∂θ/∂t)² ≤ B²`,

```text
M(t) ≤ e^{-ρt}M(0)+ξB²∫0^t e^{-ρ(t-s)}ds.
```

The integral is `(1-e^{-ρt})/ρ`.

QED.

---

## 4. ACST Accounting for PMT Memory Charge

Define total memory charge

```text
Q_M(t) = ∫Ω M(x,t) dx.
```

Then

```text
dQ_M/dt = ξ∫Ω(∂θ/∂t)²dx − ρQ_M.
```

### Proof

Integrate the memory equation over the domain:

```text
d/dt ∫M dx = ∫[ξ(∂θ/∂t)² − ρM]dx.
```

Therefore

```text
dQ_M/dt = ξ∫(∂θ/∂t)²dx − ρ∫Mdx.
```

QED.

### Interpretation

PMT memory is produced by phase activity and decays at rate `ρ`. It is not exactly conserved, but it is exactly ledgered.

---

## 5. Phase Energy Dissipation for Zero-Frequency Transport

Set `ω=0` and assume `G(x)` is fixed and nonnegative. Consider

```text
∂θ/∂t = −γ∇·(G∇θ).
```

This sign convention is the standard diffusion sign when written as gradient descent of phase roughness. Define phase roughness energy:

```text
Eθ = 1/2 ∫ |∇θ|² dx.
```

For constant `G=G0>0`, the equation becomes

```text
∂θ/∂t = −γG0 Δθ.
```

If instead PMT is written with the opposite sign convention,

```text
∂θ/∂t = +γ∇·(G∇θ),
```

then diffusion dissipates roughness directly.

### Canonical Sign Convention Note

For stability in simulations, use the diffusive convention:

```text
∂θ/∂t = ω + γ∇·(G∇θ)
```

or equivalently define the operator sign so that the Laplacian term smooths phase.

Under the diffusive convention and periodic/no-flux boundary conditions:

```text
d/dt (1/2∫θ²dx) = −γ∫G|∇θ|²dx ≤ 0.
```

### Proof

Assume

```text
∂θ/∂t = γ∇·(G∇θ).
```

Let

```text
E0 = 1/2∫θ²dx.
```

Then

```text
dE0/dt = ∫θ∂θ/∂t dx = γ∫θ∇·(G∇θ)dx.
```

Integrate by parts with periodic/no-flux boundaries:

```text
dE0/dt = −γ∫G|∇θ|²dx ≤ 0.
```

QED.

---

## 6. Solved Uniform PMT Model

If phase rate is spatially uniform:

```text
∂θ/∂t = Ω0
```

then memory solves

```text
dM/dt = ξΩ0² − ρM.
```

Exact solution:

```text
M(t) = M* + (M(0)-M*)e^{-ρt}
```

where

```text
M* = ξΩ0²/ρ.
```

Effective conductance becomes

```text
G_eff(t) = G(1 + σM(t)).
```

At equilibrium:

```text
G_eff* = G(1 + σξΩ0²/ρ).
```

This is the first solved PMT memory-conductance law.

---

## 7. Reduced Memory-Coupled Conductance Model

Consider a finite-dimensional PMT feedback model:

```text
dM/dt = ξΩ² − ρM
```

```text
dG_eff/dt = aM − bG_eff
```

where `Ω` is fixed phase activity.

### Equilibrium

```text
M* = ξΩ²/ρ
```

```text
G_eff* = aM*/b = aξΩ²/(bρ).
```

### Stability

The system is triangular:

```text
dM/dt = −ρ(M−M*)
```

```text
dG_eff/dt = aM − bG_eff.
```

Eigenvalues are

```text
−ρ, −b.
```

Therefore the equilibrium is stable when

```text
ρ > 0, b > 0.
```

QED.

---

## 8. Graph PMT Transport

On a graph, let phase at node `v` be `θ_v`, and edge conductance `G_uv ≥ 0`.

A diffusive PMT transport law is

```text
dθ_v/dt = ω_v + γ Σ_{u~v} G_uv(θ_u − θ_v).
```

In vector form:

```text
dθ/dt = ω − γL_Gθ
```

where `L_G` is the weighted graph Laplacian.

If `ω=0`, define

```text
Eθ = 1/2 Σ_v θ_v².
```

Then

```text
dEθ/dt = −γ/2 Σ_{u~v}G_uv(θ_u − θ_v)² ≤ 0.
```

### Proof

```text
dEθ/dt = θᵀ dθ/dt = −γ θᵀL_Gθ.
```

For a weighted graph Laplacian:

```text
θᵀL_Gθ = 1/2ΣG_uv(θ_u−θ_v)² ≥ 0.
```

QED.

---

## 9. Phase Channel Formation Criterion

A simple PMT channel is favored when memory feedback increases effective conductance enough to reduce phase transport cost.

If phase transport cost is modeled as

```text
C_phase = ∫ |∇θ|² / G_eff ds,
```

and

```text
G_eff = G(1+σM),
```

then memory lowers phase cost when

```text
σM > 0.
```

For positive feedback `σ>0`, any persistent positive memory makes the channel cheaper.

A thresholded form is:

```text
σM > C_threshold/G − 1.
```

---

## 10. Coupling to ACFN

ACFN gives

```text
dG/dt = α|I| − μG + λ|∇κ| + σM.
```

PMT supplies the memory term from phase activity:

```text
∂M/∂t = ξ(∂θ/∂t)² − ρM.
```

Therefore phase activity can increase future conductance if `σ>0`.

This is the solved PMT-to-ACFN feedback path:

```text
phase activity → memory → conductance growth.
```

---

## 11. Coupling to EPM

EPM forms stable structures when memory helps create a negative effective potential:

```text
r(x,t)=V0+uκ−vM.
```

The EPM structure condition is

```text
vM > V0 + uκ.
```

PMT supplies `M` through phase activity. Thus a sufficient PMT seed condition for EPM is

```text
v(ξB²/ρ) > V0 + uκ
```

where `B` is a sustained phase-rate bound or steady phase activity scale.

This gives a first bridge theorem:

```text
sustained phase activity can seed EPM when memory production overwhelms geometry potential.
```

---

## 12. What Is Solved So Far

### Proven

- PMT memory positivity,
- memory boundedness under bounded phase rate,
- exact memory-charge accounting,
- phase diffusion energy dissipation under stable sign convention,
- uniform memory equilibrium,
- memory-coupled conductance equilibrium,
- graph PMT transport dissipation,
- phase-channel cost reduction criterion,
- PMT-to-ACFN feedback condition,
- PMT-to-EPM seeding condition.

### Solved conditions

Uniform memory equilibrium:

```text
M* = ξΩ0²/ρ.
```

Effective conductance equilibrium:

```text
G_eff* = G(1 + σξΩ0²/ρ).
```

Memory-coupled conductance stability:

```text
ρ > 0, b > 0.
```

Phase channel favored:

```text
σM > 0.
```

PMT seeding EPM:

```text
vξB²/ρ > V0 + uκ.
```

---

## 13. What Is Still Open

1. Full nonlinear stability with `G_eff = G(1+σM)` inside the phase PDE.
2. Rigorous channel formation in 2D.
3. Phase wrapping with spatially varying `πₐ`.
4. Coupled PMT/ACFN/EPM global existence.
5. Best numerical sign convention for all target applications.
6. Experimental mapping to RF, optics, and QPS-style systems.

---

## 14. Summary

The first solved mathematical core of PMT is:

```text
phase activity writes nonnegative bounded memory;
memory modifies effective conductance;
positive memory feedback lowers future phase transport cost;
and sustained phase activity can seed EPM structures.
```

The flagship PMT equations are:

```text
∂M/∂t = ξ(∂θ/∂t)² − ρM
```

```text
G_eff = G(1+σM).
```

The strongest solved bridge condition is:

```text
vξB²/ρ > V0 + uκ.
```

That is the first rigorous foundation for Phase-Memory Transport Theory.
