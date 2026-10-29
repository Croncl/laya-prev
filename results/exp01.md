# Exp01 - Zero-shot laya-multilingual (50 exemplos sinteticos)
- laya 0.4.17
- Carga: 5.5s | Latencia media: 103 ms (p95 124 ms)
- Acuracia Laya zero-shot: 62.00%
- Acuracia baseline TF-IDF+LR (CV 5-fold): 86.00%
- confidence: media acertos 0.702 | erros 0.261 | AUROC 0.900
- answer_confidence: media acertos 0.845 | erros 0.529 | AUROC 0.891

Matriz de confusao (linhas=real, colunas=previsto):
                concessao  manutencao  disciplinar  atendimento  gestao_pessoas
concessao               3           0            1            3               3
manutencao              1           1            1            3               4
disciplinar             0           0            8            1               1
atendimento             0           0            0           10               0
gestao_pessoas          0           1            0            0               9

