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
- `interpreting-ols.qmd` — final chapter: what an OLS coefficient means when effects are heterogeneous
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

## Correction (2026-08-01i) — the demo implied plain OLS behaves like FE. It does not.

Reader objection, and it was right: the section is titled "How OLS weights the data",
every regression in it is `feols(... | id)`, and nothing warned that dropping the unit
effects changes the answer. The natural inference — plain OLS does the same thing — is
false, and the demo had been **constructed so it looked true**: both halves of the
two-group example were built around zero, which made "distance from the grand mean" and
"within-unit spread" numerically coincide.

New chunk parks the steady half away from zero:

| | fixed effects | plain OLS |
|---|---|---|
| steady half centred at 0 | 1.984 | 1.983 |
| steady half parked at 10 | 1.984 | 0.311 |
| steady half parked at 100 | 1.984 | 0.004 |

FE is invariant — the within transformation removes each unit's own mean first, so no
unit can sit far from it. Plain OLS collapses, for two reasons the text now separates:
the steady half *gains* weight as it moves away from the grand mean (a tight cluster far
out carries heavy weight despite barely moving), and a between-group channel opens that
is not weighting at all.

Key sentence now in the text: `Vtilde` is a deviation from *whatever mean the model
removes* — the unit's own mean with unit effects, the grand mean without. So "the weight
is how much x moves" is a statement about the demeaned case only.

`park(0)` reproduces the preceding chunk's 1.984 exactly (same `set.seed(1)`, same draw
order), so the two chunks compose. If either is edited, check that still holds.

**Process note:** this survived three prior revisions of the section because every check
run was on centred data. When a demo's conclusion depends on a construction choice, vary
that choice before publishing.

## Revision (2026-08-01j) — derive the OLS-vs-FE result, don't simulate it

Author's instruction: get this from theory, not simulation; simulation is fine as a
check, but not as the source. The previous version discovered the OLS collapse by
parking a group at different values and reporting what came out. Replaced with the
closed form.

Law of total covariance on two equally sized groups (means `mu_g`, within variances
`sigma_g^2`, slopes `beta_g`, group mean outcomes `ybar_g`):

```
plim beta_OLS = [ (1/2)(b1 s1^2 + b2 s2^2) + (1/4) dmu * dybar ]
                / [ (1/2)(s1^2 + s2^2)     + (1/4) dmu^2       ]
```

i.e. a variance-weighted average of `beta_within = (b1 s1^2 + b2 s2^2)/(s1^2+s2^2)` and
`beta_between = dybar/dmu`, weighted by within variance and between variance.

Everything then follows on paper. FE estimates `beta_within` = 18/9.04 = **1.991**, which
contains no `mu_g`, so parking cannot move it. In this design `beta_between = 0` (steady
slope is zero, both intercepts zero, so the group means sit at equal height). Hence
`plim beta_OLS = 9.04/(4.52 + dmu^2/4)`.

Predictions vs simulation: 1.991/1.983, 0.305/0.311, 0.004/0.004. The chunk now prints
an `OLS predicted` column beside `OLS actual` so the table reads as a check.

Used `\text{plim}` rather than `\operatorname*{plim}` — the latter is package-dependent
in MathJax and this book has no math preamble.

## Correction (2026-08-01k) — Słoczyński direction was stated backwards

The text read: "a coefficient from a sample that is 10% treated is mostly telling us
about the 90%." **Backwards**, and it contradicted the sentence immediately before it
("the smaller group receives the larger weight").

Słoczyński: `beta_OLS = (1-rho) ATT + rho ATU`, `rho` = treated share. So at `rho = 0.1`
the weight on **ATT** is 0.9 — the coefficient mostly reports the effect on the treated
tenth, not the untreated majority. The ATE is the same two numbers with the weights
reversed, `rho ATT + (1-rho) ATU`.

Verified by simulation (n = 400k, ~8.8% treated, heterogeneous `tau = 1 + 2x`):
ATT 2.3896, ATU 0.8709, ATE 1.0039, OLS 2.2611. `(1-rho)ATT + rho ATU` = 2.2565 matches;
`rho ATT + (1-rho) ATU` = 1.0039 is the ATE and does not. Those figures are now quoted
in the text so the direction is anchored to something checkable.

## Full audit (2026-08-01l) — five more errors in the new sections

Author asked for a re-read of the whole section after the Słoczyński direction error.
Five found, all now fixed:

1. **"average each unit over time and run `N` regressions"** — collapsing produces one
   regression on `N` rows, not `N` regressions.
2. **Mundlak stated wrongly.** Text claimed the coefficient on `xbar` "reproduces what
   the collapsed regression estimates". It does not: regressing `y` on `x` and `xbar`
   gives `beta_within` on `x` and `beta_between - beta_within` on `xbar`, so the *sum*
   is the between estimate. Verified: between 1.7874, within 1.0191, Mundlak `x` 1.0191,
   Mundlak `xbar` 0.7683 = 1.7874 - 1.0191, sum 1.7874. The later demo paragraph had it
   right all along, so the chapter contradicted itself.
3. **`xtreg, re` named as a Stata equivalent** — random effects is never run in any
   chunk. Changed to `regress`, `xtreg, be`, `xtreg, fe`.
4. **"Only one estimator is run in what follows"** — true of the next chunk, false of
   the parking chunk, which runs FE and plain OLS. Scoped to "the next chunk".
5. **Numerator constant wrong: `9.04` should be `9`.** The numerator is
   `(1/2)(b1 s1^2 + b2 s2^2) = 9`; `9.04` is `s1^2 + s2^2`, a different quantity. With
   9.04 the shift-0 prediction would be 2.0000, contradicting the chunk's own 1.991.

Checked and correct: the FWL formula; the within/between decomposition and its `1/2`
and `1/4` constants; `beta_within = 18/9.04 = 1.991`; `beta_between = 0` in this design;
the three table simplifications including `(T-1)Var_i(x)` and `n_x d(1-d)`; every
number quoted from a chunk against that chunk's output.

## Consolidation (2026-08-01m) — two-representation framing added, repetition cut

Added a `### Two ways to read the coefficient` subsection: the outcome representation
`betahat = sum omega_i y_i` with `omega_i = Vtilde_i / sum Vtilde^2` beside the effect
representation `betahat = sum w_i b_i / sum w_i` with `w_i = Vtilde_i V_i`, and a table
comparing them on what is weighted / sign / computability / when the reading holds /
what question each answers. Guidance is explicit: **default to the effect
representation**; use the outcome one only to detect negative weights, which squares
cannot express.

