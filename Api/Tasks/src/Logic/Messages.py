from typing import Any
import smtplib

from pathlib import Path

from email.mime.multipart import MIMEMultipart

class Messages:

    def __init__(
        self, Host: str, Port: int, Pass: str, User: str
    ) -> None:
        self.HOST: str = Host
        self.PORT: int = Port
        self.PASS: str = Pass
        self.USER: str = User

    async def SendEmail(self, subscriber: str, content: Any) -> None:
        if isinstance(content, Path):
            try:
                async with open(content, 'r') as file:
                    content = file.read()
            except Exception as e:
                return e
        async with smtplib.SMTP(self.HOST, self.PORT) as smtp:
            try:
                smtp.login(self.USER, self.PASS)
                msg = MIMEMultipart()
                msg['From'] = self.USER
                msg['To'] = subscriber
                msg['Subject'] = 'New Message'
                msg.attach(content)
                smtp.sendmail(self.USER, subscriber, msg.as_string())
            except Exception as e:
                return e


    async def sendSMS() -> None:
        ...