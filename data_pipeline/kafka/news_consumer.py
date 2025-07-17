# news_consumer.py
import time
import json
import datetime
from kafka import KafkaConsumer
from kafka.errors import KafkaError

consumer = KafkaConsumer(
    "raw_news",
    bootstrap_servers=["kafka:9092"],
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="latest",
    enable_auto_commit=True,
    group_id='news_consumer_group'
)

print("Listening to 'raw_news'...")

while True:
    try:
        for message in consumer:
            article = message.value
            content = article.get("content") or ""
            first_word = content.strip().split()[0] if content else "NO_CONTENT"
            print(f"[{article.get('title')[:15]}] → First word: {first_word}")
            print(f"[Kafka] Received at {str(datetime.datetime.now())} → pushed_at={article['pushed_at']}")
    except KafkaError as e:
        print(f"Kafka error: {e}. Retrying in 5 seconds...")
        time.sleep(5)