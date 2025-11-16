from django_components import component

@component.register("tabs")
class TabsComponent(component.Component):
    template_file = "tabs.html"

    def get_template_data(self, args, kwargs, slots, context):
        return {"tabs": kwargs["tabs"]}
