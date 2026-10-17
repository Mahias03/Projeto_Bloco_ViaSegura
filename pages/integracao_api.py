import pandas as pd
import requests
import streamlit as st

URL_API = "http://127.0.0.1:8000"

st.title("Integração com a API")

st.write(
    """
    Esta página consulta e envia dados utilizando a API do Via Segura.
    A API deve estar em execução para que as funcionalidades estejam disponíveis.
    """
)

try:
    resposta_inicial = requests.get(
        f"{URL_API}/acidentes",
        params={"limite": 100},
        timeout=10
    )

    resposta_inicial.raise_for_status()
    acidentes_api = pd.DataFrame(resposta_inicial.json()["acidentes"])

    st.success("Conexão com a API realizada com sucesso.")

except requests.RequestException:
    st.error("Não foi possível conectar com a API.")

    st.code("python -m uvicorn api:app --reload")

    st.stop()

if acidentes_api.empty:
    st.warning("A API não retornou acidentes.")
    st.stop()

# Utiliza os dados da própria API para preparar as opções dos formulários.
opcoes_uf = sorted(acidentes_api["uf"].dropna().astype(str).unique().tolist())
opcoes_classificacao = sorted(acidentes_api["classificacao_acidente"].dropna().astype(str).unique().tolist())
opcoes_fase_dia = sorted(acidentes_api["fase_dia"].dropna().astype(str).unique().tolist())

st.header("Consultar acidentes")

coluna_consulta1, coluna_consulta2, coluna_consulta3 = st.columns(3)

with coluna_consulta1:
    uf_consulta = st.selectbox("Estado para consulta", ["Todos"] + opcoes_uf)

with coluna_consulta2:
    classificacao_consulta = st.selectbox("Classificação para consulta", ["Todas"] + opcoes_classificacao)

with coluna_consulta3:
    fase_consulta = st.selectbox("Fase do dia para consulta", ["Todas"] + opcoes_fase_dia)

limite = st.slider(
    "Quantidade máxima de registros",
    min_value=1,
    max_value=100,
    value=20
)

if st.button("Consultar acidentes pela API"):
    parametros = {"limite": limite}

    if uf_consulta != "Todos":
        parametros["uf"] = uf_consulta

    if classificacao_consulta != "Todas":
        parametros["classificacao"] = classificacao_consulta

    if fase_consulta != "Todas":
        parametros["fase_dia"] = fase_consulta

    try:
        resposta_consulta = requests.get(
            f"{URL_API}/acidentes",
            params=parametros,
            timeout=10
        )

        resposta_consulta.raise_for_status()
        resultado = resposta_consulta.json()
        acidentes_encontrados = pd.DataFrame(resultado["acidentes"])

        st.metric("Acidentes retornados pela API", resultado["quantidade"])

        if acidentes_encontrados.empty:
            st.warning("Nenhum acidente foi encontrado com os filtros selecionados.")
        else:
            st.dataframe(
                acidentes_encontrados,
                width="stretch",
                hide_index=True
            )

    except requests.RequestException as erro:
        st.error(f"Erro ao consultar a API: {erro}")

st.divider()

st.header("Enviar novo acidente")

st.caption("O registro será validado e mantido temporariamente pela API.")

with st.form("formulario_novo_acidente"):
    data_acidente = st.date_input("Data do acidente")

    coluna_envio1, coluna_envio2 = st.columns(2)

    with coluna_envio1:
        uf_envio = st.selectbox("Estado do novo registro", opcoes_uf)
        classificacao_envio = st.selectbox("Classificação do novo registro", opcoes_classificacao)

    with coluna_envio2:
        municipio_envio = st.text_input("Município")
        fase_envio = st.selectbox("Fase do dia do novo registro", opcoes_fase_dia)

    coluna_numero1, coluna_numero2 = st.columns(2)

    with coluna_numero1:
        mortos_envio = st.number_input(
            "Número de mortos",
            min_value=0,
            value=0,
            step=1
        )

    with coluna_numero2:
        feridos_envio = st.number_input(
            "Número de feridos",
            min_value=0,
            value=0,
            step=1
        )

    enviar_acidente = st.form_submit_button("Enviar acidente para a API")

if enviar_acidente:
    novo_acidente = {
        "data_inversa": data_acidente.isoformat(),
        "uf": uf_envio,
        "municipio": municipio_envio,
        "classificacao_acidente": classificacao_envio,
        "fase_dia": fase_envio,
        "mortos": mortos_envio,
        "feridos": feridos_envio
    }

    try:
        resposta_envio = requests.post(
            f"{URL_API}/acidentes",
            json=novo_acidente,
            timeout=10
        )

        if resposta_envio.status_code == 201:
            resultado_envio = resposta_envio.json()

            st.success(resultado_envio["mensagem"])
            st.json(resultado_envio["registro"])
        else:
            st.error(f"A API recusou o registro: {resposta_envio.text}")

    except requests.RequestException as erro:
        st.error(f"Erro ao enviar dados para a API: {erro}")