# Econometrics Guide

An internal econometrics reference guide by Research Computing Services at Harvard Business School, built as a [Quarto book](https://quarto.org/docs/books/).

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

## Build

```bash
quarto render     # renders to _book/
quarto preview    # live preview with hot reload
```

## Sources

Materials drawn from Davidson and MacKinnon's *Econometric Theory and Methods*, Chris Baum's *An Introduction to Modern Econometrics Using Stata*, and other sources. Not intended for publication.
