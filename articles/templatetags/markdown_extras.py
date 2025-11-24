# myapp/templatetags/markdown_extras.py
import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

register = template.Library()


class DaisyClassTreeprocessor(Treeprocessor):
    extra_classes = (
        ("table", "table"),
        ("ul", "list-disc m-4 w-full gap-1"),
        ("ol", "list-decimal m-4 w-full gap-1"),
        ("h1", "my-4"),
        ("p", "pb-4"),
        ("h2", "my-4"),
        ("h3", "my-4"),
        ("h4", "my-4"),
        ("h5", "my-4"),
        ("h6", "my-4"),
    )

    def run(self, root):
        for extra_class in self.extra_classes:
            for elem in root.iter(extra_class[0]):
                current_class = elem.get("class", "")
                if current_class:
                    elem.set("class", f"{current_class} {extra_class[1]}")
                else:
                    elem.set("class", extra_class[1])
        return root


class DaisyClassExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(
            DaisyClassTreeprocessor(md), "daisy_class_processor", 0
        )


@register.filter
@stringfilter
def convert_markdown(value):
    return mark_safe(
        markdown.markdown(
            value, extensions=["fenced_code", "extra", "nl2br", DaisyClassExtension()]
        )
    )
