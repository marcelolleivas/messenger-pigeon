import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from messenger.utils import template_render


class NotificationService(object):
    """
    Principal class, where everything is prepared and e-mail is sent.

    Attributes:
        - access_email(str): e-mail that will be used to log in on SMTP.
        It should be gmail.
        - password(str): password of the e-mail that will be used. You must
        configure it following the steps on this link:
        https://devanswers.co/create-application-specific-password-gmail/
    """

    def __init__(self, access_email, password):
        self.access_email = access_email
        self.password = password

    @staticmethod
    def _check_attachment(attachment, attachment_name, subtype, mime):
        """
        Method checking attachment and adding it to mime if exists
        :param attachment: file that will be attached;
        :param attachment_name: name the attachment will have on email;
        :param subtype: the attachment subtype;
        :param mime.
        """
        if attachment:
            if attachment_name and subtype:
                mime.attach(
                    MIMEApplication(
                        attachment, Name=attachment_name, _subtype=subtype
                    )
                )
            else:
                pass

    def _send_email(self, email_from, email_to, message):
        """
        Create secure connection using ssl.create_default_context() and then
        send the email using SMTP
        :param email_from (str): sender e-mail
        :param email_to (str): receiver e-mail
        :param message (MIMEMultipart): mime with all content that will be sent
        on email
        """
        ssl.create_default_context()

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self.access_email, self.password)
            server.sendmail(email_from, email_to, message.as_string())

    def send_notification(
        self,
        template_path,
        template_name,
        email_from,
        email_to,
        subject,
        attachment=None,
        attachment_name=None,
        subtype=None,
    ):
        """
        Principal method from the class. It prepares everything and then
        sends the e-mail
        :param template_path : path where it will look for the template
        to be rendered
        :param template_name: name of the template to be rendered
        :param email_from: sender e-mail
        :param email_to: receiver e-mail
        :param subject: subject from the e-mail
        :param attachment: the attachment content, in bytes
        :param attachment_name: the attachment name
        :param subtype: the subtype of the attachment
        """
        message = MIMEMultipart("alternative")
        message["From"] = email_from
        message["To"] = email_to
        message["Subject"] = subject

        self._check_attachment(
            attachment, attachment_name, subtype, mime=message
        )

        content = template_render(template_path, template_name)

        message.attach(MIMEText(content, "html"))

        self._send_email(email_from, email_to, message)
