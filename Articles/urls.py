from django.urls import path
from .views import ArticleListCreateView, ArticleRetrieveUpdateDestroyView, ArticleFetchView, GenerateSummariesView, \
    DailyAICompiledSummaryView

urlpatterns = [
    path("", ArticleListCreateView.as_view(), name="article-list-create"),
    path("<int:pk>/", ArticleRetrieveUpdateDestroyView.as_view(), name="article-detail"),
    path("fetch/", ArticleFetchView.as_view(), name="fetch-articles"),
    path("summary/", GenerateSummariesView.as_view(), name="summarize-articles"),
    path("user_daily/", DailyAICompiledSummaryView.as_view(), name="daily-user-summary")
]
