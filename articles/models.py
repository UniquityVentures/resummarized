# Create your models here.


from django.db import models
from django.utils.timezone import now
from pgvector.django import VectorField
from resummarized_django.embeddings import gen_embedding
from django.contrib.auth import get_user_model
from pgvector.django import CosineDistance


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

    def get_links(self):
        links = [source.get_link() for source in self.sources()]
        return links

    def __str__(self):
        return f"{self.name} - {self.source_count()} sources"


class ArxivSource(models.Model):
    arxiv_id = models.TextField(null=False)
    source = models.ForeignKey(
        Source, on_delete=models.CASCADE, related_name=SourceType.ARXIV
    )

    def get_link(self):
        return f"https://arxiv.org/abs/{self.arxiv_id}"


class WebSource(models.Model):
    url = models.TextField(null=False)
    source = models.ForeignKey(
        Source, on_delete=models.CASCADE, related_name=SourceType.WEB_PAGE
    )

    def get_link(self):
        return self.url


class ArticleTag(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    vector = VectorField(dimensions=768)

    def save(self, *args, **kwargs):
        self.vector = gen_embedding(self.description)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Article(models.Model):
    title = models.TextField()

    lead_paragraph = models.TextField(
        help_text="A concise summary of the article's main point."
    )

    based_on = models.ForeignKey(
        Source, on_delete=models.SET_NULL, null=True, related_name="articles"
    )

    created_at = models.DateTimeField(default=now, blank=True)

    tags = models.ManyToManyField(ArticleTag, blank=True)

    def __str__(self):
        return self.title

    def update_tags(self):
        query_vector = self.vector.first().vector

        SIMILARITY_THRESHOLD = 0.2
        N = 5

        similar_tags_query0 = ArticleTag.objects.annotate(
            distance=CosineDistance("vector", query_vector)
        )
        
        similar_tags_pks = similar_tags_query0.filter(
            distance__lt=1.0 - SIMILARITY_THRESHOLD
        ).order_by("distance").values_list('pk', flat=True)[:N]
        

        self.tags.set(similar_tags_pks)


class UserArticleHistory(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="user_history"
    )
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="article_history"
    )
    datetime = models.DateTimeField(default=now, blank=True)


class ArticlePins(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="pins")
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="pins"
    )
    datetime = models.DateTimeField(default=now, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["article", "user"], name="unique_pins")
        ]
