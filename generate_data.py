"""
generate_data.py

Generates two SYNTHETIC datasets used across this project:

1. ab_test_data.csv — user-level A/B test data for a signup-funnel experiment
   (control vs. treatment), with a real, known treatment effect baked in so
   the statistical tests can be validated against ground truth.

2. diff_in_diff_data.csv — a quasi-experiment: a product change was rolled
   out in one region but not another (no random assignment), observed
   before and after launch. Used to demonstrate difference-in-differences,
   a causal inference method for exactly this kind of non-randomized
   real-world scenario.

All data is synthetic - randomly generated for demonstration only.
"""
import csv
import random
from pathlib import Path

random.seed(7)

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

CHANNELS = ["organic", "paid_search", "email", "referral"]

# ---------------------------------------------------------------------------
# 1. A/B test: signup funnel experiment
# ---------------------------------------------------------------------------
N_PER_ARM = 4000
CONTROL_CONVERSION_RATE = 0.18     # baseline signup completion rate
TRUE_LIFT = 0.02                   # true absolute lift from the treatment (2pp)


def generate_ab_test_data():
    rows = []
    user_id = 1
    for variant, rate in [("control", CONTROL_CONVERSION_RATE),
                           ("treatment", CONTROL_CONVERSION_RATE + TRUE_LIFT)]:
        for _ in range(N_PER_ARM):
            converted = 1 if random.random() < rate else 0
            rows.append({
                "user_id": f"U{user_id:06d}",
                "variant": variant,
                "channel": random.choice(CHANNELS),
                "sessions": random.randint(1, 12),
                "avg_session_length_sec": round(random.gauss(180, 60), 1),
                "pages_viewed": random.randint(1, 20),
                "converted": converted,
            })
            user_id += 1

    path = DATA_DIR / "ab_test_data.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return rows, path


# ---------------------------------------------------------------------------
# 2. Difference-in-differences: non-randomized regional rollout
# ---------------------------------------------------------------------------
TRUE_DID_EFFECT = 5.0  # true causal effect of the launch, in metric units


def generate_diff_in_diff_data():
    """
    Two regions, two periods (pre/post launch). Region 'West' gets the
    product change at the start of the post period; 'East' does not
    (control). Both regions share a common time trend, but only West gets
    the additional treatment bump after launch - the classic DiD setup.
    """
    rows = []
    day_id = 1
    for region, treated in [("West", 1), ("East", 0)]:
        for period, is_post in [("pre", 0), ("post", 1)]:
            for _ in range(60):  # 60 daily observations per region/period
                base = 50 + random.gauss(0, 4)      # shared baseline noise
                time_trend = 3 if is_post else 0    # common trend both regions experience
                treatment_effect = TRUE_DID_EFFECT if (treated and is_post) else 0
                metric_value = base + time_trend + treatment_effect
                rows.append({
                    "day_id": day_id,
                    "region": region,
                    "period": period,
                    "treated": treated,
                    "post": is_post,
                    "metric_value": round(metric_value, 2),
                })
                day_id += 1

    path = DATA_DIR / "diff_in_diff_data.csv"
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    return rows, path


if __name__ == "__main__":
    ab_rows, ab_path = generate_ab_test_data()
    did_rows, did_path = generate_diff_in_diff_data()
    print(f"Generated {len(ab_rows)} A/B test rows -> {ab_path}")
    print(f"Generated {len(did_rows)} diff-in-diff rows -> {did_path}")
