from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, Response, JSONResponse


# Importando rutas de modulos
from src.modulos.login.routes.login_router import login_router
from src.modulos.usuarios.routes.user_admin_router import user_router_administrador
from src.modulos.usuarios.routes.user_final_router import user_router_final


app = FastAPI()

app.title = "Proyecto FastApi"
app.version = "1.0.0 - Beta"

@app.middleware('http')
async def http_error_handler(request: Request, call_next) -> Response | JSONResponse:
    print('Middleware is running!')
    return await call_next(request)


@app.get('/', tags=["Home"])
def welcome():
    return RedirectResponse("/docs")

# Login
app.include_router(prefix="/login", router=login_router)

# Usuarios
app.include_router(prefix="/usuarios-administradores", router=user_router_administrador)
app.include_router(prefix="/usuarios-finales", router=user_router_final)


