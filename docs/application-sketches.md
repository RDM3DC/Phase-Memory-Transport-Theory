# PMT Application Sketches

First-pass mappings from Phase-Memory Transport Theory variables into possible engineering toy models.

---

## RF Routing

| PMT term | RF interpretation |
|---|---|
| `θ` | carrier or beamforming phase |
| `M` | path-use memory from coherent transmission |
| `G_eff` | effective route or channel conductance |
| `κ` | environmental or geometric curvature proxy |

Toy target: let repeated coherent packet paths increase `M`, then measure whether `G_eff = G(1+σM)` lowers phase-roughness cost along that corridor.

---

## Adaptive Optics

| PMT term | Optics interpretation |
|---|---|
| `θ` | wavefront phase |
| `M` | correction or material response memory |
| `G_eff` | adaptive correction strength |
| `κ` | lens, mirror, or medium curvature |

Toy target: write memory where wavefront correction activity is strongest, then test whether future phase error decays faster in reinforced regions.

---

## QPS-Style Phase Refresh

| PMT term | QPS interpretation |
|---|---|
| `θ_R` | resolved lifted phase |
| `M` | drift or refresh ledger |
| `G_eff` | refresh pathway capacity |
| `πₐ` | local adaptive wrap scale |

Toy target: compare phase-rate memory and gradient memory as refresh triggers for branch-aware phase evolution.

---

## AdaptiveCAD Path Routing

| PMT term | CAD interpretation |
|---|---|
| `θ` | path phase, toolpath clock, or slicing coordinate |
| `M` | historically stable route memory |
| `G_eff` | preferred path conductance |
| `κ` | local surface or path curvature |

Toy target: use PMT memory to bias route selection toward coherent, repeatable paths while penalizing high curvature or phase roughness.

---

## Shared Metrics

- memory contrast: `max(M)/mean(M)`
- conductance contrast: `max(G_eff)/mean(G_eff)`
- phase roughness: `mean(|∇θ|²)`
- channel fraction: fraction of cells where `M > mean(M)+std(M)`
- EPM seed margin: `vM − (V0 + uκ)`