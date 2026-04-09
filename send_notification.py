import smtplib
import os
from email.message import EmailMessage


def send_email():
    # As variáveis são puxadas do GitHub Actions (Secrets)
    email_sender = os.environ.get("EMAIL_USER")
    email_password = os.environ.get("EMAIL_PASS")

    # Recebe a string de e-mails do GitHub Secrets
    # Exemplo esperado na Secret: email1@teste.com, email2@teste.com
    email_receiver_raw = os.environ.get("EMAIL_RECEIVER")

    if not email_receiver_raw:
        print("Erro: Variável EMAIL_RECEIVER não configurada.")
        return

    # Lê o status real de cada job passado como variável de ambiente
    status_test = os.environ.get("STATUS_TEST", "unknown")
    status_build = os.environ.get("STATUS_BUILD", "unknown")
    status_deploy = os.environ.get("STATUS_DEPLOY", "unknown")

    # Define o status geral do pipeline
    todos_ok = all(s == "success" for s in [
                   status_test, status_build, status_deploy])
    status_geral = "✅ SUCESSO" if todos_ok else "❌ FALHA"

    # Transforma a string em uma lista de e-mails
    receivers_list = [addr.strip() for addr in email_receiver_raw.split(',')]

    msg = EmailMessage()
    msg['Subject'] = f"[CI/CD] Pipeline Mercadinho — {status_geral}"
    msg['From'] = email_sender
    msg['To'] = ", ".join(receivers_list)
    msg.set_content(
        f"O pipeline de CI/CD foi finalizado.\n\n"
        f"Status Geral: {status_geral}\n\n"
        f"  • Testes:  {status_test}\n"
        f"  • Build:   {status_build}\n"
        f"  • Deploy:  {status_deploy}\n\n"
        f"Atividade: C14 - Engenharia de Software — Inatel"
    )

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(msg)
        print(
            f"Notificação enviada com sucesso para: {len(receivers_list)} destinatário(s)!")
    except Exception as e:
        print(f"Erro ao enviar notificação: {e}")


if __name__ == "__main__":
    send_email()
