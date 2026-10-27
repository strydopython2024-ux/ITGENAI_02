import pandas as pd
from sklearn.linear_model import LinearRegression

def forecast(df,date_col,target,horizon):
    if date_col not in df or target not in df: raise ValueError('Selected columns were not found.')
    try:h=int(horizon)
    except: raise ValueError('Forecast horizon must be an integer.')
    if h<1 or h>365: raise ValueError('Forecast horizon must be between 1 and 365.')
    d=pd.DataFrame({'date':pd.to_datetime(df[date_col],errors='coerce',format='mixed'),'y':pd.to_numeric(df[target],errors='coerce')}).dropna().sort_values('date')
    if len(d)<3: raise ValueError('Forecasting requires at least 3 valid date/numeric observations.')
    d=d.groupby('date',as_index=False)['y'].mean()
    if len(d)<3: raise ValueError('Forecasting requires at least 3 unique dates.')
    x=(d['date'].astype('int64')/86400000000000).values.reshape(-1,1); y=d.y.values
    model=LinearRegression().fit(x,y)
    last=d.date.max(); freq=pd.infer_freq(d.date) or 'D'; future=pd.date_range(last,periods=h+1,freq=freq)[1:]
    pred=model.predict((future.astype('int64')/86400000000000).values.reshape(-1,1))
    return {'success':True,'date_column':date_col,'target':target,'horizon':h,'historical':[{'date':a.strftime('%Y-%m-%d'),'value':float(b)} for a,b in zip(d.date,d.y)],'forecast':[{'date':a.strftime('%Y-%m-%d'),'value':float(b)} for a,b in zip(future,pred)]}
