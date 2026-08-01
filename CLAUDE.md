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
car, stats4, dplyr, mvtnorm, MASS, AER, ivreg, gmm, strucchange, ggfortify, survival, fixest

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

## Review pass (2026-07-30)
Fresh sweep of all 12 substantive chapters — the book had had no commits since the 2026-07-04 agy-review fix pass (commit c9c333c). Report: `../_review3/review_20260730.md`. The earlier passes evidently landed: the per-observation vs full-sample information distinction, the Heckman `ρσ` covariance, the hazard `/Δt` limit, the Newey–West scaling, the multinomial/conditional logit separation, the `R²` intercept caveat and the WLS scaling-vs-weighting note are all now correct. Four real errors plus eight smaller items.

**ols: the exogeneity hierarchy was inverted.** The text said contemporaneous exogeneity "is itself stronger than predeterminedness". It is the reverse: with `X_t` measurable wrt `F_{t-1}`, iterated expectations gives `E[u_t|X_t] = E[E[u_t|F_{t-1}]|X_t] = 0`, so predeterminedness *implies* contemporaneous exogeneity. Conditioning on a larger information set is more restrictive, not less. Replaced with an explicit strict ⇒ predetermined ⇒ contemporaneous list plus the LIE argument — which also explains why contemporaneous exogeneity is the right condition to cite for *consistency*.

**discrete: the non-identification claim was false.** The chapter said a formula with both choice-varying regressors `W_tl` and choice-specific coefficients `β^l` "is not separately identified". Choice probabilities depend on `W_tj β^j − W_tl β^l`, which pins down each `β^j` when the `W_tj` vary independently across alternatives — no normalization needed. Verified by simulation (3 alternatives, n=2e5, true β = 0.5/−1.0/1.5): free MLE returns 0.5054/−1.0138/1.4926 with a positive-definite Hessian (min eigenvalue 18,107). It is what Stata's `asclogit` fits. The "conflates two models" criticism was kept; the real cost is restated as ambiguity about which normalization is in force. Also added the ordered-probit *location* and *scale* normalizations, which the chapter stated for multinomial logit but omitted here.

**mle: the comment contradicted the code** — "Use OLS estimates as starting values" sat above `optim(c(1,1,-1,-1,-1), ...)`, while OLS is (37.1055, −0.0009, −0.0312, −3.8009) with σ²=6.0935. The comment now describes the naive starts and why they make the demonstration stronger (it converges: code 0, max |β̂−OLS| = 3.9e-4).

**count-data: dead link** — `hbs-rcs.github.io/blog/2014/09/17/poisson-models/` returns 404. Removed; the `blog_book` pointer in the same sentence was kept. (The four `xiangao.github.io` links in `index.qmd` all return 200; note `econometrics-guide` with a **hyphen** is the live URL — the underscore form 404s.)

**Smaller items:** `mle` asymptotic-efficiency item — `V` was called the variance of `θ̂` then used as the variance of the limit of `√n(θ̂−θ)`; fixed, and the *regular*-CAN qualifier added (Hodges' estimator named, since without it the claim is false). `gmm` — `W` denoted both the weighting matrix and the instrument (and the data column is `w`); disambiguated, `gmm()`'s arguments described correctly, and the chapter's gap filled: optimal `W = S^{-1}`, asymptotic variance `(G'S^{-1}G)^{-1}`, two-step GMM, and 2SLS as efficient GMM only under homoskedasticity. `endogeneity` — the geometry passage asserted a similar-triangles identity requiring `x₁ ⊥ x₂` while explicitly ruling out the one construction that delivers it; rewritten around `x = x^⊥ + x^∥` (projection onto `u`), which makes both orthogonalities hold by construction, and the infeasible-regression algebra is now shown. `survival` — `exp <- survreg(...)` shadowed base `exp()` (renamed `exp_fit`), and an AFT-vs-PH sign-convention warning was added for reading `survreg` beside `coxph`. `missing-data` — the MI recipe drew `α` but never a residual, i.e. improper imputation, the very defect charged against single regression imputation two sections earlier. `panel-data` — education is not time-invariant in general.

**Verified correct by re-derivation or execution (no action).** `censored`'s full-information Heckman likelihood, including the `Φ[(Wγ+ρ(y−Xβ)/σ)/√(1−ρ²)]` term re-derived from `v|u ~ N(ρu/σ, 1−ρ²)`; `count-data`'s NB2 pmf re-derived from the Gamma mixture; `dynamic-panel`'s `Cov(y_{i,t−1},C_i) = σ_c²/(1−γ)` and Nickell's covariance (the chapter's form equals `−σ_ε²[(T−1)−Tγ+γ^T]/[T²(1−γ)²]`), and the `−(1+γ)/(T−1)` approximation giving exactly the claimed −0.1667 at T=10, γ=0.5; `survival`'s Greenwood formula and Weibull hazard; `gls`'s `Ψ'ΩΨ = I`. Executed: `sctest(type="Chow")` and `anova(fm0,fm1)` give identical F=3.9268, p=0.06307; `ivreg` = manual 2SLS = control function to 1.9e-15; `gmm` = `ivreg` to 5.8e-15 and `gmm` = `lm` to 2.0e-15; OLS omitting z gives 1.5961 against the theoretical 1.6.

