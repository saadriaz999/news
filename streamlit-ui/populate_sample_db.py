import requests
import time

BASE_URL = "http://django:8000/articles"

def populate_articles():
    print("Fetching articles from the past 10 days...")
    response = requests.post(f"{BASE_URL}/fetch/", json={"days": 10, "n": 15})
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])
        print(f"✅ Fetched and saved {len(articles)} articles.")
        return articles
    else:
        print("❌ Failed to fetch articles:", response.text)
        return []

def generate_summaries(article_ids):
    print("Generating summaries...")
    for id in article_ids:
        print('s', id)
        response = requests.post(f"{BASE_URL}/generate-summary/", json={"article_id": id})
        if response.status_code == 201:
            print(f"✅ Summary generated for Article ID {id}")
        else:
            print(f"❌ Failed to generate summary for Article ID {id}: {response.text}")
        time.sleep(0.5)  # To avoid rate limits

def generate_embeddings(articles_ids):
    print("Generating embeddings...")
    for id in articles_ids:
        print('e', id)
        response = requests.post(f"{BASE_URL}/generate-embedding/", json={"article_id": id})
        if response.status_code == 201:
            print(f"✅ Embedding saved for Article ID {id}")
        else:
            print(f"❌ Failed to embed Article ID {id}: {response.text}")
        time.sleep(0.5)

if __name__ == "__main__":
    article_ids = populate_articles()
    print(article_ids)
    if article_ids:
        generate_summaries(article_ids)
        generate_embeddings(article_ids)
    else:
        print("❌ No articles to process.")
