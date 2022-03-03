from twilio.rest import Client
import smtplib

TWILIO_SID = "ACb9bd00773b02b240af801a3d935f2e86"
TWILIO_TOKEN = "028093cdc1a70e153e82527121d18f41"
TWILIO_VIRTUAL_NUM = "+19105698924"
TWILIO_VER_NUM = "+234 706 352 9084"

MY_EMAIL = "deeyuan0@gmail.com"
PASSWORD = "Cupid80dipuC"


class NotificationManager:

    def __init__(self):
        self.client = Client(
            TWILIO_SID,
            TWILIO_TOKEN
        )

    def send_sms(self, text):
        message = self.client.messages.create(
            body=text,
            from_=TWILIO_VIRTUAL_NUM,
            to=TWILIO_VER_NUM
        )
        print(message.sid)

    def send_emails(self, emails, message, link):
        try:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(
                    user=MY_EMAIL,
                    password=PASSWORD
                )
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject: New Low Price Alert!\n\n{message}\n{link}".encode('utf-8')
                )
        except smtplib.SMTPConnectError as e:
            print(e)
