from django.urls import path
from .views import ArticleListCreateView, ArticleRetrieveUpdateDestroyView, ArticleFetchView, NewsQueryView, \
    GenerateSummaryView, GenerateEmbeddingView

urlpatterns = [
    path("", ArticleListCreateView.as_view(), name="article-list-create"),
    path("<int:pk>/", ArticleRetrieveUpdateDestroyView.as_view(), name="article-detail"),
    path("fetch/", ArticleFetchView.as_view(), name="fetch-articles"),
    path("generate-summary/", GenerateSummaryView.as_view(), name="generate-summary"),
    path("generate-embedding/", GenerateEmbeddingView.as_view(), name="generate-embedding"),
    path("query/", NewsQueryView.as_view(), name="query")
]
