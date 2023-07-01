from pydantic import BaseModel

from .base import ResponseSchema


class RegisterUserSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class LoginUserSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class RegisterResponseDataSchema(BaseModel):
    username: str
    access: str
    refresh: str


class RegisterResponseSchema(ResponseSchema):
    data: RegisterResponseDataSchema


class LoginResponseDataSchema(BaseModel):
    access: str
    refresh: str


class LoginResponseSchema(ResponseSchema):
    data: LoginResponseDataSchema
