from django_components import component

@component.register("card")
class CardComponent(component.Component):
    template_file = "card.html"

    def get_template_data(self, args, kwargs, slots, context):
        return kwargs
