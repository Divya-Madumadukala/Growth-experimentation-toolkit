import pandas as pd

from analysis.funnel import funnel_by_variant


def test_conversion_rate_calculation():
    df = pd.DataFrame([
        {"user_id": "U1", "variant": "control", "pages_viewed": 10, "converted": 1},
        {"user_id": "U2", "variant": "control", "pages_viewed": 2, "converted": 0},
        {"user_id": "U3", "variant": "control", "pages_viewed": 1, "converted": 0},
        {"user_id": "U4", "variant": "control", "pages_viewed": 8, "converted": 1},
        {"user_id": "U5", "variant": "treatment", "pages_viewed": 10, "converted": 1},
        {"user_id": "U6", "variant": "treatment", "pages_viewed": 9, "converted": 1},
        {"user_id": "U7", "variant": "treatment", "pages_viewed": 1, "converted": 0},
        {"user_id": "U8", "variant": "treatment", "pages_viewed": 8, "converted": 1},
    ])
    result = funnel_by_variant(df).set_index("variant")

    assert result.loc["control", "conversion_rate"] == 0.5
    assert result.loc["treatment", "conversion_rate"] == 0.75
    # engagement = pages_viewed >= 5
    assert result.loc["control", "engagement_rate"] == 0.5
    assert result.loc["treatment", "engagement_rate"] == 0.75
