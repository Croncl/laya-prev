CLASSES = {
    "concessao": ("Concessão de Benefícios Previdenciários",
        "concessão de aposentadoria, pensão, auxílio-doença, BPC, salário-maternidade, auxílio-reclusão"),
    "manutencao": ("Manutenção e Atualização de Benefícios",
        "revisão, reativação, prova de vida, alteração cadastral ou bancária de benefício"),
    "disciplinar": ("Disciplinar",
        "PAD, sindicância, advertência, investigação administrativa, conduta funcional"),
    "atendimento": ("Atendimento ao Público",
        "reclamação, agendamento, ouvidoria, atendimento presencial ou remoto"),
    "gestao_pessoas": ("Gestão de Pessoas",
        "férias, licenças, escalas, folha de ponto, capacitação, movimentação de servidores"),
}

KEYS = list(CLASSES)

QUESTIONS = {
    "tema": {
        "type": "choice",
        "instructions": "Qual é o assunto principal deste documento?",
        "criteria": {k: v[1] for k, v in CLASSES.items()},
    }
}