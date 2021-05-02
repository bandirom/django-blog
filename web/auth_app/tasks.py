from typing import Union, List

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.translation import activate

from main.decorators import smtp_shell
from src.celery import app


@app.task()
def send_information_email(
    subject: str, html_email_template_name: str,
    context: dict, to_email: Union[List[str], str], letter_language: str = 'en'
):
    activate(letter_language)
    to_email = [to_email] if isinstance(to_email, str) else to_email
    email_message = EmailMultiAlternatives(subject=subject, to=to_email)
    html_email = loader.render_to_string(html_email_template_name, context)
    email_message.attach_alternative(html_email, 'text/html')
    send_email(email_message)


@smtp_shell
def send_email(email_message):
    email_message.send()
