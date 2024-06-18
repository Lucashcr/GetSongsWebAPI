# API

A API do projeto é responsável pelo acesso ao banco de dados de músicas, servindo através de uma API RESTFUL os endpoints para obtenção dos dados de categorias, artistas e músicas, bem como ações de filtro das consultas.

## Modelos (Models)

Os dados estão estruturados em um modelo entidade-relacionamento que pode ser resumido no diagrama a seguir:

[DIAGRAMA]

Resumindo, tem-se três tabelas. A primeira tabela é a de Categorias. Ela é responsável por organizar o catálogo de categorias possíveis para uma música. O GetSongsWeb possui um total de 10 categorias, classificando as músicas com relação à sua função litúrgica dentro de uma celebração. São elas:

|ID (id)|Nome (name)|Slug (slug)|
|-|-|-|
|1|Canto de Entrada|entrada|
|2|Ato Penitencial|ato=penitencial|
|3|Hino de Louvor|gloria|
|4|Aclamação ao Evangelho|aclamacao-evangelho|
|5|Ofertório|ofertorio|
|6|Santo|santo|
|7|Cordeiro|cordeiro|
|8|Comunhão|comunhao|
|9|Canto Final|final|
|10|Diversas|diversas|

Tem-se também a tabela de Artistas. Esta, por sua vez, tem por objetivo guardar os dados relativos aos artistas das músicas, permitindo classificar as músicas entre seus artistas.

Por fim, a tabela de Músicas é a principal deste módulo e armazena os dados de todas as músicas da aplicação. Ao contrário das anteriores, esta é mais dinâmica, pois deve crescer constantemente à medida que novas músicas são cadastradas para ficar disponíveis para utilização por parte dos usuários.

## Índice de busca (Meilisearch)

Além da busca no banco de dados, este módulo também é encarregado de gerenciar o índice de busca do Meilisearch.

A princípio, foi criado um _signal_ do tipo _post save_ para o modelo de Músicas de modo que, ao criar ou atualizar um registro, ele é automaticamente indexado para o Meilisearch. Entretanto, se o registro for criado ou alterado direto no banco de dados o dado não será indexado, apenas quando é feito pela interface de administração da aplicação.

Para suprir esta limitação e exapndir as possibilidades de gerenciamento, foram criados comandos do Django:

### Populate

O comando `populate` é responsável por indexar os documentos de músicas no Meilisearch, fazendo a atualização dos documentos a partir de todos os registros presentes no banco de dados.

Para executá-lo:

```sh
python manage.py populate songs
```

### Rebuild

Já o comando `rebuild` faz uma atualização por completo do índice, não só dos documentos, ou seja, ele reconstrói o índice por completo, deletando todos os documentos, indexando-os novamente e atualizando os campos de filtro.

Para executá-lo:

```sh
python manage.py rebuild songs
```

## Rotas

Para utilizar a API e fazer as consultas, são disponibilizadas os 7 _endpoints_ listados a seguir:

### Listagem das categorias

**Descrição:** Lista todos os registros de categorias cadastrados no banco de dados.

```http
GET /api/category
```

Exemplo de resposta:

```json
// RESPONSE 200 OK
[
    {
        "id": 1,
        "name": "Canto de Entrada",
        "slug": "entrada"
    },
    {
        "id": 2,
        "name": "Ato Penitencial",
        "slug": "ato-penitencial"
    },
    // ...
]
```

### Detalhamento de uma categoria específica

**Descrição:** Exibe os dados de um determinado registro de categoria.

```http
GET /api/category/<int:category_id>
```

Exemplo de resposta:

```json
// RESPONSE 200 OK
{
    "id": 1,
    "name": "Canto de Entrada",
    "slug": "entrada"
}
```

### Listagens dos artistas

**Descrição:** Lista todos os registros de artistas cadastrados no banco de dados.

A busca pode ser filtrada por categoria, retornando os artistas que possuem pelo menos uma música da categoria informada.

```http
GET /api/artist
```

> Parâmetros opcionais:
>
> - category_id: Filtra apenas os artistas que possuem pelo menos uma música da categoria informada.

Exemplo de resposta:

```json
// RESPONSE 200 OK
[
    {
        "id": 1,
        "name": "Adoração e Vida",
        "slug": "adoracao-e-vida"
    },
    {
        "id": 2,
        "name": "Amor e Adoração",
        "slug": "amor-e-adoracao"
    },
    // ...
]
```

