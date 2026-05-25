# PMT Notation

Canonical notation for Phase-Memory Transport Theory.

---

## Core Variables

| Symbol | Meaning |
|---|---|
| `θ` | phase field / resolved phase |
| `θ_R` | Phase-Lift resolved phase |
| `M` | memory density |
| `G` | adaptive conductance / transport capacity |
| `G_eff` | memory-modified effective conductance |
| `κ` | curvature field |
| `I` | flow, intensity, current, or load |

---

## PMT Parameters

| Symbol | Meaning |
|---|---|
| `ω` | intrinsic angular frequency |
| `γ` | phase transport strength |
| `ξ` | memory creation rate |
| `ρ` | memory decay rate |
| `σ` | memory feedback strength |

---

## Coupling Parameters

| Symbol | Meaning |
|---|---|
| `α` | ARP growth coefficient |
| `μ` | ARP relaxation coefficient |
| `λ` | curvature-gradient coupling |
| `η` | curvature transport coefficient |
| `β` | curvature relaxation coefficient |

---

## Canonical PMT Equations

```text
∂θ/∂t = ω + γ ∇·(G ∇θ)
```

```text
∂M/∂t = ξ(∂θ/∂t)² − ρM
```

```text
G_eff = G(1 + σM)
```

---

## Coupled ACFN/PMT System

```text
dG/dt = α|I| − μG + λ|∇κ| + σM
```

```text
∂κ/∂t = η ∇·(G ∇κ) − βκ
```

```text
∂θ/∂t = ω + γ ∇·(G ∇θ)
```

The examples use the diffusive sign convention above. On graphs, the equivalent form is `dθ/dt = ω − γL_Gθ` for a positive weighted Laplacian `L_G`.

```text
∂M/∂t = ξ(∂θ/∂t)² − ρM
```

---

## Relationship to Phase-Lift

Use `⧉` for Phase-Lifted evaluation.

```text
(⧉f)(z; θ_ref) = f(z; θ_R)
```

PMT transports `θ_R` over time.

---

## Relationship to Adaptive-π

Use `πₐ` for the adaptive phase-period field.

```text
θ = θ_R + 2πₐ(x,t)w
```

PMT evolves the resolved phase. Adaptive-π defines local wrap structure.
