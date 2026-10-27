import pandas as pd

def detect_columns(df: pd.DataFrame):
    out={"numeric":[],"categorical":[],"date":[],"boolean":[],"text":[]}
    if df.empty: return out
    for col in df.columns:
        s=df[col]
        if pd.api.types.is_bool_dtype(s):
            out["boolean"].append(col); continue
        if pd.api.types.is_numeric_dtype(s):
            out["numeric"].append(col); continue
        nonnull=s.dropna()
        if len(nonnull):
            parsed=pd.to_datetime(nonnull, errors="coerce", format="mixed")
            if parsed.notna().mean() >= .70:
                out["date"].append(col); continue
        nunique=int(s.nunique(dropna=True)); n=len(nonnull)
        if n==0 or nunique <= max(20, min(50, int(max(1,n*.20)))):
            out["categorical"].append(col)
        else:
            out["text"].append(col)
    return out
