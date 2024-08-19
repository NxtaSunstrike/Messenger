from faststream.rabbit.router import RabbitRouter
from faststream import Depends

from dependency_injector.wiring import inject, Provide

from Di.Messages import MessagesContainer

from Logic.Messages import Messages

from Shemas.EmailShema import SendEmail


router = RabbitRouter()


@router.subscriber(queue = 'send-email')
@inject
async def CreateEmail(
    Body: SendEmail, Email: Messages = Depends(Provide[MessagesContainer.Messages])
) -> None:
    return await Email.SendEmail(
        subscriber = Body.subscriber, content = Body.content
    )


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



