from fastapi import FastAPI, Query, Path, HTTPException, status, Body
from typing import List, Optional
from fastapi.responses import JSONResponse


app = FastAPI()

app.title = "Proyecto FastApi"
app.version = "1.0.0 - Beta"


users = [
    {
    "id": 1,
    "nombres": "Javier Ricardo",
    "apellidos": "Baron Fuentes",
    "correo": "javierbaron6@gmail.com",
    "telefono": "35042844093"
    },
    {
    "id": 2,
    "nombres": "Ana Maria",
    "apellidos": "Rodriguez Perez",
    "correo": "anamaria@example.com",
    "telefono": "3001234567"
    },
    {
    "id": 3,
    "nombres": "Carlos Alberto",
    "apellidos": "Gomez Sanchez",
    "correo": "carlosalberto@example.com",
    "telefono": "3109876543"
    },
    {
    "id": 4,
    "nombres": "Sofia",
    "apellidos": "Lopez Diaz",
    "correo": "sofia@example.com",
    "telefono": "3205551212"
    },
    {
    "id": 5,
    "nombres": "Miguel Angel",
    "apellidos": "Hernandez Castro",
    "correo": "miguelangel@example.com",
    "telefono": "3508889900"
    },
    {
    "id": 6,
    "nombres": "Valentina",
    "apellidos": "Garcia Morales",
    "correo": "valentina@example.com",
    "telefono": "3014445566"
    },
    {
    "id": 7,
    "nombres": "Andres Felipe",
    "apellidos": "Martinez Ruiz",
    "correo": "andresfelipe@example.com",
    "telefono": "3127778899"
    },
    {
    "id": 8,
    "nombres": "Isabella",
    "apellidos": "Perez Vargas",
    "correo": "isabella@example.com",
    "telefono": "3211112233"
    },
    {
    "id": 9,
    "nombres": "Juan David",
    "apellidos": "Torres Ramirez",
    "correo": "juandavid@example.com",
    "telefono": "3502223344"
    },
    {
    "id": 10,
    "nombres": "Camila",
    "apellidos": "Diaz Rodriguez",
    "correo": "camila@example.com",
    "telefono": "3025556677"
    },
    {
    "id": 11,
    "nombres": "Sebastian",
    "apellidos": "Sanchez Perez",
    "correo": "sebastian@example.com",
    "telefono": "3118889900"
    },
    {
    "id": 12,
    "nombres": "Mariana",
    "apellidos": "Gomez Morales",
    "correo": "mariana@example.com",
    "telefono": "3221237890"
    },
    {
    "id": 13,
    "nombres": "Nicolas",
    "apellidos": "Hernandez Ruiz",
    "correo": "nicolas@example.com",
    "telefono": "3514561237"
    },
    {
    "id": 14,
    "nombres": "Laura",
    "apellidos": "Castro Vargas",
    "correo": "laura@example.com",
    "telefono": "3037894561"
    },
    {
    "id": 15,
    "nombres": "Daniel",
    "apellidos": "Martinez Ramirez",
    "correo": "daniel@example.com",
    "telefono": "3131235678"
    },
    {
    "id": 16,
    "nombres": "Juliana",
    "apellidos": "Perez Diaz",
    "correo": "juliana@example.com",
    "telefono": "3234568901"
    },
    {
    "id": 17,
    "nombres": "Samuel",
    "apellidos": "Torres Rodriguez",
    "correo": "samuel@example.com",
    "telefono": "3527891234"
    },
    {
    "id": 18,
    "nombres": "Valentina",
    "apellidos": "Diaz Sanchez",
    "correo": "valentina@example.com",
    "telefono": "3041239876"
    },
    {
    "id": 19,
    "nombres": "David",
    "apellidos": "Sanchez Morales",
    "correo": "david@example.com",
    "telefono": "3144562378"
    },
    {
    "id": 20,
    "nombres": "Sara",
    "apellidos": "Gomez Ruiz",
    "correo": "sara@example.com",
    "telefono": "3247895610"
    },
    {
    "id": 21,
    "nombres": "Juan Pablo",
    "apellidos": "Hernandez Vargas",
    "correo": "juanpablo@example.com",
    "telefono": "3531238901"
    },
    {
    "id": 22,
    "nombres": "Maria Jose",
    "apellidos": "Castro Ramirez",
    "correo": "mariajose@example.com",
    "telefono": "3054561239"
    },
    {
    "id": 23,
    "nombres": "Santiago",
    "apellidos": "Martinez Diaz",
    "correo": "santiago@example.com",
    "telefono": "3157894562"
    },
    {
    "id": 24,
    "nombres": "Sofia",
    "apellidos": "Perez Rodriguez",
    "correo": "sofia@example.com",
    "telefono": "3251237894"
    },
    {
    "id": 25,
    "nombres": "Mateo",
    "apellidos": "Torres Sanchez",
    "correo": "mateo@example.com",
    "telefono": "3544569870"
    },
    {
    "id": 26,
    "nombres": "Emilia",
    "apellidos": "Diaz Morales",
    "correo": "emilia@example.com",
    "telefono": "3067891235"
    },
    {
    "id": 27,
    "nombres": "Lucas",
    "apellidos": "Sanchez Ruiz",
    "correo": "lucas@example.com",
    "telefono": "3161234568"
    },
    {
    "id": 28,
    "nombres": "Antonia",
    "apellidos": "Gomez Vargas",
    "correo": "antonia@example.com",
    "telefono": "3264567891"
    },
    {
    "id": 29,
    "nombres": "Martin",
    "apellidos": "Hernandez Ramirez",
    "correo": "martin@example.com",
    "telefono": "3557891236"
    },
    {
    "id": 30,
    "nombres": "Victoria",
    "apellidos": "Castro Diaz",
    "correo": "victoria@example.com",
    "telefono": "3071239875"
    },
    {
    "id": 31,
    "nombres": "Joaquin",
    "apellidos": "Martinez Rodriguez",
    "correo": "joaquin@example.com",
    "telefono": "3174562379"
    }
]
  

