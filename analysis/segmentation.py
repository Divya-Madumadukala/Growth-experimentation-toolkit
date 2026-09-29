"""
segmentation.py

Simple behavioral user segmentation via K-Means clustering on engagement
features (sessions, session length, pages viewed) - the kind of
segmentation used to identify which audiences respond differently to a
treatment, or to target growth efforts (opportunity sizing by segment).
"""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


FEATURES = ["sessions", "avg_session_length_sec", "pages_viewed"]


def segment_users(df: pd.DataFrame, n_segments: int = 3, random_state: int = 42) -> pd.DataFrame:
    """
    Returns the input dataframe with an added 'segment' column, plus a
    separate segment-profile summary (mean feature values and conversion
    rate per segment) to make each cluster interpretable.
    """
    X = df[FEATURES]
    X_scaled = StandardScaler().fit_transform(X)

    kmeans = KMeans(n_clusters=n_segments, random_state=random_state, n_init=10)
    df = df.copy()
    df["segment"] = kmeans.fit_predict(X_scaled)
    return df


def segment_profile(df_with_segments: pd.DataFrame) -> pd.DataFrame:
    profile = df_with_segments.groupby("segment").agg(
        users=("user_id", "count"),
        avg_sessions=("sessions", "mean"),
        avg_session_length_sec=("avg_session_length_sec", "mean"),
        avg_pages_viewed=("pages_viewed", "mean"),
        conversion_rate=("converted", "mean"),
    ).round(2).reset_index()
    return profile
