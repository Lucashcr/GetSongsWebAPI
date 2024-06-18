# GSAUTH

a app *gsauth* é responsável por estender as funcionalidades de autenticação e gerenciamento de usuários da aplicação. Apesar do Django já fornecer um sistema de autenticação pronto, este app provê recuperação de senha, registro de usuário, troca e recuperação de senha via API REST para serem utilizadas pelo frontend.

## Modelos (Models)

Os dados estão estruturados em um modelo entidade-relacionamento que pode ser resumido no diagrama a seguir:

[DIAGRAMA]

Para este *app*, tem-se apenas um modelo responsável por gerenciar os dados de recuperação de senha. Ao solicitar a recuperação de senha, Um novo registro é criado com um novo *token* e um email é enviado para o usuário com um link que expira em 30 minutos.

Esse registro é usado por questões de segurança para garantir que o acesso à página foi feito uma única vez e apenas pelo link enviado para o email. Além disso, ele contém a informação do usuário que solicitou a recuperação, permitindo a troca da senha.

## Rotas

Para utilizar a API e fazer as consultas, são disponibilizadas os 7 *endpoints* listados a seguir:

### Dados de usuário corrente

**Descrição:** Retorna os dados de perfil do usuário corrente.

```http
GET /user/me/
```

Exemplo de resposta:

```json
// RESPONSE 200 OK
{
    "username": "testuser",
    "first_name": "Usuário",
    "last_name": "Teste",
    "email": "testuser@email.com",
    "full_name": "Usuário Teste"
}
```

### Registro de usuários

**Descrição:** Responsável pela ação de registrar novos usuários na aplicação.

```http
POST /user/register/
{
    "username": "testuser",
    "first_name": "Usuário",
    "last_name": "Teste",
    "email": "testuser@email.com",
    "password": "p4sst3st"
}
```

Exemplo de resposta:

```json
// RESPONSE 200 OK
{
    "username": "testuser",
    "first_name": "Usuário",
    "last_name": "Teste",
    "email": "testuser@email.com"
}
```

### Envio de email de contato

**Descrição:** Responsável pela ação de enviar os emails de mensagens enviadas via formulário de contato.

```http
POST /user/sendmail/
{
    "name?": "Usuário Teste",
    "email?": "testuser@email.com",
    "message": "..."
}
```

Exemplo de resposta:

```json
// RESPONSE 200 OK
Email enviado com sucesso
```

### Solicitação de recuperação de senha

**Descrição:** Responsável pela ação de validar e registrar uma solicitação de recuperação de senha e enviar email ao usuário com instruções e link para recuperar senha.

```http
POST /user/forgot-password/
{
    "email": "testuser@email.com"
}
```

Exemplo de resposta:

```json
// RESPONSE 200 OK
{
    "ok": True,
    "message": "Email enviado com sucesso"
}
```

### Recuperação de senha

**Descrição:** Responsável pela ação de validar o token de recuperação de senha e enviar os dados com a nova senha para recuperação.

```http
GET /user/reset-password/

POST /user/reset-password/
{
    "token": "...",
    "password": "p4sst3st"
}
```

Exemplo de resposta:

```json
// RESPONSE 200 OK
{
    "ok": True,
    "messages": ["Senha alterada com sucesso"]
}
```

### Troca de senha

**Descrição:** Responsável pela ação de alterar a senha do usuário corrente.

```http
POST /user/change-password/
{
    "old_password": "0ldp4sst3st",
    "new_password": "n3wp4sst3st"
}
```

Exemplo de resposta:

```json
// RESPONSE 200 OK
{
    "ok": True,
    "messages": ["Senha alterada com sucesso"]
}
```
