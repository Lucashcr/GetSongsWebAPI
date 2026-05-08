# GetSongsWebAPI

Somos uma plataforma de montagem e geração automática de hinários. Nosso serviço é especialmente projetado para ajudar músicos católicos a criar hinários personalizados com facilidade. Se você está procurando um hinário para um casamento, batizado, missa ou outro evento, o GetSongs é a escolha perfeita. Nosso compromisso de oferecer uma experiência de montagem de hinário fácil, rápida e conveniente para todos os tipos de eventos e ocasiões.

Aqui você pode montar seu hinário escolhendo entre uma ampla variedade de músicas disponíveis em nossa biblioteca e personalizá-lo de acordo com as suas necessidades. Além disso, nossa equipe está sempre atualizando a biblioteca com as últimas músicas e tendências, para garantir que você tenha acesso às músicas mais recentes e populares.

Após finalizar a montagem do hinário, o GetSongs pode, com apenas um clique, exportar automaticamente um documento em formato PDF com todas as letras das músicas na sequência estabelecida e com as configurações definidas pelo usuário. Isso significa que você pode ter acesso a seu hinário personalizado a qualquer momento, em qualquer lugar e em qualquer dispositivo, permitindo que você compartilhe seu hinário com facilidade.

Portanto, se você precisa de um hinário para uma ocasião especial, o GetSongs é a escolha perfeita. Obrigado por escolher o GetSongs. Experimente já nosso serviço e veja como é fácil criar seu próprio hinário personalizado.

[![Python](https://img.shields.io/badge/Python-3.14-blue.svg)](https://www.python.org/) [![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://www.djangoproject.com/) [![MeiliSearch](https://img.shields.io/badge/MeiliSearch-LATEST-green.svg)](https://github.com/meilisearch/MeiliSearch)

[![Django CI](https://github.com/Lucashcr/GetSongsWebAPI/actions/workflows/main.yml/badge.svg)](https://github.com/Lucashcr/GetSongsWebAPI/actions/workflows/main.yml)

## Requisitos

| Dependência | Versão |
| - | - |
| Python | 3.14+ |
| Django | 5.2.8+ |
| Django REST Framework | 3.16.1+ |
| Gunicorn | 23.0.0+ |
| psycopg | 3.2.13+ |
| Pillow | 12.0.0+ |
| python-dotenv | 1.2.1+ |
| httpx | 0.28.1+ |
| Meilisearch | 0.38.0+ |
| Reportlab | 4.4.5+ |
| Beautiful Soup | 0.0.2+ |
| django-cors-headers | 4.9.0+ |
| dj-database-url | 3.0.1+ |
| django-anymail[resend] | 14.0+ |
| WhiteNoise | 6.11.0+ |
| drf-spectacular | 0.29.0+ |
| sentry-sdk[django] | 2.46.0+ |

_Vide pyproject.toml_

## Variáveis de ambiente

Copie o arquivo de exemplo e preencha com seus valores:

```bash
cp .env.example .env
```

| Variável | Descrição |
| - | - |
| `DEBUG` | Modo debug do Django (`True` em desenvolvimento) |
| `SECRET_KEY` | Chave secreta do Django |
| `DATABASE_URL` | URL de conexão PostgreSQL |
| `FRONTEND_BASE_URL` | URL base do frontend (usada em e-mails e CORS) |
| `MEILI_URL` | URL da instância Meilisearch |
| `MEILI_MASTER_KEY` | Chave mestre do Meilisearch |
| `EMAIL_HOST_USER` | Endereço de e-mail remetente (Resend) |
| `EMAIL_HOST_PASSWORD` | API key do Resend |
| `SENTRY_DSN` | DSN do Sentry para error tracking (opcional) |

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/Lucashcr/GetSongsWebAPI.git
```

2. Entre no diretório do projeto:

```bash
cd GetSongsWebAPI/backend
```

3. Instale o Poetry (gerenciador de dependências):

```bash
pip install poetry
```

4. Instale as dependências:

```bash
poetry install
```

5. Configure as variáveis de ambiente:

```bash
cp .env.example .env
```

6. Execute as migrações do banco de dados:

```bash
poetry run python manage.py migrate
```

## Uso

Execute o servidor de desenvolvimento:

```bash
poetry run python manage.py runserver
```

Acesse o projeto em [http://localhost:8000/](http://localhost:8000/)

### Indexar músicas no Meilisearch

Para popular o índice de busca com as músicas do banco de dados:

```bash
poetry run python manage.py populate songs
```

Para reconstruir o índice do zero:

```bash
poetry run python manage.py rebuild songs
```

### Testes

Execute a suite de testes com:

```bash
poetry run pytest
```

### Docker

Build da imagem:

```bash
docker build -t getsongs-api .
```

Execução do container:

```bash
docker run -p 8000:8000 --env-file .env getsongs-api
```

## Contribuição

1. Faça o fork do projeto (<https://github.com/seu_usuario/seu_projeto/fork>)
2. Crie uma branch para sua modificação (`git checkout -b feature/sua_feature`)
3. Faça o commit (`git commit -am 'Adicione sua feature'`)
4. Faça o push para a branch (`git push origin feature/sua_feature`)
5. Crie um novo Pull Request

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Se você tiver dúvidas ou sugestões, por favor entre em contato.
