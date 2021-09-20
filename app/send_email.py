from flask import render_template
from flask_mail import Message
import os
from dotenv import load_dotenv
from .commands import mail

load_dotenv()


def mail_message(subject, template, to, **kwargs):
    sender_email = os.environ.get('MAIL_USERNAME')
    email = Message(subject, sender=sender_email, recipients=[to])
    email.body = render_template(template + ".txt", **kwargs)
    email.html = render_template(template + ".html", **kwargs)
    mail.send(email)
