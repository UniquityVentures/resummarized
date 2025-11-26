from django_components import component
from django.http import QueryDict
from django.db.models import Count


@component.register("for_you_articles")
class ForYouArticles(component.Component):
    template_file = "for_you_articles.html"

    def get_template_data(self, args, kwargs, slots, context):
        offset = int(kwargs.get("offset", 0))
        limit = int(kwargs.get("limit", 10))
        request = context["request"]
        user = request.user
        tags = kwargs.get("tags", [])
        if len(tags) > 0:
            articles = list(
                user.for_you()
                .filter(tags__in=tags)
                .alias(num_tags=Count("tags"))
                .filter(num_tags=len(tags))[offset : offset + limit]
            )
        else:
            articles = list(user.for_you()[offset : offset + limit])
        query = QueryDict("", mutable=True)
        query["offset"] = offset + limit
        query.setlist("filter_tags", tags)
        if len(articles) > 0:
            last = articles.pop()
            query["limit"] = limit
            next = f"/articles/for_you/?{query.urlencode()}"
            return {
                "last": last,
                "articles": articles,
                "limit": limit,
                "offset": offset,
                "next": next,
            }

        query["limit"] = 0
        next = f"/articles/for_you/?{query.urlencode()}"
        return {
            "last": None,
            "articles": [],
            "limit": 0,
            "offset": offset,
            "next": next,
        }

    class View:
        def get(self, request, *args, **kwargs):
            limit = request.GET.get("limit", None)
            offset = request.GET.get("offset", None)
            tags = request.GET.getlist("filter_tags")
            return self.component_cls.render_to_response(
                request=request,
                context={"request": request},
                kwargs={
                    "limit": limit,
                    "offset": offset,
                    "tags": tags,
                },
            )
