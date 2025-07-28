import numpy as np
from google import genai
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import F
from pgvector.django import CosineDistance
from datetime import timedelta

from .models import Article, Summary, Embedding
from .serializers import ArticleSerializer
from .utils import get_previous_day_articles_by_category

GEMINI_CLIENT = genai.Client(api_key="AIzaSyC3DCjjQV2_dUP_tg7Wrt8Kr5QUIg6ifaE")

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


class GenerateSummaryView(APIView):
    """
    Takes article_id, generates a summary using Gemini, and saves it in the Summary table.
    """

    def post(self, request, *args, **kwargs):
        article_id = request.data.get("article_id")
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({"error": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

        prompt = f"""
        Generate a summary of the following news article:

        Article: {article.content}

        ONLY output the summary.
        """
        try:
            response = GEMINI_CLIENT.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            summary_text = response.text.strip()
            Summary.objects.create(article_id=article.id, summary=summary_text)
            return Response({"summary": summary_text}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GenerateEmbeddingView(APIView):
    """
    Takes article_id, generates embedding using Gemini, and saves it in the Embedding table.
    """

    def post(self, request, *args, **kwargs):
        article_id = request.data.get("article_id")
        try:
            article = Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return Response({"error": "Article not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            result = GEMINI_CLIENT.models.embed_content(
                model="models/text-embedding-004",
                contents=[article.content],
            )
            embedding_vector = result.embeddings[0].values
            Embedding.objects.create(article_id=article.id, embedding=embedding_vector)
            return Response({"message": "Embedding saved successfully."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class NewsQueryView(APIView):
    """
    Accepts date_range (1 or 7) and a query.
    Filters articles by date, finds top-K similar using pgvector cosine distance,
    fetches summaries, and uses Gemini to answer the query.
    """

    def post(self, request, *args, **kwargs):
        date_range = request.data.get("date_range")
        query = request.data.get("query")

        if not query or date_range not in [1, 7]:
            return Response({"error": "Invalid input. Provide 'query' and 'date_range' (1 or 7)."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Filter recent articles
            since_date = timezone.now().date() - timedelta(days=date_range)
            articles = Article.objects.filter(date__gte=since_date)

            if not articles.exists():
                return Response({"error": "No articles found in that date range."}, status=status.HTTP_404_NOT_FOUND)

            article_ids = list(articles.values_list("id", flat=True))

            # Get query embedding via Gemini
            result = GEMINI_CLIENT.models.embed_content(
                model="models/text-embedding-004",
                contents=[query],
            )
            query_vector = result.embeddings[0].values

            # Use pgvector to get top-K similar embeddings
            K = 5
            similar_embeddings = (
                Embedding.objects
                .filter(article_id__in=article_ids)
                .annotate(distance=CosineDistance(F("embedding"), query_vector))
                .order_by("distance")[:K]
            )

            if not similar_embeddings:
                return Response({"error": "No similar articles found."}, status=status.HTTP_404_NOT_FOUND)

            top_k_ids = [e.article_id for e in similar_embeddings]

            # Fetch summaries
            summaries = Summary.objects.filter(article_id__in=top_k_ids)

            if not summaries.exists():
                return Response({"error": "No summaries found for similar articles."}, status=status.HTTP_404_NOT_FOUND)

            combined_summaries = "\n\n".join([s.summary for s in summaries])

            # Construct prompt and query Gemini
            prompt = f"""
            Use ONLY the following news article summaries to answer the user query.
            
            News Summaries:
            {combined_summaries}
            
            User Query:
            {query}
            
            ONLY output the answer. Do not include any extra text.
            """

            gemini_response = GEMINI_CLIENT.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            answer = gemini_response.text.strip()

            return Response({"answer": answer}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
