from typing import Optional
from fastapi import Query, status, Body, APIRouter
from fastapi.responses import JSONResponse
from ..models.user_model import User, UserCreate, UserUpdate
from ....config.db import conn  #connection
from sqlalchemy import text
from ..tables.user_final import users #data_tabla
import json
from cryptography.fernet import Fernet

user_router_final = APIRouter() 

key = Fernet.generate_key()
f = Fernet(key)

# Usuarios Finales
@user_router_final.get('/listarUF', tags=["usuarios-finales"])
async def listarUF(
    porPagina: int = Query(10, description="Número de items por página"),
    numeroPagina: int = Query(1, description="Número de página"),
    sort: Optional[str] = Query(None, description="Campo por el cual ordenar (ej: nombre, apellido)"),
    campoFiltro: Optional[str] = Query(None, description="Campo por el cual filtrar (ej: nombre, apellido)"),
    filtro: Optional[str] = Query(None, description="Valor del filtro"),
):
    # Construir la consulta base
    query = "SELECT id, name, lastname, email, password FROM mod_usuarios_finales"
    
    # Aplicación de filtros si existen
    if campoFiltro and filtro:
        query += f" WHERE {campoFiltro} LIKE :filtro_value"
    
    # Aplicación de ordenación si existe
    if sort:
        query += f" ORDER BY {sort}"
    
    # Paginación
    offset = (numeroPagina - 1) * porPagina
    query += f" LIMIT :limit OFFSET :offset"
    
    # Ejecutar la consulta y obtener la descripción de las columnas
    try:
        # Ejecutar la consulta con los parámetros
        result = conn.execute(
            text(query),
            {"filtro_value": f"%{filtro}%" if filtro else "", "limit": porPagina, "offset": offset}
        )
        
        # Obtener los nombres de las columnas
        columns = [column[0] for column in result.cursor.description]  # Ahora usamos result.cursor.description para obtener las columnas
        
        # Obtener los resultados
        rows = result.fetchall()

        # Convertir las filas a diccionarios usando los nombres de las columnas
        result_dicts = [dict(zip(columns, row)) for row in rows]

    # Capturo errores si el problema es de la consulta    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "mensaje": e.args[0], 
                "data": []
            }
        )
    
    # Analizo si hay resultados de usuarios
    if len(result_dicts):
        mensaje = "Lista de usuarios encontrados" # Devuelve los resultados en formato de diccionario
        result_dicts = result_dicts
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content={
                "mensaje": mensaje, 
                "data": result_dicts
            }
        )
    else:
        mensaje= "No se encontraron registros"  # Devuelve los resultados en formato de diccionario
        result_dicts = []
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content={
                "mensaje": mensaje, 
                "data": result_dicts
            }
        )
    
@user_router_final.get('/detalleUF', tags=["usuarios-finales"])
def detalleUF(
    campoFiltro: Optional[str] = Query(None, description="Campo por el cual filtrar"),
    palabraFiltro: Optional[str] = Query(None, description="Valor por el cual va a filtrar"),
):
    # Construir la consulta base
    query = "SELECT * FROM mod_usuarios_finales"
    
    # Aplicación de filtros si existen
    if campoFiltro and palabraFiltro:
        query += f" WHERE {campoFiltro} LIKE :filtro_value"
    
    # Ejecutar la consulta y obtener la descripción de las columnas
    try:        
        # Ejecutar la consulta con los parámetros
        result = conn.execute(
            text(query),
            {"filtro_value": f"%{palabraFiltro}%" if palabraFiltro else ""}
        )
        
        # Obtener los nombres de las columnas
        columns = [column[0] for column in result.cursor.description]  # Ahora usamos result.cursor.description para obtener las columnas
        
        # Obtener los resultados
        rows = result.fetchall()

        # Convertir las filas a diccionarios usando los nombres de las columnas
        result_dicts = [dict(zip(columns, row)) for row in rows]

    # Capturo errores si el problema es de la consulta    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "mensaje": e.args[0], 
                "data": []
            }
        )
    
    # Analizo si hay resultados de usuarios
    if len(result_dicts):
        mensaje = "Usuarios encontrado" # Devuelve los resultados en formato de diccionario
        result_dicts = result_dicts
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content={
                "mensaje": mensaje, 
                "data": result_dicts
            }
        )
    else:
        mensaje= "No se encontraro ningun registro"  # Devuelve los resultados en formato de diccionario
        result_dicts = []
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content={
                "mensaje": mensaje, 
                "data": result_dicts
            }
        )
    
@user_router_final.post('/crearUF', tags=["usuarios-finales"])
def crearUF(
    user: UserCreate
):
    resultado = detalleUF('email', user.email)

    if len(json.loads(resultado.body)['data']) > 0:
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content={
                "mensaje": json.loads(resultado.body)['mensaje'], 
                "data": []
            }
        )
    
    query = "INSERT INTO mod_usuarios_finales (`name`, `lastname`, `email`, `password`, `password_dencrypt`) VALUES (:name, :lastname, :email, :password, :password_dencrypt)"
    
    conn.execute(
        text(query),
        {
            "name": user.name, 
            "lastname": user.lastname, 
            "email": user.email, 
            "password": f.encrypt(user.password.encode("utf-8")), 
            "password_dencrypt": user.password
        }
    )
    conn.commit() 

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content={
            "mensaje": "Usuario creado con exito", 
            "data": []
        }
    )

@user_router_final.delete('/eliminarUF', tags=["usuarios-finales"])
def eliminarUF(
    _id: int = Query(None, description="Id del usuario a eliminar"),
):        

    query = "SELECT * FROM mod_usuarios_finales WHERE id = :_id"

    # Ejecutar la consulta y obtener la descripción de las columnas
    try:        
        # Ejecutar la consulta con los parámetros
        result = conn.execute(
            text(query),
            {"_id": _id}
        )

        # Obtener los nombres de las columnas
        columns = [column[0] for column in result.cursor.description]  # Ahora usamos result.cursor.description para obtener las columnas
        
        # Obtener los resultados
        rows = result.fetchall()

        # Convertir las filas a diccionarios usando los nombres de las columnas
        result_dicts = [dict(zip(columns, row)) for row in rows]

        if len(result_dicts) > 0:
            query = "DELETE FROM mod_usuarios_finales WHERE id = :_id"

            result = conn.execute(
                text(query),
                {"_id": _id}
            )

            # Confirmar transacción
            conn.commit()
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "mensaje": "El usuario fue eliminado con exito", 
                    "data": []
                }
            )
        else :
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "mensaje": f"El usuario con id {_id} no existe", 
                    "data": []
                }
            )
            

    # Capturo errores si el problema es de la consulta    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "mensaje": e.args[0], 
                "data": []
            }
        )

@user_router_final.put('/actualizarUF/{_idUsuario}', tags=["usuarios-finales"])
def actualizarUF(
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
