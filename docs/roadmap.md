# PMT Roadmap

Roadmap for developing Phase-Memory Transport Theory as a standalone research/programming repository.

---

## v0.1 — Scaffold

- [x] Fill README
- [x] Add standalone PMT paper
- [x] Add notation guide
- [x] Add first minimal simulation
- [x] Add plots and figures

---

## v0.2 — Toy Simulations

- [x] 1D phase-memory transport simulation
- [x] 2D phase-memory channel simulation
- [x] Compare memory laws:
  - `ξ(∂θ/∂t)^2`
  - `ξ|∇θ|^2`
  - mixed phase-gradient laws
- [x] Add visualization scripts

---

## v0.3 — Coupling to ACFN

- [x] Couple PMT to Adaptive Curvature Flow Networks
- [x] Add four-field solver for `G, κ, θ, M`
- [ ] Visualize adaptive phase-memory geodesics
- [x] Track persistence and channel stability metrics

---

## v0.4 — Applications

- [x] Add first application mapping notes
- [ ] RF routing toy model
- [ ] Adaptive optics toy model
- [ ] AdaptiveCAD path-routing example
- [ ] QPS-style phase refresh example

---

## v1.0 — Formal Draft

- [ ] Full white paper
- [ ] Mathematical assumptions section
- [ ] Simulation validation section
- [ ] API / package layout
- [ ] Stable canonical notation

---

## Open Questions

1. What memory law is most stable numerically?
2. Does PMT naturally form channels in 2D?
3. Can PMT define a coherence metric useful for RF/optics?
4. How should PMT couple to Adaptive-π local wrap structure?
5. Can PMT produce stable structures that feed into EPM?
