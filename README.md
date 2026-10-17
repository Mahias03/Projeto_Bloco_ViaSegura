# Via Segura

Projeto individual desenvolvido por Matheus Afonso para o TP3 da disciplina de Projeto de Bloco — Inteligência Artificial Aplicada.

## Descrição

O Via Segura é uma aplicação desenvolvida em Python para facilitar a consulta e a interpretação de dados sobre acidentes em rodovias federais brasileiras.

O projeto combina uma interface multipágina criada com Streamlit, dados abertos da Polícia Rodoviária Federal, notícias coletadas da web e uma API desenvolvida com FastAPI.

## Funcionalidades

- Navegação entre diferentes páginas da aplicação.
- Indicadores de acidentes, mortos e feridos.
- Filtros por estado, classificação do acidente e fase do dia.
- Exibição dos registros em tabela.
- Upload de arquivos CSV compatíveis com a base.
- Manutenção dos dados enviados durante a sessão.
- Download dos registros filtrados.
- Coleta de notícias com Requests e BeautifulSoup.
- Pesquisa nos títulos e subtítulos das notícias.
- Estatísticas de palavras, gráfico de frequência e nuvem de palavras.
- Consulta de acidentes e notícias por meio de uma API.
- Envio temporário de novos acidentes para a API.
- Documentação automática dos endpoints com Swagger.

## Páginas da aplicação

| Página | Conteúdo |
|---|---|
| Início | Apresentação do projeto, objetivos, ODS e iniciativas semelhantes |
| Acidentes | Upload, filtros, indicadores, tabela e download dos dados |
| Notícias | Pesquisa, tabela, estatísticas e nuvem de palavras |
| API | Consulta e envio de dados utilizando a API Via Segura |

## API Via Segura

A API foi desenvolvida com FastAPI e possui os seguintes endpoints:

| Método | Endpoint | Função |
|---|---|---|
| GET | `/` | Verificar o funcionamento da API |
| GET | `/acidentes` | Consultar acidentes e aplicar filtros |
| POST | `/acidentes` | Enviar temporariamente um novo acidente |
| GET | `/noticias` | Consultar as notícias coletadas |

A documentação interativa da API fica disponível em:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Os acidentes enviados pelo endpoint `POST /acidentes` são armazenados somente na memória da API. Eles podem ser consultados pelo endpoint `GET /acidentes` enquanto o servidor estiver em execução.

Esses registros não alteram o arquivo original da PRF, não aparecem automaticamente na página comum de acidentes e são removidos quando o servidor da API é reiniciado.

## Coleta de conteúdo da web

As notícias são coletadas da página de comunicação do Observatório Nacional de Segurança Viária.

A página disponibiliza o conteúdo diretamente em seu HTML. Por isso, Requests e BeautifulSoup foram suficientes para a coleta.

O uso do Selenium foi avaliado, mas não foi necessário nesta etapa. Ele poderá ser utilizado futuramente caso a fonte escolhida passe a carregar informações dinamicamente com JavaScript.

## Estrutura do projeto

- `01_business_understanding`: Project Charter e entendimento do problema.
- `02_data_ingest_understanding`: dados, coleta de notícias e Data Summary Report.
- `03_modeling`: documentação da etapa de modelagem.
- `04_deployment`: documentação da implantação.
- `05_acceptance`: documentação dos testes e da aceitação.
- `pages`: páginas da aplicação Streamlit.
- `app.py`: configuração da navegação entre as páginas.
- `comum.py`: caminhos e funções compartilhadas.
- `api.py`: API desenvolvida com FastAPI.
- `requirements.txt`: dependências da aplicação Streamlit.
- `requirements_api.txt`: dependências necessárias para a API.
- `.gitignore`: arquivos e pastas que não devem ser enviados ao GitHub.

## Como executar

Abra o terminal na pasta principal do projeto.

### 1. Criar o ambiente virtual

```powershell
py -m venv .venv
```

### 2. Ativar o ambiente no Windows

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
python -m pip install -r requirements_api.txt
```

### 4. Executar a API

No primeiro terminal:

```powershell
python -m uvicorn api:app --reload
```

A API ficará disponível em:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

### 5. Executar a aplicação

Mantenha a API funcionando e abra um segundo terminal. Ative novamente o ambiente virtual e execute:

```powershell
python -m streamlit run app.py
```

A aplicação será aberta no navegador. Para utilizar a página de integração com a API, os dois serviços precisam estar funcionando simultaneamente.

### 6. Atualizar as notícias

Quando for necessário realizar uma nova coleta:

```powershell
python 02_data_ingest_understanding/coletar_noticias.py
```

## Fontes de dados

- [Dados Abertos da Polícia Rodoviária Federal](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf)
- [Dicionário de Dados de Acidentes da PRF](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dicionario-acidentes)
- [Observatório Nacional de Segurança Viária](https://www.onsv.org.br/comunicacao)
- [API de Localidades do IBGE](https://servicodados.ibge.gov.br/api/docs/localidades)

## Tecnologias utilizadas

- Python
- Pandas
- Streamlit
- FastAPI
- Uvicorn
- Pydantic
- Requests
- BeautifulSoup
- WordCloud
- Git e GitHub
- CSV e JSON

## Limitações atuais

A aplicação utiliza uma amostra de 20 acidentes da PRF para demonstrar suas funcionalidades. Portanto, os resultados não representam todos os acidentes ocorridos no Brasil.

A API funciona localmente e os dados enviados para ela não possuem armazenamento permanente.

A integração com uma LLM ainda não foi implementada. Os dados estruturados em CSV e JSON preparam o projeto para essa possibilidade em uma etapa futura.

## Melhorias futuras

- Utilizar os dados completos da PRF entre 2021 e 2025.
- Adicionar filtros por ano, município e rodovia.
- Integrar a API de Localidades do IBGE.
- Criar um mapa interativo utilizando latitude e longitude.
- Adicionar armazenamento permanente aos dados recebidos pela API.
- Desenvolver novos gráficos e indicadores.
- Utilizar uma LLM para gerar resumos e auxiliar na interpretação dos resultados.
- Publicar a aplicação e a API em serviços de hospedagem.