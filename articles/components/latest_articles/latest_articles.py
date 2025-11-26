from django_components import component
from django.db.models import Count
from django.http import QueryDict
from articles.models import Article


@component.register("latest_articles")
class LatestArticles(component.Component):
    template_file = "latest_articles.html"

    def get_template_data(self, args, kwargs, slots, context):
        offset = int(kwargs.get("offset", 0))
        limit = int(kwargs.get("limit", 10))
        tags = kwargs.get("tags", [])
        print(tags)
        if len(tags) > 0:
            articles = list(
                Article.objects.all()
                .order_by("-created_at")
                .filter(tags__in=tags)
                .alias(num_tags=Count("tags"))
                .filter(num_tags=len(tags))[offset : offset + limit]
            )
            print(articles)
        else:
            articles = list(
                Article.objects.all().order_by("-created_at")[offset : offset + limit]
            )

        query = QueryDict("", mutable=True)
        query["offset"] = offset + limit
        query.setlist("filter_tags", tags)
        if len(articles) > 0:
            last = articles.pop()
            query["limit"] = limit
            next = f"/articles/latest/?{query.urlencode()}"
            return {
                "last": last,
                "articles": articles,
                "limit": limit,
                "offset": offset,
                "next": next,
            }

        query["limit"] = 0
        next = f"/articles/latest/?{query.urlencode()}"
        return {
            "last": None,
            "articles": [],
            "limit": 0,
            "offset": offset,
            "next": next,
        }

    class View:
        # Define handlers
        def get(self, request, *args, **kwargs):
            limit = request.GET.get("limit", None)
            offset = request.GET.get("offset", None)
            tags = request.GET.getlist("filter_tags")
            return LatestArticles.render_to_response(
                request=request,
                kwargs={
                    "limit": limit,
                    "offset": offset,
                    "tags": tags,
                },
            )
