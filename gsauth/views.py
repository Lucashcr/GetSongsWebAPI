from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.translation import gettext_lazy as _

from gsauth.models import PasswordRecoveryToken
from mysite.settings import FRONTEND_BASE_URL, EMAIL_HOST_USER
from services.email import EmailService


class GetCurrentUserView(APIView):
    def get(self, request):
        data = model_to_dict(
            request.user,
            [
                "username",
                "email",
                "first_name",
                "last_name",
            ],
        )
        data["full_name"] = f"{data['first_name']} {data['last_name']}"
        return JsonResponse(data)


def validate_password(user, password):
    msg = []

    if len(password) < 8:
        msg.append(_("A senha deve ter no mínimo 8 caracteres"))

    if password.isdigit() or password.isalpha():
        msg.append(_("A senha deve conter letras e números"))

    if password.lower().find(user.username.lower()) != -1:
        msg.append(_("A senha não deve conter o nome de usuário"))

    if password.lower().find(user.first_name.lower()) != -1:
        msg.append(_("A senha não deve conter o primeiro nome"))

    if password.lower().find(user.last_name.lower()) != -1:
        msg.append(_("A senha não deve conter o último nome"))

    return msg


class RegisterUserView(APIView):
    permission_classes = []

    def post(self, request: HttpRequest):
        new_user = User(
            username=request.data.get("username"),
            email=request.data.get("email"),
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
        )

        if User.objects.filter(email=new_user.email).exists():
            return JsonResponse([_("Email já cadastrado")], status=400, safe=False)

        password = request.data.get("password")
        if msg := validate_password(new_user, password):
            return JsonResponse(msg, status=400, safe=False)

        new_user.set_password(password)

        try:
            validate_email(new_user.email)
            new_user.full_clean()
        except ValidationError as e:
            return JsonResponse(e.messages, status=400, safe=False)
        else:
            new_user.save()
            return JsonResponse(
                model_to_dict(
                    new_user, ["username", "email", "first_name", "last_name"]
                ),
                status=201,
            )


class SendEmailAPIView(APIView):
    def post(self, request):
        if not (message := request.data.get("message")):
            return HttpResponseBadRequest("Dados inválidos")

        full_name = f"{request.user.first_name} {request.user.last_name}"
        name = request.data.get("name", full_name)
        email = request.data.get("email", request.user.email)

        message = f"Usuário: {name}"
        message += f"\nEmail: {email}"
        message += f"\n\n{message}"

        email = EmailService(
            to_emails=[user.email for user in User.objects.filter(is_superuser=True)],
            subject="Contato - GetSongs",
        )
        email.set_plain_text_message(message)

        response = email.send()

        if response == 1:
            return HttpResponse("Email enviado com sucesso")

        return HttpResponse("Erro ao enviar email", status=500)


class ForgotPasswordAPIView(APIView):
    permission_classes = []

    def post(self, request):
        if not request.data.get("email"):
            return JsonResponse({"ok": False, "message": "Email não pode ser vazio"})

        try:
            user = User.objects.get(email=request.data["email"])
        except User.DoesNotExist:
            return JsonResponse({"ok": True, "message": "Email enviado com sucesso"})

        token = PasswordRecoveryToken.objects.create(user=user)

        message = f"<h1>Olá, {user.first_name}!</h1>"
        message += "<p>Para recuperar sua senha, clique no link abaixo:</p>"
        message += f'<div><a href="{FRONTEND_BASE_URL}/auth/recover-password?t={token.token}">Recuperar senha</a></div>'
        message += "<p>Se você não solicitou a recuperação de senha, desconsidere este email.</p>"

        response = send_mail(
            "Recuperação de senha - GetSongs",
            "",
            EMAIL_HOST_USER,
            [user.email],
            html_message=message,
            fail_silently=False,
        )

        if response == 1:
            return JsonResponse({"ok": True, "message": "Email enviado com sucesso"})

        return JsonResponse({"ok": False, "message": "Erro ao enviar email"})


class ResetPasswordAPIView(APIView):
    permission_classes = []

    def get(self, request):
        token = request.GET.get("t")
        if not token:
            return JsonResponse({"ok": False})

        try:
            token = PasswordRecoveryToken.objects.get(token=token)
        except:
            return JsonResponse({"ok": False})

        if not token.is_valid or token.expired:
            return JsonResponse({"ok": False})

        return JsonResponse({"ok": True})

    def post(self, request):
        if not all([request.data.get(fields) for fields in ("token", "password")]):
            return JsonResponse({"ok": False, "messages": ["Dados inválidos"]})

        try:
            token = PasswordRecoveryToken.objects.get(token=request.data["token"])
        except:
            return JsonResponse({"ok": False, "messages": ["Dados inválidos"]})

        user = token.user

        if msg := validate_password(user, request.data["password"]):
            return JsonResponse({"ok": False, "messages": msg})

        user.set_password(request.data["password"])
        user.save()

        token.delete()

        return JsonResponse({"ok": True, "messages": ["Senha alterada com sucesso"]})


class ChangePasswordAPIView(APIView):
    def post(self, request):
        if not all(
            [request.data.get(fields) for fields in ("old_password", "new_password")]
        ):
            return JsonResponse({"ok": False, "messages": ["Dados inválidos"]})

        user = request.user

        if not user.check_password(request.data["old_password"]):
            return JsonResponse({"ok": False, "messages": ["Senha atual incorreta"]})

        if msg := validate_password(user, request.data["new_password"]):
            return JsonResponse({"ok": False, "messages": msg})

        user.set_password(request.data["new_password"])
        user.save()

        return JsonResponse({"ok": True, "messages": ["Senha alterada com sucesso"]})
