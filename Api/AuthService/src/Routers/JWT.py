from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException


router = APIRouter()


@router.get("/Refresh")
async def refresh():
    return await ...