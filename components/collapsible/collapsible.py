from django_components import component

@component.register("collapsible")
class CollapsibleComponent(component.Component):
    template_file = "collapsible.html"

    def get_template_data(self, args, kwargs, slots, context):
        return {"title": kwargs["title"]}
