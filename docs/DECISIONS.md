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
## D-012 Exp02: nenhuma reformulação de descrição superou v0_atual (dev 62%; teste 44%, n=25)
## D-013 Zero-shot inviável para produção; fine-tuning é requisito da Fase 2
## D-014 Nenhum limiar de `confidence` atinge 90% de acerto; calibrar após fine-tuning
## D-015 Pendente: v2/v3 possivelmente truncadas (head_max_len); baseline não avaliado no teste separado