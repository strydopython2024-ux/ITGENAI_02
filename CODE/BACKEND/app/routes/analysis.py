from fastapi import APIRouter, HTTPException
from app.services.generic_analysis_service import profile,statistics,categorical,correlation,generic_sales
from app.services.forecasting_service import run_forecast
from app.services.segmentation_service import run_segmentation
from app.services.anomaly_service import run_anomalies
router=APIRouter(prefix='/api/analysis',tags=['Analysis'])
@router.get('/profile')
def get_profile(): return profile()
@router.get('/statistics')
def stats(column:str):
    try:return statistics(column)
    except Exception as e: raise HTTPException(400,str(e))
@router.get('/categorical')
def cats(column:str):
    try:return categorical(column)
    except Exception as e: raise HTTPException(400,str(e))
@router.get('/correlation')
def corr(): return correlation()
@router.get('/forecast')
def forecast(date_column:str,target:str,horizon:int=7):
    try:return run_forecast(date_column,target,horizon)
    except Exception as e: raise HTTPException(400,str(e))
@router.get('/segmentation')
def segmentation(columns:str,k:int=3):
    try:return run_segmentation([c.strip() for c in columns.split(',') if c.strip()],k)
    except Exception as e: raise HTTPException(400,str(e))
@router.get('/anomalies')
def anomalies(columns:str=''):
    try:return run_anomalies([c.strip() for c in columns.split(',') if c.strip()] or None)
    except Exception as e: raise HTTPException(400,str(e))
@router.get('/sales')
def sales():
    try:return generic_sales()
    except Exception as e: raise HTTPException(400,str(e))
