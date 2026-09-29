"""
ab_test.py

Two-proportion z-test for a binary conversion metric (e.g., signup
completion), the standard way to evaluate a randomized A/B test on a
conversion rate. Also computes absolute/relative lift and a 95% confidence
interval on the difference in proportions.
"""
from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass
class ABTestResult:
    n_control: int
    n_treatment: int
    conversions_control: int
    conversions_treatment: int
    rate_control: float
    rate_treatment: float
    absolute_lift: float
    relative_lift_pct: float
    z_statistic: float
    p_value: float
    ci_95_low: float
    ci_95_high: float
    significant_at_95: bool


def two_proportion_ztest(n_control: int, conversions_control: int,
                          n_treatment: int, conversions_treatment: int) -> ABTestResult:
    p1 = conversions_control / n_control
    p2 = conversions_treatment / n_treatment

    # Pooled proportion for the z-test under the null hypothesis (no difference)
    p_pool = (conversions_control + conversions_treatment) / (n_control + n_treatment)
    se_pool = np.sqrt(p_pool * (1 - p_pool) * (1 / n_control + 1 / n_treatment))

    z = (p2 - p1) / se_pool if se_pool > 0 else 0.0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))  # two-tailed

    # Unpooled standard error for the confidence interval on the difference
    se_diff = np.sqrt(p1 * (1 - p1) / n_control + p2 * (1 - p2) / n_treatment)
    diff = p2 - p1
    ci_low = diff - 1.96 * se_diff
    ci_high = diff + 1.96 * se_diff

    return ABTestResult(
        n_control=n_control,
        n_treatment=n_treatment,
        conversions_control=conversions_control,
        conversions_treatment=conversions_treatment,
        rate_control=round(p1, 4),
        rate_treatment=round(p2, 4),
        absolute_lift=round(diff, 4),
        relative_lift_pct=round((diff / p1) * 100, 2) if p1 > 0 else 0.0,
        z_statistic=round(z, 3),
        p_value=round(p_value, 5),
        ci_95_low=round(ci_low, 4),
        ci_95_high=round(ci_high, 4),
        significant_at_95=p_value < 0.05,
    )