## Deep read (2026-07-30) — 12/12 chapters, no mathematical errors

Full-depth pass over every chapter. Log:
`~/projects/books/_review3/deepread_econometrics_guide.md`.

**This is a derivation book**: 7 of the 12 chapters (`gls`, `panel-data`,
`dynamic-panel`, `missing-data`, `discrete`, `count-data`, `censored`) contain no
executable code at all, and `ols` has one chunk. So the review lever here is
re-deriving the mathematics and simulating it where possible — not re-executing and
diffing output, which is what works for the other three books.

**No mathematical errors were found.** Everything re-derived came out correct,
including the Heckman selection log-likelihood (the third term follows from
`E[v|u] = (rho/sigma)u` with `Var(v|u) = 1-rho^2`), Greenwood's variance, the Cox
partial likelihood with Breslow ties, Rubin's rules, the NB2 pmf and its
`mu(1+mu/theta)` variance, and the full Newey-West sandwich (the T factors cancel
exactly). The Nickell bias formula was checked by simulation at N=40,000 across six
(T, gamma) pairs and matches to about three decimals.

What was left to find were precision and completeness gaps:

- `ols` introduced `E(Xu)=0` as "weaker" and then `E(u_t|X_t)=0` as "much weaker" two
  paragraphs later, which reads as though mean independence were weaker than zero
  covariance. Added contemporaneous orthogonality as the explicit bottom rung.
- `censored`'s section titled "Switching Regression" shows a model with one beta and
  one delta — a constant effect. Added the distinction from the Roy model.
- `gls` attributed one transformation to both Cochrane-Orcutt and Prais-Winsten;
  they differ exactly in the first observation, which the chapter's own Psi framework
  supplies.
- `gmm`'s worked example reproduces 2SLS only because it is just-identified (the
  J-test in its own output reports df 0), not in general.
- `mle` built the information matrix and the efficiency bound but never presented
  LR/Wald/LM. Added.

**If you extend this book, the failure mode to watch is prose that drifts from the
algebra** — every issue found in two passes has been of that kind (an inverted
hierarchy, a mis-titled model, an elided intercept, a normalization left unstated),
not a wrong formula.

## Addition (2026-08-01) — aggregation vs long format in `panel-data`

New `##` section after the Hausman test: "Collapse to unit means, or keep the long
format?" Written in the chapter's own notation (`z_i`, `x_it`, `c_i`, `ȳ_i`).

Content: (1) with a balanced panel and only time-invariant regressors, pooled OLS on
`NT` rows equals the between regression on `N` unit means *exactly*, and RE gives the
same coefficient — Wooldridge (2010) §20.3.4; (2) the degrees-of-freedom trap, `N − k`
not `NT − k`, citing Moulton (1990) and Donald & Lang (2007) — clustering repairs the
SE asymptotically but not the dof at small `N`; (3) once a time-varying regressor
enters, all coefficients differ, including those on `z_i`, since collapsing yields the
between estimator while pooled OLS mixes within and between; (4) three-row summary
table; (5) Mundlak as the reconciliation, linking to the regression-based Hausman
paragraph directly above.

Two references added to `references.qmd`: Donald & Lang (2007), Moulton (1990).

Deliberately excluded: the Clark (1973) / Baayen et al. (2008) psychology result that
averaging over a factor you still need to generalize across gives Type I error near
0.24–0.31 against nominal 0.05, and does not improve with sample size. Correct and
relevant, but off-register for this book. Add as a plain paragraph, not a callout, if
it ever goes in — the book uses no callouts.

Edit gotcha hit here: the Hausman caveat is one very long single line, so a short
`old_string` anchor matched only its prefix and orphaned the tail onto the end of the
new section. Anchor on whole lines in this file.

## Addition (2026-08-01b) — `panel-data` demo section, first code in the chapter

Second new section, "What the long format buys", answering the complaint that the
first one only said what you lose. Three `fixest` chunks on simulated data, `N = 1000`,
`T = 6`, seed 42:

