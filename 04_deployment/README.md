# Deployment

A aplicação Via Segura é executada pelo arquivo `app.py` e utiliza o Streamlit como interface.

## Execução local

Na pasta principal do projeto, crie e ative o ambiente virtual:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:
```powershell
python -m pip install -r requirements.txt
```

Caso seja necessário atualizar as notícias, execute:
```powershell
python 02_data_ingest_understanding\coletar_noticias.py
```

Para iniciar a aplicação:
```powershell
python -m streamlit run app.py
```

## Preparação para implantação

O projeto está preparado para uma futura publicação em um serviço compatível com Streamlit porque:

- o código está armazenado no GitHub;
- as dependências estão registradas no `requirements.txt`;
- o arquivo principal é o `app.py`;
- os caminhos dos arquivos são relativos à pasta do projeto;
- os arquivos CSV necessários estão organizados no diretório de dados;
- a aplicação não depende de credenciais ou informações secretas.

Nesta etapa, a aplicação será validada localmente. A publicação em um serviço externo poderá ser realizada posteriormente.