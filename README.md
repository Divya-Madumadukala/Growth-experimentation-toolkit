# Growth Experimentation Toolkit

A small, self-contained Python toolkit covering the core statistical methods
behind growth/product data science: A/B test significance testing, power
analysis, funnel breakdowns, user segmentation, and causal inference via
difference-in-differences for non-randomized rollouts.

**All data in this project is synthetic** (randomly generated with known,
built-in effects so the methods can be validated against ground truth). No
real user data is used anywhere.

## Why this project

Built to develop real, hands-on experience with the experimentation and
causal inference methods used in growth/product data science roles —
complementing a SQL/BI-heavy analytics background with statistically rigorous
A/B testing, power analysis, and quasi-experimental causal inference.

## What's inside

| Module | What it does |
|---|---|
| `analysis/ab_test.py` | Two-proportion z-test for a binary conversion metric, with lift and a 95% confidence interval |
| `analysis/power.py` | Required sample size for a target minimum detectable effect, and the reverse: minimum detectable effect at a given sample size |
| `analysis/funnel.py` | Conversion/engagement funnel broken out by A/B variant |
| `analysis/segmentation.py` | K-Means behavioral segmentation with interpretable segment profiles |
| `analysis/diff_in_diff.py` | Difference-in-differences causal estimate (OLS with a treated × post interaction term) for a non-randomized regional rollout |

## The two synthetic scenarios

1. **A/B test** — a signup funnel experiment (control vs. treatment) with a
   known, built-in 2-percentage-point lift, so the z-test's output can be
   checked against the true effect.
2. **Difference-in-differences** — a quasi-experiment: a product change
   launched in one region but not another (no random assignment), observed
   before and after. DiD is the standard method for estimating a causal
   effect in exactly this kind of real-world, non-randomized scenario.

## Running it

```bash
pip install -r requirements.txt
python generate_data.py   # writes data/ab_test_data.csv, data/diff_in_diff_data.csv
python main.py             # runs the full analysis suite
pytest                      # runs the unit tests
```

Results land in `output/` (per-analysis CSVs plus a combined
`analysis_report.json`) — git-ignored since they're generated, not source.

## Testing philosophy

Rather than just checking "does the code run," the tests validate
**statistical correctness against known ground truth**: the A/B test
correctly detects a real effect and correctly does *not* flag a false
positive when there's no true difference; the DiD estimator recovers the
exact built-in causal effect on noise-free synthetic data; segmentation
correctly separates two obviously distinct behavioral groups. This is the
same kind of validation you'd want before trusting these methods on real
experiment data.

## Possible next steps

- Add sequential testing / always-valid p-values for peeking-safe monitoring
- Extend segmentation with a supervised propensity model for heterogeneous
  treatment effect estimation (who responds most to the treatment)
- Add a Bayesian A/B testing option alongside the frequentist z-test
