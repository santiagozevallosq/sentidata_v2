# client_with_comments.py
import requests
from datetime import datetime, timedelta
from app.modules.social.comments_service import get_mock_comments

BASE_URL = "http://127.0.0.1:8000"

def get_tweets(username: str, start_date: str, end_date: str, max_results: int = 5, mock: bool = True):
    """
    Recupera tweets desde el endpoint /social/collect/twitter
    """
    params = {
        "username": username,
        "start_date": start_date,
        "end_date": end_date,
        "max_results": max_results,
        "mock": mock
    }
    response = requests.get(f"{BASE_URL}/social/collect/twitter", params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("data", {}).get("data", [])  # lista de tweets


def analyze_texts(texts: list):
    """
    Por el momento, clasifica todos los textos como 'RELEVANTE'
    """
    return ["RELEVANTE" for _ in texts]


def pipeline_example(username: str, start_date: str, end_date: str, limit: int = 5):
    print(f"Obteniendo tweets de @{username} desde {start_date} hasta {end_date}...")
    tweets = get_tweets(username, start_date, end_date, max_results=limit)

    if not tweets:
        print("No se obtuvieron tweets.")
        return []

    tweet_ids = [tweet.get("id") for tweet in tweets]
    texts = [tweet.get("text", "") for tweet in tweets if tweet.get("text")]
    print(f"Analizando {len(texts)} tweets con LLM mock...")

    classifications = analyze_texts(texts)

    # Obtener comentarios mock para cada tweet
    comments_dict = get_mock_comments(tweet_ids)

    # Combinar los datos originales con la clasificación y comentarios
    analyzed_tweets = []
    for i, tweet in enumerate(tweets):
        analyzed_tweets.append({
            "id": tweet.get("id"),
            "text": tweet.get("text"),
            "created_at": tweet.get("created_at"),
            "author_id": tweet.get("author_id"),
            "public_metrics": tweet.get("public_metrics"),
            "classification": classifications[i] if i < len(classifications) else "RELEVANTE",
            "comments": comments_dict.get(tweet.get("id"), [])
        })

    return analyzed_tweets


if __name__ == "__main__":
    start = (datetime.utcnow() - timedelta(days=10)).isoformat()
    end = datetime.utcnow().isoformat()

    results = pipeline_example("ministeriovivienda", start_date=start, end_date=end, limit=5)

    for tweet in results:
        print(f"Tweet: {tweet['text']}")
        print(f"Clasificación: {tweet['classification']}")
        print(f"Comentarios ({len(tweet['comments'])}):")
        for comment in tweet['comments']:
            print(f" - {comment['text']} (autor: {comment['author_id']})")
        print("\n")
