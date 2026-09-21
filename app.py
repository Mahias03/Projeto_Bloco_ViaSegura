import re
import pandas       as pd
import streamlit    as st

from pathlib        import Path
from wordcloud      import WordCloud
from collections    import Counter

st.set_page_config(
    page_title="Via Segura",
    page_icon="🚦",
    layout="wide")

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

caminho_dados = (
    Path(__file__).parent
    / "02_data_ingest_understanding"
    / "data"
    / "amostra_acidentes.csv"
)

caminho_noticias = (
    Path(__file__).parent
    / "02_data_ingest_understanding"
    / "data"
    / "noticias_seguranca_viaria.csv"
)

st.title("🚦 Via Segura")
st.subheader("Análise de acidentes em rodovias federais brasileiras")

st.markdown(
    """
    O Via Segura é um projeto de análise de dados que busca facilitar
    a consulta e a interpretação dos registros de acidentes disponibilizados
    pela Polícia Rodoviária Federal.
    """
)

st.header("Problema de negócio")

st.write(
    """
    Os dados de acidentes em rodovias federais estão divididos em arquivos
    anuais e possuem muitas variáveis. Isso dificulta a identificação de
    padrões por usuários sem conhecimento técnico em análise de dados.
    """
)

st.header("Objetivos do projeto")

st.markdown(
    """
    - Organizar os dados oficiais de acidentes da PRF.
    - Apresentar indicadores de acidentes, feridos e mortos.
    - Permitir análises por período, estado, município e rodovia.
    - Identificar as principais causas e tipos de acidentes.
    - Facilitar a interpretação dos resultados por meio de um dashboard.
    - Futuramente, gerar resumos automáticos utilizando uma LLM.
    """
)

st.header("ODS relacionados")

coluna_ods3, coluna_ods11 = st.columns(2)

with coluna_ods3:
    st.subheader("ODS 3 — Saúde e Bem-Estar")
    st.write(
        """
        Relaciona-se à redução de mortes e lesões provocadas
        por acidentes de trânsito.
        """
    )

with coluna_ods11:
    st.subheader("ODS 11 — Cidades e Comunidades Sustentáveis")
    st.write(
        """
        Relaciona-se ao desenvolvimento de sistemas de transporte
        mais seguros e sustentáveis.
        """
    )

st.header("Análise interativa dos acidentes")

try:
    dados = carregar_dados(caminho_dados)

    # Prepara as opções disponíveis para cada filtro.
    opcoes_uf = sorted(dados["uf"].dropna().astype(str).unique())
    opcoes_classificacao = sorted(dados["classificacao_acidente"].dropna().astype(str).unique())
    opcoes_fase_dia = sorted(dados["fase_dia"].dropna().astype(str).unique())

    coluna_filtro1, coluna_filtro2, coluna_filtro3 = st.columns(3)

    with coluna_filtro1:
        ufs_selecionadas = st.multiselect("Estado", opcoes_uf)

    with coluna_filtro2:
        classificacoes_selecionadas = st.multiselect("Classificação", opcoes_classificacao)

    with coluna_filtro3:
        fases_selecionadas = st.multiselect("Fase do dia", opcoes_fase_dia)

    st.caption("Quando nenhuma opção é selecionada, todos os registros são apresentados.")

    dados_filtrados = dados.copy()

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

    st.caption(f"Exibindo {total_acidentes} de {len(dados)} acidentes disponíveis na amostra.")

except FileNotFoundError:
    st.error("O arquivo amostra_acidentes.csv não foi encontrado.")

st.header("Segurança viária na web")

st.write(
    """
    Esta seção apresenta notícias coletadas do site do Observatório Nacional
    de Segurança Viária por meio de Requests e BeautifulSoup.
    """
)

try:
    noticias = carregar_dados(caminho_noticias)

    busca = st.text_input(
        "Pesquisar nas notícias",
        placeholder="Digite uma palavra, como rodovia ou segurança"
    )

    noticias_filtradas = noticias

    # Pesquisa a palavra informada nos títulos e subtítulos das notícias.
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

st.header("Projetos e iniciativas semelhantes")

st.markdown(
    """
    - [Indicadores de Segurança Viária — Infra S.A.](https://paineis.infrasa.gov.br/dashboard/9)  
      Painel que apresenta indicadores e informações relacionadas aos sinistros de trânsito e à segurança viária.

    - [Dados e Dashboards — Observatório Nacional de Segurança Viária](https://www.onsv.org.br/estudos/dados)  
      Reúne estudos, painéis e projetos de análise de dados sobre acidentes, mortalidade e segurança no trânsito.

    - [Projeto Vida no Trânsito — Ministério da Saúde](https://www.gov.br/saude/pt-br/composicao/svsa/vigilancia-de-doencas-cronicas-nao-transmissiveis/vigilancia-de-violencias-e-acidentes/pvt)  
      Iniciativa que utiliza dados e evidências para apoiar o planejamento e a avaliação de ações de prevenção de mortes e lesões no trânsito.
    """
)

st.divider()

st.caption("Projeto individual desenvolvido por Matheus Afonso.")