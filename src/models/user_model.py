from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ValidationInfo, field_validator


# Inicio Modelo
class User(BaseModel):
    id: Optional[int] = None
    nombres: str
    apellidos: str
    telefono: str
    correo: str

class UserCreate(BaseModel):
    id: Optional[int] = None
    nombres: str = Field(min_length=3, max_length=50) # una forma de validacion
    apellidos: str = Field(min_length=3, max_length=50)
    correo: EmailStr
    telefono: str

    @field_validator('nombres') # otra forma de validacion
    def validate_nombres(cls, value, info: ValidationInfo):
        if len (value) < 3:
            raise ValueError('Campo nombres debe tener almenos 3 caracteres')
        if len (value) > 50:
            raise ValueError('Campo nombres debe tener maximo 50 caracteres')
        return value   

class UserUpdate(BaseModel):
    nombres: str
    apellidos: str
    correo: EmailStr
    telefono: str