from app.services.data_service import get_dataframe
from app.ml.segmentation import segment
def run_segmentation(columns,k=3): return segment(get_dataframe(),columns,k)
