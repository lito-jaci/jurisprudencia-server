from fastapi import FastAPI, Body
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import date

app = FastAPI(title="Jurisprudência Oficial – Servidor", version="1.0.0")

class SearchRequest(BaseModel):
    query: str
    tribunal: str = "TODOS"  # STF, STJ, TJPE, TJSP, TJMG, CJF, TODOS
    limite: int = 5
    strict: bool = True
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None

class Decision(BaseModel):
    tribunal: str
    numero: Optional[str] = None
    orgao: Optional[str] = None
    relator: Optional[str] = None
    data: Optional[date] = None
    ementa: Optional[str] = None
    tese: Optional[str] = None
    url_oficial: HttpUrl
    url_pdf: Optional[HttpUrl] = None
    fonte: str

@app.get("/health")
async def health():
    return {"status": "ok"}

def exemplos_reais(query: str, tribunal: str, limite: int) -> List[Decision]:
    exemplos = [
        Decision(
            tribunal="STJ",
            numero="AgInt no REsp 1234567/SP",
            orgao="Segunda Turma",
            relator="Min. Exemplo",
            data=date(2024,5,10),
            ementa="Tema exemplificativo. Ementa resumida para testes do fluxo GPT.",
            tese="Fixação exemplificativa para testes.",
            url_oficial="https://www.stj.jus.br/sites/portalp/Paginas/Comunicacao/Decisoes/Exemplo.html",
            fonte="stj",
        ),
        Decision(
            tribunal="TJPE",
            numero="APL 0000000-00.2023.8.17.0001",
            orgao="2ª Câmara Cível",
            relator="Des. Exemplo",
            data=date(2024,3,18),
            ementa="Ementa demonstrativa do TJPE com link oficial para testes.",
            tese="Aplicação de tese exemplificativa para validação do pipeline.",
            url_oficial="https://www.tjpe.jus.br/web/guest/decisoes",
            fonte="tjpe",
        ),
        Decision(
            tribunal="CJF",
            numero="AG 1000000-00.2022.4.05.0000",
            orgao="TRF5 Turma",
            relator="Des. Federal Exemplo",
            data=date(2023,11,7),
            ementa="Ementa demonstrativa em matéria previdenciária.",
            tese="Tese exemplificativa.",
            url_oficial="https://www.cjf.jus.br/cjf/decisoes",
            fonte="cjf",
        ),
        Decision(
            tribunal="STF",
            numero="RE 000000 (Tema 000)",
            orgao="Plenário",
            relator="Min. Exemplo",
            data=date(2024,2,1),
            ementa="Ementa demonstrativa do STF.",
            tese="Repercussão geral exemplificativa.",
            url_oficial="https://portal.stf.jus.br/processos/listarProcessos.asp",
            fonte="stf",
        ),
    ]
    if tribunal and tribunal != "TODOS":
        exemplos = [d for d in exemplos if d.tribunal.upper() == tribunal.upper()]
    return exemplos[:max(1, min(limite, 20))]

@app.post("/pesquisar", response_model=List[Decision])
async def pesquisar(payload: SearchRequest = Body(...)):
    resultados = exemplos_reais(payload.query, payload.tribunal, payload.limite)
    if payload.strict:
        filtrados = []
        for d in resultados:
            if (d.url_oficial.host.endswith('.jus.br') and d.data is not None and d.tribunal):
                filtrados.append(d)
        resultados = filtrados
    return resultados
