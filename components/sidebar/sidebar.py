from django_components import component

@component.register("sidebar")
class SidebarComponent(component.Component):
    template_file = "sidebar.html"

