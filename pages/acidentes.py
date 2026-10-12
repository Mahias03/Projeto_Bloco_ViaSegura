import pandas as pd
import streamlit as st

from comum import carregar_dados, caminho_dados

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