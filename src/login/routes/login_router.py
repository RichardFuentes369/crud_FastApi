from typing import Optional
from fastapi import Query, status, Body, APIRouter
from fastapi.responses import JSONResponse
from src.usuarios.models.user_model import User, UserCreate, UserUpdate

login_router = APIRouter()

# Login
@login_router.get('/login', tags=["Login"])
def login():
    return {
        "sub": "",
        "token": "",
        "iat": "121221",
    }
@login_router.get('/refresh-token', tags=["Login"])
def refreshToken():
    return 'Hola mundo!'
@login_router.get('/logout', tags=["Login"])
def logout():
    return 'Hola mundo!'

