from pathlib import Path
from zipfile import ZipFile

import pandas as pd

pasta_downloads = Path.home() / "Downloads"

arquivos_zip = sorted(
    pasta_downloads.glob("datatran2025*.zip"),
    key=lambda arquivo: arquivo.stat().st_mtime,
    reverse=True
)

if not arquivos_zip:
    raise FileNotFoundError(
        "O arquivo datatran2025.zip não foi encontrado na pasta Downloads."
    )

arquivo_zip = arquivos_zip[0]

with ZipFile(arquivo_zip) as arquivo_compactado:
    arquivos_csv = [
        nome for nome in arquivo_compactado.namelist()
        if nome.lower().endswith(".csv")
    ]

    if not arquivos_csv:
        raise FileNotFoundError("Nenhum arquivo CSV foi encontrado dentro do ZIP.")

    with arquivo_compactado.open(arquivos_csv[0]) as arquivo_csv:
        dados = pd.read_csv(
            arquivo_csv,
            sep=";",
            encoding="latin-1",
            low_memory=False
        )

colunas_desejadas = [
    "id",
    "data_inversa",
    "dia_semana",
    "horario",
    "uf",
    "br",
    "km",
    "municipio",
    "causa_acidente",
    "tipo_acidente",
    "classificacao_acidente",
    "fase_dia",
    "condicao_metereologica",
    "tipo_pista",
    "tracado_via",
    "pessoas",
    "mortos",
    "feridos",
    "feridos_leves",
    "feridos_graves",
    "veiculos",
    "latitude",
    "longitude"
]

colunas_encontradas = [
    coluna for coluna in colunas_desejadas
    if coluna in dados.columns]

amostra = dados[colunas_encontradas].sample(
    n=min(20, len(dados)),
    random_state=42)

caminho_saida = (
    Path(__file__).parent
    / "data"
    / "amostra_acidentes.csv")

amostra.to_csv(
    caminho_saida,
    index=False,
    encoding="utf-8")

print("Amostra criada com sucesso!")
print(f"Arquivo salvo em: {caminho_saida}")
print(amostra.head())