@app.get('/', tags=["Home"])
def welcome():
    return 'Welcome to my app!'

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


# Usuarios Administradores
@app.get('/listarUA', tags=["usuario-administrador"])
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
    usuarios_paginados = usuarios_filtrados[inicio:fin]

    return usuarios_paginados
@app.get('/detalleUA', tags=["usuario-administrador"])
def detalleUA(
    _campoFiltro: Optional[str] = Query(None, description="Campo por el cual filtrar"),
    _palabraFiltro: Optional[str] = Query(None, description="Valor por el cual va a filtrar"),
):
    
    # Validar que _campoFiltro exista en los usuarios
    for usuario in users:
        if _campoFiltro not in usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El campo '{_campoFiltro}' no existe en los datos de usuario."
            )
        
    # Filtrado
    usuarios_filtrados = users
    if _campoFiltro and _palabraFiltro:
        usuarios_filtrados = [
            usuario for usuario in usuarios_filtrados if _palabraFiltro.lower() in str(usuario.get(_campoFiltro, "")).lower()
        ]

    mensaje = ''

    if len(usuarios_filtrados):
        mensaje = "Usuario encontrado con exito"
    else:
        mensaje = "Usuario no existe en nuestra base de datos"
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "mensaje": mensaje, 
            "data": usuarios_filtrados
        }
    )
@app.post('/crearUA', tags=["usuario-administrador"])
def crearUA(
    id:int = Body(), 
    nombres: str = Body(), 
    apellidos:str = Body(), 
    correo:str = Body(), 
    telefono:str = Body()
):
    usuario_nuevo = {
        'id': id,
        'nombres': nombres,
        'apellidos': apellidos,
        'correo': correo,
        'telefono': telefono
    }
    users.append(usuario_nuevo)

    mensaje = 'Usuario creado exitosamente'

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "mensaje": mensaje, 
            "data": usuario_nuevo
        }
    )
@app.delete('/eliminarUA', tags=["usuario-administrador"])
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El usuario con id '{_id}' no existe en nuestros registros."
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
@app.get('/actualizarUA/{_idUsuario}', tags=["usuario-administrador"])
def actualizarUA():
    return 'Actualizar Usuario'
