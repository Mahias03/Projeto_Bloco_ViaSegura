import time
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


pasta_dados = Path(__file__).parent / "data"
caminho_entrada = pasta_dados / "noticias_seguranca_viaria.csv"
caminho_saida = pasta_dados / "noticias_com_texto.csv"

if caminho_saida.exists():
    raise FileExistsError(f"O arquivo de saída já existe: {caminho_saida}")

noticias = pd.read_csv(caminho_entrada)
cabecalhos = {"User-Agent": "Mozilla/5.0 Projeto acadêmico Via Segura"}
textos_noticias = []

for numero, url in enumerate(noticias["link"], start=1):
    texto_noticia = ""

    try:
        resposta = requests.get(url, headers=cabecalhos, timeout=30)
        resposta.raise_for_status()
        sopa = BeautifulSoup(resposta.text, "html.parser")

        # Seleciona o bloco identificado nos testes com as notícias.
        bloco = sopa.select_one("div.wg-text.container")

        if bloco:
            paragrafos = [p.get_text(" ", strip=True) for p in bloco.find_all("p")]
            paragrafos = [texto for texto in paragrafos if texto and texto.casefold() != "leia na íntegra"]
            texto_noticia = "\n\n".join(paragrafos)
        else:
            print(f"Bloco de texto não encontrado: {url}")

    except requests.RequestException as erro:
        print(f"Falha ao acessar {url}: {erro}")

    textos_noticias.append(texto_noticia)
    print(f"{numero}/{len(noticias)} | {len(texto_noticia)} caracteres | {url}")

    time.sleep(0.5)

noticias["texto"] = textos_noticias

# Cria um arquivo separado, sem substituir o CSV original.
noticias.to_csv(caminho_saida, index=False, encoding="utf-8-sig", mode="x")

print(f"\nArquivo salvo em: {caminho_saida}")
print(f"Notícias com texto: {(noticias['texto'].str.len() > 0).sum()}")