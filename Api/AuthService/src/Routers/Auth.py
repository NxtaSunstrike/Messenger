from fastapi import APIRouter
from fastapi import Depends

from Dependencies.Auth import createUser
from Dependencies.Auth import CreateUser
from Dependencies.Auth import ConfirmUser
from Dependencies.Auth import confirmUser
from Dependencies.Auth import LoginUser
from Dependencies.Auth import loginUser


AuthRouter = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@AuthRouter.post("/CreateUser")
async def CreateUser(
    create: CreateUser = Depends(createUser)
):
    return create

@AuthRouter.post('/Confirm')
async def Confirm(
    confirm: ConfirmUser = Depends(confirmUser)
):
    return confirm

@AuthRouter.post('/Login')
async def Login(
    login: LoginUser = Depends(loginUser)
):
    return login