### Detalhamento de um artista específico

**Descrição:** Exibe os dados de um determinado registro de artista.

```http
GET /api/artist/<int:artist_id>
```

Exemplo de resposta:

```json
// RESPONSE 200 OK
{
    "id": 1,
    "name": "Adoração e Vida",
    "slug": "adoracao-e-vida"
}
```

### Listagem das músicas

**Descrição:** Lista todos os registros de músicas cadastrados no banco de dados.

A busca pode ser filtrada por categoria ou por artista, retornando as músicas que possuem a categoria e/ou artista informado.

```http
GET /api/song
```

> Parâmetros opcionais:
>
> - category_id: Filtra apenas as músicas que pertencem à categoria informada
> - artist_id: Filtra apenas as músicas que pertencem ao artista informado

Exemplo de resposta:

```json
// RESPONSE 200 OK
[
    {
        "id": 20,
        "name": "Kyrie",
        "slug": "kyrie",
        "artist": {
            "id": 8,
            "name": "Capella",
            "slug": "capella"
        },
        "category": {
            "id": 2,
            "name": "Ato Penitencial",
            "slug": "ato-penitencial"
        },
        "lyrics_url": "https://www.letras.mus.br/capella/kyrie/",
        "preview_url": "https://www.youtube.com/embed/p3__LsTHMzQ"
    },
    {
        "id": 33,
        "name": "Quero confessar",
        "slug": "quero-confessar",
        "artist": {
            "id": 2,
            "name": "Amor e Adoração",
            "slug": "amor-e-adoracao"
        },
        "category": {
            "id": 2,
            "name": "Ato Penitencial",
            "slug": "ato-penitencial"
        },
        "lyrics_url": "https://www.letras.mus.br/ministerio-amor-e-adoracao/1882956/",
        "preview_url": "https://www.youtube.com/embed/SJ8OBgF9xD0?si=fPbtqlNNNNKf9fju"
    },
    // ...
]
```

### Detalhamento de uma música específica

**Descrição:** Exibe os dados de um determinado registro de música.

```http
GET /api/song/<int:song_id>
```

Exemplo de resposta:

```json
// RESPONSE 200 OK
{
    "id": 20,
    "name": "Kyrie",
    "slug": "kyrie",
    "artist": {
        "id": 8,
        "name": "Capella",
        "slug": "capella"
    },
    "category": {
        "id": 2,
        "name": "Ato Penitencial",
        "slug": "ato-penitencial"
    },
    "lyrics_url": "https://www.letras.mus.br/capella/kyrie/",
    "preview_url": "https://www.youtube.com/embed/p3__LsTHMzQ"
}
```

### Busca de uma música pelo Meilisearch

**Descrição:** Lista todos registros de músicas indexadas no Meilisearch. Pode-se passar como parâmetro um termo para busca nos campos textuais dos documentos.

A busca pode ser filtrada por categoria ou por artista, retornando as músicas que possuem a categoria e/ou artista informado.

```http
GET /api/song-search
```

> Parâmetros opcionais:
>
> - q: Filtra apenas as músicas que possuem ocorrência do valor informado em qualquer um de seus campos textuais.
> - category_id: Filtra apenas as músicas que pertencem à categoria informada
> - artist_id: Filtra apenas as músicas que pertencem ao artista informado

Exemplo de resposta:

```json
// RESPONSE 200 OK
[
    {
        "id": 20,
        "name": "Kyrie",
        "slug": "kyrie",
        "artist": {
            "id": 8,
            "name": "Capella",
            "slug": "capella"
        },
        "category": {
            "id": 2,
            "name": "Ato Penitencial",
            "slug": "ato-penitencial"
        },
        "lyrics_url": "https://www.letras.mus.br/capella/kyrie/",
        "preview_url": "https://www.youtube.com/embed/p3__LsTHMzQ"
    },
    {
        "id": 33,
        "name": "Quero confessar",
        "slug": "quero-confessar",
        "artist": {
            "id": 2,
            "name": "Amor e Adoração",
            "slug": "amor-e-adoracao"
        },
        "category": {
            "id": 2,
            "name": "Ato Penitencial",
            "slug": "ato-penitencial"
        },
        "lyrics_url": "https://www.letras.mus.br/ministerio-amor-e-adoracao/1882956/",
        "preview_url": "https://www.youtube.com/embed/SJ8OBgF9xD0?si=fPbtqlNNNNKf9fju"
    },
    // ...
]
```
