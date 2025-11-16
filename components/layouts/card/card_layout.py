from django_components import component

@component.register("card_layout")
class CardComponent(component.Component):
    template_file = "card_layout.html"
