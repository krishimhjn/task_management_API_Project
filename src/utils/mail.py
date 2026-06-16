from fastapi_mail import (
    FastMail,
    MessageSchema,
    ConnectionConfig,
    MessageType,
)
from typing import List
from src.utils.settings import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_USERNAME,
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Krishi Mahajan",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_email(emails: List[str]):
    html = """
    <html>
        <body>
            <h2>Registration Successful</h2>
            <p>Hello,</p>
            <p>Thank you for registering with us.</p>
            <p>Welcome aboard!</p>
            <br>
            <p>Regards,</p>
            <p>Krishi Mahajan</p>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="Registration Confirmation",
        recipients=emails,
        body=html,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)

    await fm.send_message(message)

    return {
        "message": "Email sent successfully"
    }