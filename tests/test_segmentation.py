import pandas as pd

from analysis.segmentation import segment_users, segment_profile


def _two_obviously_different_groups():
    rows = []
    # Low-engagement group: few sessions, short visits, few pages
    for i in range(30):
        rows.append({"user_id": f"L{i}", "sessions": 1, "avg_session_length_sec": 30,
                     "pages_viewed": 1, "converted": 0})
    # High-engagement group: many sessions, long visits, many pages
    for i in range(30):
        rows.append({"user_id": f"H{i}", "sessions": 10, "avg_session_length_sec": 300,
                     "pages_viewed": 18, "converted": 1})
    return pd.DataFrame(rows)


def test_segmentation_separates_distinct_behavior_groups():
    df = _two_obviously_different_groups()
    segmented = segment_users(df, n_segments=2)
    profile = segment_profile(segmented)

    assert len(profile) == 2
    # the two segments' average pages_viewed should be clearly different
    pages_by_segment = sorted(profile["avg_pages_viewed"].tolist())
    assert pages_by_segment[1] - pages_by_segment[0] > 10

    # the low-engagement segment should have the lower conversion rate
    low_seg = profile.loc[profile["avg_pages_viewed"].idxmin()]
    high_seg = profile.loc[profile["avg_pages_viewed"].idxmax()]
    assert low_seg["conversion_rate"] < high_seg["conversion_rate"]
