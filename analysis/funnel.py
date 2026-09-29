"""
funnel.py

Funnel analysis: conversion and drop-off rates at each stage, computed
overall and broken out by A/B variant - the kind of "where are we losing
people, and did the treatment change that" analysis behind most growth
data science work.
"""
import pandas as pd


def funnel_by_variant(df: pd.DataFrame) -> pd.DataFrame:
    """
    Given user-level data with a 'converted' column and a 'variant' column,
    returns conversion rate per variant plus a simple engagement funnel
    (sessions >= 1 -> pages_viewed >= 5 -> converted).
    """
    df = df.copy()
    df["reached_step_1_visited"] = 1  # everyone in the dataset visited
    df["reached_step_2_engaged"] = (df["pages_viewed"] >= 5).astype(int)
    df["reached_step_3_converted"] = df["converted"]

    summary = df.groupby("variant").agg(
        users=("user_id", "count"),
        engaged=("reached_step_2_engaged", "sum"),
        converted=("reached_step_3_converted", "sum"),
    ).reset_index()

    summary["engagement_rate"] = (summary["engaged"] / summary["users"]).round(4)
    summary["conversion_rate"] = (summary["converted"] / summary["users"]).round(4)
    summary["engaged_to_converted_rate"] = (summary["converted"] / summary["engaged"]).round(4)

    return summary
