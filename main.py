"""
main.py - Entry point.

Runs the full analysis suite against the synthetic datasets:
  1. A/B test significance test (two-proportion z-test) on the signup funnel
  2. Power analysis: required sample size and minimum detectable effect
  3. Funnel breakdown by variant
  4. User segmentation (K-Means) with segment profiles
  5. Difference-in-differences causal estimate on the regional rollout

Run with:  python main.py
"""
import json
from pathlib import Path

import pandas as pd

from analysis.ab_test import two_proportion_ztest
from analysis.power import required_sample_size_per_arm, minimum_detectable_effect
from analysis.funnel import funnel_by_variant
from analysis.segmentation import segment_users, segment_profile
from analysis.diff_in_diff import estimate_diff_in_diff

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"


def run():
    OUTPUT_DIR.mkdir(exist_ok=True)
    report = {}

    # --- 1 & 2. A/B test + power analysis -----------------------------------
    ab_df = pd.read_csv(DATA_DIR / "ab_test_data.csv")
    control = ab_df[ab_df["variant"] == "control"]
    treatment = ab_df[ab_df["variant"] == "treatment"]

    ab_result = two_proportion_ztest(
        n_control=len(control), conversions_control=int(control["converted"].sum()),
        n_treatment=len(treatment), conversions_treatment=int(treatment["converted"].sum()),
    )
    report["ab_test"] = ab_result.__dict__

    required_n = required_sample_size_per_arm(baseline_rate=ab_result.rate_control, minimum_detectable_lift=0.02)
    mde = minimum_detectable_effect(baseline_rate=ab_result.rate_control, n_per_arm=ab_result.n_control)
    report["power_analysis"] = {
        "required_n_per_arm_for_2pp_lift": required_n,
        "minimum_detectable_effect_at_current_n": mde,
    }

    # --- 3. Funnel by variant ------------------------------------------------
    funnel = funnel_by_variant(ab_df)
    funnel.to_csv(OUTPUT_DIR / "funnel_by_variant.csv", index=False)
    report["funnel_by_variant"] = funnel.to_dict(orient="records")

    # --- 4. Segmentation -------------------------------------------------------
    segmented = segment_users(ab_df, n_segments=3)
    profile = segment_profile(segmented)
    profile.to_csv(OUTPUT_DIR / "segment_profile.csv", index=False)
    report["segment_profile"] = profile.to_dict(orient="records")

    # --- 5. Difference-in-differences ----------------------------------------
    did_df = pd.read_csv(DATA_DIR / "diff_in_diff_data.csv")
    did_result = estimate_diff_in_diff(did_df)
    report["diff_in_diff"] = did_result.__dict__

    # --- Write full report -----------------------------------------------------
    with open(OUTPUT_DIR / "analysis_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)

    return report


if __name__ == "__main__":
    result = run()

    print("\n=== A/B TEST RESULT ===")
    for k, v in result["ab_test"].items():
        print(f"  {k}: {v}")

    print("\n=== POWER ANALYSIS ===")
    for k, v in result["power_analysis"].items():
        print(f"  {k}: {v}")

    print("\n=== DIFFERENCE-IN-DIFFERENCES (causal estimate) ===")
    for k, v in result["diff_in_diff"].items():
        print(f"  {k}: {v}")

    print("\n=== SEGMENT PROFILE ===")
    for row in result["segment_profile"]:
        print(f"  {row}")

    print("\nFull report written to output/analysis_report.json")
