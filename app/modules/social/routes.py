from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from datetime import datetime, timedelta
from app.modules.social.twitter_service import get_mock_tweets, get_real_tweets

router = APIRouter()

@router.get("/collect/twitter")
def collect_twitter(
    username: str = Query(..., description="Nombre de usuario de Twitter"),
    start_date: Optional[str] = Query(None, description="Fecha de inicio (ISO8601)"),
    end_date: Optional[str] = Query(None, description="Fecha de fin (ISO8601)"),
    max_results: int = Query(5, description="Cantidad máxima de tweets a obtener"),
    mock: bool = Query(True, description="Usar datos simulados en lugar de reales"),
):
    """
    Endpoint que recolecta tweets reales o simulados.
    Por defecto, usa el modo 'mock' para devolver datos ficticios.
    """
    try:
        # Si no se pasan fechas, usar últimos 7 días por defecto
        if not start_date or not end_date:
            end_date = datetime.utcnow().isoformat()
            start_date = (datetime.utcnow() - timedelta(days=7)).isoformat()

        if mock:
            data = get_mock_tweets(username, start_date, end_date, max_results=max_results)
        else:
            # Aquí puedes luego pasar un token real
            data = get_real_tweets(username, start_date, end_date, bearer_token="")

        return {
            "status": "ok",
            "source": "twitter_mock" if mock else "twitter_real",
            "params": {
                "username": username,
                "start_date": start_date,
                "end_date": end_date,
                "max_results": max_results,
            },
            "data": data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
