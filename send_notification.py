import smtplib
import os
from email.message import EmailMessage


def send_email():
    # As variáveis são puxadas do GitHub Actions (Secrets)
    email_sender = os.environ.get("EMAIL_USER")
    email_password = os.environ.get("EMAIL_PASS")

    # Recebe a string de e-mails do GitHub Secrets
    # Exemplo esperado na Secret: e-mail1@teste.com, e-mail2@teste.com
    email_receiver_raw = os.environ.get("EMAIL_RECEIVER")

    if not email_receiver_raw:
        print("Erro: Variável EMAIL_RECEIVER não configurada.")
        return

    # Transforma a string em uma lista de e-mails reais
    receivers_list = [addr.strip() for addr in email_receiver_raw.split(',')]

    msg = EmailMessage()
    msg['Subject'] = "Status do Pipeline CI/CD - Mercadinho"
    msg['From'] = email_sender
    msg['To'] = ", ".join(receivers_list)  # Exibe todos os destinatários no cabeçalho
    msg.set_content(
        "O pipeline foi finalizado com sucesso! ✅\n\n"
        "Status: Os testes unitários passaram e o deploy foi realizado conforme os requisitos.\n\n"
        "Atividade: C14 - Engenharia de Software [cite: 4]"
    )

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_sender, email_password)
            # Envia para a lista completa de destinatários
            smtp.send_message(msg)
        print(f"Notificação enviada com sucesso para: {len(receivers_list)} destinatário(s)!")
    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")


if __name__ == "__main__":
    send_email()