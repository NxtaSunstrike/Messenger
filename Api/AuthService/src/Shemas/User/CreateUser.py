from pydantic import BaseModel
from pydantic import EmailStr


class CreateUser(BaseModel):
    Name: str
    LastName: str
    Email: EmailStr
    Password: str
    UserName: str


class ConfirmUser(BaseModel):
    Email: str
    ConfirmationCode: int


class Login(BaseModel):
    Email: EmailStr
    Password: str
