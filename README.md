# Via Segura

Projeto individual desenvolvido por Matheus Afonso para o TP5 da disciplina de Projeto de Bloco — Inteligência Artificial Aplicada.

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
- Geração experimental de resumos dos acidentes filtrados com uma LLM local.
- Gráfico de acidentes por fase do dia.
- Resumo experimental de notícias com uma LLM local.

## Páginas da aplicação

| Página | Conteúdo |
|---|---|
| Início | Apresentação do projeto, objetivos, ODS e iniciativas semelhantes |
| Acidentes | Upload, filtros, indicadores, tabela e download dos dados |
| Notícias | Pesquisa, tabela, estatísticas, nuvem de palavras e resumo com IA |
| API | Consulta e envio de dados utilizando a API Via Segura |

## API Via Segura

A API foi desenvolvida com FastAPI e possui os seguintes endpoints:

| Método | Endpoint | Função |
|---|---|---|
| GET | `/` | Verificar o funcionamento da API |
| GET | `/acidentes` | Consultar acidentes e aplicar filtros |
| POST | `/acidentes` | Enviar temporariamente um novo acidente |
| GET | `/noticias` | Consultar as notícias coletadas |
| POST | `/resumo` | Gerar um resumo dos indicadores e filtros recebidos |
| POST | `/resumo-noticia` | Gerar um resumo do texto de uma notícia |

A documentação interativa da API fica disponível em:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Os acidentes enviados pelo endpoint `POST /acidentes` são armazenados somente na memória da API. Eles podem ser consultados pelo endpoint `GET /acidentes` enquanto o servidor estiver em execução.

Esses registros não alteram o arquivo original da PRF, não aparecem automaticamente na página comum de acidentes e são removidos quando o servidor da API é reiniciado.

## Coleta de conteúdo da web

As notícias são coletadas da página de comunicação do Observatório Nacional de Segurança Viária.

A página disponibiliza o conteúdo diretamente em seu HTML. Por isso, Requests e BeautifulSoup foram suficientes para a coleta.

O uso do Selenium foi avaliado, mas não foi necessário nesta etapa. Ele poderá ser utilizado futuramente caso a fonte escolhida passe a carregar informações dinamicamente com JavaScript.

Os textos das matérias são extraídos para `noticias_com_texto.csv` e utilizados na geração dos resumos.

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
- `modelo_llm.py`: carregamento e execução local do modelo de linguagem.

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

### 4. Preparar o modelo local

Na primeira utilização em uma máquina, baixe o modelo:

```powershell
python -c "from huggingface_hub import snapshot_download; snapshot_download('Qwen/Qwen2.5-1.5B-Instruct')"
```

O download requer internet. Depois de baixado, o modelo é carregado do cache local e executado na CPU.

### 5. Executar a API

No primeiro terminal:

```powershell
python -m uvicorn api:app --reload
```

A API ficará disponível em:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

### 6. Executar a aplicação

Mantenha a API funcionando e abra um segundo terminal. Ative novamente o ambiente virtual e execute:

```powershell
python -m streamlit run app.py
```

A aplicação será aberta no navegador. Para utilizar a página de integração com a API, os dois serviços precisam estar funcionando simultaneamente.

### 7. Atualizar as notícias

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
- PyTorch
- Transformers
- Hugging Face Hub

## Limitações atuais

A aplicação utiliza uma amostra de 20 acidentes da PRF para demonstrar suas funcionalidades. Portanto, os resultados não representam todos os acidentes ocorridos no Brasil.

A API funciona localmente e os dados enviados para ela não possuem armazenamento permanente.

A LLM é experimental e pode gerar textos incorretos, contraditórios ou incompletos. Os indicadores e a tabela devem ser usados para conferir seus resultados.

Os resumos das notícias devem ser conferidos com as matérias originais. Nos testes realizados, a geração levou aproximadamente entre 1min50s e 2min30s, podendo variar conforme a notícia e o computador.

## Melhorias futuras

- Utilizar os dados completos da PRF entre 2021 e 2025.
- Adicionar filtros por ano, município e rodovia.
- Integrar a API de Localidades do IBGE.
- Criar um mapa interativo utilizando latitude e longitude.
- Adicionar armazenamento permanente aos dados recebidos pela API.
- Desenvolver novos gráficos e indicadores.
- Publicar a aplicação e a API em serviços de hospedagem.