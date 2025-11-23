from django_components import component


@component.register("link")
class LinkComponent(component.Component):
    template_file = "link.html"

    def get_template_data(self, args, kwargs, slots, context):
        return {"href": kwargs["href"], "title": kwargs["title"]}
