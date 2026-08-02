---
status: accepted
---

# Componente Unico de Grid

Decidimos que todas as tabelas do sistema passam por **um unico componente** `renderizar_grid()` (`src/ui_components/data_grid.py`), com assinatura estavel, encapsulando formatacao pt-BR (moeda, data), badge de status reaproveitando o `MAPA_STATUS_POR_DOMINIO` existente, ordenacao, filtro por coluna, selecao e paginacao. Hoje existem 24 chamadas soltas de `st.dataframe`, cada uma com formatacao propria, mais duas telas que simulam tabela com `st.columns` manual e uma que sobrepoe `<div>` a `st.columns`.

**Implementacao: `streamlit-aggrid`**, conforme pedido nominal do professor. O spike da F0 validou a compatibilidade com o Streamlit 1.60 ja instalado.

## Resultado do spike (F0)

`streamlit-aggrid==1.2.1.post2`, instalado no `.venv` e fixado em `requirements.txt`.

- **Sem conflito de dependencias.** A resolucao nao rebaixa nada: Streamlit 1.60.0 e Altair 6.2.2 permanecem. A restricao do AgGrid e `streamlit>=1.2` e `altair!=5.4.0,!=5.4.1,<7,>=4.0` — ambas satisfeitas. Unica dependencia transitiva nova: `python-decouple==3.8`.
- **Superficie de API completa.** `AgGrid`, `GridOptionsBuilder`, `GridUpdateMode`, `DataReturnMode`, `JsCode` e `ColumnsAutoSizeMode` presentes.
- **Formatacao pt-BR funciona.** `JsCode` com `toLocaleString('pt-BR')` para moeda e `toLocaleDateString('pt-BR')` para data sobrevive a serializacao do `build()` — era o ponto mais fragil do spike.
- **Selecao multipla com checkbox e paginacao** configuraveis via builder.
- **Frontend empacotado**, servido localmente (`url=None`, `path` preenchido, 23 arquivos com `index.html`). Nao exige servidor Node em producao, o que mantem o `Dockerfile` inalterado.

O spike virou guarda permanente em [`tests/test_aggrid_compat.py`](../../tests/test_aggrid_compat.py) — 4 testes que falham se um upgrade futuro de Streamlit ou AgGrid quebrar essa superficie, antes de 24 telas quebrarem juntas.

## Por que a assinatura fica desacoplada mesmo assim

O fallback (`st.dataframe` nativo com `column_config` + `selection_mode`/`on_select`, disponivel no Streamlit 1.60) continua sendo um caminho valido. Manter `renderizar_grid()` como unica fronteira significa que trocar a implementacao depois — por incompatibilidade futura, licenca ou performance — custa um arquivo, nao 24 call sites. O contrato e o ativo; o AgGrid e o detalhe.
