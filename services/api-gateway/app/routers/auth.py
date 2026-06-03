
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
import jwt, hashlib, os
from datetime import datetime, timedelta

router = APIRouter()
security = HTTPBearer()
SECRET = "churchhub-secret-2024"

USERS = {
    "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "hq_admin", "name": "Admin User"},
    "pastor": {"password": hashlib.sha256("pastor123".encode()).hexdigest(), "role": "pastor", "name": "Pastor John"},
    "partner": {"password": hashlib.sha256("partner123".encode()).hexdigest(), "role": "hq_admin", "name": "Partner User"},
}

class LoginRequest(BaseModel):
    username: str
    password: str

class ChangePasswordRequest(BaseModel):
    username: str
    old_password: str
    new_password: str

@router.post("/login")
async def login(req: LoginRequest):
    user = USERS.get(req.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    if user["password"] != hashlib.sha256(req.password.encode()).hexdigest():
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = jwt.encode({
        "sub": req.username,
        "name": user["name"],
        "role": user["role"],
        "exp": datetime.utcnow() + timedelta(days=7)
    }, SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer", "name": user["name"], "role": user["role"]}

@router.post("/change-password")
async def change_password(req: ChangePasswordRequest):
    user = USERS.get(req.username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user["password"] != hashlib.sha256(req.old_password.encode()).hexdigest():
        raise HTTPException(status_code=401, detail="Old password incorrect")
    USERS[req.username]["password"] = hashlib.sha256(req.new_password.encode()).hexdigest()
    return {"message": "Password changed successfully"}

@router.get("/me")
async def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=["HS256"])
        return {"username": payload["sub"], "name": payload["name"], "role": payload["role"]}
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
