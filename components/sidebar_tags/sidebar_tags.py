from django_components import component
from django.http import QueryDict


@component.register("sidebar_tags")
class SidebarTagsComponent(component.Component):
    template_file = "sidebar_tags.html"

    def get_template_data(self, args, kwargs, slots, context):
        from articles.models import ArticleTag

        base_query: QueryDict = context["request"].GET.copy()

        selected_tags = base_query.getlist("filter_tags")

        entries = []

        for tag in ArticleTag.objects.all():
            str_id = str(tag.id)

            link_query = base_query.copy()

            if str_id in selected_tags:
                current_list = link_query.getlist("filter_tags")
                current_list.remove(str_id)
                link_query.setlist("filter_tags", current_list)

                icon = "minus"
            else:
                link_query.appendlist("filter_tags", str_id)

                icon = "plus"

            entries.append(
                {
                    "name": tag.name,
                    "link": f"?{link_query.urlencode()}",
                    "icon": icon,
                    "active": str_id in selected_tags,
                }
            )

        return {
            "entries": entries,
        }
