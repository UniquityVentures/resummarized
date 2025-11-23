from django_components import component


@component.register("article_card")
class ArticleCardView(component.Component):
    template_file = "article_card.html"

    def get_template_data(self, args, kwargs, slots, context):
        return {
            "article": kwargs["article"],
            "attrs": kwargs.get("attrs", {}),
            "is_pinned": kwargs["article"].pins.filter(user=context["user"]).exists()
            if context.get("user", None) is not None
            else None,
        }
