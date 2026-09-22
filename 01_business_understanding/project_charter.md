# Project Charter — Via Segura

## 1. Título do projeto

Via Segura: análise de acidentes em rodovias federais brasileiras.

## 2. Contexto do projeto

A Polícia Rodoviária Federal disponibiliza dados abertos sobre acidentes ocorridos nas rodovias federais brasileiras. Esses arquivos possuem muitas variáveis e podem exigir conhecimentos técnicos para serem consultados e interpretados.

O Via Segura foi proposto para transformar parte desses dados em informações mais acessíveis, utilizando uma aplicação web interativa desenvolvida com Python e Streamlit.

## 3. Problema de negócio

A quantidade de registros, a variedade das informações e a divisão dos dados em arquivos dificultam a identificação de padrões por cidadãos, estudantes, pesquisadores e outros usuários sem experiência em análise de dados.

Além disso, notícias e informações relacionadas à segurança viária estão distribuídas em páginas externas, dificultando a consulta conjunta dos dados de acidentes e dos conteúdos informativos.

## 4. Objetivo geral

Desenvolver uma aplicação interativa para organizar, consultar e apresentar dados de acidentes em rodovias federais, complementando a análise com conteúdos públicos coletados da web sobre segurança viária.

## 5. Objetivos específicos

- Organizar uma amostra dos dados oficiais de acidentes disponibilizados pela PRF.
- Apresentar indicadores de acidentes, pessoas feridas e mortes.
- Permitir filtros por estado, classificação do acidente e fase do dia.
- Apresentar os registros filtrados em uma tabela interativa.
- Permitir que o usuário envie arquivos CSV com novos registros.
- Manter os dados enviados durante as interações do usuário com a aplicação.
- Permitir o download dos registros filtrados em formato CSV.
- Coletar notícias sobre segurança viária utilizando Requests e BeautifulSoup.
- Armazenar o conteúdo coletado da web em um arquivo CSV.
- Permitir pesquisas nos títulos e subtítulos das notícias.
- Gerar estatísticas de palavras e uma nuvem de palavras com base no conteúdo coletado.
- Utilizar cache para evitar leituras e processamentos desnecessários.
- Disponibilizar uma interface simples e de fácil utilização.

## 6. Metas e indicadores de sucesso

| Meta | Indicador de sucesso |
|---|---|
| Carregar os dados de acidentes | Amostra da PRF apresentada sem erros na aplicação |
| Permitir a consulta interativa | Filtros por estado, classificação e fase do dia funcionando |
| Apresentar os principais indicadores | Quantidades de acidentes, feridos e mortos atualizadas pelos filtros |
| Integrar conteúdo externo | Notícias coletadas com Requests e BeautifulSoup e armazenadas em CSV |
| Analisar o conteúdo coletado | Pesquisa, tabela, estatísticas, gráfico e nuvem de palavras disponíveis |
| Permitir o envio de dados | Arquivos CSV compatíveis adicionados à análise |
| Manter os dados durante as interações | Dados enviados preservados com estado de sessão |
| Permitir a exportação dos resultados | Download dos registros filtrados em CSV funcionando |
| Melhorar a performance | Leitura e processamento de dados realizados com cache |
| Garantir a reprodução do projeto | Aplicação executada utilizando o `requirements.txt` |

## 7. Público-alvo

O público-alvo é formado por cidadãos, motoristas, pesquisadores, estudantes e profissionais interessados em segurança viária.

A aplicação também pode auxiliar gestores públicos e organizações do setor na consulta e interpretação inicial dos dados, sem substituir análises oficiais ou estudos técnicos especializados.

## 8. ODS atendidos

### ODS 3 — Saúde e Bem-Estar

O projeto está relacionado ao ODS 3 por trabalhar com informações sobre mortes e lesões provocadas por acidentes de trânsito. A análise desses dados pode contribuir para a compreensão dos fatores associados às ocorrências.

### ODS 11 — Cidades e Comunidades Sustentáveis

