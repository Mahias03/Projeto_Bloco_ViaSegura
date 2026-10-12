import re
from collections import Counter
from pathlib import Path

import pandas as pd
import streamlit as st


pasta_projeto = Path(__file__).parent

caminho_dados = (
    pasta_projeto
    / "02_data_ingest_understanding"
    / "data"
    / "amostra_acidentes.csv"
)

caminho_noticias = (
    pasta_projeto
    / "02_data_ingest_understanding"
    / "data"
    / "noticias_seguranca_viaria.csv"
)


@st.cache_data
def carregar_dados(caminho):
    return pd.read_csv(caminho)


@st.cache_data
def analisar_noticias(dados):
    texto = " ".join(dados["titulo"].fillna("") + " " + dados["subtitulo"].fillna("")).lower()

    # Separa as palavras e remove termos comuns que não ajudam na análise.
    palavras = re.findall(r"\b[a-záàâãéêíóôõúç]{4,}\b", texto)

    palavras_ignoradas = {
        "aos", "como", "com", "das", "dos", "entre", "essa", "esse",
        "esta", "este", "mais", "nas", "nos", "para", "pela", "pelas",
        "pelo", "pelos", "por", "porque", "sobre", "suas", "seus",
        "também", "uma"
    }

    palavras_filtradas = [palavra for palavra in palavras if palavra not in palavras_ignoradas]
    frequencias = Counter(palavras_filtradas)
    tabela_frequencias = pd.DataFrame(frequencias.most_common(10), columns=["palavra", "frequencia"])
    texto_nuvem = " ".join(palavras_filtradas)

    return texto_nuvem, tabela_frequencias, len(palavras_filtradas), len(frequencias)