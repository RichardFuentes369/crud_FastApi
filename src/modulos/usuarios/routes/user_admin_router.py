from typing import Optional
from fastapi import Query, status, Body, APIRouter
from fastapi.responses import JSONResponse
from ..models.user_model import User, UserCreate, UserUpdate
from ....config.db import conn  #connection
from sqlalchemy import text
from ..tables.user_admin import users #data_tabla
  
user_router_administrador = APIRouter()

# Usuarios Administradores
@user_router_administrador.get('/listarUA', tags=["usuario-administrador"])
async def listarUA(
    porPagina: int = Query(10, description="Número de items por página"),
    numeroPagina: int = Query(1, description="Número de página"),
    sort: Optional[str] = Query(None, description="Campo por el cual ordenar (ej: nombre, apellido)"),
    campoFiltro: Optional[str] = Query(None, description="Campo por el cual filtrar (ej: nombre, apellido)"),
    filtro: Optional[str] = Query(None, description="Valor del filtro"),
):
    # Construir la consulta base
    query = "SELECT * FROM mod_usuarios_administradores"
    
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
    
@user_router_administrador.get('/detalleUA', tags=["usuario-administrador"])
def detalleUA(
    campoFiltro: Optional[str] = Query(None, description="Campo por el cual filtrar"),
    filtro: Optional[str] = Query(None, description="Valor por el cual va a filtrar"),
):
    # Construir la consulta base
    query = "SELECT * FROM mod_usuarios_administradores"
    
    # Aplicación de filtros si existen
    if campoFiltro and filtro:
        query += f" WHERE {campoFiltro} LIKE :filtro_value"
    
    # Ejecutar la consulta y obtener la descripción de las columnas
    try:        
        # Ejecutar la consulta con los parámetros
        result = conn.execute(
            text(query),
            {"filtro_value": f"%{filtro}%" if filtro else ""}
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

    query = "SELECT * FROM mod_usuarios_administradores WHERE id = :_id"

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
            query = "DELETE FROM mod_usuarios_administradores WHERE id = :_id"

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
    """ 
    try:




        query = "DELETE FROM mod_usuarios_administradores WHERE id = :_id"

        result = conn.execute(
            text(query),
            {"_id": _id}
        )

        # Confirmar transacción
        conn.commit()
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "mensaje": e.args[0], 
                "data": []
            }
        )
        
         return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "mensaje": "El usuario fue eliminado con exito", 
            "data": []
        }
    )
    """

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
    
'''
    Ya funciona el 
        listarUA
        detalleUA
        eliminarUA

    Falta el 
        crearUA
        actualizarUA
        autenticacion
    
'''