O projeto também está relacionado ao ODS 11 por apresentar informações relacionadas à segurança dos sistemas de transporte e dos deslocamentos realizados em rodovias federais.

## 9. Escopo do projeto

### Itens incluídos no escopo atual

- Utilização de uma amostra de acidentes registrados pela PRF em 2025.
- Apresentação de indicadores de acidentes, feridos e mortos.
- Aplicação de filtros interativos.
- Exibição dos registros em tabela.
- Upload de arquivos CSV compatíveis com a base.
- Download dos dados filtrados.
- Utilização de cache e estado de sessão.
- Coleta de notícias de segurança viária em uma página pública.
- Armazenamento do conteúdo coletado em CSV.
- Pesquisa nas notícias coletadas.
- Estatísticas de palavras, gráfico de frequência e nuvem de palavras.
- Controle de versão com Git e armazenamento do projeto no GitHub.

### Itens fora do escopo atual

- Monitoramento de acidentes em tempo real.
- Análise de acidentes ocorridos exclusivamente em vias estaduais ou municipais.
- Previsão de acidentes utilizando modelos de aprendizado de máquina.
- Substituição das análises realizadas pelos órgãos responsáveis.
- Geração automática de conclusões por modelo de linguagem.
- Integração completa dos dados de 2021 a 2025.
- Disponibilização de um mapa interativo de acidentes.

Os itens fora do escopo atual poderão ser considerados em etapas futuras do projeto.

## 10. Fontes de dados

### Polícia Rodoviária Federal

Fonte principal dos registros de acidentes. O protótipo atual utiliza uma amostra de 20 acidentes extraídos da base de 2025.

### Observatório Nacional de Segurança Viária

Fonte do conteúdo coletado da web. Foram extraídos títulos, subtítulos, datas de publicação, links e identificação da fonte das notícias.

### Instituto Brasileiro de Geografia e Estatística

Fonte prevista para uma etapa futura de padronização e complementação das informações geográficas de estados e municípios.

## 11. Stakeholders

- Responsável pelo desenvolvimento: Matheus Afonso.
- Instituição de ensino: Instituto Infnet.
- Fornecedor dos dados de acidentes: Polícia Rodoviária Federal.
- Fornecedor do conteúdo sobre segurança viária: Observatório Nacional de Segurança Viária.
- Fonte geográfica prevista: Instituto Brasileiro de Geografia e Estatística.
- Usuários da aplicação: cidadãos, motoristas, estudantes, pesquisadores, profissionais e gestores públicos.

## 12. Tecnologias utilizadas

- Python
- Pandas
- Streamlit
- Requests
- BeautifulSoup
- WordCloud
- Git
- GitHub
- Arquivos CSV
- Ambiente virtual Python

## 13. Principais entregáveis

- Aplicação interativa desenvolvida em Streamlit.
- Script separado para coleta de notícias da web.
- Arquivo CSV com a amostra de acidentes.
- Arquivo CSV com as notícias coletadas.
- Filtros e indicadores interativos.
- Serviço de upload e download de arquivos CSV.
- Nuvem de palavras e estatísticas do conteúdo coletado.
- Arquivo `requirements.txt`.
- Documentação do projeto.
- Repositório versionado no GitHub.

## 14. Organização do projeto

O desenvolvimento segue uma estrutura inspirada no TDSP, separando as etapas de entendimento do negócio, ingestão e entendimento dos dados, modelagem, implantação e aceitação.

O Git é utilizado para registrar as alterações do código, enquanto o GitHub mantém o repositório remoto do projeto.

## 15. Melhorias futuras

- Ampliar a análise para os dados completos da PRF entre 2021 e 2025.
- Adicionar filtros por ano, município e rodovia.
- Integrar a API de Localidades do IBGE.
- Criar um mapa interativo utilizando latitude e longitude.
- Desenvolver novos gráficos e indicadores.
- Avaliar a utilização de uma LLM para gerar resumos dos resultados.
- Preparar a implantação pública da aplicação.