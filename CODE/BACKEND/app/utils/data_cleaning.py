import pandas as pd
import numpy as np

MISSING_MARKERS = {"", "na", "n/a", "null", "none", "nan", "-", "--", "unknown"}

def clean_dataframe(df: pd.DataFrame):
    log=[]
    before=len(df)
    df=df.dropna(how="all").copy()
    if len(df)!=before: log.append(f"Removed {before-len(df)} completely empty rows.")
    original=list(df.columns)
    df.columns=[str(c).strip() for c in df.columns]
    if original!=list(df.columns): log.append("Trimmed column-name whitespace.")
    for col in df.columns:
        if pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_string_dtype(df[col]):
            s=df[col].astype("string").str.strip()
            lowered=s.str.lower()
            s=s.mask(lowered.isin(MISSING_MARKERS), pd.NA)
            # Convert only when almost all non-null values are numeric and conversion is lossless enough.
            converted=pd.to_numeric(s, errors="coerce")
            valid=s.notna().sum()
            if valid and converted.notna().sum()/valid >= .95:
                df[col]=converted
                log.append(f"Converted numeric-looking column '{col}'.")
            else:
                df[col]=s
    return df, log
