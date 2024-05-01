# GetSongsWebAPI

Somos uma plataforma de montagem e geração automática de hinários. Nosso serviço é especialmente projetado para ajudar músicos católicos a criar hinários personalizados com facilidade. Se você está procurando um hinário para um casamento, batizado, missa ou outro evento, o GetSongs é a escolha perfeita. Nosso compromisso de oferecer uma experiência de montagem de hinário fácil, rápida e conveniente para todos os tipos de eventos e ocasiões.

Aqui você pode montar seu hinário escolhendo entre uma ampla variedade de músicas disponíveis em nossa biblioteca e personalizá-lo de acordo com as suas necessidades. Além disso, nossa equipe está sempre atualizando a biblioteca com as últimas músicas e tendências, para garantir que você tenha acesso às músicas mais recentes e populares.

Após finalizar a montagem do hinário, o GetSongs pode, com apenas um clique, exportar automaticamente um documento em formato PDF com todas as letras das músicas na sequência estabelecida e com as configurações definidas pelo usuário. Isso significa que você pode ter acesso a seu hinário personalizado a qualquer momento, em qualquer lugar e em qualquer dispositivo, permitindo que você compartilhe seu hinário com facilidade.

Portanto, se você precisa de um hinário para uma ocasião especial, o GetSongs é a escolha perfeita. Obrigado por escolher o GetSongs. Experimente já nosso serviço e veja como é fácil criar seu próprio hinário personalizado.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/) [![Django](https://img.shields.io/badge/Django-5.0-green.svg)](https://www.djangoproject.com/) [![MeiliSearch](https://img.shields.io/badge/MeiliSearch-LATEST-green.svg)](https://github.com/meilisearch/MeiliSearch)

## Requisitos

|Dependência|Versão|
|-|-|
|Python|3.11|
|Django|5.0|
|Django REST Framework|3.14|
|Gunicorn|2.12|
|Beautiful Soup|4.12|
|httpx|0.25|
|Meilisearch|0.30|
|Reportlab|4.0|

_Vide requirements.txt_

## Instalação

1. Clone o repositório:

> git clone https://github.com/Lucashcr/GetSongsWebAPI.git

2. Entre no diretório do projeto:

> cd GetSongsWebAPI

3. Instale as dependências:

> pip install -r requirements.txt

4. Execute as migrações do banco de dados:

> python manage.py migrate

## Uso

Execute o servidor de desenvolvimento:

> python manage.py runserver

Acesse o projeto em [http://localhost:8000/](http://localhost:8000/)

## Contribuição

1. Faça o fork do projeto (https://github.com/seu_usuario/seu_projeto/fork)
2. Crie uma branch para sua modificação (`git checkout -b feature/sua_feature`)
3. Faça o commit (`git commit -am 'Adicione sua feature'`)
4. Faça o push para a branch (`git push origin feature/sua_feature`)
5. Crie um novo Pull Request

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Se você tiver dúvidas ou sugestões, por favor entre em contato.