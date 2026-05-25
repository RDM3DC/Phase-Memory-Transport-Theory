# Phase-Memory Transport Theory (PMT)

**Standalone White Paper**  
**Canonical Core Arm:** 07  
**Date:** 2026-05-25  
**Status:** Draft scaffold

---

## Abstract

Phase-Memory Transport Theory (PMT) defines an adaptive transport layer where phase evolution writes memory and memory modifies future transport. It extends Curve Memory, Phase-Lift, Adaptive-π Geometry, and Adaptive Curvature Flow Networks into a single phase-memory feedback system.

The central loop is:

```text
phase → memory → adaptation → geometry → future phase
```

PMT is intended as a mathematical, computational, and engineering framework for systems where phase coherence, historical path use, and adaptive routing interact.

---

## 1. Motivation

Phase is usually treated as an instantaneous variable, such as an angle, oscillator state, wave phase, or branch coordinate.

PMT treats phase as history-bearing.

That means phase does not only describe where a system is in a cycle. It also contributes to what the system remembers and how future signals move.

Examples of systems that suggest PMT-style behavior:

- RF and wireless routing with phase coherence
- optical systems with wavefront memory
- adaptive oscillator networks
- quantum-inspired navigation models
- signal paths that become easier after repeated coherent use
- geometric computation with memory-bearing phase fields

---

## 2. Core Fields

PMT uses four main state variables:

| Variable | Meaning |
|---|---|
| `θ` | phase field or resolved phase |
| `M` | memory density |
| `G` | adaptive conductance / transport capacity |
| `κ` | curvature field, usually supplied by ACFN |

The minimum PMT pair is:

```text
θ, M
```

The full coupled PMT/ACFN system is:

```text
G, κ, θ, M
```

---

## 3. Minimal Equations

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

Interpretation:

- phase evolves according to frequency and transport through `G`
- rapid phase evolution writes memory
- memory modifies the effective future transport capacity

---

## 4. Coupled Four-Field Form

When PMT is coupled to Adaptive Curvature Flow Networks:

```text
dG/dt = α|I| − μG + λ|∇κ| + σM

∂κ/∂t = η ∇·(G ∇κ) − βκ

∂θ/∂t = ω − γ ∇·(G ∇θ)

∂M/∂t = ξ(∂θ/∂t)² − ρM
```

This gives the expanded adaptive field loop:

```text
θ writes M
M modifies G
G transports κ and θ
κ changes geometry
geometry changes future θ
```

---

## 5. Relation to Phase-Lift

Phase-Lift gives branch-aware semantics:

```text
(⧉f)(z; θ_ref) = f(z; θ_R)
```

PMT gives dynamics to the resolved phase `θ_R`:

```text
∂θ_R/∂t = ω − γ ∇·(G ∇θ_R)
```

So:

```text
Phase-Lift tells us how to evaluate on the right branch.
PMT tells us how the phase branch moves and stores memory.
```

---

## 6. Relation to Adaptive-π

Adaptive-π defines a local phase wrap unit:

```text
θ = θ_R + 2πₐ(x,t)w
```

PMT can transport the resolved phase `θ_R` while Adaptive-π controls local wrapping.

This separates:

- phase transport
- phase wrapping
- winding bookkeeping

---

## 7. Memory Writing Laws

The canonical first law is:

```text
∂M/∂t = ξ(∂θ/∂t)² − ρM
```

Other possible memory laws include:

```text
∂M/∂t = ξ|∇θ|² − ρM
```

```text
∂M/∂t = ξ|∇θ · v| − ρM
```

The squared phase-rate law is preferred as the starting model because it is simple and strongly emphasizes rapid phase evolution.

---

## 8. Transport Regimes

### 8.1 Low-memory regime

```text
M ≈ 0
G_eff ≈ G
```

Transport is mostly determined by existing adaptation.

### 8.2 Memory-reinforced regime

```text
σ > 0
G_eff > G
```

Historically coherent paths become easier.

### 8.3 Memory-blocked regime

```text
σ < 0
G_eff < G
```

Memory represents damage, decoherence, congestion, or fatigue.

---

## 9. PMT Applications

### RF / wireless routing

Phase-coherent paths may be reinforced as memory-bearing transport corridors.

### Adaptive optics

Wavefront corrections can be modeled as phase-memory updates.

### Quantum-inspired positioning

PMT gives a non-claiming mathematical layer for history-sensitive phase routing, useful near QPS-style ideas without requiring a claim of new quantum mechanics.

### AdaptiveCAD / geometry kernels

PMT can guide phase-aware geometric routing, toolpath coherence, and non-triangular adaptive slicing.

---

## 10. Simulation Target

A minimal 2D PMT simulation should demonstrate:

```text
persistent phase channels created by phase-memory feedback
```

Pseudo-code:

```text
initialize θ, M, G
for each time step:
    G_eff = G*(1 + σ*M)
    θ_t = ω - γ*div(G_eff*grad(θ))
    M_t = ξ*θ_t**2 - ρ*M
    θ += dt*θ_t
    M += dt*M_t
```

Expected visible behavior:

- phase waves move through the field
- high phase-change regions write memory
- memory modifies future phase transport
- channels or persistent paths may emerge

---

## 11. Canonical Claim

PMT does not claim that all phase transport in nature is adaptive.

The canonical claim is:

```text
PMT defines a general adaptive transport theory in which phase evolution writes memory, and memory modifies future transport.
```

---

## 12. Next Work

- Build numerical toy models
- Plot phase-memory channel formation
- Compare memory-write laws
- Couple PMT to ACFN curvature fields
- Add stability metrics
- Explore RF, optics, QPS, and AdaptiveCAD examples
