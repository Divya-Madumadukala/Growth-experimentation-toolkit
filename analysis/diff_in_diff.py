"""
diff_in_diff.py

Difference-in-differences (DiD): a causal inference method for estimating
the effect of a change that WASN'T randomly assigned - e.g., a product
change rolled out in one region but not another. Compares the change over
time in the treated group against the change over time in the control
group; the difference between those two differences is the estimated
causal effect, under the "parallel trends" assumption.

Implemented as an OLS regression with a treated x post interaction term -
the standard way to estimate DiD and get a p-value/confidence interval
for the effect in the same step.
"""
from dataclasses import dataclass

import pandas as pd
import statsmodels.formula.api as smf


@dataclass
class DiDResult:
    did_estimate: float
    p_value: float
    ci_95_low: float
    ci_95_high: float
    significant_at_95: bool


def estimate_diff_in_diff(df: pd.DataFrame) -> DiDResult:
    """
    df must have columns: metric_value, treated (0/1), post (0/1).
    The coefficient on the treated:post interaction term is the DiD
    estimate - the causal effect of treatment in the post period.
    """
    model = smf.ols("metric_value ~ treated * post", data=df).fit()
    interaction_term = "treated:post"

    coef = model.params[interaction_term]
    pval = model.pvalues[interaction_term]
    ci = model.conf_int().loc[interaction_term]

    return DiDResult(
        did_estimate=round(coef, 3),
        p_value=round(pval, 5),
        ci_95_low=round(ci[0], 3),
        ci_95_high=round(ci[1], 3),
        significant_at_95=pval < 0.05,
    )
