# Exp02 - Variantes de descricao (laya-multilingual, zero-shot)
## Desenvolvimento (n=50)
      variante  acc_dev  auroc_dev  lat_ms
      v0_atual     0.62      0.900 113.796
      v1_curta     0.48      0.771  71.982
   v2_exemplos     0.48      0.577 121.581
v3_contrastiva     0.44      0.761 115.967

Melhor variante (dev): v0_atual

## Teste separado (n=25)
- v0_atual: acuracia 44.00% | AUROC conf 0.740

Acuracia por classe no teste (v0_atual):
classe
atendimento       0.8
concessao         0.4
disciplinar       0.4
gestao_pessoas    0.4
manutencao        0.2

## Cobertura x acuracia (v0_atual, dev+teste, n=75)
 limiar_conf  cobertura  acuracia
         0.0      1.000     0.560
         0.2      0.787     0.712
         0.3      0.653     0.755
         0.4      0.547     0.756
         0.5      0.480     0.778
         0.6      0.400     0.833
         0.7      0.307     0.826
