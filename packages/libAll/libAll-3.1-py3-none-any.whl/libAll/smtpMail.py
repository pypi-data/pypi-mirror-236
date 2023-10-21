import smtplib
from email.mime.text import MIMEText


class smtpMail_C():
    soutput = True
    output = False
    host = None
    mail = None

    def connect(self, address="smtp.gmail.com", port=587, typet="tls"):
        try:
            if typet == "tls":
                self.host = smtplib.SMTP(address, port)
                self.host.starttls()
            elif typet == "ssl":
                self.host = smtplib.SMTP_SSL(address, port)
            else:
                if self.soutput == True:
                    return "Unknown type"
                else:
                    self.output = "Unknown type"
                    return "error"


        except Exception as ex:
            if self.soutput == True:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"

    def login(self, email, password):
        try:
            self.mail = email
            self.host.login(email, password)
        except Exception as ex:
            if self.soutput == True:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"

    def send(self, from_mail, to_mail, subject_text, message_text):
        try:
            msg = MIMEText(message_text)
            msg["Subject"] = subject_text
            self.host.sendmail(from_mail, to_mail, msg.as_string())
        except Exception as ex:
            if self.soutput == True:
                return ('error ', ex)
            else:
                self.output = ('error ', ex)
                return "error"
