from django_components import component
from articles.models import Article


@component.register("latest_articles")
class LatestArticles(component.Component):
    template_file = "latest_articles.html"

    def get_template_data(self, args, kwargs, slots, context):
        offset = int(kwargs.get("offset", 0))
        limit = int(kwargs.get("limit", 10))
        articles = list(Article.objects.all()[offset : offset + limit])

        if len(articles) > 0:
            last = articles.pop()
            return {"last": last, "articles": articles, "limit": limit, "offset": offset}
        return {"last": None, "articles": [], "offset": offset, "limit": 0}

    class View:
        # Define handlers
        def get(self, request, *args, **kwargs):
            limit = request.GET.get("limit", None)
            offset = request.GET.get("offset", None)
            return LatestArticles.render_to_response(
                request=request,
                kwargs={
                    "limit": limit,
                    "offset": offset,
                },
            )
