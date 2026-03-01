import plotly.express as px
import pandas as pd
from typing import Optional
from plotly.graph_objects import Figure


def make_chart(df: pd.DataFrame, intent: str, metric: str, groupby: Optional[str], date_col: Optional[str]) -> Optional[Figure]:
    if df is None or df.empty:
        return None
    if intent == "trend":
        # line chart
        return px.line(df, x="date", y=metric, markers=True)
    if intent == "top":
        # bar sorted
        ycol = "count" if metric == "__count__" else metric
        fig = px.bar(df.sort_values(ycol, ascending=False), x=groupby, y=ycol)
        return fig
    if intent == "breakdown":
        ycol = "count" if metric == "__count__" else metric
        if len(df) <= 5:
            return px.pie(df, names=groupby, values=ycol)
        else:
            return px.bar(df, x=groupby, y=ycol)
    if intent == "count":
        ycol = "count" if metric == "__count__" else metric
        return px.bar(df, x=groupby or metric, y=ycol)
    # generic fallback
    try:
        return px.bar(df, x=groupby or df.columns[0], y=metric)
    except Exception:
        return px.scatter(df, x=df.columns[0], y=metric)
