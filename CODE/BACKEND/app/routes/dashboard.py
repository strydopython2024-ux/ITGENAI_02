from fastapi import APIRouter
from app.services.generic_analysis_service import profile
router=APIRouter(prefix='/api',tags=['Dashboard'])
@router.get('/dashboard')
def dashboard():
    p=profile(); return {'success':p.get('success',False),'profile':p}
