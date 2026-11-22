# Data Summary Report — Via Segura

## 1. Objetivo do documento

Este documento apresenta as fontes, as principais características e os objetivos de uso dos dados utilizados no projeto Via Segura.

## 2. Dados de acidentes da PRF

A principal fonte do projeto é a base de dados abertos da Polícia Rodoviária Federal:

[Dados Abertos da Polícia Rodoviária Federal](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf)

Os dados são disponibilizados em arquivos CSV e organizados por ocorrência. Cada linha representa um acidente registrado em uma rodovia federal.

O protótipo utiliza uma amostra de 20 acidentes de 2025, armazenada em:

`02_data_ingest_understanding/data/amostra_acidentes.csv`

As principais informações utilizadas são:

| Grupo | Colunas | Objetivo |
|---|---|---|
| Identificação | id, data_inversa e horario | Identificar a ocorrência e o momento do acidente |
| Localização | uf, br, km e municipio | Identificar onde o acidente ocorreu |
| Características | causa_acidente, tipo_acidente, classificacao_acidente e fase_dia | Analisar as condições da ocorrência |
| Consequências | pessoas, mortos e feridos | Gerar os indicadores da aplicação |
| Coordenadas | latitude e longitude | Possibilitar análises geográficas futuras |

Na aplicação, esses dados são utilizados nos filtros, indicadores e na tabela de acidentes.

## 3. Notícias sobre segurança viária

A segunda fonte utilizada é a página de comunicação do Observatório Nacional de Segurança Viária:

[Comunicação do Observatório Nacional de Segurança Viária](https://www.onsv.org.br/comunicacao)

As notícias são coletadas com Requests e BeautifulSoup. O script obtém o título, subtítulo, data de publicação, link e fonte das dez primeiras matérias encontradas.

O resultado é armazenado em:

`02_data_ingest_understanding/data/noticias_seguranca_viaria.csv`

Esses dados são utilizados na pesquisa de notícias, na tabela de conteúdos, no gráfico de frequência e na nuvem de palavras.

Para a sumarização, um segundo script acessa os links das notícias e extrai o texto das matérias. Os textos são armazenados em `02_data_ingest_understanding/data/noticias_com_texto.csv`.

Na aplicação, o usuário seleciona uma notícia e solicita um resumo. O texto coletado é enviado à API e processado localmente pelo modelo Qwen2.5-1.5B-Instruct.

O uso de Selenium foi avaliado, mas não foi necessário porque o conteúdo utilizado já está presente no HTML obtido pelo Requests. BeautifulSoup atende à necessidade atual com menor complexidade e tempo de execução. O Selenium poderá ser utilizado futuramente caso uma fonte dependa de conteúdo carregado por JavaScript.

## 4. Upload e download de dados

A aplicação permite o envio de arquivos CSV com a mesma estrutura da amostra de acidentes.

As colunas do arquivo são verificadas antes da inclusão. Os novos registros são combinados com a base existente e as duplicidades são removidas.

Os dados enviados são mantidos durante a sessão do usuário, mas não são gravados permanentemente. Também é possível baixar os registros apresentados após a aplicação dos filtros.

## 5. Tratamentos realizados

Os principais tratamentos são:

- verificação das colunas dos arquivos enviados;
- remoção de registros duplicados;
- conversão das quantidades de mortos e feridos para valores numéricos, considerando valores ausentes ou não numéricos como zero;
- tratamento de valores ausentes;
- aplicação de filtros por estado, classificação e fase do dia;
- separação e contagem das palavras das notícias;
- remoção de palavras comuns na análise textual;
- utilização de cache para evitar processamentos repetidos.
- extração do texto das notícias a partir das páginas originais;
- validação do tamanho do texto enviado para sumarização.

## 6. Qualidade e limitações

Os dados da PRF representam somente acidentes registrados em rodovias federais. A amostra atual contém apenas 20 registros e serve para demonstrar o funcionamento da aplicação, não sendo suficiente para representar todos os acidentes do país.

A coleta das notícias depende da estrutura da página do Observatório. Caso o site seja alterado, o script poderá precisar de ajustes.

Os arquivos enviados pelo usuário também precisam possuir as mesmas colunas da base utilizada pelo projeto.

Os resumos gerados pela IA podem conter erros e devem ser comparados com a notícia original. Em um dos testes, o modelo informou que 19 Detrans foram avaliados, quando esse número se referia aos que apresentaram melhora. O tempo de geração também pode variar conforme o texto e os recursos do computador.

## 7. API do projeto

O projeto possui uma API desenvolvida com FastAPI para disponibilizar os dados em formato JSON.

As principais rotas são:

- `GET /acidentes`: consulta acidentes com filtros opcionais;
- `POST /acidentes`: recebe e valida um novo registro;
- `GET /noticias`: consulta as notícias coletadas.
- `POST /resumo`: recebe filtros e indicadores e retorna um resumo textual.
- `POST /resumo-noticia`: recebe o texto de uma notícia e retorna um resumo gerado pela LLM.

A documentação interativa fica disponível em `/docs`.

Os registros enviados pelo `POST /acidentes` permanecem temporariamente na memória da API. Eles podem ser consultados enquanto o servidor estiver em execução, mas não alteram o CSV oficial da PRF e são removidos quando a API é reiniciada.

## 8. Resumo dos acidentes com LLM

A página de acidentes calcula os totais de acidentes, mortos e feridos, além das contagens por estado e fase do dia. Os filtros e os indicadores são enviados em JSON para a rota `POST /resumo`.

A API valida a estrutura e as contagens recebidas. Para resultados com acidentes, o modelo Qwen2.5-1.5B-Instruct, executado localmente, gera um texto curto. Quando não há acidentes, a API retorna uma mensagem pronta sem chamar a LLM.

O texto gerado é experimental e pode conter erros ou contradições. Os indicadores e a tabela devem ser consultados para conferência.

## 9. Possibilidades futuras

Nas próximas etapas, o projeto poderá incluir:

- dados completos da PRF de outros anos;
- filtros por município, rodovia e período;
- integração com a API de Localidades do IBGE;
- mapa interativo utilizando latitude e longitude;
- novos gráficos e indicadores.