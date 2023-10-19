import smtplib, os
from log import logging_decorator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


@logging_decorator
def send_mail(
    mail_from: str,
    passw: str,
    mails_to: list[str],
    subject: str,
    message: str,
    server_smtp: str='smtp.office365.com',
    port_smtp: int = 587,
    attach=None) -> None:
    
    # Configuração do servidor SMTP
    server_smtp: str='smtp.office365.com'
    port_smtp: int = 587

    # Criar objeto MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = mail_from
    msg['To'] = ', '.join(mails_to)  # Converta p/ str sep= ','
    msg['Subject'] = subject

    # Adicionar corpo da message
    msg.attach(MIMEText(message, 'plain'))

    # Adicionar attach, se houver
    if attach:
        for path_attachment in attach:
            file_name = os.path.basename(path_attachment)
            attach_file = open(path_attachment, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attach_file).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % file_name)
            msg.attach(part)

    # Conectar ao servidor SMTP e enviar email
    try: 
        server = smtplib.SMTP(server_smtp, port_smtp)
        server.starttls()
        server.login(mail_from, passw)
        texto_email = msg.as_string()
        server.sendmail(mail_from, mails_to, texto_email)
        server.quit()
        print('Sent!')
        
    except smtplib.SMTPException as e:
        print('Error - Email not send: {e}')