Also cut roughly 95 lines of repetition. The same claims had been restated three or
four times each as the section grew through revision:

- "which mean is subtracted" appeared four times — now stated once where `Vtilde` is
  introduced, with one back-reference at the two-group example
- Mundlak was explained in full twice — now explained once in "Collapse to unit means"
  and only referenced in the demo
- three separate closers ("not precision" / "not a defect" / "the practical reading")
  collapsed to one per section
- the `T_i`-is-a-special-case point appeared three times, now once

Net 644 -> 572 lines. All six chunks verified byte-identical after the rewrite, and
every number quoted in prose re-checked against the chunk that produces it.

**Standing lesson:** this section accumulated its repetition because each fix was
appended rather than integrated. After a run of corrections, re-read the whole section
once and consolidate before considering it done.

## Addition (2026-08-02) — derivation of the within/between split, plus a figure

The chapter stated the decomposition without deriving it. Now shows both laws:
total covariance for the numerator (within term `(1/2)(b1 s1^2 + b2 s2^2)`; between term
`(1/4) dmu dybar`, using `Cov(a,b) = (1/4)(a1-a2)(b1-b2)` for two-point equal-probability
variables) and total variance for the denominator. Then splits the result explicitly
into `beta_within` and `beta_between` as a convex combination, notes that `beta_within`
is itself a variance-weighted average one level up, that `beta_between` is a two-point
slope and so unconstrained by either group's interior, and that the `1/4` generalises to
`p(1-p)` — Angrist's weight again.

New base-R figure chunk (`set.seed(5)`, own seed so it does not disturb the `set.seed(7)`
chunk after it): two scatter panels, groups sharing a centre versus parked ten apart,
with the mean of `x` dotted, the centre-to-centre line dashed, and the fit solid. Prints

|                      | share a centre | far apart |
|---|---|---|
| slope inside wobbly  | 2.019 | 2.009 |
| slope inside steady  | 0.007 | -0.288 |
| between slope        | 0.882 | -0.007 |
| weight on between %  | 0.026 | 85.113 |
| OLS                  | 2.010 | 0.291 |

Two traps handled in the prose: the left panel's between slope of 0.882 is meaningless
(`dmu ~ 0`, so it divides by almost nothing) but harmless, since its weight is 0.026%;
and the right panel's steady slope of -0.288 is noise, not signal — a regression on an
`x` with sd 0.2 has SE around 0.35.

**Open question from the author:** whether to move this material into a separate
chapter, "Interpreting OLS". See the proposal in the session notes — the weighting
material is now roughly half of `panel-data.qmd` and is not panel-specific.

## Split (2026-08-02) — `interpreting-ols.qmd` created

`panel-data.qmd` had grown to ~640 lines, half of it not about panels. Everything from
"How OLS weights the data" onward moved to a new final chapter, `interpreting-ols.qmd`,
registered in `_quarto.yml` between `missing-data` and `references`. `panel-data` keeps
Background/RE/FE/Hausman plus collapse-versus-long-format, and ends with a forward link.

**Chunk portability.** The moved chunks depended on `N`, `T` and `library(fixest)` from
a chunk that stayed behind. The new chapter has a hidden setup chunk defining them. Every
moved chunk re-seeds internally (`set.seed(1)`, `set.seed(5)`, `set.seed(7)`, and
`set.seed(1)` inside `park()`), so all outputs are byte-identical after the move —
verified. If a chunk without its own seed is ever added there, this breaks.

**New material:** the point-to-centroid slope `s_i = (y_i - ybar)/(x_i - xbar)`, the
identity `betahat = sum (x_i-xbar)^2 s_i / sum (x_i-xbar)^2`, and a section warning that
`s_i` is not a measurement of `b_i`: correlation 0.019, sd 117.4 against 0.5, yet the
weighted averages agree (0.950 / 0.992, OLS 0.950). The point of that section is that
the `s_i` identity is model-free but vacuous, the `b_i` version carries the content but
needs an assumption, and the genuinely useful object is the weights, which need neither.

## Addition (2026-08-02b) — why averaging `s_i` recovers `b_i`

A reader objected, correctly: we want the `b_i`, we average `s_i`, and the two barely
correlate. The chapter reported the 0.019 without answering it. Two sections added.

**`w_i` is the inverse variance of `s_i`.** With `d_i = x_i - xbar`,
`s_i = b + (e_i - ebar)/d_i`, so `Var(s_i) = sigma^2 / d_i^2` and therefore
`w_i = d_i^2 = sigma^2 / Var(s_i)`. OLS is inverse-variance weighting of `n` unbiased
slope estimates — precision weighting, as in a meta-analysis. Verified by binning on
`|d|`: `w * Var(s)` is flat at ~4 = `sigma^2` across bins. The cancellation is algebraic:
`w_i s_i = d_i^2 (y_i - ybar)/d_i = d_i (y_i - ybar)`.

The first bin (|d| down to 1e-10) has no finite variance and reads 4e13. Kept in the
output and explained rather than trimmed: it is why the *unweighted* mean of `s_i` is
-23,816 against 0.999 weighted. The weighting is not an efficiency refinement; without
it the estimator does not exist.

**How much is noise?** Sweeping `sigma_e` from 2 to 0: Spearman goes 0.252 -> 0.997 and
the Pearson correlation among observations away from the mean reaches 1.000. So less
noise does tighten the link. **But at `sigma_e = 0` exactly, Pearson is 0.906, not 1** —
even with no error `s_i = b_i - ybar/(x_i - xbar)`, which explodes near the mean
(max |s_i - b_i| = 25.9 overall, 0.0074 on the far half). The irreducible gap is the
centring, not the noise, and it sits exactly where the weight is smallest.

Also softened the earlier "correlation 0.019 --- none". That is Pearson on a heavy-tailed
variable, dominated by a few exploded values; the rank correlation is much higher. The
signal is buried, not absent — a different claim.

## Audit (2026-08-02c) — five defects in `interpreting-ols.qmd`, all fixed

1. **Heading level broken by the move.** "When the weighting changes the answer" was
   `###`, so after the split it nested under "The slope of a single observation" instead
   of standing on its own. Promoted to `##`.
