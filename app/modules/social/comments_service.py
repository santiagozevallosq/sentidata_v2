# app/modules/social/comments_service.py
from datetime import datetime, timedelta
from typing import List, Dict, Any

import random
import tweepy


def get_mock_comments(tweet_ids: List[str], max_comments_per_post: int = 5) -> Dict:
    """
    Genera comentarios simulados para una lista de IDs de tweets.
    Retorna una estructura similar a lo que devolvería un endpoint real de comentarios.
    """

    comments_response = {}
    for tweet_id in tweet_ids:
        num_comments = random.randint(1, max_comments_per_post)
        comments = []

        for i in range(num_comments):
            comment_id = f"{tweet_id}_c{i}"
            created_at = (datetime.utcnow() - timedelta(minutes=random.randint(0, 10000))).isoformat() + "Z"
            text = random.choice([
                                "¡Excelente iniciativa!",
                "Me parece muy positivo para la comunidad.",
                "Gracias por mantenernos informados.",
                "Espero que esto mejore la seguridad en la zona.",
                "Ojalá continúen con más proyectos como este."
            ])
            author_id = f"user_{random.randint(1000, 9999)}"

            comments.append({
                "id": comment_id,
                "tweet_id": tweet_id,
                "text": text,
                "created_at": created_at,
                "author_id": author_id,
                "like_count": random.randint(0, 50),
                "reply_count": random.randint(0, 10)
            })

        comments_response[tweet_id] = comments

    return comments_response


def get_real_comments(tweet_ids: List[str], bearer_token: str, max_results: int = 20) -> Dict[str, Any]:
    """
    Obtiene las respuestas (comentarios) reales a una lista de tweets usando Tweepy + API v2.
    """

    client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
    comments_response: Dict[str, List[Dict[str, Any]]] = {}

    for tweet_id in tweet_ids:
        try:
            # 1️⃣ Obtener tweet original (para conocer su conversation_id y author_id)
            tweet_resp = client.get_tweet(
                id=tweet_id,
                tweet_fields=["conversation_id", "author_id"]
            )

            if not tweet_resp or not getattr(tweet_resp, "data", None):
                comments_response[tweet_id] = []
                continue

            conversation_id = tweet_resp.data["conversation_id"]
            author_id = tweet_resp.data["author_id"]

            # 2️⃣ Buscar respuestas dentro del hilo
            query = f"conversation_id:{conversation_id} -from:{author_id}"

            search_resp = client.search_recent_tweets(
                query=query,
                max_results=max_results,
                tweet_fields=[
                    "id", "text", "author_id", "created_at",
                    "public_metrics", "in_reply_to_user_id",
                    "referenced_tweets"
                ],
                expansions=["author_id"],
                user_fields=[
                    "id", "name", "username", "profile_image_url", "verified"
                ],
            )

            # 3️⃣ Estructurar datos
            tweets_data = getattr(search_resp, "data", None)
            if not tweets_data:
                comments_response[tweet_id] = []
                continue

            formatted_comments = []
            for t in tweets_data:
                metrics = t["public_metrics"] if "public_metrics" in t else {}
                formatted_comments.append({
                    "id": t["id"],
                    "tweet_id": tweet_id,
                    "text": t["text"],
                    "created_at": t["created_at"],
                    "author_id": t["author_id"],
                    "like_count": metrics.get("like_count", 0),
                    "reply_count": metrics.get("reply_count", 0),
                })

            comments_response[tweet_id] = formatted_comments

        except tweepy.TweepyException as e:
            comments_response[tweet_id] = [{
                "error": True,
                "message": str(e)
            }]

    return {
        "status": "success",
        "comments": comments_response
    }