Jurisprudência Oficial – Servidor FastAPI (STF, STJ, TJPE, TJSP, TJMG, CJF) – Modo SEGURO

Endpoints:
- GET /health  → 200 OK
- POST /pesquisar → recebe {query, tribunal, limite, strict, data_inicio, data_fim} e retorna lista de decisões

Deploy no Railway (upload):
1) No projeto → Add → Deploy → Upload → envie este ZIP.
2) Settings → Start Command:
   uvicorn main:app --host 0.0.0.0 --port $PORT
3) Quando estiver RUNNING, copie a URL HTTPS e cole no servers.url da Action no ChatGPT.
4) Teste com /juris_previd.

Última revisão: 2025-10-21
