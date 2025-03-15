from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os

app = FastAPI(title="Mymail Backend")

# Configure FastAPI-Mail
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "your_email@mymail.local"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "your_password"),
    MAIL_FROM=os.getenv("MAIL_FROM", "your_email@mymail.local"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "mailserver"),
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)

class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    body: str

async def send_email(message: MessageSchema):
    fm = FastMail(conf)
    await fm.send_message(message)

@app.post("/send-email")
async def send_email_endpoint(email_data: EmailSchema, background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject=email_data.subject,
        recipients=[email_data.email],
        body=email_data.body,
        subtype="html"
    )
    background_tasks.add_task(send_email, message)
    return {"message": "Email queued for sending."}
