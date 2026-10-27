from pydantic import BaseModel, EmailStr, Field
class RegisterRequest(BaseModel):
    name:str=Field(min_length=2,max_length=100)
    email:EmailStr
    password:str=Field(min_length=6,max_length=200)
class LoginRequest(BaseModel):
    email:EmailStr
    password:str
class AIRequest(BaseModel):
    question:str=Field(default='Analyze this dataset and provide useful insights.',max_length=2000)
