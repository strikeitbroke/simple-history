from django.db import models
from simple_history.models import HistoricalRecords, HistoricForeignKey


# Author model (Many Authors can write Many Articles)
class Author(models.Model):
    class Meta:
        db_table = "author"
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    history = HistoricalRecords(table_name="author_history")

# Article model (Many-to-Many with Authors, One-to-Many with Comments)
class Article(models.Model):
    class Meta:
        db_table = "article"
    title = models.CharField(max_length=200)
    content = models.TextField()
    authors = models.ManyToManyField(Author, related_name='articles')  # Many-to-Many with Author
    history = HistoricalRecords(table_name="article_history", m2m_fields=[authors])

# Comment model (One-to-Many relationship with Article)
class Comment(models.Model):
    class Meta:
        db_table = "comment"
    article = HistoricForeignKey(Article, related_name='comments', on_delete=models.CASCADE)  # One-to-Many
    text = models.TextField()
    history = HistoricalRecords(table_name="comment_history")