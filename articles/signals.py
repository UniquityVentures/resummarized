from django.db.models.signals import post_save
from django.dispatch import receiver
from resummarized_django.embeddings import gen_embedding
from .models import Article, ArticleVector


@receiver(post_save, sender=Article)
def post_article_save(sender, instance, created, **kwargs):
    new_vector = gen_embedding(instance.lead_paragraph)
    article_vector_instance, _ = ArticleVector.objects.update_or_create(
        article=instance,
        defaults={'vector': new_vector}
    )
