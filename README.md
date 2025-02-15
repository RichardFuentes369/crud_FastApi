# crud_FastApi


## Crear Proyecto
cd ./project   (crea una carpeta)
python3.12 -m venv venv (instala entorno virtual)
source venv/bin/activate (activa entorno virtual)
pip install fastapi uvicorn email-validator python-multipart python-jose sqlalchemy pymysql (modulos necesarios)

## Correr proycto
uvicorn src.main:app --port 8000 --reload (corre "localmente" app)
uvicorn src.main:app --port 2020 --host 0.0.0.0 --reload (corre "ejecutandose en red" app)

## Documentación EndPoints
http://localhost:8000/docs (documentacion endpoints)



## Errores
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "mensaje": "El usuario fue actualizado con exito", 
            "data": item
        }
    )