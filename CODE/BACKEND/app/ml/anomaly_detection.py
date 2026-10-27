import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df,columns=None):
    if columns is None: columns=list(df.select_dtypes(include='number').columns)
    if not columns: raise ValueError('Anomaly detection requires at least one numeric column.')
    X=df[columns].apply(pd.to_numeric,errors='coerce')
    X=X.fillna(X.median(numeric_only=True)).fillna(0)
    if len(X)<5: raise ValueError('Anomaly detection requires at least 5 rows.')
    model=IsolationForest(contamination='auto',random_state=42,n_estimators=200)
    labels=model.fit_predict(X); scores=model.decision_function(X)
    out=df.copy(); out['_anomaly']=labels; out['_anomaly_score']=scores
    anomalies=out[out['_anomaly']==-1].drop(columns=['_anomaly','_anomaly_score']).copy()
    return {'success':True,'columns':columns,'total_records':len(df),'normal_records':int((labels==1).sum()),'anomaly_count':int((labels==-1).sum()),'anomaly_percentage':float((labels==-1).mean()*100),'anomalies':anomalies.head(200).where(pd.notnull(anomalies),None).to_dict(orient='records')}
