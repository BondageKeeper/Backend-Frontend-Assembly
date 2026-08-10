import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = "smtp.yandex.ru"
SMTP_PORT = 465

SENDER_EMAIL = "[HERE IS YOUR MAIL]"
SENDER_PASSWORD = "thdoxplbwpsblplv"

def send_recovery_email(receiver_email: str, new_password: str):
    try:
        #here we create a structure of the letter
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
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
        server = smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT)
        #here we are loging...:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        #and here we are sending the letter:(msg.as_string() - gathers all elements like text and subject into one letter)
        server.sendmail(SENDER_EMAIL,receiver_email,msg.as_string())

        server.quit()
        return True

    except Exception as error:
        print(f'Error happened during sending: {error}')
        return False

