import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def segment(df,columns,k=3):
    if len(columns)<2: raise ValueError('Select at least two numeric columns.')
    k=int(k); X=df[columns].apply(pd.to_numeric,errors='coerce').dropna()
    if len(X)<max(5,k): raise ValueError('Not enough complete numeric rows for segmentation.')
    if k<2 or k>min(10,len(X)): raise ValueError('Cluster count must be between 2 and the number of usable rows (maximum 10).')
    z=StandardScaler().fit_transform(X); labels=KMeans(n_clusters=k,n_init=10,random_state=42).fit_predict(z)
    dist=pd.Series(labels).value_counts().sort_index()
    points=[]
    for idx,row in X.iterrows(): points.append({'index':str(idx),'x':float(row[columns[0]]),'y':float(row[columns[1]]),'cluster':int(labels[list(X.index).index(idx)])})
    return {'success':True,'columns':columns,'cluster_count':k,'distribution':[{"cluster":int(i),"count":int(v)} for i,v in dist.items()], 'assignments':[{'index':str(i),'cluster':int(c)} for i,c in zip(X.index,labels)],'points':points[:5000]}
