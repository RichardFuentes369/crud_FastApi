from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ValidationInfo, field_validator


# Inicio Modelo
class User(BaseModel):
    id: Optional[int] = None
    name: str
    lastname: str
    email: str

class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50) # una forma de validacion
    lastname: str = Field(min_length=3, max_length=50) # una forma de validacion
    email: EmailStr
    password: str = Field(min_length=10, max_length=50) # una forma de validacion

    @field_validator('name') # otra forma de validacion
    def validate_name(cls, value, info: ValidationInfo):
        if len (value) < 3:
            raise ValueError('Campo nombres debe tener almenos 3 caracteres')
        if len (value) > 50:
            raise ValueError('Campo nombres debe tener maximo 50 caracteres')
        return value   

class UserUpdate(BaseModel):
    id: Optional[int] = None
    name: str = Field(min_length=3, max_length=50) # una forma de validacion
    lastname: str = Field(min_length=3, max_length=50) # una forma de validacion
    password: str = Field(min_length=10, max_length=50) # una forma de validacion
    email: EmailStr