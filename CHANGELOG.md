# Changelog

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
