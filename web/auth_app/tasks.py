from typing import Union, List

from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template import loader
from django.template.loader import get_template
from django.utils.translation import activate

from main.decorators import smtp_shell
from src.celery import app


def send_email(subject: str, template, content: dict, to_email: Union[str, List[str]]):
    html_content = template.render(content)
    send_mail(
        subject=subject,
        from_email=None,
        message='',
        recipient_list=[to_email] if isinstance(to_email, str) else to_email,
        html_message=html_content
    )


@app.task()
def send_verification_email(**kwargs):
    content = kwargs.get('content', {})
    to_email = kwargs.get('to_email')
    subject = 'Please Confirm Your E-mail Address'
    template = get_template('emails/verify_email.html')
    send_email(subject, template, content, to_email)


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
