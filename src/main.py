from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.routes.user_router import user_admin_router

app = FastAPI()

app.title = "Proyecto FastApi"
app.version = "1.0.0 - Beta"

@app.get('/', tags=["Home"])
def welcome():
    return RedirectResponse("/docs")

# Usuarios
app.include_router(prefix="/userA", router=user_admin_router)

# Login
@app.get('/login', tags=["Login"])
def login():
    return {
        "sub": "",
        "token": "",
        "iat": "121221",
    }
@app.get('/refresh-token', tags=["Login"])
def refreshToken():
    return 'Hola mundo!'
@app.get('/logout', tags=["Login"])
def logout():
    return 'Hola mundo!'

