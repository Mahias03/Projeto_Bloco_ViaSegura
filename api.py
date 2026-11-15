from datetime import date
from enum import Enum
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, model_validator

import logging
from functools import lru_cache
from threading import Lock
from typing import Annotated

class UnidadeFederativa(str, Enum):
    AC = "AC"
    AL = "AL"
    AP = "AP"
    AM = "AM"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MT = "MT"
    MS = "MS"
    MG = "MG"
    PA = "PA"
    PB = "PB"
    PR = "PR"
    PE = "PE"
    PI = "PI"
    RJ = "RJ"
    RN = "RN"
    RS = "RS"
    RO = "RO"
    RR = "RR"
    SC = "SC"
    SP = "SP"
    SE = "SE"
    TO = "TO"


class ClassificacaoAcidente(str, Enum):
    com_vitimas_fatais = "Com Vítimas Fatais"
    com_vitimas_feridas = "Com Vítimas Feridas"
    sem_vitimas = "Sem Vítimas"


class FaseDia(str, Enum):
    amanhecer = "Amanhecer"
    anoitecer = "Anoitecer"
    plena_noite = "Plena Noite"
    pleno_dia = "Pleno dia"

class NovoAcidente(BaseModel):
    data_inversa: date
    uf: UnidadeFederativa
    municipio: str = Field(min_length=2, max_length=100)
    classificacao_acidente: ClassificacaoAcidente
    fase_dia: FaseDia
    mortos: int = Field(default=0, ge=0)
    feridos: int = Field(default=0, ge=0)

app = FastAPI(
    title="API Via Segura",
    description="API para consulta e envio de dados relacionados à segurança viária.",
    version="1.0.0"
)

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

acidentes_recebidos: list[dict] = []

@app.get("/")
def inicio():
    return {
        "projeto": "Via Segura",
        "mensagem": "API funcionando corretamente.",
        "status": "online"
    }

@app.get("/acidentes")
def consultar_acidentes(
    uf: UnidadeFederativa | None = None,
    classificacao: ClassificacaoAcidente | None = None,
    fase_dia: FaseDia | None = None,
    limite: int = Query(
        default=20,
        ge=1,
        le=100
    )
):
    """Consulta acidentes com filtros opcionais e inclui registros temporários enviados à API."""

    try:
        dados = pd.read_csv(caminho_dados)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="O arquivo de acidentes não foi encontrado.")

    # Coloca os registros enviados antes dos acidentes da amostra.
    if acidentes_recebidos:
        dados_recebidos = pd.DataFrame(list(reversed(acidentes_recebidos)))
        dados_recebidos = dados_recebidos.reindex(columns=dados.columns)

        dados = pd.concat(
            [dados_recebidos, dados],
            ignore_index=True
        )

    # Aplica somente os filtros recebidos pela API.
    if uf:
        dados = dados[dados["uf"].astype(str) == uf.value]

    if classificacao:
        dados = dados[
            dados["classificacao_acidente"].astype(str)
            == classificacao.value
        ]

    if fase_dia:
        dados = dados[
            dados["fase_dia"].astype(str)
            == fase_dia.value
        ]

    dados = dados.head(limite).fillna("")

    return {
        "quantidade": len(dados),
        "acidentes": dados.to_dict(orient="records")
    }

@app.get("/noticias")
def consultar_noticias(
    busca: str | None = None,
    limite: int = Query(
        default=10,
        ge=1,
        le=50
    )
):
    """Consulta as notícias coletadas, permitindo pesquisar uma palavra."""

    try:
        noticias = pd.read_csv(caminho_noticias)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="O arquivo de notícias não foi encontrado.")

    # Procura o termo nos títulos e subtítulos.
    if busca:
        filtro_titulo = noticias["titulo"].str.contains(
            busca,
            case=False,
            na=False,
            regex=False
        )

        filtro_subtitulo = noticias["subtitulo"].str.contains(
            busca,
            case=False,
            na=False,
            regex=False
        )

        noticias = noticias[filtro_titulo | filtro_subtitulo]

    noticias = noticias.head(limite).fillna("")

    return {
        "quantidade": len(noticias),
        "noticias": noticias.to_dict(orient="records")
    }

@app.post("/acidentes", status_code=201)
def adicionar_acidente(novo_acidente: NovoAcidente):
    """Recebe um acidente e o mantém temporariamente na memória da API."""

    registro = {
        "id": f"API-{len(acidentes_recebidos) + 1}",
        **novo_acidente.model_dump(mode="json")
    }

    acidentes_recebidos.append(registro)

    return {
        "mensagem": "Acidente recebido com sucesso.",
        "registro": registro
    }

class DadosResumo(BaseModel):
    estado: list[str]
    classificacao: list[str]
    fase_dia: list[str]
    acidentes: int = Field(ge=0, strict=True)
    mortos: int = Field(ge=0, strict=True)
    feridos: int = Field(ge=0, strict=True)
    acidentes_por_estado: dict[str, Annotated[int, Field(ge=0, strict=True)]]
    acidentes_por_fase_dia: dict[str, Annotated[int, Field(ge=0, strict=True)]]

    # Confere se cada distribuição soma o total de acidentes.
    @model_validator(mode="after")
    def validar_contagens(self):
        if sum(self.acidentes_por_estado.values()) != self.acidentes:
            raise ValueError("A soma por estado deve ser igual ao total de acidentes.")

        if sum(self.acidentes_por_fase_dia.values()) != self.acidentes:
            raise ValueError("A soma por fase do dia deve ser igual ao total de acidentes.")

        return self

class RespostaResumo(BaseModel):
    tipo_analise: str
    dados: DadosResumo
    resumo: str

trava_modelo = Lock()

@lru_cache(maxsize=1)
def obter_recursos_modelo():
    # Carrega o modelo somente quando ele for necessário.
    from modelo_llm import carregar_modelo, gerar_resumo

    tokenizador, modelo = carregar_modelo()

    return tokenizador, modelo, gerar_resumo

@app.post("/resumo", response_model=RespostaResumo)
def resumir_acidentes(dados: DadosResumo):
    """Gera um resumo dos indicadores e filtros recebidos."""

    if dados.acidentes == 0:
        if dados.mortos > 0 or dados.feridos > 0:
            raise HTTPException(
                status_code=422,
                detail="Não pode haver mortos ou feridos quando há zero acidentes."
            )

        resumo = "Nenhum acidente foi encontrado na base disponível com os filtros informados."

    else:
        # Evita carregamentos ou gerações simultâneas no mesmo processo.
        with trava_modelo:
            try:
                tokenizador, modelo, gerar_resumo = obter_recursos_modelo()
            except Exception:
                logging.exception("Falha ao carregar o modelo local.")
                raise HTTPException(
                    status_code=503,
                    detail="O modelo local não está disponível. Verifique o terminal da API."
                )

            try:
                dados_modelo = dados.model_dump(mode="json")
                resumo = gerar_resumo(tokenizador, modelo, dados_modelo)

                if not resumo:
                    raise ValueError("O modelo retornou uma resposta vazia.")

            except Exception:
                logging.exception("Falha ao gerar o resumo.")
                raise HTTPException(
                    status_code=500,
                    detail="Não foi possível gerar o resumo. Verifique o terminal da API."
                )

    return {
        "tipo_analise": "Resumo dos acidentes filtrados",
        "dados": dados,
        "resumo": resumo
    }