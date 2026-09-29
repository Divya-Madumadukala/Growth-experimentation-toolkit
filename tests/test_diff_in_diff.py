import pandas as pd

from analysis.diff_in_diff import estimate_diff_in_diff


def _deterministic_did_data(true_effect: float):
    """
    Builds a near-noise-free DiD dataset with a known, exact treatment
    effect, so the estimator's output can be checked against ground truth.

    Both regions share a baseline of 50 and a +3 common time trend after
    'launch'; only the treated region gets an additional bump in the post
    period, sized at exactly `true_effect`.
    """
    rows = []
    for region, treated in [("West", 1), ("East", 0)]:
        for period, post in [("pre", 0), ("post", 1)]:
            for i in range(20):
                # tiny deterministic jitter avoids a perfectly-fit (zero-residual)
                # model, which would make the standard error undefined
                jitter = 0.01 * (i - 10)
                value = 50 + (3 if post else 0) + (true_effect if (treated and post) else 0) + jitter
                rows.append({"region": region, "period": period, "treated": treated,
                             "post": post, "metric_value": value})
    return pd.DataFrame(rows)


def test_recovers_the_true_effect_with_no_noise():
    df = _deterministic_did_data(true_effect=5.0)
    result = estimate_diff_in_diff(df)
    assert abs(result.did_estimate - 5.0) < 0.001


def test_zero_effect_is_not_significant():
    df = _deterministic_did_data(true_effect=0.0)
    result = estimate_diff_in_diff(df)
    assert abs(result.did_estimate) < 0.001
    assert bool(result.significant_at_95) is False
