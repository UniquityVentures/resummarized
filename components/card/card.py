from django_components import component

@component.register("card")
class CardComponent(component.Component):
    template_file = "card.html"
