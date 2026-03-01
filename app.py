import streamlit as st
import pandas as pd

from src.data_loader import read_csv
from src.schema_detect import detect_columns
from src.nl_parser import parse_query
from src.analysis import run_analysis
from src.charts import make_chart

# Streamlit page config
st.set_page_config(page_title="AI-Powered Financial Customer Intelligence Agent", layout="wide")

st.title("💡 Financial Customer Intelligence Agent")
st.caption("Upload any CSV and get instant insights. Optional OpenAI support.")



# session state defaults
if "df" not in st.session_state:
    st.session_state.df = None
if "schema" not in st.session_state:
    st.session_state.schema = None
if "plan" not in st.session_state:
    st.session_state.plan = None
if "result" not in st.session_state:
    st.session_state.result = None

# utility

AGG_OPTIONS = ["sum", "mean", "median", "count"]
INTENTS = ["top", "breakdown", "count", "trend"]


def reset_state():
    st.session_state.plan = None
    st.session_state.result = None


# --- Upload Section ---
with st.sidebar:
    st.header("Upload data")
    uploaded = st.file_uploader("CSV file", type=["csv"])
    if uploaded:
        try:
            df = read_csv(uploaded)
            st.session_state.df = df
            st.success(f"Loaded {len(df):,} rows × {df.shape[1]} cols")
            st.dataframe(df.head(50))
            # detect schema
            sch = detect_columns(df)
            st.session_state.schema = sch
            reset_state()
            # debug
            with st.expander("Detected columns"):
                st.write(sch)
        except Exception as e:
            st.error(f"Unable to load file: {e}")
            st.session_state.df = None
            st.session_state.schema = None


# Main panel
if st.session_state.df is None:
    st.info("Please upload a CSV on the left.")
else:
    df = st.session_state.df
    sch = st.session_state.schema
    # controls
    st.subheader("Analysis Options")
    col1, col2 = st.columns(2)
    with col1:
        intent = st.selectbox("Intent", INTENTS, index=0, help="Type of analysis")
        metric = st.selectbox("Metric", [None] + sch["numeric"],
                              index=1 if sch["numeric"] else 0, help="Numeric column")
    with col2:
        groupby = st.selectbox("Group by", [None] + sch["dims"],
                               index=1 if sch["dims"] else 0, help="Dimension column")
        date_col = st.selectbox("Date column", [None] + sch["dates"],
                                index=1 if sch["dates"] else 0, help="Only for trend")

    agg = st.selectbox("Aggregation", AGG_OPTIONS, index=0)
    top_n = st.slider("Top N (for ranking)", min_value=1, max_value=50, value=10)

    # Natural language query box
    st.markdown("---")
    nl = st.text_input("Or ask in plain English", key="nl_query")
    if nl:
        parsed = parse_query(nl, sch)
        # overlay manual selections only if parse found something
        if parsed.get("intent"):
            intent = parsed["intent"]
        if parsed.get("metric"):
            metric = parsed["metric"]
        if parsed.get("groupby"):
            groupby = parsed["groupby"]
        if parsed.get("date_col"):
            date_col = parsed["date_col"]
        if parsed.get("agg"):
            agg = parsed["agg"]

    # validation
    errors = []
    if intent == "trend" and not date_col:
        errors.append("Trend analysis requires a valid date column.")
    if intent != "trend" and not groupby:
        errors.append("This intent requires a group-by / dimension column.")
    if intent != "count" and not metric:
        errors.append("Please select a numeric metric column.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        if st.button("Run"):
            plan = {"intent": intent, "metric": metric, "groupby": groupby,
                    "date_col": date_col, "agg": agg, "top_n": top_n}
            st.session_state.plan = plan
            try:
                result = run_analysis(df, metric, groupby, date_col, intent, agg)
                if intent == "top" and top_n and result is not None:
                    ycol = "count" if agg == "count" else metric
                    result = result.sort_values(ycol, ascending=False).head(top_n)
                st.session_state.result = result
            except Exception as exc:
                st.error(f"Analysis error: {exc}")

    # show results
    if st.session_state.result is not None:
        st.subheader("Results")
        st.dataframe(st.session_state.result)
        fig = make_chart(st.session_state.result, intent, metric, groupby, date_col)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    # debug panel
    with st.expander("Debug info", expanded=False):
        st.write("Plan:", st.session_state.plan)
        if st.session_state.result is not None:
            st.write("Result shape:", st.session_state.result.shape)

# openai toggle (optional)
with st.sidebar:
    st.markdown("---")
    use_ai = st.checkbox("Enable OpenAI", value=False)
    if use_ai:
        st.text_input("OpenAI API Key", type="password", key="openai_key")
