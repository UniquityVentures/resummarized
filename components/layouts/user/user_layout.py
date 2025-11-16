from django_components import component

@component.register("user_layout")
class UserComponent(component.Component):
    template_file = "user_layout.html"
