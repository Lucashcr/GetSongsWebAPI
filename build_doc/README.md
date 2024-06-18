# BUILD DOC

*build_doc* não é um app Django, mas sim um módulo Python que tem ao objetivo de encapsular as funções para a geração do hinário em formato PDF. Sua funcionalidade baseia-se em encapsular a biblioteca responsável por gerar o PDF, implementando uma classe com um contrato bem definido para que o core possa utilizá-lo. Essa decisão foi tomada para manter a responsabilidade de geração do PDF separada do core, garantindo a coesão e a separação de responsabilidades, além de facilitar a manutenção e a evolução da aplicação.

Desta forma, este módulo define toda a parte de estilização do documento, tanto com relação ao tipo, tamanho e peso da fonte, margens, plano de fundo, entre outros e ainda Define os dois modelos de documento disponibilizados na plataforma como passíveis de escolha para geração dos hinários:

- `SingleColumnTemplate`: Modelo estruturado em páginas com uma única coluna.
- `TwoColumnsTemplate`: Modelo estruturado em páginas com duas colunas.

Estes modelos de documento são classes que possuem os métodos responsáveis por montar progressivamente a estrutura do corpo do documento e, ao final da montagem, construir o documento em si baseado na estrutura definida. Segue adiante um exemplo de utilização:

```python
from build_doc.styles import HEADING_2
from build_doc.templates import SingleColumnTemplate

doc = SingleColumnTemplate("document.pdf")

doc.insert_heading("Título do documento")
doc.insert_paragraph("Um parágrafo de exemplo")
doc.insert_paragraph_link("GetSongs", "https://getsongs.up.railway.app")

doc.build()
```
