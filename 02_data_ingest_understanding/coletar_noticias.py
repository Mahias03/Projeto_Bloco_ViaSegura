import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup


URL_PAGINA = "https://www.onsv.org.br/comunicacao"

cabecalhos = {"User-Agent": "Mozilla/5.0 Projeto acadêmico Via Segura - Matheus Afonso"}

resposta = requests.get(
    URL_PAGINA,
    headers=cabecalhos,
    timeout=30
)

resposta.raise_for_status()

sopa = BeautifulSoup(resposta.text, "html.parser")

urls_noticias = []

# Mantém somente links de matérias pertencentes ao site do Observatório.
for link in sopa.find_all("a", href=True):
    endereco = link["href"]
    url_completa = urljoin(URL_PAGINA, endereco)
    endereco_analisado = urlparse(url_completa)

    if (
        endereco_analisado.netloc == "www.onsv.org.br"
        and endereco_analisado.path.startswith("/comunicacao/materias/")
        and url_completa not in urls_noticias
    ):
        urls_noticias.append(url_completa)

if not urls_noticias:
    raise RuntimeError("Nenhuma notícia foi encontrada na página do Observatório.")

noticias = []

# Limita a coleta às dez primeiras notícias encontradas.
for url_noticia in urls_noticias[:10]:
    resposta_noticia = requests.get(
        url_noticia,
        headers=cabecalhos,
        timeout=30
    )

    resposta_noticia.raise_for_status()

    sopa_noticia = BeautifulSoup(resposta_noticia.text, "html.parser")

    elemento_titulo = sopa_noticia.find("h1")
    elemento_subtitulo = sopa_noticia.find("h2")

    titulo = elemento_titulo.get_text(" ", strip=True) if elemento_titulo else "Título não encontrado"
    subtitulo = elemento_subtitulo.get_text(" ", strip=True) if elemento_subtitulo else ""

    texto_pagina = sopa_noticia.get_text(" ", strip=True)

    # Procura a data no formato utilizado pelo site.
    data_encontrada = re.search(r"\d{2}\s+[A-Z]{3}\s+\d{4}\s*-\s*\d{2}H\d{2}", texto_pagina)
    data_publicacao = data_encontrada.group() if data_encontrada else "Data não encontrada"

    noticias.append(
        {
            "titulo": titulo,
            "subtitulo": subtitulo,
            "data_publicacao": data_publicacao,
            "link": url_noticia,
            "fonte": "Observatório Nacional de Segurança Viária"
        }
    )

    time.sleep(0.5)

dados_noticias = pd.DataFrame(noticias)

# Armazena o resultado da coleta na pasta de dados do projeto.
caminho_saida = Path(__file__).parent / "data" / "noticias_seguranca_viaria.csv"
caminho_saida.parent.mkdir(parents=True, exist_ok=True)

dados_noticias.to_csv(
    caminho_saida,
    index=False,
    encoding="utf-8-sig"
)

print(f"Notícias coletadas: {len(dados_noticias)}")
print(f"Arquivo salvo em: {caminho_saida}")
print(dados_noticias[["titulo", "data_publicacao"]])