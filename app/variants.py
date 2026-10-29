from app.taxonomy import CLASSES

VARIANTS = {
    "v0_atual": {
        "instr": "Qual é o assunto principal deste documento?",
        "crit": {k: v[1] for k, v in CLASSES.items()},
    },
    "v1_curta": {
        "instr": "Qual é o tema do documento?",
        "crit": {
            "concessao": "pedido de benefício novo",
            "manutencao": "alteração de benefício já concedido",
            "disciplinar": "apuração de falta de servidor",
            "atendimento": "contato do cidadão com a unidade",
            "gestao_pessoas": "vida funcional do servidor",
        },
    },
    "v2_exemplos": {
        "instr": "Qual é o assunto principal deste documento?",
        "crit": {
            "concessao": "pedido inicial de benefício: aposentadoria, pensão por morte, auxílio-doença, BPC, salário-maternidade, auxílio-reclusão",
            "manutencao": "mudança em benefício que já existe: revisão de valor, reativação, prova de vida, troca de endereço ou conta bancária",
            "disciplinar": "apuração de falta funcional de servidor: PAD, sindicância, advertência, penalidade, investigação administrativa",
            "atendimento": "contato do cidadão com a unidade: reclamação, elogio, agendamento, ouvidoria, informação, atendimento presencial ou remoto",
            "gestao_pessoas": "vida funcional do próprio servidor: férias, licença, escala, ponto, curso, remoção",
        },
    },
    "v3_contrastiva": {
        "instr": "Qual categoria descreve melhor o assunto principal deste documento?",
        "crit": {
            "concessao": "benefício pedido pela primeira vez, ainda não concedido; não é revisão nem alteração de benefício existente",
            "manutencao": "benefício já concedido que precisa ser revisado, reativado ou ter dados alterados; não é pedido novo",
            "disciplinar": "investigação ou punição de servidor por falta funcional; não é reclamação de cidadão nem licença",
            "atendimento": "cidadão reclamando, elogiando, agendando ou pedindo informação; não é pedido de benefício",
            "gestao_pessoas": "assuntos administrativos do servidor como férias, licenças, escala e ponto; não é benefício de segurado nem punição",
        },
    },
}

def make_questions(name):
    v = VARIANTS[name]
    return {"tema": {"type": "choice", "instructions": v["instr"], "criteria": v["crit"]}}