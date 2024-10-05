from django.test import TestCase
from django.utils import timezone

from .models import Author, Article, Comment


class SimpleHistory(TestCase):
    def test_foreign_key_relation(self):
        article_1 = Article.objects.create(title="article 1", content="this is article 1")
        comment_1 = Comment.objects.create(article=article_1, text="this is a good article.")
        t0 = timezone.now()

        comment_2 = Comment.objects.create(article=article_1, text="this is a bad article.")
        t1 = timezone.now()
        article_asof_t0 = article_1.history.as_of(t0)
        res = article_asof_t0.comments.all()
        self.assertEqual(res[0].text, "this is a good article.")

        article_asof_t1 = article_1.history.as_of(t1)
        res = article_asof_t1.comments.all()
        self.assertEqual(res[0].text, "this is a bad article.")
        self.assertEqual(res[1].text, "this is a good article.")

        article_1.title = "article 1 updated" 
        article_1.save()
        t2 = timezone.now()

        article_asof_t2 = article_1.history.as_of(t2)
        self.assertEqual(article_asof_t2.title, "article 1 updated")


    
    def test_m2m_relation(self):
        article = Article.objects.create(title="article 1", content="this is article 1")
        comment = Comment.objects.create(article=article, text="this is a good read.")
        author = Author.objects.create(name="Jack", bio="i like to write.")
        article.authors.add(author.pk)
        t0 = timezone.now()

        author.bio = "i don't like to write anymore."
        author.save()

        t1 = timezone.now()
        author = article.authors.filter(id=author.pk).first()
        author_asof_t1 = author.history.as_of(t1)
        self.assertEqual(author_asof_t1.bio, "i don't like to write anymore.")

