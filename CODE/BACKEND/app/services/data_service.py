from pathlib import Path
import pandas as pd
from app.utils.data_cleaning import clean_dataframe
from app.utils.column_detection import detect_columns

ROOT=Path(__file__).resolve().parents[4]
DATA_DIR=ROOT/'CODE'/'DATA_BASE'/'data'
DATA_PATH=DATA_DIR/'current_dataset.csv'
DATA_DIR.mkdir(parents=True, exist_ok=True)

def save_dataframe(df):
    DATA_DIR.mkdir(parents=True, exist_ok=True); df.to_csv(DATA_PATH,index=False)

def get_dataframe():
    if not DATA_PATH.exists(): return pd.DataFrame()
    try: return pd.read_csv(DATA_PATH)
    except Exception as e: raise ValueError(f"Active dataset could not be read: {e}")

def has_dataset():
    return DATA_PATH.exists() and DATA_PATH.stat().st_size>0 and not get_dataframe().empty

def get_dataset_metadata():
    if not DATA_PATH.exists(): return {"exists":False,"filename":None,"rows":0,"columns":0}
    try:
        df=get_dataframe(); return {"exists":not df.empty,"filename":DATA_PATH.name,"rows":len(df),"columns":len(df.columns),"column_names":list(df.columns)}
    except Exception as e: return {"exists":True,"filename":DATA_PATH.name,"error":str(e)}

def process_upload(content):
    import io
    last=None
    for enc in ('utf-8','latin-1'):
        try:
            df=pd.read_csv(io.BytesIO(content), encoding=enc)
            last=None; break
        except Exception as e: last=e
    if last: raise ValueError(f"CSV could not be parsed: {last}")
    if df.empty or len(df.columns)==0: raise ValueError("CSV must contain at least one row and one column.")
    df,log=clean_dataframe(df)
    if df.empty or len(df.columns)==0: raise ValueError("CSV contains no usable rows or columns after cleaning.")
    save_dataframe(df)
    return df,log,detect_columns(df)