2. **Notation collision — the worst of the five.** The chapter used `w_i` for two
   different quantities: `w_i = Vtilde_i V_i = d_i x_i` (weights `b_i`, from "Two ways to
   read") and `d_i^2` (weights `s_i`, in the geometry sections). They are not the same
   observation by observation — correlation 0.966 when `xbar = 0.745` — and coincide only
   when `x` is centred, though they always sum to the same total since
   `sum d_i x_i = sum d_i^2`. `w_i` is now reserved for the effect weight; the `s_i`
   weight is written `d_i^2` throughout, with a paragraph naming the distinction.
3. **`Var(s_i)` stated as exactly `sigma^2/d_i^2`.** It is `sigma^2 (1 - 1/n)/d_i^2`;
   `ebar` appears in every `s_i`. Corrected with the approximation flagged.
4. **Prose quoted numbers no chunk printed** — the unweighted mean of `s_i` (-23,816)
   against the weighted one (0.999), and `max |s_i - b_i|` of 25.9 / 0.0074. All four now
   emitted by the chunks that own them.
5. **Panel notation used without introduction.** The simplifications table borrows
   `x_it`, `z_i`, `T` from the panel chapter, which this one no longer defines. Added a
   sentence saying so and noting the rule needs no panel.

Verified after: 9 chunk outputs, every number quoted in prose matched against the chunk
that produces it, heading tree correct, `w_i` appears only as the effect weight.

## Restructure (2026-08-02d) — build-up from two points, Angrist/Słoczyński detail, references

**Opening rebuilt on the author's suggested progression.** The chapter now starts with
two points, then three, then four, introducing `s_i` and the weight `d_i^2` concretely
before any algebra. One reusable `show()` function; the outputs make the mechanism
visible:

- 2 points: both `s_i` = 3, weights 50/50, OLS 3 — weights are *irrelevant* when the
  slopes agree
- 3 points: `s_i` = 1.8 / 9.0 / 0.0, weights 59.5% / 2.4% / 38.1%, OLS 1.2857 — the
  steepest own-slope gets 2.4% because it sits on the centroid
- 4 points (adding `x = 9`): the new point takes 64.9% alone, and the `x = 4` point
  falls from 38% to **0.18%** because the centroid moved to 4.25 and landed on it. OLS
  1.29 → 0.31 without touching any existing point.

That last one is the pedagogically valuable case: weight is not a property of an
observation, it is a property relative to the sample, and adding data rewrites it
everywhere. The `s_i` block was also moved ahead of the general rule, so the order is
concrete → structural → general.

**New section: "Angrist and Słoczyński, exactly."** Derives Angrist's weight from ours:
with binary `d` and saturated controls, `sum_{i in x} dtilde_i d_i = n_x dhat(1-dhat)`
because `d_i^2 = d_i`. Verified — the two weight vectors agree to 5.6e-10 and Angrist's
weighted average reproduces OLS exactly (2.0121, and 2.8740 in a low-`rho` design).
Notes that with a binary regressor no single observation *has* a slope, so the stratum
is the smallest unit carrying an effect: granularity is set by the regressor.

Słoczyński is the same weights aggregated to two groups, and the sharp statement is that
`betahat -> (1-rho) ATT + rho ATU` while `ATE = rho ATT + (1-rho) ATU` — the same two
numbers with the weights swapped. **The raw-`rho` form is exact only without covariates**;
with controls it gives 2.029 against an exact 2.012, and 2.858 against 2.874. Both are in
the chunk output so the approximation is visible rather than asserted.

Closes with a table placing the three (what each sorts by, smallest unit with an effect,
when exact) and Hazlett–Shinkre underneath all of them.

**References added** (all verified via Crossref except the arXiv one): Frisch & Waugh
(1933) 10.2307/1907330, Lovell (1963) 10.1080/01621459.1963.10480682, Mundlak (1978)
10.2307/1913646, Hazlett & Shinkre (2024) arXiv:2403.03299. Mundlak initially landed
before Moreira — alphabetical order is Moreira, Moulton, Mundlak.

Also changed an R comment inside a chunk from `##` to `#`: it parses as a heading to any
markdown tool scanning the source, even though Quarto renders it correctly.

## Figures (2026-08-02e) — plots for the two/three/four-point build-up

The build-up had tables but no pictures. `show()` now draws as well as prints: points,
the centroid as a hollow circle, a dotted line at `xbar`, rays from centroid to each
point with **thickness proportional to weight**, the fit, and each point's weight share
as a label. Same function, three calls, so the three panels are directly comparable.

Two label defects caught by actually looking at the rendered PNGs rather than trusting
the code: the rightmost label was clipped at the panel edge (fixed with
`xlim = c(-0.5, 11.5)`), and the label on the point sitting at the centroid collided
with the centroid marker (fixed with `pos = ifelse(y >= yb, 3, 1)`, so labels go above
or below depending on which side of the centroid the point is on). Also switched to one
decimal so the 0.2% point does not read as "0%".

**Worth repeating as practice:** read the generated image. Both defects were invisible in
the source and in the printed table.

## Fix (2026-08-02f) — cross-reference and heading damage from the restructure

Reader caught "the effect weight **above** was `w_i = Vtilde_i V_i`" in the `s_i`
section. After moving the `s_i` block ahead of "The rule", `w_i` is defined 200 lines
*below* that sentence — a forward reference written as a backward one. The comparison now
lives in "Two ways to read the coefficient", where both weights are known, and points
back at `d_i^2`.

Swept every directional word in the file (above / below / earlier / later / shortly /
next section) against the section it sits in. Only that one was broken; the other eleven
resolve correctly.

The sweep also exposed heading damage. Everything from the square derivation through the
simplifications table had been sitting under `### Two ways to read the coefficient`,
which describes none of it. Split into `### Where the square comes from` and
`### When the weight simplifies`. Also promoted `Do not mistake s_i for b_i` to `##`,
since "The identity behind it" was carrying four substantial subsections it does not
describe.

**Pattern, now three for three:** every content move in this chapter has broken something
invisible in the diff — orphaned text, stranded numbers, wrong heading levels, reversed
cross-references. After any move, sweep directional references and re-check the heading
tree before rendering.

## Tooling (2026-08-02g) — `audit_chapters.py`

Written after too many defects were found by the author rather than by me. Run it after
any edit to `panel-data.qmd` or `interpreting-ols.qmd`:

```
quarto render && python3 audit_chapters.py
```

Checks: heading-level skips (counted outside code chunks — an R comment starting `#`
otherwise reads as a heading); every 3+ digit number in prose appearing in some chunk
output of that chapter; citations resolving to `references.qmd`; internal `.qmd` links
existing; unmatched `$$`; blank lines inside `$$…$$` (this book's known rendering
killer). Rounding like 1.845 → "about 1.85" still flags, so triage rather than treat
every hit as an error.

Two checks deliberately dropped after testing: raw-LaTeX-in-HTML fires on MathJax's
client-side source in every chapter including untouched ones, and per-chunk variable
scoping is already enforced by the render failing.

**What it caught on its first run:** a second Słoczyński passage left behind after the
dedicated section was added, quoting a simulation (8.8% treated, ATT 2.39, ATU 0.87,
OLS 2.26) that no chunk in the book produces. Replaced with a cross-reference.

Also verified by hand this pass: all four external links live, both DOIs resolve to the
right papers via Crossref, zero repeated sentences within or across the two chapters.

## Correction (2026-08-02h) — conditioning on X, and a wrong analogy

Author asked why `d_i` is treated as a constant in `Var(s_i)`. It is because everything
is conditional on `X` — the standard convention, and load-bearing here: the weights are
functions of `x` alone, so the weighting argument only exists in the conditional world.
It also explains the degenerate first bin of the variance table: conditionally each
`Var(s_i)` is finite, merely enormous; it is unconditionally, over draws of `x` landing
near `xbar`, that it is unbounded. Now stated in the text.

**A wrong claim removed.** The chapter said OLS is "precision weighting, the same
operation as pooling studies in a meta-analysis". The weights part is right; the analogy
is not, because meta-analysis presumes *independent* estimates and the `s_i` are not
independent — the shared `ebar` gives `Cov(s_i, s_j) = -sigma^2/(n d_i d_j)`. OLS is
efficient here by Gauss–Markov, not by that route. Both the `(1-1/n)` and the covariance
are the same `ebar` term; I had noticed one and missed the other.

Derivation now in the text, two lines: `Var(e_i - ebar) = sigma^2(1 - 1/n)` and
`Cov(e_i - ebar, e_j - ebar) = -sigma^2/n`, divided by `d_i` and `d_i d_j`.

**Process note from the author:** stop reaching for simulation when the result is a
two-line derivation. Both facts here are algebra; no chunk was needed or added.

## Standing rule (2026-08-02i) — every simulation gets a lead-in

Author's instruction: always say what a simulation or illustration is doing, before the
code. Prompted by the variance-binning chunk, which was unreadable: `t(sapply(split(...)))`
three transformations deep, introduced by a single line.

Swept both chapters. Six chunks had no description of their setup — only a heading or a
paragraph about the surrounding idea. Each now says, in a sentence or two, what is being
generated, what is being computed, and what the reader should look for in the output.
The binning chunk gets the fullest treatment: six equal-sized groups sorted by distance
from the mean, and the point is that the last column is `sigma^2` in every group.

`audit_chapters.py` does not check this — the lead-in sweep is a separate loop over
chunks comparing each against the preceding paragraph. Worth folding in if this recurs.

Related note from the same exchange: prefer deriving to simulating when the result is a
few lines of algebra, and when a claim turns out to be wrong, **delete it** rather than
qualify it in place. A denial of a claim the reader never saw is worse than the claim.

## Rewrite (2026-08-04) — `interpreting-ols` rebuilt from a concise draft; within/between made general

The author was unhappy with the long narrative version of the chapter and had drafted
alternatives in a scratch repo, `~/projects/opencode/` (draft history there: `interpreting-ols.qmd`
= v1 917-line narrative, v2/v4 narrative, v3/v5 ~368-line concise, **v6 521-line merge = the
strongest**). Rebuilt the book chapter from v6, tightening rather than re-narrating. **917 → 546
lines.** Three decisions taken with the author up front: (1) base on v6 and tighten; (2) convert
equation numbering; (3) align prose to a shorter register.

- **Equation numbering.** All hand-typed `\tag{13.x}` replaced with Quarto `{#eq-name}` labels
  and `@eq-name` cross-references (32 equations). Numbers now auto-derive from the chapter's
  position — it is chapter 13, so they render 13.1–13.32 — and survive reordering. Do not
  reintroduce `\tag{}`.
- **Executable code.** v6 shipped three chunks fenced ```` ```r ```` (inert) instead of
  ```` ```{r} ````: the Angrist simulation, the `park()` shift simulation, and the two-panel
  figure. As written their cited numbers would never have rendered. Fixed. Every number in the
  prose was then checked against live output and matches (2.012 / 1.998 / 2.874; 2.029 / 2.858;
  sd(s) 117.4; noiseless corr 0.14; FE 1.98 & 0.47%; 1.983→0.004, β_within 1.991, V_within 4.52,
  numerator 9; 2.01 / 0.29 / 0.882 / 85% / −0.288; 1.53 / 1.01 / 1.54; N=100 furthest 35.4% /
  nearest 0.14%; 2.4% / 65% / 0.18% by hand).
- **Citations.** Normalized inline to the book's `Author (Year)` house style (v6 mixed
  `[Angrist, 1998]` and `Angrist [1998]`). References themselves were already correct and present
  in `references.qmd` (Angrist 1998, Słoczyński 2022, Hazlett & Shinkre 2024). The book uses **no
  `.bib`/`@citekey`** — plain-text list — so do not convert citations to `@`.

