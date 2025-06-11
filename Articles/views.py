import os
import cohere
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from transformers import T5Tokenizer, T5ForConditionalGeneration

from .models import Article, Summary
from .serializers import ArticleSerializer
from .utils import get_previous_day_articles_by_category, summarize_content
from Summarizer.settings import BASE_DIR


co = cohere.Client("MIfT9OBEe6PdyxOUgZXJJ7iN5dgI5ZLcUosBrb99")

# List and Create Articles
class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

# Retrieve, Update, and Delete a Single Article
class ArticleRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class ArticleFetchView(APIView):
    """
    This view fetches articles from the previous day for a list of categories,
    saves them to the database, and returns a success message with the saved articles.
    """
    def post(self, request, *args, **kwargs):
        # Define the categories and API key
        categories = ['technology', 'health', 'business', 'sports']  # Example categories

        # Fetch and save the articles using your existing function
        get_previous_day_articles_by_category(categories)

        # Optionally serialize the saved articles
        serialized_articles = ArticleSerializer(Article.objects.all(), many=True)

        # Return a response with the success message and saved articles
        return Response({
            "message": "Articles for the previous day have been fetched and saved.",
            "articles": serialized_articles.data
        }, status=status.HTTP_200_OK)


class GenerateSummariesView(APIView):
    """
    Generates summaries for articles that don't already have a summary,
    based on raw article_id (no foreign key).
    """

    def post(self, request, *args, **kwargs):
        existing_article_ids = Summary.objects.values_list('article_id', flat=True)
        articles_without_summary = Article.objects.exclude(id__in=existing_article_ids)

        path = os.path.join(BASE_DIR, "media", "ml_models", "flan-t5-small-cnn_dailymail")
        model = T5ForConditionalGeneration.from_pretrained(path)
        tokenizer = T5Tokenizer.from_pretrained(path)

        created_count = 0
        for article in articles_without_summary:
            summary_text = summarize_content(article.content, model, tokenizer)
            Summary.objects.create(article_id=article.id, summary=summary_text)
            created_count += 1

        return Response({
            "message": "Summaries generated successfully.",
            "summaries_created": created_count
        }, status=status.HTTP_200_OK)


class DailyAICompiledSummaryView(APIView):
    """
    Takes user preferences, gets summaries of matching previous day's articles,
    generates a prompt, and sends it to Cohere for a summarized response.
    """

    def post(self, request, *args, **kwargs):
        preferences = request.data.get('preferences', [])

        if not preferences:
            return Response({"error": "Preferences list is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get yesterday's date
        yesterday = timezone.now().date() - timedelta(days=2)

        # Get article IDs from yesterday matching preferences
        articles = Article.objects.filter(category__in=preferences)
        article_ids = articles.values_list('id', flat=True)

        # Get corresponding summaries
        summaries = Summary.objects.filter(article_id__in=article_ids).values_list('summary', flat=True)

        if not summaries:
            return Response({"message": "No summaries found for the given preferences."}, status=status.HTTP_404_NOT_FOUND)

        # Build the prompt
        summaries_text = "\n\n".join(summaries)
        prompt = (
            "You are an AI News summarizer that will create a daily summary using the following summaries:\n\n"
            f"{summaries_text}\n\n"
            "Using the above summaries of articles, make a daily summary of about 100 words. "
            "You can merge content of different summaries into the same sentence if you find that appropriate. "
            "Only give the summary as output nothing else."
        )

        # Call Cohere
        try:
            response = co.generate(
                model="command",  # or "command-light" if you want a smaller model
                prompt=prompt,
                max_tokens=300,
                temperature=0.7
            )
            summary_result = response.generations[0].text.strip()
        except Exception as e:
            return Response({"error": f"Failed to generate summary: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "prompt": prompt,
            "generated_summary": summary_result
        }, status=status.HTTP_200_OK)
