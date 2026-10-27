from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.data_service import process_upload,get_dataframe,get_dataset_metadata
router=APIRouter(prefix='/api/data',tags=['Data'])
@router.post('/upload')
async def upload(file:UploadFile=File(...)):
    if not file.filename: raise HTTPException(400,'A CSV file is required.')
    if not file.filename.lower().endswith('.csv'): raise HTTPException(400,'Only .csv files are supported.')
    content=await file.read()
    if not content: raise HTTPException(400,'The uploaded file is empty.')
    if len(content)>25*1024*1024: raise HTTPException(413,'File is too large. Maximum size is 25 MB.')
    try: df,log,types=process_upload(content)
    except ValueError as e: raise HTTPException(400,str(e))
    return {'success':True,'message':'Dataset uploaded successfully.','filename':file.filename,'rows':len(df),'columns':len(df.columns),'column_names':list(df.columns),'column_types':types,'cleaning_log':log}
@router.get('')
def data():
    try: df=get_dataframe()
    except Exception as e: raise HTTPException(500,str(e))
    if df.empty:return {'success':True,'has_dataset':False,'metadata':get_dataset_metadata(),'rows':[]}
    safe=df.head(100).where(df.head(100).notna(),None).to_dict(orient='records')
    return {'success':True,'has_dataset':True,'metadata':get_dataset_metadata(),'rows':safe}
