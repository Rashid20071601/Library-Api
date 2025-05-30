from typing import Annotated
from pydantic import BaseModel, EmailStr, constr


class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, constr(min_length=6)]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str