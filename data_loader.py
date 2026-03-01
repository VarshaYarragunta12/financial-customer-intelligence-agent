import pandas as pd


def read_csv(file) -> pd.DataFrame:
    """Read a CSV file-like object robustly. Try common encodings and delimiters.

    Returns a DataFrame or raises ValueError on failure.
    """
    # if bytes, use BytesIO
    kwargs = {}
    try:
        df = pd.read_csv(file, **kwargs)
        return df
    except Exception:
        # try sniff delimiter
        file.seek(0)
        text = file.read().decode('utf-8', errors='ignore')
        from io import StringIO
        import csv
        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(text[:10000])
            delim = dialect.delimiter
            file.seek(0)
            return pd.read_csv(file, delimiter=delim)
        except Exception:
            pass
    raise ValueError("Unable to read CSV; check file format and encoding.")