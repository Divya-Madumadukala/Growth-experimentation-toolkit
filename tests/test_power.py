from analysis.power import required_sample_size_per_arm, minimum_detectable_effect


def test_required_sample_size_is_positive():
    n = required_sample_size_per_arm(baseline_rate=0.18, minimum_detectable_lift=0.02)
    assert n > 0


def test_smaller_lift_requires_more_sample():
    """Detecting a smaller effect reliably should require a larger sample."""
    n_small_lift = required_sample_size_per_arm(baseline_rate=0.18, minimum_detectable_lift=0.01)
    n_large_lift = required_sample_size_per_arm(baseline_rate=0.18, minimum_detectable_lift=0.05)
    assert n_small_lift > n_large_lift


def test_mde_shrinks_as_sample_grows():
    """With more users per arm, you should be able to detect a smaller effect."""
    mde_small_n = minimum_detectable_effect(baseline_rate=0.18, n_per_arm=1000)
    mde_large_n = minimum_detectable_effect(baseline_rate=0.18, n_per_arm=10000)
    assert mde_large_n < mde_small_n
