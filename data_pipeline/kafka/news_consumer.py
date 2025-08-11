# news_consumer.py
import time
import json
import requests
from kafka import KafkaConsumer
from kafka.errors import KafkaError

DJANGO_SUMMARY_URL = "http://django:8000/articles/generate-summary/"
DJANGO_EMBEDDING_URL = "http://django:8000/articles/generate-embedding/"

consumer = KafkaConsumer(
    "raw_news",
    bootstrap_servers=["kafka:9092"],
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id="news_consumer_group"
)

def process_article(article_id):
    # Generate Summary
    summary_res = requests.post(DJANGO_SUMMARY_URL, json={"article_id": article_id})
    if summary_res.status_code == 201:
        print(f"[{article_id}] Summary generated.")
    else:
        print(f"[{article_id}] Failed to generate summary: {summary_res.text}")

    # Generate Embedding
    embed_res = requests.post(DJANGO_EMBEDDING_URL, json={"article_id": article_id})
    if embed_res.status_code == 201:
        print(f"[{article_id}] Embedding generated.")
    else:
        print(f"[{article_id}] Failed to generate embedding: {embed_res.text}")

print("Listening to 'raw_news' for article IDs...")

while True:
    try:
        for message in consumer:
            payload = message.value
            article_id = payload.get("article_id")
            if article_id:
                print(f"Processing article_id={article_id}")
                process_article(article_id)
    except KafkaError as e:
        print(f"Kafka error: {e}. Retrying in 5 seconds...")
        time.sleep(5)
