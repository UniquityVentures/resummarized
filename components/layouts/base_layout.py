from django_components import component

@component.register("base_layout")
class BaseComponent(component.Component):
    template_file = "base.html"
