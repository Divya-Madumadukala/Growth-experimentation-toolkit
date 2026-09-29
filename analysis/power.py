"""
power.py

Sample size / minimum detectable effect (MDE) calculations - the "how big
does this experiment need to be" question that has to be answered *before*
launching an A/B test, not after. Uses statsmodels' power analysis for a
two-proportion z-test.
"""
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def required_sample_size_per_arm(baseline_rate: float, minimum_detectable_lift: float,
                                  alpha: float = 0.05, power: float = 0.8) -> int:
    """
    How many users per arm are needed to reliably detect a given absolute
    lift over a baseline conversion rate, at the given significance level
    and statistical power.
    """
    effect_size = proportion_effectsize(baseline_rate, baseline_rate + minimum_detectable_lift)
    analysis = NormalIndPower()
    n = analysis.solve_power(effect_size=effect_size, alpha=alpha, power=power, ratio=1.0)
    return int(round(n))


def minimum_detectable_effect(baseline_rate: float, n_per_arm: int,
                               alpha: float = 0.05, power: float = 0.8) -> float:
    """
    The inverse question: given a fixed sample size per arm, what's the
    smallest true lift this experiment has enough power to reliably detect?
    Solved by searching over candidate effect sizes.
    """
    analysis = NormalIndPower()
    low, high = 0.0001, 0.5
    for _ in range(60):  # binary search on the lift magnitude
        mid = (low + high) / 2
        effect_size = proportion_effectsize(baseline_rate, baseline_rate + mid)
        achieved_power = analysis.power(effect_size=effect_size, nobs1=n_per_arm, alpha=alpha, ratio=1.0)
        if achieved_power < power:
            low = mid
        else:
            high = mid
    return round(high, 4)
