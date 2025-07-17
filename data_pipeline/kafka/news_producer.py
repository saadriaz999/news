# news_producer.py
import json
import requests
import datetime
from kafka import KafkaProducer


producer = KafkaProducer(
    bootstrap_servers=["kafka:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def fetch_news():
    res = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=ab92986727314bb6ac45748b0061f106")
    res.raise_for_status()
    return res.json().get("articles", [])

def send_to_kafka(articles):
    for article in articles:
        data = {
            "title": article["title"],
            "content": article["content"],
            "source": article["source"]["name"],
            "published_at": article["publishedAt"],
            "pushed_at": str(datetime.datetime.now())
        }
        producer.send("raw_news", value=data)
    producer.flush()
    print(f"Sent {len(articles)} articles to Kafka")

if __name__ == "__main__":
    articles = fetch_news()
    send_to_kafka(articles)
