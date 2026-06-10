# Econometrics Guide

## Project Overview
A Quarto book covering core econometrics topics (OLS, MLE, GLS, IV, GMM, discrete choice, count data, panel data, survival analysis, dynamic panels, missing data). Originally an Rmd document, converted to a multi-chapter Quarto book in March 2026.

## Structure
- `_quarto.yml` — book configuration (cosmo theme, chapters, parts)
- `index.qmd` — preamble/landing page
- `ols.qmd`, `mle.qmd`, `gls.qmd` — core estimation chapters
- `endogeneity.qmd`, `gmm.qmd` — causal inference & IV part
- `censored.qmd`, `discrete.qmd`, `count-data.qmd` — limited DV part
- `panel-data.qmd`, `survival.qmd`, `dynamic-panel.qmd`, `missing-data.qmd` — advanced topics
- `_book/` — rendered HTML output
- `econometrics_guide.rmd` — legacy single-file version (kept for reference)
- `*.png` — images converted from EPS (ols, davidson, davidson2)

## Build
```
quarto render        # build the book
quarto preview       # live preview in browser
```

## R Dependencies
car, stats4, dplyr, mvtnorm, MASS, AER, ivreg, gmm, strucchange, ggfortify, survival

## Notes
- Each chapter with R code has a hidden setup chunk (`#| include: false`) loading its required libraries
- `execute: freeze: auto` in `_quarto.yml` caches R output; delete `_freeze/` to force re-run
- Images are PNG (converted from EPS for HTML compatibility)

## Review pass (2026-06-07)
Full math/code audit + fixes across 10 chapters (audit trail: ../_review/). Key corrections:
- count-data: QML-Poisson sandwich meat matrix was inverted (`A^{-1}B^{-1}A^{-1}` → `A^{-1}BA^{-1}`).
- discrete: probit score had CDF where the density `f` belongs; MNL denominator summed a constant index.
- mle: joint Gaussian density `(2πσ²)^{-n/2}`; removed spurious `Σ` that multiplied the SSR by n; Newey–West bread needed `^{-1}`.
- survival: Weibull "density" was the CDF; Cox one-unit hazard change is `exp(β)` not `1-exp(β)`.
- ols: distinguished OLS residual `û` from structural error `u` in the fitness decomposition.
- missing-data: MI estimate is the mean `(1/M)Σ`, not a sum.
- panel-data: chapter was TRUNCATED mid-sentence — authored the missing FE within-estimator + Hausman section.
- Held for author: censored.qmd Heckman `ρ` vs `ρσ` covariance parameterization (reported, not edited).
Re-rendered clean.

## Review pass 2 (2026-06-10)
Fresh independent 2-agent audit of all 13 chapters (reports `../_review2/econ_1.md`, `econ_2.md`; full edit list `../_review2/FIXLOG.md`). 0 CRIT. Highlights:
- censored: applied the held Heckman item after hand-derivation — covariance off-diagonal `ρσ` (both models), `u=ρσv+e` with `Var(e)=σ²(1−ρ²)`, two-step Mills coefficient `ρσ`. The MLE selection term `Φ((Wγ+ρ(y−Xβ)/σ)/√(1−ρ²))` is CORRECT as printed (E[v|u]=ρu/σ) — do not "fix" it.
- Rendering MAJORs: blank lines inside `$$…$$` destroyed equations in the published HTML (ols ×3 core conditions, gls model+WLS, survival Cox ×2, panel-data base model) — Pandoc display math cannot contain a blank line. Also `\[…\]` is stripped (gmm kurtosis) — use `$$`.
- survival: hazard definition was missing `/Δt` (limit as printed = 0).
- mle: Newey–West derivation had `√T` where `1/√T` belongs.
- endogeneity+gmm: the shared simulation covariance `[[1,.6,.8],[.6,1,0],[.8,0,1]]` was exactly singular (.6²+.8²=1; x≡.6z+.8w, no first-stage error) — `crxw` changed to .5; prose claims unaffected (OLS plim 1.6 unchanged).
- dynamic-panel: AB instrument matrix had a spurious all-zero first row; Nickell (1981) attribution; Nickell covariance formula MC-verified correct.
- Plus ~30 MED/MINOR fixes (notation, df symbols, AR-test hypothesis wording, MI combining rules m/M, zero-truncation NB denominator, etc.).
Re-rendered clean; CI deploys via Pages render-from-`_freeze` on push (commit `_freeze/` with qmd changes).
