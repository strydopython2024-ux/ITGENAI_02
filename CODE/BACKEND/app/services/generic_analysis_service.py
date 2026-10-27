import pandas as pd
import numpy as np
from app.services.data_service import get_dataframe
from app.utils.column_detection import detect_columns

def _empty(msg): return {"success":False,"message":msg}

def profile():
    try: df=get_dataframe()
    except Exception as e: return _empty(str(e))
    if df.empty:
        return {"success":True,"dataset":{"rows":0,"columns":0,"column_names":[],"missing_values":0,"duplicate_rows":0},"column_types":{"numeric":[],"categorical":[],"date":[],"boolean":[],"text":[]},"numeric_summary":{},"categorical_summary":{},"date_summary":{},"correlations":{},"available_analysis":{"overview":False,"statistics":False,"categorical":False,"correlation":False,"forecasting":False,"segmentation":False,"anomaly_detection":False}}
    types=detect_columns(df); nums={}; cats={}; dates={}
    for c in types['numeric']:
        s=pd.to_numeric(df[c],errors='coerce'); nums[c]={"count":int(s.count()),"mean":float(s.mean()) if s.count() else None,"median":float(s.median()) if s.count() else None,"min":float(s.min()) if s.count() else None,"max":float(s.max()) if s.count() else None,"std":float(s.std()) if s.count()>1 else 0.0}
    for c in types['categorical']:
        vc=df[c].astype('string').fillna('<missing>').value_counts().head(10); cats[c]={"unique_count":int(df[c].nunique(dropna=True)),"top_values":[{"value":str(k),"frequency":int(v)} for k,v in vc.items()]}
    for c in types['date']:
        s=pd.to_datetime(df[c],errors='coerce',format='mixed'); dates[c]={"min":s.min().isoformat() if s.notna().any() else None,"max":s.max().isoformat() if s.notna().any() else None,"valid_count":int(s.notna().sum())}
    corr={}
    if len(types['numeric'])>=2:
        m=df[types['numeric']].apply(pd.to_numeric,errors='coerce').corr().round(4); corr=m.where(pd.notnull(m),None).to_dict()
    n=len(types['numeric']); r=len(df)
    avail={"overview":True,"statistics":n>=1,"categorical":len(types['categorical'])>=1,"correlation":n>=2,"forecasting":len(types['date'])>=1 and n>=1,"segmentation":n>=2 and r>=5,"anomaly_detection":n>=1 and r>=5}
    return {"success":True,"dataset":{"rows":r,"columns":len(df.columns),"column_names":list(df.columns),"missing_values":int(df.isna().sum().sum()),"duplicate_rows":int(df.duplicated().sum())},"column_types":types,"numeric_summary":nums,"categorical_summary":cats,"date_summary":dates,"correlations":corr,"available_analysis":avail}

def statistics(column):
    df=get_dataframe()
    if df.empty:return _empty('No dataset uploaded.')
    if column not in df.columns:return _empty('Numeric column not found.')
    s=pd.to_numeric(df[column],errors='coerce').dropna()
    if s.empty:return _empty('Selected column has no numeric values.')
    return {"success":True,"column":column,"stats":{"count":int(s.count()),"mean":float(s.mean()),"median":float(s.median()),"min":float(s.min()),"max":float(s.max()),"std":float(s.std()) if len(s)>1 else 0.0},"values":s.tolist()[:5000]}

def categorical(column):
    df=get_dataframe()
    if df.empty:return _empty('No dataset uploaded.')
    if column not in df.columns:return _empty('Categorical column not found.')
    vc=df[column].astype('string').fillna('<missing>').value_counts().head(30)
    return {"success":True,"column":column,"unique_count":int(df[column].nunique(dropna=True)),"frequencies":[{"value":str(k),"frequency":int(v)} for k,v in vc.items()]}

def correlation():
    df=get_dataframe(); types=detect_columns(df)
    if len(types['numeric'])<2:return _empty('Correlation analysis requires at least two numeric columns.')
    m=df[types['numeric']].apply(pd.to_numeric,errors='coerce').corr(); pairs=[]
    for i,a in enumerate(m.columns):
        for b in m.columns[i+1:]: pairs.append((a,b,float(m.loc[a,b])))
    pos=sorted(pairs,key=lambda x:x[2],reverse=True)[:5]; neg=sorted(pairs,key=lambda x:x[2])[:5]
    return {"success":True,"columns":list(m.columns),"matrix":m.round(4).fillna(0).to_dict(),"strongest_positive":[{"a":a,"b":b,"value":v} for a,b,v in pos],"strongest_negative":[{"a":a,"b":b,"value":v} for a,b,v in neg]}

def generic_sales(): return statistics(next(iter(detect_columns(get_dataframe())['numeric']),'')) if not get_dataframe().empty and detect_columns(get_dataframe())['numeric'] else _empty('No generic numeric column is available.')
