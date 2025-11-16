from django_components import component

@component.register("navbar_layout")
class NavbardComponent(component.Component):
    template_file = "navbar_layout.html"
