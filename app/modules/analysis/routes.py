# app/modules/analysis/routes.py
from fastapi import APIRouter, Body, HTTPException
from typing import List
from app.modules.analysis.analysis_service import classify_relevance_for_mivivienda

router = APIRouter()

@router.post("/analyze/posts")
def analyze_text_endpoint(
    texts: List[str] = Body(..., description="Lista de textos a analizar"),
):
    """
    Recibe una lista de textos (por ejemplo, tweets o publicaciones) y realiza un análisis general.
    """
    if not texts:
        raise HTTPException(status_code=400, detail="Debe enviarse al menos un texto para analizar.")

    # Combinar todo el contenido
    combined_text = "\n".join(texts)

    analysis = classify_relevance_for_mivivienda(combined_text)

    return {
        "status": "ok",
        "input_count": len(texts),
        "analysis": analysis,
    }
