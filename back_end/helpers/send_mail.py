import smtplib
from email.mime.text import MIMEText


class SendMail:

    def __init__(self):
        self.sender_email = "jerrypatents@gmail.com"
        self.sender_email_password = "jerrypatents123"
        self.receiver_emails = ["madhawadias2@gmail.com", "ashenicas@gmail.com"]

    def runner(self, file_url, file_name):
        text = "Please refer following link to download the search result of {}  : {}".format(file_name, file_url)
        receive = ",".join(self.receiver_emails)

        msg = MIMEText(text)
        msg['Subject'] = 'Patent Extraction result of {}'.format(file_name)
        msg['From'] = self.sender_email
        msg['To'] = receive
        print("Email Body", msg)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.ehlo()
        s.login(self.sender_email, self.sender_email_password)
        s.sendmail(self.sender_email, self.receiver_emails, msg.as_string())
        print("Email Sent")
        s.quit()


SendMail().runner(file_name="rotaru", file_url="test url")
