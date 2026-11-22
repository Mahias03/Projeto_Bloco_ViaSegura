# Modeling

Esta pasta reúne a documentação e os testes relacionados à modelagem do projeto.

Uma possibilidade será classificar a gravidade dos acidentes utilizando características como período, condição meteorológica, tipo de pista e traçado da via.

## TP4 — Avaliação de modelos de linguagem

### Objetivo

A função escolhida para o TP4 é gerar um resumo textual dos acidentes após a aplicação dos filtros.

Os indicadores e as contagens por estado e fase do dia são calculados pela aplicação e enviados à LLM. O modelo é responsável por redigir o resumo, não por calcular os dados.

### Decisões iniciais

- Executar o modelo localmente, sem utilizar uma API externa.
- Comparar duas versões da família Qwen2.5 antes de escolher o modelo.
- Realizar os testes na CPU.
- Manter a análise limitada aos dados disponíveis na aplicação, sem tratá-los como o total de acidentes do Brasil.

### Ambiente de teste

- Processador: Intel Core i5-13400F.
- Memória RAM: 31,9 GB.
- Python: 3.14.6.
- PyTorch: 2.15.0 para CPU.
- Transformers: 5.23.0.

### Primeira comparação

Foram utilizados três conjuntos de dados fictícios e a mesma instrução para os dois modelos. Cada caso foi executado uma vez por modelo.

| Modelo | Carregamento sem download | Caso 1 | Caso 2 | Caso 3 | Média de geração |
|---|---:|---:|---:|---:|---:|
| [Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct) | 3,12 s | 2,72 s | 3,08 s | 3,13 s | 2,98 s |
| [Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct) | 4,68 s | 7,84 s | 11,27 s | 7,02 s | 8,71 s |

Os tempos são indicativos e podem variar conforme a máquina e a entrada.

### Observações

- O modelo menor foi mais rápido, mas acrescentou uma referência a dia que não havia sido informada no primeiro caso.
- O modelo maior apresentou respostas mais claras nos dois primeiros casos, com os números informados.
- No terceiro caso, ambos tiveram dificuldade para expressar que nenhum registro havia sido encontrado com os filtros aplicados. O modelo maior também trocou o sentido da classificação “Sem Vítimas”.
- Os resultados ainda não são suficientes para considerar qualquer um dos modelos aprovado para todos os cenários.

### Planejamento após a primeira comparação

- Testar uma instrução revisada e casos com múltiplas seleções e filtros vazios.
- Escolher o modelo considerando fidelidade, clareza, tempo e recursos necessários.
- Para resultados sem registros, exibir uma mensagem da aplicação sem solicitar um resumo à LLM.
- Integrar o modelo escolhido ao FastAPI e à interface Streamlit.

### Segunda rodada de testes

A instrução foi revisada e foram acrescentados dois casos: um com múltiplos filtros selecionados e outro sem filtros. Foram cinco casos fictícios, executados uma vez por modelo.

| Modelo | Carregamento | Geração média | Maior tempo de geração |
|---|---:|---:|---:|
| Qwen2.5-0.5B-Instruct | 3,37 s | 3,41 s | 4,15 s |
| Qwen2.5-1.5B-Instruct | 4,45 s | 13,66 s | 15,66 s |

O modelo menor confundiu o estado RJ e informou ausência de registros em dois casos que possuíam acidentes.

O modelo maior preservou melhor as informações, mas omitiu o número de mortos em um caso e acrescentou uma orientação não solicitada em outro.

O Qwen2.5-1.5B-Instruct é o candidato inicial para integração, sujeito à avaliação do tempo de resposta e a novos testes. As respostas geradas devem ser conferidas com os indicadores calculados pela aplicação.

## Comparação dos modelos

Foram testados três modelos locais com os mesmos cinco casos
fictícios de indicadores de acidentes.

| Modelo | Carregamento sem download | Geração média por caso |
|---|---:|---:|
| Qwen2.5-0.5B-Instruct | 3,37 s | 3,41 s |
| Qwen2.5-1.5B-Instruct | 4,45 s | 13,66 s |
| Granite-3.3-2B-Instruct | 6,64 s | 32,53 s |

