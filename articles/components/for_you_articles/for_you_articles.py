from django_components import component

@component.register("for_you_articles")
class ForYouArticles(component.Component):
    template_file = "for_you_articles.html"

    def get_template_data(self, args, kwargs, slots, context):
        offset = int(kwargs.get("offset", 0))
        limit = int(kwargs.get("limit", 10))
        user = context['request'].user

        articles = list(user.for_you()[offset:offset+limit])
        if len(articles) > 0:
            last = articles.pop()
            print(last)
            return {"last": last, "articles": articles, "limit": limit, "offset": offset}
        return {"last": None, "articles": [], "limit": 0, "offset": offset}


    class View:
        def get(self, request, *args, **kwargs):
            limit = request.GET.get("limit", None)
            offset = request.GET.get("offset", None)
            return self.component_cls.render_to_response(
                request=request,
                context={"request": request},
                kwargs={
                    "limit": limit,
                    "offset": offset,
                },
            )

