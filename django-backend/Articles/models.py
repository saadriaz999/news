from django.db import models
from django.utils import timezone
from pgvector.django import VectorField

class Article(models.Model):
    title = models.CharField(max_length=255, default='Untitled Article')
    content = models.TextField(default='No content available.')
    category = models.CharField(max_length=20, default='General')
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('title', 'date')

    def __str__(self):
        return self.title


class Embedding(models.Model):
    article_id = models.IntegerField()
    embedding = VectorField(dimensions=768)


class Summary(models.Model):
    article_id = models.IntegerField()
    summary = models.TextField()

    def __str__(self):
        return f"Summary for Article ID: {self.article_id}"
