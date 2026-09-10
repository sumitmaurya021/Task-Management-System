from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List


conf = ConnectionConfig(
    MAIL_USERNAME = "mauryasumit222@gmail.com",
    MAIL_PASSWORD = "vtyrunlkvvrqwgte",
    MAIL_FROM = "mauryasumit222@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Task Management System",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


async def send_email(emails:List[str]):
    html = """<p>Hi, <br><br>Thanks for registration. our team will connect you soon <br><br>Regards,<br>Task Management System</p> """

    message = MessageSchema(
        subject="Task Management System",
        recipients=emails,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "Email sent successfully"}