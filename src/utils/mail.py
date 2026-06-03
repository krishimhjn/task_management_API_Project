from fastapi_mail import FastMail,MessageSchema,ConnectionConfig,MessageType
from pydantic import EmailStr,BaseModel
from typing import List
from src.utils.settings import settings






conf = ConnectionConfig(
    MAIL_USERNAME =settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = "krishimhjn@gmail.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Krishi Mahajan",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


async def send_email(emails: List[str]):
    html="""<p> Hello , Thank you registration ,Krishi Mahajan this side</p>"""
    message = MessageSchema(
        subject="Rgistration Confirmation",
        recipients=emails,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message":"email has been sent"}