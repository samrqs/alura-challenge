import smtplib
import os

from flask_mail import Message
from flask import render_template

from app import mail
from app.metrics import feedbacks_week, generate_summary

def send_email():

    data = feedbacks_week()

    if data["total_feedbacks"] == 0:
        print("Sem feedbacks na última semana.")
        return

    summary = generate_summary(data)

    # Renderiza o HTML com os dados
    email_body = render_template(
        "summary.html",
        total=data["total_feedbacks"],
        positivos=data["porcentagem_positivos"],
        negativos=data["porcentagem_negativos"],
        funcionalidades=data["funcionalidades"],
        resumo=summary
    )

    msg = Message(
        subject="Resumo Semanal de Feedbacks",
        recipients=[os.getenv('MAIL_DESTINATARIO')],
        html=email_body
    )

    try:
        mail.send(msg)
        print("Resumo enviado com sucesso!")
    except Exception as e:
        print("Erro ao enviar e-mail:", e)
