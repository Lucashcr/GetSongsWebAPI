from services.email.base import EmailServiceBaseClass
from .strategy import EmailServiceStrategy


EmailService = EmailServiceStrategy.resolve("django")
