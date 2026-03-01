import pandas as pd


def detect_columns(df: pd.DataFrame, date_threshold: float = 0.8) -> dict:
    """Return dictionary with lists: dates, numeric, dims.
    - dates: columns where pd.to_datetime parses most values
    - numeric: int/float dtype or convertible >80%
    - dims: the rest
    """
    dates, nums, dims = [], [], []
    for c in df.columns:
        ser = df[c]
        # attempt numeric first
        is_num = False
        if pd.api.types.is_numeric_dtype(ser):
            is_num = True
        else:
            # try conversion on sample
            sample = ser.dropna().astype(str).iloc[:1000]
            if len(sample) > 0:
                coerced = pd.to_numeric(sample, errors="coerce")
                if coerced.notna().mean() >= date_threshold:
                    is_num = True
        if is_num:
            nums.append(c)
            continue
        # try date parse - only non numeric
        try:
            parsed = pd.to_datetime(ser.dropna().iloc[:1000], errors="coerce", infer_datetime_format=True)
            if len(parsed) > 0 and parsed.notna().mean() >= date_threshold:
                dates.append(c)
                continue
        except Exception:
            pass
        dims.append(c)
    return {"dates": dates, "numeric": nums, "dims": dims}
