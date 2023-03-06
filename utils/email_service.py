import os
from os import getenv
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class EmailService:
    def __init__(self) -> None:
        load_dotenv()
        self.__email_service = getenv("EMAIL_SERVICE")
        self.__sengrid_api_key = getenv('SENDGRID_API_KEY')

    def send_an_email(self, destinatary_email, subject, message_body):
        message = Mail(
            from_email=self.__email_service,
            to_emails=destinatary_email,
            subject=subject,
            html_content=f"<strong>{message_body}</strong>")
        try:
            sendgrid_client = SendGridAPIClient(
                "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")
            response = sendgrid_client.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as exc:
            raise exc