# Acceptance

A etapa de aceitação verifica se a aplicação atende aos objetivos definidos para o TP3.

## Critérios de aceitação

A aplicação deve:

- ser instalada utilizando o `requirements.txt` e o `requirements_api.txt`;
- iniciar pelo arquivo `app.py` sem apresentar erros;
- apresentar navegação entre as páginas de início, acidentes, notícias e API;
- carregar a amostra de acidentes da PRF;
- apresentar indicadores de acidentes, feridos e mortos;
- permitir filtros por estado, classificação e fase do dia;
- atualizar os indicadores e a tabela conforme os filtros;
- permitir o upload de arquivos CSV compatíveis;
- manter os dados enviados durante a sessão;
- permitir a remoção dos dados enviados;
- permitir o download dos registros filtrados;
- apresentar as notícias coletadas da web;
- permitir pesquisas nos títulos e subtítulos;
- apresentar estatísticas e uma nuvem de palavras;
- iniciar a API pelo arquivo `api.py`;
- disponibilizar as rotas de consulta de acidentes e notícias;
- permitir o envio temporário de acidentes pelo método POST;
- apresentar a documentação automática da API;
- integrar a API com a aplicação Streamlit;
- exibir corretamente as fontes e os projetos semelhantes;
- possuir documentação atualizada.

## Resultado esperado

A aplicação será considerada aceita quando as funcionalidades da interface e da API forem executadas sem erros e os resultados apresentados forem compatíveis com os filtros e arquivos utilizados.

Os acidentes enviados para a API devem permanecer disponíveis enquanto o servidor estiver funcionando. A remoção desses registros após o encerramento do servidor é o comportamento esperado nesta versão.

A revisão final também deverá confirmar que o repositório está atualizado no GitHub e não possui alterações pendentes.