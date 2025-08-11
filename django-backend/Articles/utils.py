from datetime import datetime, timedelta
from newsapi import NewsApiClient
from finlight_client import FinlightApi, ApiConfig
from finlight_client.models import GetArticlesParams
from .models import Article

def get_articles_news_api(categories, n=10):
    """
    Fetches articles for given categories (yesterday),
    saves only new ones based on (title, date), and returns their IDs.
    """
    newsapi = NewsApiClient(api_key='ab92986727314bb6ac45748b0061f106')
    yesterday = datetime.now() - timedelta(1)
    yesterday_date = yesterday.strftime('%Y-%m-%d')
    date_obj = datetime.strptime(yesterday_date, '%Y-%m-%d').date()

    new_article_ids = []

    for category in categories:
        response = newsapi.get_everything(
            q=category,
            from_param=yesterday_date,
            to=yesterday_date,
            language='en',
            sort_by='publishedAt',
            page_size=100
        )
        articles = response.get('articles', [])[:n]

        for article_data in articles:
            title = (article_data.get('title') or '').strip()
            content = article_data.get('content') or ''

            # Skip if already exists
            if Article.objects.filter(title=title, date=date_obj).exists():
                continue

            article = Article.objects.create(
                title=title or "Untitled Article",
                content=content or "No content available.",
                category=category,
                date=date_obj
            )
            new_article_ids.append(article.id)

    return new_article_ids


def get_articles(days, n=10):
    """
    Fetches the latest articles using the Finlight API,
    saves only new ones based on (title, date), and returns their IDs.
    """
    # 1. Configure and initialize the Finlight API client
    client = FinlightApi(
        config=ApiConfig(
            # It's best practice to store API keys in environment variables
            # instead of hardcoding them in the source code.
            api_key="sk_3fb696c232236f089f65533c6818a1846742ee1909137963eab2c9c649533675"
        )
    )

    # 2. Set parameters to fetch recent articles with content
    # We fetch articles from the last day to match the previous logic.
    yesterday = datetime.now() - timedelta(days=days)

    params = GetArticlesParams(
        includeContent=True,
        excludeEmptyContent=True,
        publishedOnOrAfter=yesterday.strftime('%Y-%m-%d')  # Format date as YYYY-MM-DD string
    )

    # 3. Fetch articles from the API
    try:
        fetched_articles = client.articles.fetch_articles(params=params)
    except Exception as e:
        # If the API call fails, print an error and return an empty list.
        print(f"Error fetching articles from Finlight API: {e}")
        return []

    new_article_ids = []

    # Limit the number of articles to process, similar to the old function's 'n' parameter
    articles_to_process = fetched_articles.articles[:n] if fetched_articles.articles else []

    # 4. Process and save new articles
    for article_data in articles_to_process:
        title = (article_data.title or '').strip()

        # Skip if an article with the same title and date already exists
        if Article.objects.filter(title=title, date=article_data.publishDate).exists():
            continue

        # Create and save the new article
        article = Article.objects.create(
            title=title or "Untitled Article",
            content=article_data.content or "No content available.",
            # The new API doesn't provide a 'category' field in the same way.
            # We'll use a default value for now.
            category='finance',
            date=article_data.publishDate
        )
        new_article_ids.append(article.id)

    return new_article_ids
