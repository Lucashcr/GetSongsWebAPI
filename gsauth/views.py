from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.utils.translation import gettext_lazy as _

from mysite import settings


class GetCurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = model_to_dict(request.user, [
            'username',
            'email',
            'first_name',
            'last_name',
        ])
        data['full_name'] = f"{data['first_name']} {data['last_name']}"
        return JsonResponse(data)


class RegisterUserView(APIView):
    permission_classes = []

    def validate_password(self):
        msg = []
        user = self.request.data

        if len(user['password']) < 8:
            msg.append(_('A senha deve ter no mínimo 8 caracteres'))

        if user['password'].isdigit() or user['password'].isalpha():
            msg.append(_('A senha deve conter letras e números'))

        if user['password'].lower().find(user.get('username').lower()) != -1:
            msg.append(_('A senha não deve conter o nome de usuário'))

        if user['password'].lower().find(user.get('first_name').lower()) != -1:
            msg.append(_('A senha não deve conter o primeiro nome'))

        if user['password'].lower().find(user.get('last_name').lower()) != -1:
            msg.append(_('A senha não deve conter o último nome'))

        return msg

    def post(self, request: HttpRequest):
        new_user = User(
            username=request.data.get('username'),
            email=request.data.get('email'),
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),
        )

        password = request.data.get('password')
        new_user.set_password(password)

        if User.objects.filter(email=new_user.email).exists():
            return JsonResponse(
                [_('Email já cadastrado')],
                status=400,
                safe=False
            )

        if msg := self.validate_password():
            return JsonResponse(msg, status=400, safe=False)

        try:
            validate_email(new_user.email)
            new_user.full_clean()
        except ValidationError as e:
            return JsonResponse(e.messages, status=400, safe=False)
        else:
            new_user.save()
            return JsonResponse(
                model_to_dict(
                    new_user, ['username', 'email', 'first_name', 'last_name']
                ),
                status=201
            )


class SendEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not all([
            request.data.get(fields)
            for fields in ('name', 'email', 'message')
        ]):
            return HttpResponseBadRequest('Dados inválidos')

        message = f'Usuário: {request.data["name"]}'
        message += f'\nEmail: {request.data["email"]}'
        message += f'\n\n{request.data["message"]}'

        response = send_mail(
            'Contato - GetSongs',
            message,
            settings.EMAIL_HOST_USER,
            ['lucash.rocha123@gmail.com'],
            fail_silently=False,
        )

        if response == 1:
            return HttpResponse('Email enviado com sucesso')

        return HttpResponse('Erro ao enviar email', status=500)
