from pydantic import BaseModel
from pydantic import EmailStr


class SendEmail(BaseModel):
    subscriber: EmailStr
    content: str