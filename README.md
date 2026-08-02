# Econometrics Guide

A public econometrics study guide by Xiang Ao (Research Computing Services, Harvard Business School), built as a [Quarto book](https://quarto.org/docs/books/) and deployed at <https://xiangao.github.io/econometrics-guide/>.

## Topics

| Part | Chapters |
|------|----------|
| **Foundations** | OLS, Maximum Likelihood, GLS |
| **Causal Inference & IV** | Endogeneity & Instrumental Variables, GMM |
| **Limited Dependent Variables** | Censored/Truncated/Selection Models, Discrete Choice, Count Data |
| **Advanced Topics** | Panel Data, Survival Models, Dynamic Panels, Missing Data, Interpreting OLS |

## Prerequisites

- [Quarto](https://quarto.org/docs/get-started/) (>= 1.3)
- R with packages: `car`, `stats4`, `dplyr`, `mvtnorm`, `MASS`, `AER`, `ivreg`, `gmm`, `strucchange`, `ggfortify`, `survival`, `fixest`

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

> **2026-07-30:** Fresh sweep of all 12 substantive chapters (report in `../_review3/review_20260730.md`). Four real corrections: the exogeneity hierarchy in `ols` was inverted (contemporaneous exogeneity is the *weakest* of strict/predetermined/contemporaneous, not stronger than predeterminedness — predeterminedness implies it by iterated expectations); `discrete` claimed that choice-varying regressors with choice-specific coefficients are not separately identified, which is false (verified by simulation — MLE recovers all coefficients with a non-singular information matrix, and it is what Stata's `asclogit` fits); a comment in `mle` claimed OLS starting values the code did not use; and a dead external link in `count-data` was removed. Eight smaller items: the ordered-probit location and scale normalizations, the asymptotic-variance scaling and regularity qualifier in the MLE efficiency claim, GMM's optimal weighting matrix and asymptotic variance (previously absent) plus a notation clash between the weighting matrix and the instrument, a rewrite of the IV geometry passage around an orthogonal decomposition that actually supports its similar-triangles argument, an AFT-vs-PH sign-convention warning for `survreg` beside `coxph`, the missing residual draw in the multiple-imputation recipe, and a time-invariance example. Rendered clean.

> **2026-07-30 (deep read):** Full-depth pass over all 12 chapters; log at
> `../_review3/deepread_econometrics_guide.md`. **No mathematical errors found** —
> every likelihood, variance formula and asymptotic result re-derived correctly, and
> the Nickell bias was additionally confirmed by simulation across six (T, gamma)
> pairs. The corrections were precision and completeness ones: the exogeneity ladder
> in `ols` listed zero-covariance and mean-independence in an order that implied the
> wrong ranking; `censored`'s "Switching Regression" section presents a constant-effect
> treatment model rather than the Roy model it names; `gls` attributed a single
> transformation to both Cochrane-Orcutt and Prais-Winsten, which differ precisely in
> the first observation; `gmm`'s example coincides with 2SLS only because it is
> just-identified; and `mle` — the book's inference chapter — developed the information
> matrix and efficiency bound without ever presenting the LR, Wald and LM tests, which
> are now included.

> **2026-08-01:** New section in `panel-data`, "Collapse to unit means, or keep the
> long format?" It settles a question the chapter raised but never answered: with a
> balanced panel and only time-invariant regressors, pooled OLS on the `NT` rows and
> OLS on the `N` unit means give *identical* coefficients (Wooldridge 2010, §20.3.4),
> and the real error is reporting `NT − k` degrees of freedom instead of `N − k`
> (Moulton 1990; Donald and Lang 2007). Adding a time-varying regressor breaks the
> equivalence for *every* coefficient, not just its own, because collapsing leaves the
> between estimator while pooled OLS returns a variance-weighted mix of within and
> between — the FE-vs-RE comparison in different clothes. Mundlak's device reconciles
> the two, tying the section back to the regression-based Hausman test above it.
> A second section, "What the long format buys," demonstrates it with `fixest` on
> simulated data (the chapter's first code): the balanced case agrees to twelve digits,
> the unbalanced case does not, and with `c_i` correlated with `x̄_i` the collapsed
> regression returns 1.845 against a truth of 1 while the within estimator returns
> 0.995. Mundlak's regression reproduces the within estimate and returns the
> between-minus-within contrast as the coefficient on `x̄_i`.

> **2026-08-02:** Split the OLS-weighting material out of `panel-data` into a new final
> chapter, **Interpreting OLS**. It was roughly half of the panel chapter and almost
> none of it is panel-specific: the FWL weighting rule, the outcome-versus-effect
> representations, Angrist's variance weighting, Słoczyński's ATT/ATU split and the
> within/between decomposition all apply to a plain cross-section. `panel-data` keeps
> the collapse-versus-long-format material and links forward. The new chapter also adds
> the point-to-centroid slope `s_i` and the warning not to read it as the structural
> `b_i` — their correlation is 0.019 and `s_i` has 235 times the spread, yet their
> weighted averages agree, which is the whole reason the decomposition is about the
> weights rather than either slope.