Os testes foram executados na CPU do computador utilizado no desenvolvimento. Os tempos apresentados correspondem a uma execução de cada caso.

O modelo Qwen2.5-0.5B apresentou erros na interpretação de alguns filtros e indicadores. O Granite apresentou respostas incompletas e conclusões sem suporte nos dados.

O Qwen2.5-1.5B foi escolhido para o protótipo por apresentar, nesses testes, respostas mais adequadas e menor tempo de geração que o Granite. A avaliação com cinco casos não garante que o modelo sempre produza respostas corretas.

Os indicadores calculados pela aplicação deverão continuar disponíveis separadamente para conferência.

### Acessibilidade dos modelos

Os três modelos comparados estão disponíveis no Hugging Face sob licença Apache 2.0:

- [Qwen2.5-0.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct)
- [Qwen2.5-1.5B-Instruct](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct)
- [Granite-3.3-2B-Instruct](https://huggingface.co/ibm-granite/granite-3.3-2b-instruct)

Os modelos podem ser baixados e executados localmente. Após o download dos arquivos e a instalação das dependências, não é necessário utilizar um serviço de IA na nuvem para gerar respostas.

O Qwen2.5-1.5B foi escolhido considerando os resultados da comparação, sua disponibilidade e a possibilidade de execução local. Na aplicação, seus arquivos são carregados do cache local.

### Memória RAM

No teste em CPU, após a geração de um resumo, o processo da API apresentou uso de 3,39 GB de RAM e pico registrado de 3,43 GB. A medição inclui a API e suas bibliotecas, não apenas o modelo.

Como estimativa inicial para executar o projeto, considera-se uma máquina com 8 GB de RAM, deixando espaço também para o sistema e a interface. Esse valor não foi testado como requisito mínimo e pode variar conforme o ambiente e os dados utilizados.

### Evidências dos testes

**Resposta real — HTTP 200**

Foi enviada à rota `POST /resumo` uma requisição com os seguintes dados:

- Estado: RJ.
- Acidentes: 2.
- Mortos: 0.
- Feridos: 3.
- Fase do dia: 2 acidentes em pleno dia.

Trecho da resposta gerada:

> Foram identificados 2 acidentes no estado do Rio de Janeiro (RJ), com 3 feridos. Nenhum desses acidentes resultou em mortes.

**Dados inconsistentes — HTTP 422**

Foi informado um total de 3 acidentes, enquanto a soma por estado era 2. A API rejeitou a entrada com a mensagem:

```text
Value error, A soma por estado deve ser igual ao total de acidentes.
```

**Falhas simuladas — 503 e 500**

Os testes abaixo simularam falhas na função da API, sem realizar requisições HTTP:

```text
503: O modelo local não está disponível. Verifique o terminal da API.
500: Não foi possível gerar o resumo. Verifique o terminal da API.
```

Os resumos da LLM são experimentais e devem ser conferidos com os indicadores e registros apresentados.

### Implementação no TP4

O modelo escolhido para o protótipo foi o Qwen2.5-1.5B-Instruct, executado localmente na CPU com PyTorch e Transformers. O modelo deve ser baixado previamente e é carregado do cache local.

A aplicação calcula os indicadores e as contagens dos registros filtrados. Esses dados e os filtros selecionados são enviados em JSON para a rota `POST /resumo`, que utiliza a LLM para gerar o texto.

A resposta da API possui estrutura definida com Pydantic. Quando não há acidentes, a API retorna uma mensagem pronta sem chamar a LLM; na interface, o botão de geração não é apresentado.

Durante o desenvolvimento, algumas respostas apresentaram contradições e erros na comparação entre fases do dia. A instrução foi ajustada, mas a geração continua experimental e não há validação automática da veracidade do texto. Os indicadores e a tabela devem ser consultados para conferência.

Os tempos registrados nas comparações foram obtidos com instruções anteriores e podem diferir dos tempos da versão final.