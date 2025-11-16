# Create your models here.

from django.db import models
from django.utils.timezone import now
from pgvector.django import VectorField
from resummarized_django.embeddings import gen_embedding
from django.contrib.auth import get_user_model


class ArticleVector(models.Model):
    article = models.ForeignKey(
        "articles.Article", on_delete=models.CASCADE, related_name="vector"
    )
    # 768 is for EmbeddingGemma, if using different model, change 768 to corresponding dimensions of the other model
    vector = VectorField(dimensions=768)


class SourceType(models.TextChoices):
    ARXIV = "source_arxiv"
    WEB_PAGE = "source_web_page"



class Source(models.Model):
    name = models.TextField()

    def sources(self):
        sources = []
        for source_type, _ in SourceType.choices:
            sources.extend(getattr(self, source_type).all())
        return sources

    def source_count(self):
        count = 0
        for source_type, _ in SourceType.choices:
            count += getattr(self, source_type).count()
        return count

    def __str__(self):
        return f"{self.name} - {self.source_count()} sources"


class ArxivSource(models.Model):
    arxiv_id = models.TextField(null=False)
    source = models.ForeignKey(
        Source, on_delete=models.CASCADE, related_name=SourceType.ARXIV
    )


class WebSource(models.Model):
    url = models.TextField(null=False)
    source = models.ForeignKey(
        Source, on_delete=models.CASCADE, related_name=SourceType.WEB_PAGE
    )



# Create your models here.
class Article(models.Model):
    title = models.TextField()

    lead_paragraph = models.TextField(help_text="A concise summary of the article's main point.")
    background_context = models.TextField(help_text="Contextual information leading up to the research.")
    research_question = models.TextField(help_text="The primary question the research aims to answer.")
    simplified_methods = models.TextField(help_text="A simplified explanation of the methods used in the study.")
    core_findings = models.TextField(help_text="The main findings of the research.")
    surprise_finding = models.TextField(null=True, blank=True, help_text="Any unexpected results from the study.")
    future_implications = models.TextField(help_text="The potential implications of the research findings.")
    study_limitations = models.TextField(help_text="Limitations of the study that may affect interpretation of results.")
    next_steps = models.TextField(help_text="Suggested future research directions based on the study.")

    # Group of Sources from which this article is derived
    based_on = models.ForeignKey(
        Source, on_delete=models.SET_NULL, null=True, related_name="articles"
    )

    created_at = models.DateTimeField(default=now, blank=True)

    def save(self, *args, **kwargs):
        # Generating embedding based on summary from arxiv
        article = super(Article, self).save(*args, **kwargs)
        ArticleVector.objects.update_or_create(
            article=self, vector=gen_embedding(self.lead_paragraph)
        )
        return article


class UserArticleHistory(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="user_history"
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="article_history"
    )
    datetime = models.DateTimeField(default=now, blank=True)
