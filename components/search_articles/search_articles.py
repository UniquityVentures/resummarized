from django_components import component


@component.register("search_articles")
class SearchArticlesComponent(component.Component):
    template_file = "search_articles.html"

    def get_template_data(self, args, kwargs, slots, context):
        return {"mobile": kwargs["mobile"]}