**The within/between derivation was rewritten to be general — the substantive change.** The v6
derivation of the pooled decomposition (eq. 13.30) was written entirely in the two-equal-group
setup (the `1/2` shares, the two-point `1/4`), so it did not actually support the "same rule for
any grouping" claim the surrounding text makes. Now derived for **any number of groups of any
sizes**: define `β_within = E[Cov(x,y|G)]/E[Var(x|G)]` and `β_between = Cov(E[x|G],E[y|G])/Var(E[x|G])`,
so the convex combination `(V_w β_w + V_b β_b)/(V_w + V_b)` falls straight out of the two
total-(co)variance laws with no equal-size or two-group assumption. The explicit share-weighted
`β_within` and across-group-regression `β_between` are then given (eq. 13.31), and the `1/2`,
`1/4`, `Δȳ/Δμ` closed forms presented as the two-equal-group case behind the simulation (eq. 13.32).
The old caveat "the `1/4` is the only piece specific to equal group sizes" was **understated** and
is fixed: with unequal sizes the `1/2`'s become shares `p_g` too, and with K>2 groups `β_between`
is a genuine across-group regression slope, not a two-point ratio. Equation count was held constant
across this rewrite so `eq-pooled` stays 13.30 and no downstream number shifts.

**Connective material added on the author's request, section by section:**

- A **figure caption** on the two-panel plot naming the elements (dashed = between-slope through
  the centroids, solid = pooled fit) and tying the rotation of the fit to eq. 13.30.
- A **bridging paragraph** opening the panel section: fixed effects is the opening FWL/leverage
  rule (eq. 13.4/13.12/13.14) with the *unit* mean subtracted instead of the grand mean, so the
  whole section is eq. 13.4 read one level down. This states in one place what had been scattered
  across the FWL "which mean" line, the special-cases table, and the `s_i`-as-panel remark.
