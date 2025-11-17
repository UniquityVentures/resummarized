from django_components import component
from articles.models import Article

@component.register("articles_datalist")
class ArticlesDatalistComponent(component.Component):
    template_file = "articles_datalist.html"

    def get_template_data(self, args, kwargs, slots, context):
        query = kwargs.get("query", None)
        if query is None:
            return {"articles": Article.objects.all()}
        return {"articles": Article.objects.filter(title__icontains=query)[:5]}

    class View:
        # Define handlers
        def get(self, request, *args, **kwargs):
            query = request.GET.get("query", None)
            return ArticlesDatalistComponent.render_to_response(
                request=request,
                kwargs={
                    "query": query,
                },
            )
