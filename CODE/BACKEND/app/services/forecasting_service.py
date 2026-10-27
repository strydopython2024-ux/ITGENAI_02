from app.services.data_service import get_dataframe
from app.ml.forecasting import forecast
def run_forecast(date_col,target,horizon): return forecast(get_dataframe(),date_col,target,horizon)
