# Deployment

A aplicação Via Segura possui uma interface multipágina desenvolvida com Streamlit e uma API desenvolvida com FastAPI.

A interface é iniciada pelo arquivo `app.py`, enquanto a API é iniciada pelo arquivo `api.py`.

## Execução local

Na pasta principal do projeto, crie e ative o ambiente virtual:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
python -m pip install -r requirements_api.txt
```

Caso seja necessário atualizar as notícias, execute:

```powershell
python 02_data_ingest_understanding\coletar_noticias.py
```

Para iniciar a API, execute no primeiro terminal:

```powershell
python -m uvicorn api:app --reload
```

A documentação da API ficará disponível em:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Em um segundo terminal, ative novamente o ambiente virtual e inicie a aplicação:

```powershell
python -m streamlit run app.py
```

A API e a aplicação Streamlit devem permanecer em execução simultaneamente para utilizar a página de integração.

## Preparação para implantação

O projeto está preparado para uma futura publicação porque:

- o código está armazenado no GitHub;
- as dependências estão registradas no `requirements.txt` e no `requirements_api.txt`;
- os arquivos principais são `app.py` e `api.py`;
- a interface está organizada em páginas;
- os caminhos dos arquivos são relativos à pasta do projeto;
- os arquivos CSV necessários estão organizados no diretório de dados;
- a aplicação não depende de credenciais ou informações secretas.

Nesta etapa, a aplicação e a API serão validadas localmente. A publicação em serviços externos poderá ser realizada posteriormente.