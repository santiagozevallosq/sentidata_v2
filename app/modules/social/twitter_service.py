from datetime import datetime, timedelta
from typing import Dict, List
import random
import tweepy

def get_mock_tweets(username: str, start_date: str, end_date: str, max_results: int = 10) -> Dict:
    """
    Simula la respuesta real del endpoint:
    GET /2/users/:id/tweets
    de la API de Twitter (X) v2.
    Retorna datos similares a publicaciones reales (mock fijo).
    """

    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)

    # Simular ID de usuario y tokens de paginación
    user_id = f"user_{random.randint(1000, 9999)}"
    next_token = f"b{random.randint(10000, 99999)}"
    previous_token = f"a{random.randint(10000, 99999)}"

    # Mock fijo de publicaciones realistas
    mock_texts = [
        "Firmamos un convenio con el MTC para mejorar y modernizar más de 200 paraderos en Miraflores.",
        "¡Buenas noticias! Gracias a nuestras gestiones, iniciaremos la remodelación del Parque Kennedy.",
        "Seguimos trabajando por una ciudad más verde. Hoy sembramos 50 nuevos árboles en Av. Arequipa.",
        "Participamos en el Foro de Seguridad Ciudadana para fortalecer la coordinación con Serenazgo.",
        "Iniciamos el programa 'Miraflores sin Ruido', promoviendo el respeto por los niveles sonoros urbanos.",
        "Reforzamos la iluminación pública en Av. Benavides y Ricardo Palma para mayor seguridad vecinal.",
        "Campaña gratuita de salud en el Parque Reducto N°2 este fin de semana. ¡Te esperamos!",
        "Inauguramos nueva ciclovía conectando Av. Pardo con el Malecón Cisneros.",
        "Feria de emprendimiento local este sábado en el Parque Central. ¡Apoya a nuestros vecinos!",
        "Implementamos cámaras con inteligencia artificial para reforzar la vigilancia en zonas críticas."
    ]

    # Generar tweets simulados según rango y límite
    total_available = len(mock_texts)
    limit = min(max_results, total_available)

    delta = (end - start).total_seconds()
    tweets = []
    for i in range(limit):
        created_at = (start + timedelta(seconds=(delta / (limit + 1)) * (i + 1))).isoformat() + "Z"
        tweet_id = str(1942352849243160964 + i)
        text = mock_texts[i]

        tweets.append({
            "id": tweet_id,
            "text": text,
            "created_at": created_at,
            "edit_history_tweet_ids": [tweet_id],
            "lang": "es",
            "public_metrics": {
                "retweet_count": random.randint(0, 50),
                "reply_count": random.randint(0, 10),
                "like_count": random.randint(0, 150),
                "quote_count": random.randint(0, 5)
            },
            "possibly_sensitive": False,
            "source": "Twitter Web App",
            "author_id": user_id,
            "referenced_tweets": None
        })

    # Estructura oficial de respuesta
    response = {
        "data": list(reversed(tweets)),  # reverse-chronological order
        "includes": {
            "users": [
                {
                    "id": user_id,
                    "name": username.capitalize(),
                    "username": username,
                    "description": f"Cuenta mock de @{username} para pruebas de análisis social.",
                    "verified": True,
                    "created_at": (start - timedelta(days=400)).isoformat() + "Z",
                    "public_metrics": {
                        "followers_count": 4520,
                        "following_count": 180,
                        "tweet_count": 10240,
                        "listed_count": 32
                    },
                    "profile_image_url": f"https://picsum.photos/seed/{username}/200/200"
                }
            ]
        },
        "meta": {
            "result_count": len(tweets),
            "newest_id": tweets[-1]["id"] if tweets else None,
            "oldest_id": tweets[0]["id"] if tweets else None,
            "next_token": next_token,
            "previous_token": previous_token
        }
    }

    return response


def get_real_tweets(username: str, start_date: str, end_date: str, bearer_token: str, max_results: int = 10) -> Dict:
    """
    Obtiene tweets reales de un usuario usando la API de Twitter/X v2 con Tweepy.
    Compatible con Tweepy v4.14+ (Response object).
    """

    # Autenticación
    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

    # 1️⃣ Obtener información del usuario
    try:
        user_resp = client.get_user(
            username=username,
            user_fields=["id", "name", "username", "description",
                         "verified", "created_at", "public_metrics",
                         "profile_image_url"]
        )
    except tweepy.TweepyException as e:
        return {"status": "error", "step": "get_user", "details": str(e)}

    if not user_resp or not getattr(user_resp, "data", None):
        return {"status": "error", "message": f"No se encontró el usuario @{username}"}

    user_data = user_resp.data
    user_id = user_data.id

    # 2️⃣ Obtener tweets del usuario
    try:
        tweets_resp = client.get_users_tweets(
            id=user_id,
            max_results=max_results,
            start_time=datetime.fromisoformat(start_date).isoformat() + "Z",
            end_time=datetime.fromisoformat(end_date).isoformat() + "Z",
            tweet_fields=["id", "text", "created_at", "lang",
                          "public_metrics", "possibly_sensitive",
                          "source", "edit_history_tweet_ids", "referenced_tweets"],
            expansions=["author_id"],
            user_fields=["id", "name", "username", "description",
                         "verified", "created_at", "public_metrics",
                         "profile_image_url"]
        )
    except tweepy.TweepyException as e:
        return {"status": "error", "step": "get_tweets", "details": str(e)}

    # 3️⃣ Preparar estructura segura
    tweets_data = getattr(tweets_resp, "data", None)
    includes_data = getattr(tweets_resp, "includes", None)
    meta_data = getattr(tweets_resp, "meta", None)

    response = {
        "status": "success",
        "data": [tweet.data if hasattr(tweet, "data") else tweet for tweet in tweets_data] if tweets_data else [],
        "includes": includes_data or {},
        "meta": meta_data or {},
        "user_info": user_data
    }

    return response