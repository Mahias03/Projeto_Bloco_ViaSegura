import streamlit as st


st.set_page_config(
    page_title="Via Segura",
    page_icon="🚦",
    layout="wide"
)

pagina_inicio = st.Page(
    "pages/inicio.py",
    title="Início",
    icon="🏠",
    default=True
)

pagina_acidentes = st.Page(
    "pages/acidentes.py",
    title="Acidentes",
    icon="🚗"
)

pagina_noticias = st.Page(
    "pages/noticias.py",
    title="Notícias",
    icon="📰"
)

navegacao = st.navigation(
    [
        pagina_inicio,
        pagina_acidentes,
        pagina_noticias
    ]
)

navegacao.run()