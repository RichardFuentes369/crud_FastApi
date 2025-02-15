from typing import Optional
from fastapi import Query, status, Body, APIRouter
from fastapi.responses import JSONResponse
from ..models.user_model import User, UserCreate, UserUpdate
from ....config.db import conn  #connection
from sqlalchemy import text
from ..tables.user_admin import users #data_tabla

##users = [
##    {
##    "id": 1,
##    "nombres": "Javier Ricardo",
##    "apellidos": "Baron Fuentes",
##    "correo": "javierbaron6@gmail.com",
##    "telefono": "35042844093"
##    },
##]
  
user_router_administrador = APIRouter()

# Usuarios Administradores
@user_router_administrador.get('/listarUA', tags=["usuario-administrador"])
def listarUA(
    porPagina: int = Query(10, description="Número de items por página"),
    numeroPagina: int = Query(1, description="Número de página"),
    sort: Optional[str] = Query(None, description="Campo por el cual ordenar (ej: nombre, apellido)"),
    campoFiltro: Optional[str] = Query(None, description="Campo por el cual filtrar (ej: nombre, apellido)"),
    filtro: Optional[str] = Query(None, description="Valor del filtro"),
):

    # Filtrado
    usuarios_filtrados = users
    if campoFiltro and filtro:
        usuarios_filtrados = [
            usuario for usuario in usuarios_filtrados
            if filtro.lower() in str(usuario.get(campoFiltro, "")).lower()
        ]

    # Ordenamiento
    if sort:
        usuarios_filtrados.sort(key=lambda usuario: usuario.get(sort, ""))

    # Paginación
    inicio = (numeroPagina - 1) * porPagina
    fin = inicio + porPagina
    content = usuarios_filtrados[inicio:fin]

    return JSONResponse(
        status_code = status.HTTP_200_OK, 
        content = content,
    )
@user_router_administrador.get('/detalleUA', tags=["usuario-administrador"])
def detalleUA(
    _campoFiltro: Optional[str] = Query(None, description="Campo por el cual filtrar"),
    _palabraFiltro: Optional[str] = Query(None, description="Valor por el cual va a filtrar"),
):
    
    # Validar que _campoFiltro exista en los usuarios
    for usuario in users:
        if _campoFiltro not in usuario:
            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content={
                    "mensaje": f"El campo '{_campoFiltro}' no existe en los datos de usuario.", 
                    "data": []
                }
            )
        
    # Filtrado
    usuarios_filtrados = users
    if _campoFiltro and _palabraFiltro:
        usuarios_filtrados = [
            usuario for usuario in usuarios_filtrados if _palabraFiltro.lower() in str(usuario.get(_campoFiltro, "")).lower()
        ]

    if len(usuarios_filtrados):
        mensaje = "Usuario encontrado con exito"
        code = status.HTTP_200_OK
    else:
        mensaje = "Usuario no existe en nuestra base de datos"
        code = status.HTTP_404_NOT_FOUND
    
    return JSONResponse(
        status_code=code,
        content={
            "mensaje": mensaje, 
            "data": usuarios_filtrados
        }
    )
@user_router_administrador.post('/crearUA', tags=["usuario-administrador"])
def crearUA(
    user: UserCreate
):
    # Filtrado
    usuarios_filtrados = users
    if user.correo:
        usuarios_filtrados = [
            usuario for usuario in usuarios_filtrados
            if user.correo in str(usuario.get('correo', "")).lower()
        ]

    if len(usuarios_filtrados):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "mensaje": f"El correo'{user.correo}'ya esta registrador",
                "data": []
            }
        )
    else:
        users.append(user.model_dump())
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "mensaje": "Usuario creado exitosamente", 
                "data": user.model_dump()
            }
        )
@user_router_administrador.delete('/eliminarUA', tags=["usuario-administrador"])
def eliminarUA(
    _id: int = Query(None, description="Id del usuario a eliminar"),
):        
    # Filtrado
    usuarios_filtrados = users
    if _id:
        usuarios_filtrados = [
            usuario for usuario in usuarios_filtrados if usuario['id'] == _id
        ]

    if len(usuarios_filtrados) == 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "mensaje": "El usuario con id '{_id}' no existe en nuestros registros.", 
                "data": []
            }
        )
    # Filtro la posicion y la saco
    if _id:
        for i, user in enumerate(users):
            if user["id"] == _id:
                posicion = i
                break
        removed_user = users.pop(posicion)    
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "mensaje": "El usuario fue eliminado con exito", 
            "data": usuarios_filtrados
        }
    )
@user_router_administrador.put('/actualizarUA/{_idUsuario}', tags=["usuario-administrador"])
def actualizarUA(
    _idUsuario: int, 
    user: UserUpdate
):
    
    # Filtrado
    usuarios_filtrados = users
    if _idUsuario:
        usuarios_filtrados = [
            usuario for usuario in usuarios_filtrados if usuario['id'] == _idUsuario
        ]
    
    if len(usuarios_filtrados) == 0:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "mensaje": "El usuario con id '{_idUsuario}' no existe en nuestros registros.", 
                "data": []
            }
        )
                   
    for item in usuarios_filtrados:
        if item['id'] == _idUsuario:
            item['nombres'] = user.nombres
            item['apellidos'] = user.apellidos
            item['correo'] = user.correo
            item['telefono'] = user.telefono
            break

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "mensaje": "El usuario fue actualizado con exito", 
            "data": item
        }
    )
    
@user_router_administrador.get('/lista', tags=["usuario-administrador"])
def lista():
    result = conn.execute(
        text("SELECT * FROM mod_usuarios_administradores")
    )
    users = result.fetchall()
    for user in users:
        print(f"ID: {user.id}, Name: {user.name}")
    
    #return JSONResponse(
    #    status_code = status.HTTP_200_OK, 
    #    content = users,
    #)
