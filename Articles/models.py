from django.db import models
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=255, default='Untitled Article')
    content = models.TextField(default='No content available.')
    category = models.CharField(max_length=20, default='General')
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title


class Summary(models.Model):
    article_id = models.IntegerField()
    summary = models.TextField()

    def __str__(self):
        return f"Summary for Article ID: {self.article_id}"
