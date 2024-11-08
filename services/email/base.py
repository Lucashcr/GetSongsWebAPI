from typing import Any, Unpack

from django.conf import settings
from django.template.loader import render_to_string

from services.email.types import EmailServiceInitOptions


class EmailServiceBaseClass:
    def __init__(
        self, /, **kwargs: Unpack[EmailServiceInitOptions]
    ):
        default_from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
        self._from_email = kwargs.get("from_email", default_from_email)
        self._to_emails = kwargs.get("to_emails", [])
        self._subject = kwargs.get("subject")
        self._body = kwargs.get("body")
    
    def set_from_email(self, from_email: str):
        self._from_email = from_email
    
    def set_to_emails(self, to_emails: str):
        self._to_emails = to_emails
    
    def set_subject(self, subject: str):
        self._subject = subject
    
    def set_plain_text_message(self, body: str):
        self._body = body
        self._html = False
    
    def set_html_message(self, template: str, context: dict[str, Any]):
        self._body = render_to_string(template, context)
        self._html = True
    
    def validate(self):
        if not self._from_email:
            raise ValueError("From email is required")
        if not self._to_emails:
            raise ValueError("To email is required")
        if not self._subject:
            raise ValueError("Subject is required")
        if not self._body:
            raise ValueError("Body is required")

    def send(self): ...
