import requests
import time

BASE_URL = "http://localhost:8000/articles"

def populate_articles():
    print("Fetching yesterday's articles...")
    response = requests.post(f"{BASE_URL}/fetch/")
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])[:10]  # Take only 10 articles
        print(f"✅ Fetched and saved {len(articles)} articles.")
        return articles
    else:
        print("❌ Failed to fetch articles:", response.text)
        return []

def generate_summaries(articles):
    print("Generating summaries...")
    for article in articles:
        response = requests.post(f"{BASE_URL}/generate-summary/", json={"article_id": article["id"]})
        if response.status_code == 201:
            print(f"✅ Summary generated for Article ID {article['id']}")
        else:
            print(f"❌ Failed to generate summary for Article ID {article['id']}: {response.text}")
        time.sleep(0.5)  # To avoid rate limits

def generate_embeddings(articles):
    print("Generating embeddings...")
    for article in articles:
        response = requests.post(f"{BASE_URL}/generate-embedding/", json={"article_id": article["id"]})
        if response.status_code == 201:
            print(f"✅ Embedding saved for Article ID {article['id']}")
        else:
            print(f"❌ Failed to embed Article ID {article['id']}: {response.text}")
        time.sleep(0.5)

if __name__ == "__main__":
    articles = populate_articles()
    if articles:
        generate_summaries(articles)
        generate_embeddings(articles)
    else:
        print("❌ No articles to process.")
