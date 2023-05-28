from django.conf import settings
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Send_Mail_Service:
    @classmethod
    def send_mail(cls, html=None, content_main_body='content', header='Header', from_email='', to_emails=[]):
        assert isinstance(to_emails, list)
        msg = MIMEMultipart('alternative')
        msg['FROM'] = from_email
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = header
        txt_part = MIMEText(content_main_body, 'plain')
        msg.attach(txt_part)

        if html:
            html_part = MIMEText(html, 'html')
            msg.attach(html_part)

        msg_str = msg.as_string()
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        server.ehlo()
        server.starttls()
        server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
        server.sendmail(from_email, to_emails, msg_str)
        server.quit()
