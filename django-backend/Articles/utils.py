from datetime import datetime, timedelta
from newsapi import NewsApiClient
from django.utils import timezone
from .models import Article  # Import the Article model

def get_previous_day_articles_by_category(categories, n=10):
    # Initialize News API client
    newsapi = NewsApiClient(api_key='ab92986727314bb6ac45748b0061f106')

    # Calculate the previous day's date
    yesterday = datetime.now() - timedelta(1)
    yesterday_date = yesterday.strftime('%Y-%m-%d')

    # Initialize the results dictionary (for logging purposes)
    results = {}

    # Iterate through each category in the list
    for category in categories:
        # Perform the query for each category
        response = newsapi.get_everything(
            q=category,  # Use the category as a search term
            from_param=yesterday_date,  # Start date (yesterday)
            to=yesterday_date,  # End date (yesterday)
            language='en',  # English language articles
            sort_by='publishedAt',  # Sort by published date
            page_size=100  # Maximum number of articles per request
        )

        # Get the articles for this category
        articles = response.get('articles', [])[:n]

        # Store the articles in the results dictionary under the corresponding category
        results[category] = articles

        # Loop through the articles and save them to the database
        for article_data in articles:
            # Create or update each article in the database
            article = Article(
                title=article_data.get('title', ''),
                content=article_data.get('content', ''),
                category=category,
                date=datetime.strptime(yesterday_date, '%Y-%m-%d').date()  # Use only the date part
            )
            article.save()  # Save the article to the database

    return results  # Return the results for reference if needed


