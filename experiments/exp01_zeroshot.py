import os, sys, time
os.environ.setdefault("USE_TF", "0")
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import numpy as np, pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold, cross_val_predict
import laya
from app.taxonomy import KEYS, QUESTIONS

df = pd.read_csv(ROOT / "data/exemplos/exemplos.csv")

t0 = time.perf_counter()
agent = laya.load("convaiinnovations/laya", subfolder="multilingual")
t_load = time.perf_counter() - t0
agent.predict(df.texto[0], QUESTIONS)  # aquecimento

rows, lat = [], []
for t in df.texto:
    s = time.perf_counter()
    a = agent.predict(t, QUESTIONS)["answers"]["tema"]
    lat.append((time.perf_counter() - s) * 1000)
    rows.append((a["choice"], a["confidence"], a["answer_confidence"]))
df["pred"], df["confidence"], df["answer_conf"] = zip(*rows)
hit = (df.pred == df.classe).astype(int)

def auroc(x):
    return roc_auc_score(hit, x) if hit.nunique() == 2 else float("nan")

acc = accuracy_score(df.classe, df.pred)
cm = pd.DataFrame(confusion_matrix(df.classe, df.pred, labels=KEYS), index=KEYS, columns=KEYS)

pipe = make_pipeline(TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression(max_iter=1000))
cv = StratifiedKFold(5, shuffle=True, random_state=42)
acc_b = accuracy_score(df.classe, cross_val_predict(pipe, df.texto, df.classe, cv=cv))

def mean_or_nan(s):
    return s.mean() if len(s) else float("nan")

res = f"""# Exp01 - Zero-shot laya-multilingual (50 exemplos sinteticos)
- laya {laya.__version__ if hasattr(laya, '__version__') else '?'}
- Carga: {t_load:.1f}s | Latencia media: {np.mean(lat):.0f} ms (p95 {np.percentile(lat, 95):.0f} ms)
- Acuracia Laya zero-shot: {acc:.2%}
- Acuracia baseline TF-IDF+LR (CV 5-fold): {acc_b:.2%}
- confidence: media acertos {mean_or_nan(df.confidence[hit == 1]):.3f} | erros {mean_or_nan(df.confidence[hit == 0]):.3f} | AUROC {auroc(df.confidence):.3f}
- answer_confidence: media acertos {mean_or_nan(df.answer_conf[hit == 1]):.3f} | erros {mean_or_nan(df.answer_conf[hit == 0]):.3f} | AUROC {auroc(df.answer_conf):.3f}

Matriz de confusao (linhas=real, colunas=previsto):
{cm.to_string()}

"""
(ROOT / "results").mkdir(exist_ok=True)
(ROOT / "results/exp01.md").write_text(res, encoding="utf-8")
df.to_csv(ROOT / "results/exp01_predicoes.csv", index=False)
print(res)