1. Balanced, time-invariant regressor only — long and collapsed agree at
   `1.99351677619` vs `1.99351677619`, printed at 12 digits so the identity is visible.
2. Unbalanced (high-`z` units lose later periods) — `2.00682070731` vs `2.01481052322`.
3. `c_i` correlated with `x̄_i`, true `beta = 1` — between 1.845, pooled 1.484,
   within 0.995, Mundlak `x` 0.995, Mundlak `x̄` 0.850. Note 1.845 − 0.995 = 0.850,
   so the `x̄` coefficient is exactly the Hausman contrast.

All five numbers match theory: between = 1 + var(mu)/var(x̄) = 1 + 1/(1+1/T) = 1.857,
pooled = 1 + cov(x,c)/var(x) = 1.5. The prose quotes these values, so **if the seed,
`N`, `T` or chunk order ever changes, the prose must be re-checked** — the RNG stream
is shared across the three chunks.

`fixest` added to the R dependency lists in README.md and above. Stata equivalents
(`regress`, `xtreg, fe`, `xtreg, re`) are named inline, matching how the Hausman
section already handles Stata.

## Addition (2026-08-01c) — "How OLS weights the data" in `panel-data`

Third section, added because the `T_i` weighting in the section above reads as a
panel-specific quirk when it is an instance of the general FWL rule. States the rule
once — each observation enters weighted by the squared residualised regressor,
`sum_t Vtilde_it^2` per unit — then tabulates four cases:

| model | unit/stratum weight |
|---|---|
| `z_i` alone | `T_i * ztilde_i^2` |
| `z_i` plus time-varying `W_it` | `sum_t ztilde_it^2` (the `T_i` form dies) |
| time-varying `x_it` | `sum_t (x_it - xbar_i)^2 = (T-1) Var_i(x)` |
| binary `d`, saturated controls | `n_x dhat(x)(1-dhat(x))` — Angrist (1998) |

Fourth code chunk (seed 7, self-contained) shows when the weighting matters: with
slopes drawn independently of how much `x` moves, FE 1.0019 / plain 1.0179 /
weighted 0.9841, all equal to within noise. With slopes larger where `x` moves more,
FE 1.5338 / plain 1.0140 / weighted 1.5422 — FE tracks the weighted average, and a
reader taking it as "the" slope is off by 50%. Closes on Słoczyński (2022).

**Verified against the primary sources, and this turned up an error elsewhere:**
`blog_book/weights-ols.qmd` line 74 links Angrist (1998) as DOI `10.2307/2999578`,
which resolves to Gul, "A Comment on Aumann's Bayesian View", *Econometrica* 66(4).
The correct DOI is `10.2307/2998558` (Econometrica 66(2), 249–288), confirmed via the
Crossref API. Not fixed here — different repo. Słoczyński confirmed as
`10.1162/rest_a_00953`, REStat 104(3), 501–509. Note `doi.org` returns 403 to curl for
both (JSTOR and MIT Press block bots); use the Crossref API to verify, not the DOI URL.

The same material is covered at more depth in `blog_book/weights-ols.qmd` (unit-level
weights, signed, first power of `Dtilde`) and `blog_book/ols-ate.qmd` (Słoczyński).
Those use the *outcome*-weight object; this section uses the *effect*-weight object.
They are the same identity read at two granularities — verified numerically: OLS,
`sum omega_i y_i`, Angrist's `dhat(1-dhat)P(x)` and `sum_x Dtilde^2` all returned
1.96680501, with the last two differing by exactly the constant `n`.

## Notation (2026-08-01d, superseded 2026-08-01e) — `panel-data.qmd`

An X/W/Z remap (X = regressor of interest, W = covariates, Z = instruments) was
applied chapter-wide and then **reverted at the author's request**. The chapter keeps
its original scheme. Do not reapply it.

The scheme, now stated explicitly in a Background paragraph rather than left implicit:

- `x_it` — varies across units *and* time (price, income, usually the treatment)
- `z_i`  — varies across units only; fixed within a unit over time (religion, education)
- `w_t`  — varies across time only; common to all units in a period (a national TV campaign)
- instruments are `Z`, a different object from `z_i`, and appear only once the panel
  turns dynamic; the paragraph says so and links to Endogeneity, GMM, Dynamic Panel Data

Why the remap failed: the chapter's letters encode *time variation*, while X/W/Z
encodes *role*. Two different axes, colliding on both W and Z. If notation is ever
revisited, that is the conflict to solve first.

**Correction to the weighting table.** The first version listed four parallel rows,
one of which ("`z_i` with a time-varying `W_it`") was not a case at all — it was the
general rule with no simplification available, since `Vtilde_it` carries both
subscripts even when `V` does not. The table now lists only the three models where
`sum_t Vtilde_it^2` actually simplifies, and the prose says plainly that the `T_i`
form is the one-regressor special case rather than the general one.

