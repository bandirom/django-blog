from typing import Union
from os import environ
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.translation import activate

from main.decorators import smtp_shell
from src.celery import app


@app.task()
def send_information_email(
    subject: str, html_email_template_name: str, context: dict, to_email: Union[list[str], str],
    letter_language: str = 'en', file_url: str = None, **kwargs
):
    activate(letter_language)
    to_email = [to_email] if isinstance(to_email, str) else to_email
    email_message = EmailMultiAlternatives(subject=subject, to=to_email, bcc=kwargs.get('bcc'), cc=kwargs.get('cc'))
    html_email = loader.render_to_string(html_email_template_name, context)
    email_message.attach_alternative(html_email, 'text/html')
    if file_url:
        file_url = environ.get('APP_HOME', environ.get('HOME')) + file_url
        email_message.attach_file(file_url, kwargs.get('mimetype'))
    send_email(email_message)


@smtp_shell
def send_email(email_message):
    email_message.send()
