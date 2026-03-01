import pandas as pd
from typing import Optional


def run_analysis(df: pd.DataFrame, metric: str, groupby: Optional[str], date_col: Optional[str],
                 intent: str, agg: str) -> pd.DataFrame:
    """Perform aggregation based on intent and selections.

    intent influences grouping/time behavior.
    """
    if intent == "trend":
        if date_col is None:
            raise ValueError("Trend intent requires a date column")
        # convert
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.dropna(subset=[date_col])
        df["_period"] = df[date_col].dt.to_period("M").dt.to_timestamp()
        if agg == "count":
            res = df.groupby("_period").size().reset_index(name="count")
        else:
            res = df.groupby("_period")[metric].agg(agg).reset_index()
            res.columns = ["date", metric]
        return res
    else:
        if groupby is None:
            raise ValueError(f"Intent {intent} requires a groupby/dimension column")
        if agg == "count":
            res = df.groupby(groupby).size().reset_index(name="count")
        else:
            res = df.groupby(groupby)[metric].agg(agg).reset_index()
        return res
