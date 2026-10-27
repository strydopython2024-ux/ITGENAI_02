from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
import hashlib, hmac, secrets
from app.models.schemas import RegisterRequest, LoginRequest
from app.database.database import create_user,get_user
router=APIRouter(prefix='/api/auth',tags=['Authentication'])

def hash_password(p):
    salt=secrets.token_bytes(16); dk=hashlib.pbkdf2_hmac('sha256',p.encode(),salt,200_000); return 'pbkdf2$200000$'+salt.hex()+'$'+dk.hex()
def verify_password(p,stored):
    try:
        _,iters,salt_hex,digest=stored.split('$'); dk=hashlib.pbkdf2_hmac('sha256',p.encode(),bytes.fromhex(salt_hex),int(iters)); return hmac.compare_digest(dk.hex(),digest)
    except Exception:return False
@router.post('/register')
def register(req:RegisterRequest):
    if get_user(req.email): raise HTTPException(409,'Email is already registered.')
    uid=create_user(req.name,req.email.lower(),hash_password(req.password),datetime.now(timezone.utc).isoformat())
    return {'success':True,'message':'Registration successful.','user':{'id':uid,'name':req.name,'email':req.email.lower()}}
@router.post('/login')
def login(req:LoginRequest):
    u=get_user(req.email)
    if not u or not verify_password(req.password,u['password']): raise HTTPException(401,'Invalid email or password.')
    return {'success':True,'message':'Login successful.','user':{'id':u['id'],'name':u['name'],'email':u['email']}}
