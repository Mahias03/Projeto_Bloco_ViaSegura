import streamlit as st

from wordcloud import WordCloud

from comum import analisar_noticias, carregar_dados, caminho_noticias

st.title("Segurança viária na web")

st.write(
    """
    Esta página apresenta notícias coletadas do site do Observatório Nacional
    de Segurança Viária por meio de Requests e BeautifulSoup.
    """
)

try:
    noticias = carregar_dados(caminho_noticias)

    busca = st.text_input("Pesquisar nas notícias", placeholder="Digite uma palavra, como rodovia ou segurança")

    noticias_filtradas = noticias

    # Pesquisa a palavra informada nos títulos e subtítulos.
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

        noticias_filtradas = noticias[filtro_titulo | filtro_subtitulo]

    st.metric("Notícias encontradas", len(noticias_filtradas))

    if noticias_filtradas.empty:
        st.warning("Nenhuma notícia foi encontrada para a pesquisa informada.")
    else:
        st.dataframe(
            noticias_filtradas[
                ["titulo", "data_publicacao", "link", "fonte"]
            ],
            column_config={
                "titulo": "Título",
                "data_publicacao": "Data de publicação",
                "link": st.column_config.LinkColumn("Acessar notícia"),
                "fonte": "Fonte"
            },
            width="stretch",
            hide_index=True
        )

        texto_nuvem, tabela_frequencias, total_palavras, palavras_unicas = analisar_noticias(noticias_filtradas)

        st.subheader("Estatísticas do conteúdo coletado")

        coluna_estatistica1, coluna_estatistica2 = st.columns(2)
        coluna_estatistica1.metric("Palavras analisadas", total_palavras)
        coluna_estatistica2.metric("Palavras diferentes", palavras_unicas)

        # Gera a nuvem com as palavras encontradas nos títulos e subtítulos.
        nuvem_palavras = WordCloud(
            width=1200,
            height=500,
            background_color="#0e1117",
            colormap="Blues",
            collocations=False
        ).generate(texto_nuvem)

        coluna_nuvem, coluna_grafico = st.columns([2, 1])

        with coluna_nuvem:
            st.subheader("Nuvem de palavras")

            st.image(
                nuvem_palavras.to_array(),
                caption="Palavras mais presentes nas notícias coletadas.",
                width="stretch"
            )

        with coluna_grafico:
            st.subheader("Palavras mais frequentes")

            st.bar_chart(
                tabela_frequencias,
                x="palavra",
                y="frequencia"
            )

    st.caption("Conteúdo coletado do Observatório Nacional de Segurança Viária.")

except FileNotFoundError:
    st.error("O arquivo noticias_seguranca_viaria.csv não foi encontrado.")