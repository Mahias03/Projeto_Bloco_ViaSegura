# Modeling

Esta pasta reúne a documentação e os testes relacionados à modelagem do projeto.

Uma possibilidade será classificar a gravidade dos acidentes utilizando características como período, condição meteorológica, tipo de pista e traçado da via.

## TP4 — Avaliação de modelos de linguagem

### Objetivo

A função escolhida para o TP4 é gerar um resumo textual dos acidentes após a aplicação dos filtros.

Os indicadores serão calculados pela aplicação e enviados ao modelo. A LLM será responsável por redigir o resumo, não por calcular os dados.

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

### Próximos passos

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