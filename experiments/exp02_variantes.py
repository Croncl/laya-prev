import os, sys, time
os.environ.setdefault("USE_TF", "0")
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score
import laya
from app.variants import VARIANTS, make_questions

dev = pd.read_csv(ROOT / "data/exemplos/exemplos.csv")
test = pd.read_csv(ROOT / "data/exemplos/teste.csv")
agent = laya.load("convaiinnovations/laya", subfolder="multilingual")

def run(df, name):
    q = make_questions(name)
    out, lat = [], []
    for t in df.texto:
        s = time.perf_counter()
        a = agent.predict(t, q)["answers"]["tema"]
        lat.append((time.perf_counter() - s) * 1000)
        out.append((a["choice"], a["confidence"]))
    d = df.copy()
    d["pred"], d["conf"] = zip(*out)
    d["hit"] = (d.pred == d.classe).astype(int)
    d["variante"] = name
    return d, float(np.mean(lat))

def auroc(d):
    return roc_auc_score(d.hit, d.conf) if d.hit.nunique() == 2 else float("nan")

# 1) Seleção no conjunto de desenvolvimento (50)
dev_res, lat_ms, linhas = {}, {}, []
for name in VARIANTS:
    d, l = run(dev, name)
    dev_res[name], lat_ms[name] = d, l
    linhas.append((name, d.hit.mean(), auroc(d), l))
tab = pd.DataFrame(linhas, columns=["variante", "acc_dev", "auroc_dev", "lat_ms"])
best = tab.sort_values(["acc_dev", "auroc_dev"], ascending=False).iloc[0].variante

# 2) Confirmação no teste separado (25): baseline vs melhor
test_res = {}
for name in dict.fromkeys(["v0_atual", best]):
    test_res[name], _ = run(test, name)

# 3) Curva cobertura x acurácia (dev+test pooled, melhor variante)
pool = pd.concat([dev_res[best], test_res[best]])
curva = []
for t in [0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    sel = pool[pool.conf >= t]
    curva.append((t, len(sel) / len(pool), sel.hit.mean() if len(sel) else float("nan")))
curva = pd.DataFrame(curva, columns=["limiar_conf", "cobertura", "acuracia"])

por_classe = test_res[best].groupby("classe").hit.mean().round(2)

res = f"""# Exp02 - Variantes de descricao (laya-multilingual, zero-shot)
## Desenvolvimento (n=50)
{tab.round(3).to_string(index=False)}

Melhor variante (dev): {best}

## Teste separado (n=25)
""" + "\n".join(
    f"- {n}: acuracia {d.hit.mean():.2%} | AUROC conf {auroc(d):.3f}" for n, d in test_res.items()
) + f"""

Acuracia por classe no teste ({best}):
{por_classe.to_string()}

## Cobertura x acuracia ({best}, dev+teste, n=75)
{curva.round(3).to_string(index=False)}
"""
(ROOT / "results/exp02.md").write_text(res, encoding="utf-8")
pd.concat(list(dev_res.values()) + list(test_res.values())).to_csv(
    ROOT / "results/exp02_predicoes.csv", index=False)
print(res)