# send_alerts.py

"""This modules sends email alerts for jobs"""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self, user_id, password, recipient_address=None, subject="", recipient_name=""):
        self.user_id = user_id
        self.password = password
        self.recipient_addr = recipient_address
        self.recipient_name = recipient_name
        self.__contents__ = None
        self.__server__ = None
        self.subject = subject

    def mail_props(self):
        self.__contents__ = MIMEMultipart("alternative")
        self.__contents__["Subject"] = self.subject
        self.__contents__["From"] = self.user_id
        self.__contents__["To"] = self.recipient_addr

    # composing mail body in two formats - plain text & html
    def compose_email(self, result_count, results_text, results_html):
        text = f"""\
        Hi {self.recipient_name},
        
        Your Job alert has fetched {result_count} results. Results are available below.
        
        {results_text}
        """

        html = f"""\
        <html>
            <body>
                <p><b>Hi {self.recipient_name},</b><br>
                <br>
                Your Job alert has fetched {result_count} results. Results are available below.<br>
                <br>
                {results_html}
                </p>
            </body>
        </html>
        """

        part_1 = MIMEText(text, "plain")
        part_2 = MIMEText(html, "html")

        self.__contents__.attach(part_1)
        self.__contents__.attach(part_2)

    def login_server(self):
        self.__server__ = smtplib.SMTP_SSL("smtp.gmail.com", 465,
                                           context=ssl.create_default_context(),
                                           )
        try:
            self.__server__.login(self.user_id, self.password)
            return True
        except smtplib.SMTPAuthenticationError:
            return False
        except smtplib.SMTPServerDisconnected:
            self.__server__.connect()

    def close_server(self):
        self.__server__.quit()

    def send_email(self):
        self.__server__.sendmail(self.user_id, self.recipient_addr, self.__contents__.as_string())


def send_alert(user_addr, user_pass, text_form, html_form, res_num, recp_name, recp_addr, subj):
    mail_box = Email(user_id=user_addr,
                     password=user_pass,
                     )
    status = mail_box.login_server()
    if status:
        mail_box.recipient_name = recp_name
        mail_box.recipient_addr = recp_addr
        mail_box.subject = subj

        mail_box.mail_props()
        mail_box.compose_email(res_num, text_form, html_form)
        mail_box.send_email()
        mail_box.close_server()
    else:
        print("Invalid UserName/Password")
    return status


if __name__ == "__main__":
    import os
    send_alert(os.environ["test_sender"], os.environ["test_pass"], "result_1",
               "result_1<br>", 1, "John", os.environ["test_receiver"], "Test"
               )
