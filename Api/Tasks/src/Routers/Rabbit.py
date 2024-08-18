from faststream.rabbit.router import RabbitRouter

from fastapi import Depends

from dependency_injector.wiring import inject, Provide


router = RabbitRouter()


@router.subscriber('send-email')
@inject
async def CreateEmail(data: dict) -> None:
    return ...


@router.subscriber('send-sms')
@inject
async def SendSMS(data: dict) -> None:
    return ...


@router.subscriber('download-file')
@inject
async def DownloadFile(data: dict) -> None:
    return ...


@router.subscriber('upload-file')
@inject
async def UploadFile(data: dict) -> None:
    return ...



