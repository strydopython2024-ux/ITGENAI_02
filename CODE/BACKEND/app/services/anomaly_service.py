from app.services.data_service import get_dataframe
from app.ml.anomaly_detection import detect_anomalies
def run_anomalies(columns=None): return detect_anomalies(get_dataframe(),columns)
