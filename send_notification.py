import smtplib
import os
from email.message import EmailMessage


def send_email():
    # As variáveis são puxadas do GitHub Actions (Secrets)
    email_sender = os.environ.get("EMAIL_USER")
    email_password = os.environ.get("EMAIL_PASS")
    # nao pode conter o email do destinatário no código)
    email_receiver = os.environ.get("EMAIL_RECEIVER")

    msg = EmailMessage()
    msg['Subject'] = "Status do Pipeline CI/CD - Mercadinho"
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg.set_content(
        "O pipeline foi finalizado com sucesso! ✅\n\nOs testes passaram e o deploy foi realizado.")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(msg)
        print("Notificação enviada com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")


if __name__ == "__main__":
    send_email()
