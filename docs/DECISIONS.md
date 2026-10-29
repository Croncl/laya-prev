## D-001 Checkpoint: laya-multilingual (via laya.load, subfolder="multilingual")
## D-002 Zero-shot apenas como linha de base; fine-tuning na Fase 2
## D-003 Entrada: trecho curto do documento
## D-004 Baseline paralelo: TF-IDF + regressão logística
## D-005 API real: laya.load()/Router.predict(state, questions); laya 0.4.17
## D-006 Hello world (CPU): predição ~150 ms; carga com download 345 s (cache não medido)
## D-007 Limiares 0.85/0.90 do projeto original inviáveis sem calibração;         comparar `confidence` vs `answer_confidence` no exp01
## D-008 Exp01: zero-shot 62% vs baseline TF-IDF 86% (n=50 sintético, resultado indicativo)
## D-009 `confidence` (AUROC 0.90) adotado como campo candidato para gating; limiares a recalibrar
## D-010 Fraqueza em concessao/manutencao: testar reformulação das descrições antes de fine-tuning
## D-011 Latência CPU ~103 ms (frases curtas); carga em cache 5.5 s