import pandas as pd
import streamlit as st
import requests

from comum import carregar_dados, caminho_dados

URL_API_RESUMO = "http://127.0.0.1:8000/resumo"

st.title("Análise interativa dos acidentes")

try:
    dados = carregar_dados(caminho_dados)

    # Mantém os dados enviados durante as interações do usuário.
    if "dados_adicionais" not in st.session_state:
        st.session_state.dados_adicionais = pd.DataFrame(columns=dados.columns)

    st.subheader("Adicionar dados por arquivo CSV")

    arquivo_enviado = st.file_uploader("Selecione um CSV com a mesma estrutura da base de acidentes.", type="csv")

    if arquivo_enviado is not None:
        try:
            novos_dados = pd.read_csv(arquivo_enviado, sep=None, engine="python")

            colunas_ausentes = [coluna for coluna in dados.columns if coluna not in novos_dados.columns]

            if colunas_ausentes:
                st.error(f"Colunas ausentes no arquivo: {', '.join(colunas_ausentes)}")
            elif st.button("Adicionar dados à análise"):
                novos_dados = novos_dados[dados.columns]
                st.session_state.dados_adicionais = pd.concat(
                    [st.session_state.dados_adicionais, novos_dados],
                    ignore_index=True
                ).drop_duplicates()

                st.success(f"{len(novos_dados)} registros foram carregados para a sessão.")

        except Exception as erro:
            st.error(f"Não foi possível ler o arquivo: {erro}")

    dados_completos = pd.concat(
        [dados, st.session_state.dados_adicionais],
        ignore_index=True
    ).drop_duplicates()

    st.caption(f"Registros adicionais nesta sessão: {len(st.session_state.dados_adicionais)}")

    if not st.session_state.dados_adicionais.empty:
        if st.button("Remover dados enviados"):
            st.session_state.dados_adicionais = pd.DataFrame(columns=dados.columns)
            st.rerun()

    # Prepara as opções disponíveis para cada filtro.
    opcoes_uf = sorted(dados_completos["uf"].dropna().astype(str).unique())
    opcoes_classificacao = sorted(dados_completos["classificacao_acidente"].dropna().astype(str).unique())
    opcoes_fase_dia = sorted(dados_completos["fase_dia"].dropna().astype(str).unique())

    coluna_filtro1, coluna_filtro2, coluna_filtro3 = st.columns(3)

    with coluna_filtro1:
        ufs_selecionadas = st.multiselect("Estado", opcoes_uf)

    with coluna_filtro2:
        classificacoes_selecionadas = st.multiselect("Classificação", opcoes_classificacao)

    with coluna_filtro3:
        fases_selecionadas = st.multiselect("Fase do dia", opcoes_fase_dia)

    st.caption("Quando nenhuma opção é selecionada, todos os registros são apresentados.")

    dados_filtrados = dados_completos.copy()

    # Aplica somente os filtros que possuem opções selecionadas.
    if ufs_selecionadas:
        dados_filtrados = dados_filtrados[dados_filtrados["uf"].astype(str).isin(ufs_selecionadas)]

    if classificacoes_selecionadas:
        dados_filtrados = dados_filtrados[
            dados_filtrados["classificacao_acidente"].astype(str).isin(classificacoes_selecionadas)
        ]

    if fases_selecionadas:
        dados_filtrados = dados_filtrados[
            dados_filtrados["fase_dia"].astype(str).isin(fases_selecionadas)
        ]

    total_acidentes = len(dados_filtrados)
    total_mortos = int(pd.to_numeric(dados_filtrados["mortos"], errors="coerce").fillna(0).sum())
    total_feridos = int(pd.to_numeric(dados_filtrados["feridos"], errors="coerce").fillna(0).sum())

    coluna1, coluna2, coluna3 = st.columns(3)

    coluna1.metric("Acidentes encontrados", total_acidentes)
    coluna2.metric("Mortos encontrados", total_mortos)
    coluna3.metric("Feridos encontrados", total_feridos)

    # Organiza os valores ausentes antes de contar os registros.
    estados_registrados = dados_filtrados["uf"].astype("string").fillna("Não informado").str.strip()
    fases_registradas = dados_filtrados["fase_dia"].astype("string").fillna("Não informado").str.strip()

    estados_registrados = estados_registrados.replace("", "Não informado")
    fases_registradas = fases_registradas.replace("", "Não informado")

    acidentes_por_estado = {
        estado: int(total)
        for estado, total in estados_registrados.value_counts().items()
    }

    acidentes_por_fase_dia = {
        fase: int(total)
        for fase, total in fases_registradas.value_counts().items()
    }

    if total_acidentes > 0:
        st.subheader("Acidentes por fase do dia")

        dados_grafico = pd.DataFrame({
            "fase_dia": list(acidentes_por_fase_dia.keys()),
            "acidentes": list(acidentes_por_fase_dia.values())
        })

        st.bar_chart(dados_grafico, x="fase_dia", y="acidentes")
        st.caption("Distribuição dos acidentes nos registros filtrados.")

    st.caption(
        "Resumo gerado com base nos registros disponíveis e filtros selecionados. "
        "O texto pode conter erros; confira os indicadores apresentados."
    )

    dados_resumo = {
        "estado": list(ufs_selecionadas),
        "classificacao": list(classificacoes_selecionadas),
        "fase_dia": list(fases_selecionadas),
        "acidentes": total_acidentes,
        "mortos": total_mortos,
        "feridos": total_feridos,
        "acidentes_por_estado": acidentes_por_estado,
        "acidentes_por_fase_dia": acidentes_por_fase_dia
    }

    # Guarda o resumo durante a sessão enquanto os dados forem os mesmos.
    if "resumo_ia_acidentes" not in st.session_state:
        st.session_state.resumo_ia_acidentes = None

    if st.session_state.resumo_ia_acidentes is not None:
        if st.session_state.resumo_ia_acidentes["dados"] != dados_resumo:
            st.session_state.resumo_ia_acidentes = None

    if total_acidentes > 0 and st.button("Gerar resumo com IA"):
        st.session_state.resumo_ia_acidentes = None

        try:
            with st.spinner("Gerando resumo. Isso pode levar alguns segundos..."):
                resposta = requests.post(
                    URL_API_RESUMO,
                    json=dados_resumo,
                    timeout=(5, 120)
                )

                resposta.raise_for_status()
                resultado = resposta.json()

            if not isinstance(resultado, dict) or not isinstance(resultado.get("resumo"), str):
                raise ValueError("Resposta da API em formato inesperado.")

            if not resultado["resumo"].strip():
                raise ValueError("A API retornou um resumo vazio.")

            st.session_state.resumo_ia_acidentes = {
                "dados": dados_resumo,
                "texto": resultado["resumo"]
            }

        except requests.Timeout:
            st.error(
                "A API demorou para responder. O processamento pode continuar "
                "no servidor; aguarde antes de tentar novamente."
            )

        except requests.ConnectionError:
            st.error("Não foi possível conectar à API. Verifique se ela está em execução.")

        except requests.HTTPError as erro:
            codigo = erro.response.status_code if erro.response is not None else "desconhecido"

            if codigo == 503:
                st.error("O modelo local está indisponível. Verifique o terminal da API.")
            elif codigo == 422:
                st.error("A API recusou os dados. Confira os filtros e indicadores.")
            else:
                st.error(f"Não foi possível gerar o resumo. Código HTTP: {codigo}.")

        except ValueError:
            st.error("A API retornou uma resposta em formato inesperado.")

        except requests.RequestException:
            st.error("Ocorreu um erro na comunicação com a API.")

    if st.session_state.resumo_ia_acidentes is not None:
        with st.expander("Ver resposta da IA — experimental"):
            st.warning("O texto pode conter erros ou contradições. Confira os dados calculados.")
            st.write(st.session_state.resumo_ia_acidentes["texto"])

    if dados_filtrados.empty:
        st.warning("Nenhum acidente foi encontrado com os filtros selecionados.")
    else:
        st.dataframe(
            dados_filtrados,
            width="stretch",
            hide_index=True
        )

        # Prepara os registros filtrados para download em CSV.
        csv_filtrado = dados_filtrados.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            label="Baixar dados filtrados em CSV",
            data=csv_filtrado,
            file_name="acidentes_filtrados.csv",
            mime="text/csv"
        )

    st.caption(f"Exibindo {total_acidentes} de {len(dados_completos)} acidentes disponíveis.")

except FileNotFoundError:
    st.error("O arquivo amostra_acidentes.csv não foi encontrado.")