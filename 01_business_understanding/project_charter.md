# Project Charter — Via Segura

## 1. Título do projeto

Via Segura: análise de acidentes em rodovias federais brasileiras.

## 2. Contexto do projeto

A Polícia Rodoviária Federal disponibiliza dados abertos sobre acidentes ocorridos nas rodovias federais brasileiras. Esses arquivos possuem muitas variáveis e podem exigir conhecimentos técnicos para serem consultados e interpretados.

O Via Segura foi proposto para transformar parte desses dados em informações mais acessíveis, utilizando uma aplicação web multipágina desenvolvida com Python e Streamlit.

O projeto também reúne notícias sobre segurança viária coletadas da web e disponibiliza parte dos dados por meio de uma API desenvolvida com FastAPI.

## 3. Problema de negócio

A quantidade de registros, a variedade das informações e a divisão dos dados em arquivos dificultam a identificação de padrões por cidadãos, estudantes, pesquisadores e outros usuários sem experiência em análise de dados.

Além disso, notícias e informações relacionadas à segurança viária estão distribuídas em páginas externas, dificultando a consulta conjunta dos dados de acidentes e dos conteúdos informativos.

## 4. Objetivo geral

Desenvolver uma aplicação multipágina para organizar, consultar e apresentar dados de acidentes em rodovias federais, complementando a análise com conteúdos públicos coletados da web e disponibilizando os dados por meio de uma API.

## 5. Objetivos específicos

- Organizar uma amostra dos dados oficiais de acidentes disponibilizados pela PRF.
- Apresentar indicadores de acidentes, pessoas feridas e mortes.
- Permitir filtros por estado, classificação do acidente e fase do dia.
- Apresentar os registros filtrados em uma tabela interativa.
- Permitir o upload e o download de arquivos CSV.
- Manter os dados enviados durante a sessão do usuário.
- Coletar notícias utilizando Requests e BeautifulSoup.
- Armazenar o conteúdo coletado da web em um arquivo CSV.
- Permitir pesquisas e análises das palavras presentes nas notícias.
- Organizar a aplicação em páginas com funcionalidades distintas.
- Disponibilizar consultas aos acidentes e às notícias por uma API.
- Permitir o envio e a validação de registros por uma rota POST.
- Utilizar cache para evitar processamentos desnecessários.
- Preparar os dados para uma futura integração com uma LLM.

## 6. Metas e indicadores de sucesso

| Meta | Indicador de sucesso |
|---|---|
| Carregar os dados de acidentes | Amostra da PRF apresentada sem erros |
| Permitir a consulta interativa | Filtros por estado, classificação e fase do dia funcionando |
| Apresentar os principais indicadores | Quantidades de acidentes, feridos e mortos atualizadas pelos filtros |
| Organizar a interface | Navegação funcionando entre páginas com finalidades distintas |
| Integrar conteúdo externo | Notícias coletadas com Requests e BeautifulSoup e armazenadas em CSV |
| Analisar o conteúdo coletado | Pesquisa, tabela, estatísticas, gráfico e nuvem de palavras disponíveis |
| Permitir entrada e saída de arquivos | Upload e download de arquivos CSV funcionando |
| Manter os dados durante a sessão | Dados enviados preservados com estado de sessão |
| Disponibilizar os dados pela API | Rotas GET de acidentes e notícias funcionando |
| Permitir o envio pela API | Rota POST validando e recebendo registros |
| Integrar API e Streamlit | Consultas e envios realizados pela interface da aplicação |
| Documentar a API | Rotas apresentadas na documentação automática `/docs` |
| Garantir a reprodução do projeto | Dependências registradas em `requirements.txt` e `requirements_api.txt` |

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
- Organização da aplicação em múltiplas páginas.
- Coleta de notícias de segurança viária.
- Armazenamento do conteúdo coletado em CSV.
- Pesquisa e análise das notícias coletadas.
- API para consulta de acidentes e notícias.
- Rota POST para validação e envio temporário de registros.
- Integração da API com a aplicação Streamlit.
- Controle de versão com Git e GitHub.

### Itens fora do escopo atual

- Monitoramento de acidentes em tempo real.
- Análise de acidentes ocorridos exclusivamente em vias estaduais ou municipais.
- Integração completa dos dados de 2021 a 2025.
- Previsão de acidentes utilizando aprendizado de máquina.
- Geração automática de conclusões por uma LLM.
- Mapa interativo de acidentes.
- Armazenamento permanente dos registros enviados pela API.
- Implantação pública da API.

Os itens fora do escopo atual poderão ser considerados em etapas futuras.

## 10. Fontes de dados

### Polícia Rodoviária Federal

Fonte principal dos registros de acidentes. O protótipo utiliza uma amostra de 20 acidentes extraídos da base de 2025.

### Observatório Nacional de Segurança Viária

Fonte do conteúdo coletado da web. Foram extraídos títulos, subtítulos, datas de publicação, links e identificação da fonte das notícias.

O uso de Selenium foi avaliado, mas não foi necessário porque o conteúdo utilizado está disponível no HTML obtido pelo Requests.

### Instituto Brasileiro de Geografia e Estatística

Fonte prevista para uma etapa futura de padronização e complementação das informações geográficas de estados e municípios.

## 11. Stakeholders

- Responsável pelo desenvolvimento: Matheus Afonso.
- Instituição de ensino: Instituto Infnet.
- Fornecedor dos dados de acidentes: Polícia Rodoviária Federal.
- Fornecedor do conteúdo sobre segurança viária: Observatório Nacional de Segurança Viária.
- Fonte geográfica prevista: Instituto Brasileiro de Geografia e Estatística.
- Usuários: cidadãos, motoristas, estudantes, pesquisadores, profissionais e gestores públicos.

## 12. Tecnologias utilizadas

- Python
- Pandas
- Streamlit
- FastAPI
- Uvicorn
- Pydantic
- Requests
- BeautifulSoup
- WordCloud
- Git
- GitHub
- Arquivos CSV e JSON
- Ambiente virtual Python

## 13. Principais entregáveis

- Aplicação multipágina desenvolvida em Streamlit.
- Página inicial com o contexto do projeto.
- Página para análise interativa dos acidentes.
- Página para consulta e análise das notícias.
- Página para integração com a API.
- API com rotas GET e POST.
- Documentação automática da API.
- Script separado para coleta de notícias.
- Arquivo CSV com a amostra de acidentes.
- Arquivo CSV com as notícias coletadas.
- Serviço de upload e download de arquivos CSV.
- Nuvem de palavras e estatísticas do conteúdo coletado.
- Arquivos `requirements.txt` e `requirements_api.txt`.
- Documentação do projeto.
- Repositório versionado no GitHub.

## 14. Organização do projeto

O desenvolvimento segue uma estrutura inspirada no TDSP, separando as etapas de entendimento do negócio, ingestão e entendimento dos dados, modelagem, implantação e aceitação.

A interface, a coleta de dados e a API são mantidas em arquivos separados. O Git registra as alterações do código, enquanto o GitHub mantém o repositório remoto do projeto.

## 15. Melhorias futuras

- Ampliar a análise para os dados completos da PRF entre 2021 e 2025.
- Adicionar filtros por ano, município e rodovia.
- Integrar a API de Localidades do IBGE.
- Criar um mapa interativo utilizando latitude e longitude.
- Desenvolver novos gráficos e indicadores.
- Armazenar permanentemente os registros enviados pela API.
- Avaliar uma LLM para gerar resumos, respostas e relatórios.
- Preparar a implantação pública da aplicação e da API.