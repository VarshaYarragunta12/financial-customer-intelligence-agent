import re
from typing import Optional


def parse_query(query: str, columns: dict) -> dict:
    """Given a natural language query and detected columns dict, return plan components.

    columns: dict with keys 'dates','numeric','dims'
    Plan keys: intent, metric, groupby, date_col, agg
    """
    ql = query.lower()
    plan = {"intent": None, "metric": None, "groupby": None, "date_col": None, "agg": None}
    # simple patterns
    if "trend" in ql or "over time" in ql:
        plan["intent"] = "trend"
    elif "top" in ql or "rank" in ql or "highest" in ql:
        plan["intent"] = "top"
    elif "breakdown" in ql or "share" in ql or "contribution" in ql:
        plan["intent"] = "breakdown"
    elif "count" in ql or "volume" in ql:
        plan["intent"] = "count"
    # metric detection: look for numeric column names
    for num in columns.get("numeric", []):
        if num.lower() in ql:
            plan["metric"] = num
            break
    # groupby detection
    for dim in columns.get("dims", []):
        if dim.lower() in ql:
            plan["groupby"] = dim
            break
    # date column detection
    for d in columns.get("dates", []):
        if d.lower() in ql or "date" in ql:
            plan["date_col"] = d
            break
    # aggregation
    if "average" in ql or "avg" in ql or "mean" in ql:
        plan["agg"] = "mean"
    elif "median" in ql:
        plan["agg"] = "median"
    elif "count" in ql:
        plan["agg"] = "count"
    else:
        plan["agg"] = "sum"
    return plan
