import os, time, json
os.environ.setdefault("USE_TF", "0")  # evita travamento se houver TensorFlow

import laya

t0 = time.perf_counter()
agent = laya.load("convaiinnovations/laya", subfolder="multilingual")
print(f"load: {time.perf_counter() - t0:.1f}s")

questions = {
    "tema": {
        "type": "choice",
        "instructions": "Qual é o assunto principal deste documento?",
        "criteria": {
            "concessao": "concessão de aposentadoria, pensão, auxílio-doença, BPC, salário-maternidade, auxílio-reclusão",
            "manutencao": "revisão, reativação, prova de vida, alteração cadastral ou bancária de benefício",
            "disciplinar": "PAD, sindicância, advertência, investigação administrativa, conduta funcional",
            "atendimento": "reclamação, agendamento, ouvidoria, atendimento presencial ou remoto",
            "gestao_pessoas": "férias, licenças, escalas, folha de ponto, capacitação, movimentação de servidores",
        },
    }
}

state = "Requerimento de aposentadoria por idade."

for i in range(3):
    t0 = time.perf_counter()
    result = agent.predict(state, questions)
    print(f"predict #{i+1}: {(time.perf_counter() - t0) * 1000:.0f} ms")

print(json.dumps(result["answers"], indent=2, ensure_ascii=False, default=str))
print("laya", laya.__version__ if hasattr(laya, "__version__") else "?")