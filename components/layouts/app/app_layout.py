from django_components import component

@component.register("app_layout")
class AppComponent(component.Component):
    template_file = "app_layout.html"
