from analysis.ab_test import two_proportion_ztest


def test_detects_a_real_effect():
    """A clear, large lift with a decent sample size should be significant."""
    result = two_proportion_ztest(
        n_control=5000, conversions_control=900,      # 18.0%
        n_treatment=5000, conversions_treatment=1050,  # 21.0%
    )
    assert bool(result.significant_at_95) is True
    assert result.p_value < 0.05
    assert result.absolute_lift > 0
    assert round(result.rate_control, 3) == 0.18
    assert round(result.rate_treatment, 3) == 0.21


def test_identical_rates_are_not_significant():
    """No true difference between arms should not produce a false positive."""
    result = two_proportion_ztest(
        n_control=2000, conversions_control=360,     # 18.0%
        n_treatment=2000, conversions_treatment=360,  # 18.0%
    )
    assert bool(result.significant_at_95) is False
    assert result.p_value == 1.0
    assert result.absolute_lift == 0.0


def test_confidence_interval_brackets_the_true_lift():
    result = two_proportion_ztest(
        n_control=5000, conversions_control=900,
        n_treatment=5000, conversions_treatment=1050,
    )
    assert result.ci_95_low < result.absolute_lift < result.ci_95_high
