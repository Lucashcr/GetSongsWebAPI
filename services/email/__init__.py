from .strategy import EmailServiceStrategy

EmailService = EmailServiceStrategy.resolve("django")
