# news_producer.py
import json
import requests
import datetime
from kafka import KafkaProducer

DJANGO_FETCH_URL = "http://django:8000/articles/fetch/"

producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_new_article_ids():
    res = requests.post(DJANGO_FETCH_URL)
    res.raise_for_status()
    data = res.json()
    return data.get("new_article_ids", [])

def send_ids_to_kafka(article_ids):
    for article_id in article_ids:
        payload = {
            "article_id": article_id,
            "pushed_at": str(datetime.date.today())
        }
        producer.send("raw_news", value=payload)
    producer.flush()
    print(f"Sent {len(article_ids)} article IDs to Kafka")

if __name__ == "__main__":
    article_ids = fetch_new_article_ids()
    if article_ids:
        send_ids_to_kafka(article_ids)
    else:
        print("No new articles to send.")
