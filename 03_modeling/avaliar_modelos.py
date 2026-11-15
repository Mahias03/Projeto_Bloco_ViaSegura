import json
import sys
import time
import torch
from huggingface_hub import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer

modelos = {
    "pequeno": "Qwen/Qwen2.5-0.5B-Instruct",
    "grande": "Qwen/Qwen2.5-1.5B-Instruct",
    "granite": "ibm-granite/granite-3.3-2b-instruct"
}

if len(sys.argv) != 2 or sys.argv[1] not in modelos:
    raise SystemExit("Informe o modelo: pequeno, grande ou granite.")

nome_modelo = modelos[sys.argv[1]]

# Os mesmos dados fictícios serão utilizados para os dois modelos.
casos = [
    {
        "estado": "SP", "classificacao": "Todas", "fase_dia": "Todas",
        "acidentes": 8, "mortos": 1, "feridos": 12
    },
    {
        "estado": "RJ", "classificacao": "Com Vítimas Fatais", "fase_dia": "Plena Noite",
        "acidentes": 4, "mortos": 5, "feridos": 2
    },
    {
        "estado": "CE", "classificacao": "Sem Vítimas", "fase_dia": "Pleno dia",
        "acidentes": 0, "mortos": 0, "feridos": 0
    }
]
# Testa múltiplas seleções e filtros não aplicados.
casos.extend([
    {
        "estado": ["SP", "RJ"], "classificacao": ["Com Vítimas Feridas"], "fase_dia": ["Pleno dia", "Plena Noite"], 
        "acidentes": 7, "mortos": 0, "feridos": 5
    },
    {
        "estado": [], "classificacao": [], "fase_dia": [],
        "acidentes": 20, "mortos": 3, "feridos": 25
    }
])

instrucao = (
    "Você é um assistente do projeto Via Segura. "
    "Os dados representam registros filtrados da base disponível. "
    "Descreva em português os filtros aplicados e os indicadores em até duas frases. "
    "Listas vazias ou o valor Todas indicam filtros não aplicados. "
    "Preserve os números e não invente períodos, causas ou comparações. "
    "Se houver zero acidentes, informe que nenhum registro foi encontrado com os filtros informados. "
    "Não conclua que os dados representam todos os acidentes de um lugar."
)

print(f"Modelo: {nome_modelo}")
print("Preparando os arquivos. No primeiro uso, o modelo será baixado.")

# Separa o download da medição do carregamento do modelo.
pasta_modelo = snapshot_download(nome_modelo)

inicio_carregamento = time.perf_counter()

tokenizador = AutoTokenizer.from_pretrained(pasta_modelo, local_files_only=True)
modelo = AutoModelForCausalLM.from_pretrained(pasta_modelo, local_files_only=True)
modelo.eval()

tempo_carregamento = time.perf_counter() - inicio_carregamento
print(f"Tempo de carregamento, sem download: {tempo_carregamento:.2f} segundos")

for numero, caso in enumerate(casos, start=1):
    dados = json.dumps(caso, ensure_ascii=False)

    mensagens = [
        {"role": "system", "content": instrucao},
        {"role": "user", "content": f"Dados para análise: {dados}"}
    ]

    entradas = tokenizador.apply_chat_template(
        mensagens,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt"
    )

    inicio_geracao = time.perf_counter()

    with torch.inference_mode():
        saida = modelo.generate(
            **entradas,
            max_new_tokens=100,
            do_sample=False,
            pad_token_id=tokenizador.eos_token_id
        )

    tempo_geracao = time.perf_counter() - inicio_geracao

    # Remove o texto de entrada para exibir apenas a resposta gerada.
    novos_tokens = saida[0][entradas["input_ids"].shape[-1]:]
    resumo = tokenizador.decode(novos_tokens, skip_special_tokens=True)

    print(f"\nCaso {numero}")
    print(f"Entrada: {dados}")
    print(f"Resumo: {resumo}")
    print(f"Tempo de geração: {tempo_geracao:.2f} segundos")