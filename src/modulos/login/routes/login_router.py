from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import jwt

login_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")

users = {
    "pablo": {"username": "pablo", "email": "pablo@gmail.com", "password": "password"}
}

def encode_token(payload: dict) -> str:
    token = jwt.encode(payload, "my-secret", algorithm="HS256")
    return token

def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict: 
    data = jwt.decode(token, "my-secret", algorithms=["HS256"])
    user = users.get(data['username'])
    return user

@login_router.post('/token', tags=["login"])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.get(form_data.username)
    if not user or form_data.password != user["password"]:
        return JSONResponse(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            content = {
                "mensaje": f"Error al iniciar la sessión.", 
                "data": []
            }
        )
    token = encode_token({"username": user["username"], "email": user["email"]})
    return { "access_token": token }

@login_router.get('/profile', tags=["login"])
def profile(current_user: Annotated[dict, Depends(decode_token)]):
    return current_user


