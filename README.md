# Econometrics Guide

A public econometrics study guide by Xiang Ao (Research Computing Services, Harvard Business School), built as a [Quarto book](https://quarto.org/docs/books/) and deployed at <https://xiangao.github.io/econometrics-guide/>.

## Topics

| Part | Chapters |
|------|----------|
| **Foundations** | OLS, Maximum Likelihood, GLS |
| **Causal Inference & IV** | Endogeneity & Instrumental Variables, GMM |
| **Limited Dependent Variables** | Censored/Truncated/Selection Models, Discrete Choice, Count Data |
| **Advanced Topics** | Panel Data, Survival Models, Dynamic Panels, Missing Data |

## Prerequisites

- [Quarto](https://quarto.org/docs/get-started/) (>= 1.3)
- R with packages: `car`, `stats4`, `dplyr`, `mvtnorm`, `MASS`, `AER`, `ivreg`, `gmm`, `strucchange`, `ggfortify`, `survival`

## Legacy file

`econometrics_guide.rmd` is a deprecated single-file R Markdown archive
of an earlier version. The authoritative source is the per-chapter
`.qmd` files listed in `_quarto.yml`; the `.rmd` is kept for reference
only and is not rebuilt.

## Build

```bash
quarto render     # renders to _book/
quarto preview    # live preview with hot reload
```

## Sources

Materials drawn from Davidson and MacKinnon's *Econometric Theory and Methods*, Chris Baum's *An Introduction to Modern Econometrics Using Stata*, and other sources; see the [References](references.qmd) page for the full list. This is a compact study guide, not a comprehensive textbook.

> **2026-06-07:** Math/code review pass — see `CLAUDE.md` (Review pass section) for the list of corrections. Audit trail in `../_review/`.

> **2026-06-10:** Second independent review pass (all 13 chapters): Heckman selection re-parameterized consistently (`ρσ` covariance), hazard-function definition corrected (`/Δt`), Newey–West scaling fixed, several equations that rendered as literal text repaired (blank lines inside `$$` blocks), degenerate IV simulation DGP fixed, plus ~30 smaller corrections. Audit trail in `../_review2/`.

> **2026-06-13:** Technical-audit fix pass (Codex audit in `../_technical_audit_20260613/`). Corrected: binary-response index range (LPM vs logit/probit), exactly-identified vs overidentified IV/GMM formula, control-function scope for nonlinear models, Cox vs discrete-time proportional-odds hazard attribution, system-GMM (Blundell–Bond) description, OLS centered-decomposition intercept caveat, MLE √n scaling, WLS transformation- vs objective-weights, 2SLS SE/order-condition/weak-IV statements, QMLE-Poisson robust SEs, Heckman exclusion-restriction wording, FE matrix notation, dynamic-panel lag-mean notation. Added a References page; aligned public/internal framing; removed draft comments. Rendered clean.
