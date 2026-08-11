import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Yandex configuration:
SMTP_SERVER_YANDEX = "smtp.yandex.ru"
SMTP_PORT_YANDEX = 465
SENDER_EMAIL_YANDEX = "rychalovser@yandex.ru"
SENDER_PASSWORD_YANDEX = "thdoxplbwpsblplv"

#google configuration:
SMTP_SERVER_GOOGLE = "smtp.gmail.com"
SMTP_PORT_GOOGLE = 587
SENDER_EMAIL_GOOGLE = "rychalovser@gmail.com"
SENDER_PASSWORD_GOOGLE = "vuegowzzeaqlmelf"

def send_recovery_email(receiver_email: str, new_password: str):
    try:
        if receiver_email.strip(' ').endswith('yandex.ru'):
            #here we create a structure of the letter
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL_YANDEX
            msg['To'] = receiver_email
            msg['Subject'] = "Password Recovery" #topic of the letter
            body = f"""
            Hello!
            You requested a password reset.
            Your new temporary password is: {new_password}      
            Please log in and change it immediately for security reasons.
            """
            msg.attach(MIMEText(body,'plain','utf-8'))
            #here we connect to the yandex server
            server = smtplib.SMTP_SSL(SMTP_SERVER_YANDEX,SMTP_PORT_YANDEX,timeout=10)
            #here we are loging...:
            server.login(SENDER_EMAIL_YANDEX, SENDER_PASSWORD_YANDEX)
            #and here we are sending the letter:(msg.as_string() - gathers all elements like text and subject into one letter)
            server.sendmail(SENDER_EMAIL_YANDEX,receiver_email,msg.as_string())
            server.quit()

        elif receiver_email.strip(' ').endswith('gmail.com'):
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL_GOOGLE
            msg['To'] = receiver_email
            msg['Subject'] = "Password Recovery"
            body = f"""
            Hello!
            You requested a password reset.
            Your new temporary password is: {new_password}      
            Please log in and change it immediately for security reasons.
            """
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            server = smtplib.SMTP(SMTP_SERVER_GOOGLE,SMTP_PORT_GOOGLE,timeout=10)
            server.starttls()
            server.login(SENDER_EMAIL_GOOGLE,SENDER_PASSWORD_GOOGLE)
            server.sendmail(SENDER_EMAIL_GOOGLE,receiver_email,msg.as_string())
            server.quit()

        return True
    except Exception as error:
        print(f'Error happened during sending: {error}')
        return False

