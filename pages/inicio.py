import streamlit as st

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
    st.write("Relaciona-se à redução de mortes e lesões provocadas por acidentes de trânsito.")

with coluna_ods11:
    st.subheader("ODS 11 — Cidades e Comunidades Sustentáveis")
    st.write("Relaciona-se ao desenvolvimento de sistemas de transporte mais seguros e sustentáveis.")

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