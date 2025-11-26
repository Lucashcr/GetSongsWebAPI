from typing_extensions import Unpack
from services.email.strategy import EmailServiceBaseClass

from django.core.mail import send_mail

from services.email.types import EmailServiceInitOptions


class EmailService(EmailServiceBaseClass):
    def __init__(self, **init_options: Unpack[EmailServiceInitOptions]):
        super().__init__(**init_options)

    def send(self):
        self.validate()
        return send_mail(
            self._subject,
            self._body if not self._html else "",
            self._from_email,
            self._to_emails,
            fail_silently=False,
            html_message=self._body if self._html else None,
        )