- A **demeaning-as-collapse** sentence in the figure discussion: group-demeaning slides the shifted
  strip back so the right panel collapses onto the left, and OLS on that is the within/FE slope —
  which is why FE is flat regardless of the shift.

**Consistency pass (full read-through at the author's request).** Chapter is consistent; all cited
numbers match, all `@eq-` refs resolve, notation uniform. Two fixes applied: (1) eq. 13.23 used
`w₁, w₀` one equation before they are defined in 13.24 — added a forward pointer (the identity
itself was numerically verified correct; my hand-derivation doubting it was the error, not the
chapter); (2) the `park()` column `FE (theory 1.991)` renamed `FE estimate`, since it prints the
estimate (~1.984), not the theory value (which stays in prose). Left alone deliberately: `V` doing
double duty as the FWL regressor and as variances, and `w` as several weights — each defined
locally, in separate sections.

**Housekeeping.** Removed the obsolete draft versions that had been sitting untracked in the book
dir (`interpreting-ols-{draft,v2,v3,v4,v5}.{qmd,html}` and `_files/`); only `interpreting-ols.qmd`
remains. The v1–v6 history is preserved in `~/projects/opencode/`. Rendered full book clean after
each step; CI (Pages render-from-`_freeze`) green on every push. Commits `760f53f` and earlier this
session.

**Standing lesson:** a `` ```r `` vs `` ```{r} `` fence is a one-character difference that silently
turns a live simulation into inert listing — its cited numbers then have no source. When importing
a chapter drafted elsewhere, grep for `^```r$` before trusting any number in the prose.

## Split (2026-08-05) — Interpreting OLS becomes two chapters (Effect + Outcome Weights)

Split the single **Interpreting OLS** chapter in two. `interpreting-ols.qmd` is retitled
**"Interpreting OLS: Effect Weights"** (Ch. 13) and keeps the `sᵢ`/`dᵢ²` opening, `sᵢ`-vs-`bᵢ`, the
effect-weight FWL rule `w_i = Ṽ_i V_i` (@eq-weff), Angrist, Słoczyński and within/between. The FWL
"reads two ways" hinge, the ω/w comparison table and the outcome formula `ω_i = Ṽ_i/ΣṼ²`
(@eq-omega) moved out to **open** the new `outcome-weights.qmd`, **"Interpreting OLS: Outcome
Weights"** (Ch. 14, inserted before `references.qmd` in `_quarto.yml`). Ch. 14 cross-refs Ch. 13's
@eq-fwl/@eq-weff (resolve book-wide as 13.12/13.13; its own ω is 14.1).

Ch. 14 sections: (1) the two readings + ω/w table; (2) *What the outcome weights look like* — a
100-point figure with points sized by `|ω|`, the **two-dot slope construction** (`β̂` = rise/run
between the `|d|`-weighted centroids left and right of `x̄`) and a four-line derivation, *Why it
collapses to two points* (`β̂ = d·y / d·x`; a zero-sum `d` turns each inner product into
`W·(right-mean − left-mean)`, so `W` cancels); (3) *When the sign flips* — negative weights under
thin overlap; structural-vs-wrong-sign (wrong-sign = treated `ω<0` / control `ω>0` = linear `D̂`
outside `[0,1]` = extrapolation; verified live 17=17, 15=15), meaning (extrapolation / convex-hull
loss) and remedies (trim / interpolate / report), the Chattopadhyay–Zubizarreta (2023)
implied-weights framing with a **live `lmw` comparison** (its negatives = our `D̂∉[0,1]` units,
32=32) and the mainstream propensity-score overlap check (`WeightIt` ESS + `cobalt::bal.plot`; on
this data the logistic PS perfectly separates); (4) *Out of OLS* — the ω representation for
AIPW/DML/causal forests (Knaus 2024, `OutcomeWeights`); (5) *From two dots to four* — regression on
the treatment alone (two dots = group means, `β = ȳ₁−ȳ₀`) and the 2×2 DiD (four cell means, four
slopes), closing on staggered-TWFE negative weights (de Chaisemartin & D'Haultfœuille 2020;
Goodman-Bacon 2021) as the wrong-sign story one level up, plus a caution that the weights diagnose
estimation/overlap, not the parallel-trends identification assumption.

New render deps: **`lmw`** and **`WeightIt`** (live chunks; `cobalt` named in prose only). New
references: Chattopadhyay–Zubizarreta (2023), Crump et al. (2009), Li–Morgan–Zaslavsky (2018), de
Chaisemartin–D'Haultfœuille (2020), Goodman-Bacon (2021). Four figures in Ch. 14 (100-point,
negative-weight two-panel, treatment, DiD). Full book rendered clean; all cited numbers verified
against live output. A standalone companion note `interpreting-ols-knaus-connection.html` sits in
the book dir but is **not** in `_quarto.yml` (not part of the rendered book, left untracked).

## Modern treatments (2026-08-12) — population-level sections added to OLS, MLE, GLS

Three new sections adding modern/population-level perspectives to the classical chapters:

**OLS — "OLS as Conditional Expectation"** (after "Geometry of Least Squares", before
"Properties"). CEF definition and MMSE optimality proof (via iterated expectations on the
cross term), BLP as the population minimiser of E[(Y − X'b)²], population orthogonality
E[X(Y − X'β)] = 0 as the analog of X'û = 0, the BLP-approximates-CEF result (BLP depends
on Y only through the CEF), linear-vs-nonlinear CEF cases, and the population-to-sample
bridge showing that replacing expectations with sample averages recovers (X'X)⁻¹X'y with
the 1/n factors cancelling.

**MLE — "When the Model Is Wrong: Quasi-MLE and M-Estimation"** (after "Asymptotic
Properties", before "Example"). KL divergence motivation (MLE minimises KL from the true
density to the model), the pseudo-true value, the information matrix inequality
(J ≠ H under misspecification), sandwich variance H⁻¹JH⁻¹, QMLE for Poisson (score
depends only on E[Y|X] = exp(X'β), so consistency needs only correct conditional mean),
the same logic for logit/probit, and the M-estimator framework unifying OLS/MLE/QMLE/GMM
as special cases of Σψ(yₜ, xₜ, θ) = 0 with sandwich A⁻¹BA⁻¹'.

**GLS — "Efficiency of GLS"** (after "Feasible GLS"). Gauss-Markov proof for GLS: any
linear unbiased Cy has Var(C̃y) − Var(β̂_GLS) = DΩD' ≥ 0 because DX = 0 kills the cross
terms. GLS-vs-OLS+robust-SE tradeoff: both consistent, GLS more efficient when Ω is well
modelled, OLS+sandwich safer when it is not; modern default is OLS+robust, with RE as
an important FGLS exception where the structure is model-implied.

**Cross-references to other books** (link only, material already exists):

- `endogeneity.qmd` → LATE treatment in `causal_econometrics_guide/iv-rdd.qmd`
- `panel-data.qmd` → CRE treatment in `blog_book/correlated-random-effect.qmd`
- `discrete.qmd` → AME treatment in `blog_book/marginal-effects-fe.qmd`

**Preface rewritten.** Replaced the personal-background first paragraph with a brief
content overview of the book's chapters.

**Layout.** Right-side table of contents removed (`toc: false`); left chapter sidebar
retained. Content panel width set to 960px.

## Ch. 14 extension (2026-08-14) — chosen weights, rank, and the cost of reweighting

Four new subsections at the end of Ch. 14's DiD section (§5), inserted before *Implied versus
chosen*, answering whether outcome weighting can be pushed to favour observations satisfying
parallel trends. Chapter grew 417 → 631 lines. New render dep: **`synthdid`**.

**§5.2 *Synthetic difference-in-differences: a rank-one weighting.*** SDID is a weighted TWFE
regression (@eq-outcome-weights-12), so the FWL reading carries through and `τ̂ = Σ ω_it Y_it` with
**ω_it = u_i v_t** (@eq-outcome-weights-13) — an outer product, hence **rank one**. `synthdid`
literally computes `t(c(-omega, 1/N1)) %*% Y %*% c(-lambda, 1/T1)`. Multiplied out
(@eq-outcome-weights-14) it is the 2×2 of @eq-outcome-weights-11 with the control average
reweighted by ω and the pre-period average by λ, keeping the (+,−,−,+) block signs. Verified live: `ω'Y` = synthdid ATT = 2.2054, rank 1, weights sum to zero **on each margin** (stronger than
@eq-omega's single constraint), zero wrong-sign cells (simplex) against the DR-DiD fit's 151, 23 of
40 controls active, effective controls 14.6, effective pre-periods 1.09 with **0.957 on the last
pre-period**. Also re-derived as a weighted `lm` to 8 digits. New two-panel figure of the ω and λ
margins.

**§5.3 *The rank of the weight matrix.*** rank(Ω) = number of treated cohorts, verified 1–5.
Proof, not just simulation: staggered W = Σ_k c_k s_k' is a sum of K rank-one blocks, and
residualising on unit and time dummies is double centring, which cannot raise rank. This ties the DiD material together — block designs (plain 2×2 *and* SDID) are rank one and differ only in
whether the margins are uniform or fitted; staggered adoption lifts the rank, and only above rank
one can a treated cell enter negatively (in the block case every treated-post cell gets
1/(N₁T₁) > 0). The forbidden comparisons need the extra rank.

**§5.4 *Reweighting controls toward parallel trends.*** The question is ill-posed as asked: parallel trends
is a statement about two group means, not a property an observation has, so there is nothing at the
unit level to weight. It gains a referent only under a model where trends vary by unit (unit slopes
or a factor structure) — and at that point it is what SDID already does (also Hazlett–Xu 2018,
Imai–Kim–Wang 2023, Doudchenko–Imbens 2016). Margin decomposition, 400 reps, truth 2: under
`factor` bias 0.729 (DiD) → 0.173 (unit only) → 0.082 (time only) → **0.044** (both); under
`slopes` 1.083 → 0.603 → 0.536 → **0.403**.

**CORRECTED (2026-08-14, second pass): the surviving `slopes` bias is NOT a hull limit.** The first
draft asserted the treated mean slope lies outside the convex hull of the control slopes. Checked
and false: treated mean slope is 0.12, control slopes are N(0, 0.08²), and over n=40 the max control
slope averages **0.173**, so the treated mean clears every control slope in only **11%** of draws.
The hull usually permits the match. **Third pass replaced the hand-wave with an exact identity**, prompted by xao: "the true dgp is
eq 14.19. we are using synthdid to estimate it? Y(1)−Y(0) should not be a function of s_i t. why the
bother to estimate s_i???" Correct answer: nothing estimates `s_i`. Y(0) is unobserved for treated
post cells, so the estimator imputes it, and only the *difference* between the treated and
weighted-control trends has to vanish. Writing `D[·]` for the double difference of
@eq-outcome-weights-14 and splitting `Y_it(0)`, linearity gives **@eq-slopes-decomp**
`τ̂ − τ = D[α_i] + D[β_t] + D[s_i t] + D[ε_it]`, with the first two identically zero for ANY weights,
and **@eq-slopes-gap** `D[s_i t] = (s̄_trt − Σ ω_i s_i)(t̄_post − Σ λ_t t)`. Verified live at 300 reps:
bias 0.4000 = 0.0000 (levels) + 0.0000 (time path) + 0.3036 (trends) + 0.0964 (shocks), largest gap
across reps 0. `D[s_i t]` equals @eq-slopes-gap per replication to 4e-16. Horizon is **4.39**, not
the "~8" the second pass guessed, so the product is 0.30 not 0.55 — the earlier arithmetic was wrong
twice over (wrong horizon, and it ignored the shock term entirely). **The two mechanisms of §5.4 and
§5.5 are the two non-zero terms of one identity**: the unmatched trend, and regression to the mean
from fitting ω on noisy pre-period outcomes. **Then cut the decomposition entirely.** Trimming its `s_i`-unit rows was not enough — xao: "why is
the whole thing still there. i don't see the point of comparing s_i to an estimated s_i from weighted
obs. again, what's the point?" Correct. **Removed** `@eq-slopes-decomp`, `@eq-slopes-gap`, the
`decomp()` chunk and its table. Reasons: (1) it is not a diagnostic anyone can run on real data,
since it needs the true components; (2) the only two facts it established — unit levels and a common
time path cancel for any weights — are one line of algebra that needs no table; (3) it was redundant
with the noise/shrinkage grid, which makes the same point (bias 0.40 → 0.05 as noise falls) entirely
in ATT bias units and never touches `s_i`. What survives in §5.4: the margin table, the
noise/shrinkage grid, and prose. `panel()` reverted to returning only `Y/N0/N1/T0/T1` — the `a, b, s,
e` components and the dead `s <- NULL` went with the decomposition. Chapter is down to 19 tables and
20 equations; render ~2m20s.

**The lesson is NOT "delete when questioned twice"** (an earlier draft of this note said that; xao
rejected it: "that's not a good lesson. you'll have to have a good argument to keep it. do not change
just because i question. we need to convince each other"). Sizing a change to the size of the
objection is the actual error — the first pass trimmed the `s_i`-unit rows because that was what was
objected to, rather than settling whether the decomposition belonged at all. Decide on the merits
once: material stays if there is an argument for it and goes if there is not, and the count of
questions is irrelevant. When a claim is challenged, either produce the argument for keeping it or
concede on the substance — and say which of the two is happening.

**Report against the ATT, not against true `s_i`.** xao: "comparing to true s_i has no meaning. We
are not estimating s_i. We only need to compare to the true ATT." Cut every quantity in `s_i` units:
the `unmatched slope` and `horizon` rows from the decomposition table, the `unmatched slope` row from
the noise/shrinkage grid (now bias only, so `mismatch()` no longer touches `p$s` at all), and the
whole hull-frequency chunk (the 11% is now stated qualitatively, so no stranded number). What
remains is legitimate because **every term is in the units of the estimate and the four sum to the
bias against the true ATT**. @eq-slopes-gap stays as algebra explaining what governs the trend
term's size — it needs no table. General rule: diagnostic scaffolding in the units of a nuisance
parameter is for debugging, not for the text.

**Name the estimand before the algebra.** xao, after four questions all tracing to the same gap:
"why would we care? we only care about Y(1)−Y(0) for the treated group." The section never said
plainly that `Y(1)−Y(0)` is a difference of two things and only one is observed. Added at the head of
the decomposition: the estimand is `E[Y(1)−Y(0) | treated, post]`; `Y(1)` is data for those cells,
`Y(0)` never is, and **building that counterfactual is the whole estimation problem**, so any bias is
an error in that one imputation. `s_i` matters because the treated group's *own* untreated path
contains `s_i t` — it is not a fact about controls. And @eq-slopes-gap's two factors read as: a
leftover trend means the counterfactual grows at the wrong rate, and the horizon is how long it grows
wrongly before we read it off. **Lesson: in a weighting chapter it is easy to describe machinery for
pages without restating what is being imputed and why. State the estimand first.**

**Fourth pass — "we don't know the DGP, so we use synthdid. But we are not estimating s_i. Where is
the bias from?"** The answer the chapter had only asserted: `synthdid` matches the pre-period
outcome *path*, not slopes. If it matched the systematic part of the path, the slopes would agree as
a by-product and @eq-slopes-gap would be zero; the bias is the amount by which it fails. Two causes,
now demonstrated in a 2×2 grid (300 reps/cell) over AR(1) innovation sd × shrinkage:

| | sd .40 shrink on | sd .05 shrink on | sd .40 shrink off | sd .05 shrink off |
|---|---|---|---|---|
| bias | 0.4000 | 0.0480 | 0.3269 | 0.0183 |
| unmatched slope | 0.0688 | 0.0123 | 0.0428 | 0.0036 |

Cut the noise 8× and the gap goes 0.069 → 0.012, bias 0.40 → 0.05; turn shrinkage off too and 0.004 /
0.02. So the residual trend is **not** a limit of the design — it is what fitting ω on a short noisy
pre-period leaves behind. Given a clean pre-period the weights find the slope match without ever
estimating a slope. This grid REPLACED the shrinkage-only table (which had reported effective
controls 23.1 → 5.2); rep count set to 300 so its default cell reproduces the decomposition table's
0.4000 / 0.0688 exactly — two tables showing the same quantity must use the same reps. Hull frequency
moved to its own one-line chunk in the paragraph that cites it: **0.112**, about one draw in nine. **Gotcha found doing this:** `synthdid_estimate(..., zeta.omega =
NULL)` errors ("non-conformable arrays") — omit the argument to get the default. Also `panel()` now
returns `s` so the diagnostic reuses the same panels instead of re-deriving them from the seed.

**§5.5 *What reweighting costs.*** Weights fitted on pre-period outcomes make τ̂ non-linear in
Y (so @eq-outcome-weights-13 describes the estimate at the fitted weights, and inference needs
`vcov`'s bootstrap/jackknife/placebo, not fixed ω) and constitute a pretest (Roth 2022). Bias
anatomy: `Cov(w, ε̄_pre)(1 − β)`. Simulation where **parallel trends holds** and the groups differ
only by a persistent level gap of 1.5, AR(1) scaled to hold marginal sd at 0.5 for every ρ (so ρ
varies persistence alone): matching 10 controls on **one** pre-period gives bias 0.0271 → −0.0067
falling monotonically in ρ (**reproduces Daw–Hatfield 2018**); matching on the **8-period mean** is
hump-shaped, 0.0336 → 0.0810 at ρ=0.8. Both follow from the anatomy — one period holds
Var(ε_pre) flat so bias tracks (1−β); averaging makes Var(ε̄_pre) climb, so the factors fight.
Averaging more pre-periods relocates the worst case rather than removing it. Sign is always
upward (treated sit above, matched controls' shock reverts, control change understated). At ρ=0.8
SDID carries −0.010 vs the 8-period matcher's 0.073, because `omega.intercept = TRUE` means SDID
matches *trajectories up to a constant*, never levels — matching on levels is what produces it
(Chabé-Ferret 2015, 2017). Closing asymmetry: reweighting controls preserves the estimand and
costs variance; downweighting **treated** units silently moves the estimand.

**§5.6 revised.** The old flat caution ("no weighting of observed outcomes can test parallel
trends") is kept but qualified: chosen weights buy robustness to a *class* of violations expressible
in a posited trend model, the gain is partial because the weights are fitted on a noisy pre-period
path and shrunk toward uniform, and it is paid for in pretest and regression-to-the-mean terms. The alternative to reweighting is bounding the violation
(Rambachan–Roth 2023). Summary items 7–9 added.

**References.** Added Arkhangelsky et al. (2021), Chabé-Ferret (2015, 2017), Daw–Hatfield (2018),
Doudchenko–Imbens (2016), Hazlett–Xu (2018), Imai–Kim–Wang (2023), Rambachan–Roth (2023),
Roth (2022) — plus four the chapter had been citing with **no bibliography entry**: Sant'Anna–Zhao
(2020), Borusyak–Jaravel–Spiess (2024), Callaway–Sant'Anna (2021), Sun–Abraham (2021). All
verified against the published record. `synthdid` and `DRDID` added to the software list.

**Presentation fixes (same session).** The first draft dumped ten unexplained statistics into one
`vtab`. Split into three tables, each with a sentence saying what it checks: (1) the three routes
to τ̂ plus their largest gap, which prints as `0.000000`; (2) a `found` / `should be` table for the
three constraints the outer-product form implies; (3) the sparsity read-out with denominators in
the row labels. Note `vtab`'s kable shows 7 significant digits, so an 8-decimal claim in prose is
not supported by the display — report the gap instead. The bias formula is now
**@eq-outcome-weights-15** rather than prose only.

**Gotcha: the `eq-outcome-weights-N` labels are NOT the rendered numbers, and the offset moves.**
The numeric suffixes skip (no `-3`) and four equations carry word labels (`eq-omega`, `-ml`,
`-plr-i`, `eq-vwate`), so label `-12` does not render as 14.12 — and every equation added earlier in
the chapter shifts the offset again. A first draft hardcoded "(eq. 14.13)" into a kable row label
and was wrong by three. **Never write an equation number as literal text anywhere**, including table
row labels and column names where `@eq-` cannot go — describe the row in words instead. Prefer
descriptive labels for new equations (`{#eq-factor-dgp}`, `{#eq-slopes-dgp}`) over the numeric
series. To read the current numbers: `grep -o '\\\\tag{[0-9.]*}' _book/outcome-weights.html`. Added to `style.css`: computed tables get
`width: auto` under `.cell-output-display table.table`, since Bootstrap's `.table { width: 100% }`
pushed a two-column label/value pair to opposite edges of the 960px column. Prose tables unaffected.

**Code folded, click to show.** Added to ch.14's YAML front matter (chapter-scoped, not book-wide):
`code-fold: true` + `code-summary: "Show code"`. Collapsed by default; output, tables and figures stay
visible. To apply book-wide, move the two keys under `format: html:` in `_quarto.yml`.

*Note on the fold count:* 19 code cells produce **24** `<details>` blocks, and nothing is stale. Five
chunks print something part-way through, so knitr emits source–output–source for them, and `code-fold`
gives each source fragment its own "Show code" toggle. Those five chunks therefore show two toggles
with output between. Acceptable, but if it ever looks fragmented the fix is to move the interleaved
`vtab`/`mtab` call to the end of the chunk so there is a single source block.

**Effective sample size was undefined.** xao: "What's effective controls?" The term appeared only in a
`sprintf` row label with the formula and was never explained. Now defined in prose before the table:
`1/Σωᵢ²` for weights summing to one, equal to N₀ under equal weighting and 1 when one control carries
everything (the inverse Herfindahl index), and read as "a weighted average with effective size m is
about as precise as an unweighted average of m observations". It appears nowhere else in the book, so
this was its first use.

**No `§N` cross-references.** xao: "can you not use §1 this kind of thing?" All seven removed from
ch.14 (five predated this session). Replacements: an equation crossref where the target is an
equation (`the other constraint from @eq-omega`, `the FWL reading of @eq-omega`), otherwise a
descriptive phrase that carries the connection without a pointer ("the same sign flip seen earlier
under thin overlap", "in the cross-sectional case earlier", "the same overlap problem, now in the
design"). Several needed nothing at all — "the §3 signature of a comparison reaching off common
support" says the same thing with `§3` deleted. No other chapter in the book used them.

**Motivate the DGP terms, not just state them.** xao: "why we include a time trend term at all?"
The lead-in listed α_i, β_t, ε_it, s_i·t without saying what each is for. Now separated: α_i and β_t
are in any panel and a DiD removes them exactly (D[α]=D[β]=0 above), so they cost nothing; a term
that varies by unit AND moves with t is *required*, because that is what a parallel-trends violation
is — without one, plain DiD is unbiased and the section has nothing to study. Also added that `s_i·t`
is itself a one-factor model (loading `s_i`, factor `g_t = t`), the simplest member of the
@eq-factor-dgp class SDID targets, so it is a leading case not an exotic one. Plus an honest caveat:
if you believe trends really are unit-specific and linear, the direct fix is unit-specific trends in
the regression, not reweighting; the linear panel is used because it makes @eq-slopes-decomp
checkable.

**The false hull claim survived in a SECOND location** and was only caught on the third pass — the
simulation lead-in still said the treated mean slope "puts it outside the range the control slopes
span". Lesson: after retracting a claim, grep the whole chapter for every restatement of it, not just
the paragraph that prompted the correction.

*Not put in the chapter (mechanism unestablished):* at a matched treated-control loading gap of 0.8
control-sd, `factor` bias is 0.037 but `slopes` is 0.212 (250 reps), so `slopes` is harder by form and
not only by magnitude. Plausibly because a pure linear pre-period path makes the loading hard to pin
down against AR(1) noise, but not verified — do not assert it.

**Write the DGP as an equation, not just its distributions.** The `slopes` panel was described only
as "each unit gets its own linear trend, sd 0.08, shifted 0.12 for the treated" — xao: "what are the
slopes here? I don't see it in the model." Both generating models are now displayed:
`@eq-factor-dgp` for `Y_it(0) = α_i + β_t + f_i'g_t + ε_it` and `@eq-slopes-dgp` for
`Y_it(0) = α_i + β_t + s_i·t + ε_it`, `s_i ~ N(0, 0.08²)`. Naming a DGP variant in prose is not the
same as writing the model. Writing it out is also what exposed the false hull claim above — once
`s_i` was on the page its distribution could be checked against the treated shift.

**Every chunk needs a lead-in.** Flagged twice: the figure chunk and two output chunks appeared with
no sentence saying what they plot or compute. Now each of the nine chunks in the new material is
preceded by prose stating what it does and what to look for — this applies to figures and plain
output tables, not only to `**Simulation —**` blocks.

**Define a term at first use.** "Rank one" appeared in the §5.2 heading, a table label, and prose
before being defined 50 lines later in §5.3. Definition moved to first use, right after
@eq-outcome-weights-13 (every row a multiple of every other, so *who* cannot interact with *when*),
and the duplicate in §5.3 cut. Also dropped bare "in the sense of §3" / "in the sense of §1"
back-references where the sentence then explains itself anyway — say the thing, don't send the
reader hunting.

**Prose rewritten to xao's voice** after review. Cut: "buy parallel trends", "worth pausing on",
"one spine", "anatomy", "escapes", "runs the other way", "lucky draw", "the very constraint",
forced antithesis throughout. Headings renamed §5.4 to *Reweighting controls toward parallel
trends* and §5.5 to *What reweighting costs*. Also fixed a directional reference the new ordering
broke: from §5.3 "the staggered case of the last section" pointed at §5.2, not §5.1.

Every cited number verified against live rendered output. Chunks run ~70s total.
