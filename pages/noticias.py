import streamlit as st
import requests

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

        st.subheader("Resumo de notícia com IA")

        try:
            caminho_textos = caminho_noticias.with_name("noticias_com_texto.csv")
            noticias_com_texto = carregar_dados(caminho_textos)

            # Mostra apenas notícias filtradas que possuem texto coletado.
            opcoes = noticias_com_texto[
                noticias_com_texto["link"].isin(noticias_filtradas["link"])
            ].copy()

            opcoes["texto"] = opcoes["texto"].fillna("").astype(str).str.strip()
            opcoes = opcoes[opcoes["texto"] != ""].drop_duplicates(subset="link")

            if opcoes.empty:
                st.info("Não há textos disponíveis para as notícias filtradas.")
            else:
                titulos = dict(zip(opcoes["link"], opcoes["titulo"]))

                link_selecionado = st.selectbox(
                    "Escolha uma notícia",
                    options=list(titulos),
                    format_func=lambda link: titulos[link]
                )

                noticia = opcoes[opcoes["link"] == link_selecionado].iloc[0]
                texto_noticia = noticia["texto"]

                st.link_button("Abrir notícia original", link_selecionado)
                st.caption("Confira o resumo com a notícia original: a IA pode cometer erros.")

                if not 100 <= len(texto_noticia) <= 8000:
                    st.warning("O texto deve ter entre 100 e 8.000 caracteres.")
                elif st.button("Gerar resumo da notícia"):
                    try:
                        with st.spinner("Gerando resumo. Isso pode levar alguns segundos..."):
                            resposta = requests.post(
                                "http://127.0.0.1:8000/resumo-noticia",
                                json={"texto": texto_noticia},
                                timeout=300
                            )

                            resposta.raise_for_status()
                            resultado = resposta.json()

                        if not isinstance(resultado.get("resumo"), str) or not resultado["resumo"].strip():
                            raise ValueError("Resumo vazio ou em formato inesperado.")

                        st.write(resultado["resumo"])

                    except requests.Timeout:
                        st.error("A API demorou para responder.")
                    except requests.ConnectionError:
                        st.error("Não foi possível conectar à API. Verifique se ela está em execução.")
                    except requests.HTTPError as erro:
                        st.error(f"Não foi possível gerar o resumo. HTTP: {erro.response.status_code}.")
                    except (requests.RequestException, ValueError):
                        st.error("Ocorreu um erro ao obter o resumo.")

        except FileNotFoundError:
            st.warning("O arquivo noticias_com_texto.csv não foi encontrado.")

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