Cross-chapter links render as `href="./chapter.html"`. No `{#sec-}` labels exist in
this book, so cross-references are chapter-level only.

## Rewrite (2026-08-01f) — the heterogeneous-slopes demo in `panel-data`

The demo was misread in review as "fixed effects versus no fixed effects". It is not:
**one** estimator is run, and the other two columns are the planted true slopes averaged
two ways. The columns were named `FE` / `plain avg` / `weighted avg`, which invited
reading three estimators side by side. Rewritten:

- columns renamed `FE estimate` / `true slopes, plain avg` / `true slopes, weighted`,
  and transposed to `cbind` so the two designs are columns `(A) unrelated` /
  `(B) aligned` — also fixes output wrapping at book width
- `demo()` split into `panel()` (build data) and `compare()` (run one regression,
  return it beside the two benchmarks), so the single estimator is visible
- prose now states the claim *before* the code, says explicitly that only one
  estimator is run, and says FE is OLS with unit dummies partialled out — a reader
  asked why FE was used to illustrate a claim about OLS
- new second chunk: sort units by how much `x` moves, compare the 100 steadiest
  (avg slope 0.01, 0.35% of weight) with the 100 wobbliest (avg slope 2.01, 28.26%).
  This is what makes the 1.53-vs-1.01 gap concrete
- closes by saying the weighting is not a defect — leaning on units where `x` moves is
  efficient; it only misleads when slope correlates with movement

**Row (A) numbers changed** (0.9813/0.9716/0.9816, was 1.0019/1.0179/0.9841). Cause:
the old code passed `rnorm(N,1,1)` as a function argument, and R's lazy evaluation drew
it *after* `x` inside the body. Assigning `b1` first draws it before. Row (B) is
unchanged because its slopes use no RNG. No prose quoted row (A)'s values.

## Correction (2026-08-01g) — first-power vs squared weights in `panel-data`

The FWL section said "each observation enters weighted by `Vtilde_it^2`". **That was
wrong.** The numerator carries `Vtilde` to the *first* power, so an observation's weight
on the *outcome* is `Vtilde_it`, signed, summing to zero. Two distinct objects were
being collapsed:

- weights on **outcomes**: `omega_it = Vtilde_it / sum Vtilde^2` — first power, signed
- weights on **effects**:  `w_i = sum_t Vtilde_it^2` — second power, non-negative

The text now derives the second from the first rather than asserting it: substitute
`y_it = beta_i V_it + ...`, and `sum_t Vtilde_it V_it = sum_t Vtilde_it^2` because
`Vtilde` is orthogonal to the projected-out part of `V`.

**The per-unit identity requires saturation.** Verified numerically: with unit dummies
the identity holds globally AND unit by unit; with a linear control it holds globally
but fails per unit (max discrepancy 12.5 in a 200x6 panel). This is the Hazlett–Shinkre
point, and it is why the Angrist row assumes saturated controls. Stated in the text.

Links added to `https://xiangao.github.io/blog_book/weights-ols.html` and
`ols-ate.html` (both verified 200). Those chapters carry both weight objects; this one
only needed the second, so the cross-reference does real work — negative weights live
in the signed first-power object and cannot appear in the squared one.

Also checked: Słoczyński (2022) uses only the effect-weight representation ("a convex
combination" of ATT and ATU) and never discusses per-observation signed weights, so
there is no conflict with him — he is answering a different question.

## Rewrite (2026-08-01h) — lead the weighting demo with the extreme two-group case

The continuous heterogeneous-slopes demo did not land in review even after 2026-08-01f.
What worked in discussion was the degenerate version, so it now comes first:

- half the units barely move (`sd 0.2`) with true slope **0**, half move a lot
  (`sd 3`) with true slope **2**, so the average unit's slope is exactly 1
- FE returns **1.984**, and the steady half holds **0.473%** of the weight
- no averaging subtleties, no second design, nothing to decode — the units with
  slope 0 simply were not in the regression

The continuous (A)/(B) demo follows, justified as showing the control case the extreme
example cannot: what happens when slope and movement are *unrelated*. The
steadiest-vs-wobbliest diagnostic chunk was **removed** — the two-group case makes the
same point more starkly, and it was the third table in a row.

Chunk ordering note: the new chunk sits *before* the (A)/(B) chunk but does not disturb
it, because that chunk opens with its own `set.seed(7)`. Verified — (A)/(B) output is
byte-identical. Any future chunk inserted there must preserve that seed call.
