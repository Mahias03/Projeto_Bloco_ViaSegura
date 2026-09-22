# Via Segura

Projeto individual desenvolvido por Matheus Afonso para o TP2 da disciplina de Projeto de Bloco — Inteligência Artificial Aplicada.

## Descrição

O Via Segura é uma aplicação desenvolvida em Python com Streamlit para facilitar a consulta e a interpretação de dados sobre acidentes em rodovias federais brasileiras.

O projeto apresenta indicadores e filtros interativos, permite o envio e o download de arquivos CSV e reúne notícias sobre segurança viária coletadas da web.

## Problema de negócio

Os dados de acidentes em rodovias federais possuem muitas variáveis e são disponibilizados em arquivos separados. Isso dificulta a consulta e a identificação de informações por usuários sem conhecimento técnico em análise de dados.

## Objetivo

Organizar e apresentar dados de acidentes em uma aplicação interativa, permitindo consultar ocorrências, visualizar indicadores e acessar conteúdos relacionados à segurança viária.

## Funcionalidades

- Indicadores de acidentes, pessoas feridas e mortes.
- Filtros por estado, classificação do acidente e fase do dia.
- Tabela interativa com os registros filtrados.
- Upload de arquivos CSV com novos registros.
- Download dos dados filtrados.
- Uso de cache para melhorar o desempenho.
- Uso de estado de sessão para manter os dados enviados.
- Coleta de notícias com Requests e BeautifulSoup.
- Pesquisa nos títulos e subtítulos das notícias.
- Gráfico com as palavras mais frequentes.
- Nuvem de palavras do conteúdo coletado.

## ODS relacionados

- ODS 3 — Saúde e Bem-Estar.
- ODS 11 — Cidades e Comunidades Sustentáveis.

## Fontes de dados

- [Dados Abertos da Polícia Rodoviária Federal](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dados-abertos-da-prf)
- [Dicionário de Dados de Acidentes da PRF](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos/dicionario-acidentes)
- [Comunicação do Observatório Nacional de Segurança Viária](https://www.onsv.org.br/comunicacao)
- [API de Localidades do IBGE](https://servicodados.ibge.gov.br/api/docs/localidades) — prevista para uma etapa futura.

## Estrutura do projeto

- `01_business_understanding`: entendimento do problema e Project Charter.
- `02_data_ingest_understanding`: preparação, documentação e armazenamento dos dados.
- `02_data_ingest_understanding/coletar_noticias.py`: coleta das notícias da web.
- `02_data_ingest_understanding/criar_amostra.py`: criação da amostra de acidentes.
- `02_data_ingest_understanding/data`: arquivos CSV utilizados pela aplicação.
- `03_modeling`: planejamento da etapa de modelagem.
- `04_deployment`: informações relacionadas à implantação.
- `05_acceptance`: critérios de validação e aceitação.
- `app.py`: aplicação principal em Streamlit.
- `requirements.txt`: dependências do projeto.
- `.gitignore`: arquivos e pastas ignorados pelo Git.

## Tecnologias utilizadas

- Python
- Pandas
- Streamlit
- Requests
- BeautifulSoup
- WordCloud
- Git
- GitHub

## Situação atual

O TP2 possui filtros interativos, indicadores, coleta de conteúdo da web, análise de palavras, cache, estado de sessão e serviço de upload e download de arquivos CSV.

Como melhorias futuras, poderão ser adicionados dados de outros anos, filtros adicionais, integração com o IBGE, mapa interativo, modelos de aprendizado de máquina e geração automática de resumos.