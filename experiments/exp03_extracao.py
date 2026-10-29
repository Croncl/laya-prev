import re, argparse
from pathlib import Path
from collections import Counter
import fitz  # pymupdf
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "data/normativos"
TXT_DIR = ROOT / "data/texto"
MIN_CHARS_PAGE = 100  # abaixo disso a página é tratada como sem texto

EMENTA_RE = re.compile(
    r"\b(Dispõe|Estabelece|Regulamenta|Disciplina|Aprova|Institui|Define|Altera|Orienta|Revoga)\b.{10,400}?[.;]",
    re.S)
TITULO_RE = re.compile(
    r"(INSTRUÇÃO NORMATIVA|PORTARIA|RESOLUÇÃO|ORDEM DE SERVIÇO|MEMORANDO[- ]CIRCULAR|DECRETO|LEI|NOTA TÉCNICA)[^\n]{0,80}")
SETOR_RE = re.compile(
    r"\b((?:Diretoria|Coordena[çc][ãa]o(?:-Geral)?|Ger[êe]ncia|Divis[ãa]o|Servi[çc]o|Departamento|"
    r"Secretaria|Superintend[êe]ncia|Subsecretaria|Se[çc][ãa]o|Assessoria|Procuradoria|Ouvidoria|Corregedoria)"
    r"(?:\s+(?:de|da|do|das|dos|e)|\s+[A-ZÀ-Ú][\wà-ú-]+){1,6})")

def ocr_page(page):
    import pytesseract
    from PIL import Image
    pix = page.get_pixmap(dpi=300)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return pytesseract.image_to_string(img, lang="por")

ap = argparse.ArgumentParser()
ap.add_argument("--ocr", action="store_true", help="aplica OCR nas páginas sem texto")
args = ap.parse_args()

TXT_DIR.mkdir(parents=True, exist_ok=True)
(ROOT / "results").mkdir(exist_ok=True)
rows = []

for pdf in sorted(PDF_DIR.glob("*.pdf")):
    doc = fitz.open(pdf)
    pages = [p.get_text() for p in doc]
    low = [i for i, t in enumerate(pages) if len(t.strip()) < MIN_CHARS_PAGE]
    n_low = len(low)
    ocr_ok = ""
    if args.ocr and low:
        try:
            for i in low:
                pages[i] = ocr_page(doc[i])
            ocr_ok = "sim"
        except Exception as e:
            ocr_ok = f"erro: {type(e).__name__}"
    text = "\n".join(pages)
    (TXT_DIR / f"{pdf.stem}.txt").write_text(text, encoding="utf-8")

    status = "texto" if n_low == 0 else ("imagem" if n_low == len(pages) else "parcial")
    head = text[:6000]
    ementa = EMENTA_RE.search(head)
    titulo = TITULO_RE.search(head)
    setores = Counter(m.strip() for m in SETOR_RE.findall(text))
    rows.append({
        "arquivo": pdf.name,
        "titulo": re.sub(r"\s+", " ", titulo.group(0)).strip() if titulo else "",
        "paginas": len(pages),
        "caracteres": len(text),
        "tokens_est": len(text) // 4,
        "pag_sem_texto": n_low,
        "status": status,
        "ocr": ocr_ok,
        "artigos": len(re.findall(r"(?m)^\s*Art\.?\s*\d+", text)),
        "capitulos": len(re.findall(r"(?m)^\s*CAP[ÍI]TULO\s+[IVXLC\d]+", text)),
        "ementa": re.sub(r"\s+", " ", ementa.group(0))[:200] if ementa else "",
        "setores": "; ".join(f"{s} ({c})" for s, c in setores.most_common(5)),
    })

df = pd.DataFrame(rows)
df.to_csv(ROOT / "results/exp03_normativos.csv", index=False)

resumo = df.drop(columns=["ementa", "setores"]).to_string(index=False)
detalhe = "\n".join(
    f"- {r.arquivo}\n  ementa: {r.ementa or '(nao detectada)'}\n  setores: {r.setores or '(nenhum)'}"
    for r in df.itertuples())
(ROOT / "results/exp03.md").write_text(
    f"# Exp03 - Diagnostico de extracao (n={len(df)})\n```\n{resumo}\n```\n{detalhe}\n",
    encoding="utf-8")

rot = ROOT / "data/normativos_rotulos.csv"
if not rot.exists():
    pd.DataFrame({"arquivo": df.arquivo, "temas": "", "setor_real": ""}).to_csv(rot, index=False)

print((ROOT / "results/exp03.md").read_text(encoding="utf-8"))