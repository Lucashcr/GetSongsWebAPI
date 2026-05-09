# Changelog

## [1.0.4](https://github.com/Lucashcr/GetSongsWebAPI/releases/tag/1.0.4) - 2026-05-08

### Adicionado

- Pipeline de CI/CD agora suporta build de imagens de pré-lançamento (ex: `1.0.4-rc1`, `1.0.4-dev1`) quando disparada manualmente via `workflow_dispatch` em branch fora da `main`. Imagens pré-lançamento recebem apenas a tag de versão exata, sem `latest`, aliases de `major`/`minor`, release no GitHub ou deploy.

### Alterado

- Jobs `deploy-railway` e `deploy-azure` agora só executam em builds estáveis (`push` na `main`).
- Step `Compute image tags` aplica guard clause com saída antecipada para o caminho de pré-lançamento, evolvendo ifs aninhados.
- Scripts shell dos novos steps utilizam `set -euo pipefail` para falha imediata.

### Corrigido

- Hostname do Azure Container Apps em `ALLOWED_HOSTS` agora é construído corretamente combinando `CONTAINER_APP_NAME` e `CONTAINER_APP_ENV_DNS_SUFFIX`, conforme a documentação oficial do Azure (`$CONTAINER_APP_NAME.$CONTAINER_APP_ENV_DNS_SUFFIX`).

## [1.0.3](https://github.com/Lucashcr/GetSongsWebAPI/releases/tag/1.0.3) - 2026-05-08

### Adicionado

- Ruff como ferramenta de formatação e linting, substituindo o Black.
- Configuração do Ruff no `pyproject.toml` com regras de estilo, pyflakes e isort.
- Steps `Check code formatting` e `Lint code` na pipeline de CI utilizando Ruff.
- Seção de dependências de desenvolvimento e subseção de qualidade de código no README.
- Template HTML (`gsauth/templates/gsauth/forgot_password_email.html`) para o e-mail de recuperação de senha renderizado via Django template engine.

### Alterado

- Imports genéricos (`from x import *`) substituídos por imports explícitos em `api/`, `core/`, `gsauth/` e `build_doc/`.
- `except` sem tipo substituído por exceções específicas (`Hymnary.DoesNotExist`, `PasswordRecoveryToken.DoesNotExist`, `IntegrityError`).

### Removido

- Black removido das dependências de desenvolvimento e da pipeline de CI.

## [1.0.2](https://github.com/Lucashcr/GetSongsWebAPI/releases/tag/1.0.2) - 2026-05-08

### Corrigido

- Correção na pipeline de deploy no Railway.

## [1.0.1](https://github.com/Lucashcr/GetSongsWebAPI/releases/tag/1.0.1) - 2026-05-08

### Alterado

- Configuração de `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` e `CORS_ORIGIN_WHITELIST` migrada para variáveis de ambiente, removendo referências hardcoded ao Railway.
- `CONTAINER_APP_HOSTNAME` (injetado automaticamente pelo Azure Container Apps) é adicionado a `ALLOWED_HOSTS` quando presente.
- `ALLOWED_HOSTS` aceita lista de hosts separados por vírgula via variável de ambiente, permitindo múltiplos domínios customizados.

## [1.0.0](https://github.com/Lucashcr/GetSongsWebAPI/releases/tag/1.0.0) - 2026-05-07

### Adicionado

- Catálogo de músicas com busca full-text via MeiliSearch.
- Gerenciamento de hinários (CRUD) com reordenação por drag-and-drop.
- Geração de PDF com múltiplos layouts via ReportLab.
- Autenticação de usuários (registro, login, recuperação de senha) com tokens DRF.
- Integração com Resend para envio de e-mails transacionais via django-anymail.
- Monitoramento de erros com Sentry SDK.
- Deploy configurado para Railway.
