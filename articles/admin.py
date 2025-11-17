from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import models
from django.forms import TextInput
from .tasks import generate_article
from .models import (
    Source,
    ArxivSource,
    WebSource,
    Article,
    UserArticleHistory,
)

# --- Inlines for Source Model ---
class ArxivSourceInline(admin.TabularInline):
    """Inline for ArxivSource linked to Source."""
    model = ArxivSource
    extra = 1
    fields = ("arxiv_id",)
    can_delete = True

class WebSourceInline(admin.TabularInline):
    """Inline for WebSource linked to Source."""
    model = WebSource
    extra = 1
    fields = ("url",)
    can_delete = True



@admin.action(description="Create Articles from selected Sources")
def make_article_from_source(modeladmin, request, queryset):
    tasks = []
    for source in queryset:
        tasks.append(generate_article.delay(source.id))

    if len(tasks) > 0:
        progress_url = reverse('article_generation_progress')
            
        return HttpResponseRedirect(f'{progress_url}?task_id={tasks[0].id}')

# --- Source Admin ---
@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    """
    Admin configuration for the base Source model.
    Conditionally displays the correct inline (ArxivSource or WebSource)
    and locks the source_type after creation.
    """
    list_display = ("id", "name", "source_count")
    list_filter = ("name",)
    search_fields = ("name",)
    inlines = [ArxivSourceInline, WebSourceInline]
    actions = [make_article_from_source]


# --- Article Admin ---
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin configuration for the main Article model."""
    list_display = ("id", "title", "based_on", "created_at")
    search_fields = ("title", "lead_paragraph", "research_question")
    list_filter = ("created_at",)

    fieldsets = (
        (None, {
            # Single field per tuple
            "fields": (("title",), ("based_on",)),
        }),
        ("Core Narrative", {
            # Single field per tuple
            "fields": (
                ("lead_paragraph",), 
                ("background_context",), 
                ("research_question",)
            ),
            # Note: 'description' here is correct for ModelAdmin fieldsets
            "description": "The core narrative elements of the article.",
        }),
        ("Study Details", {
            # Single field per tuple
            "fields": (
                ("simplified_methods",),
                ("core_findings",),
                ("surprise_finding",),
                ("study_limitations",),
            ),
            "description": "In-depth information about the study.",
        }),
        ("Forward Look", {
            # Single field per tuple
            "fields": (("future_implications",), ("next_steps",)),
            "description": "Impact and future work.",
        }),
        ("Metadata", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )


    # Make sure text fields use the large text input widget
    formfield_overrides = {
        models.TextField: {
            "widget": TextInput(attrs={"size": 80})  # Use TextInput widget instead of TextArea
        },
    }

# --- UserArticleHistory Admin ---
@admin.register(UserArticleHistory)
class UserArticleHistoryAdmin(admin.ModelAdmin):
    """Admin configuration for tracking when users viewed articles."""
    list_display = ("id", "user", "article", "datetime")
    list_filter = ("datetime",)
    search_fields = ("user__username", "article__title")
    raw_id_fields = ("user", "article")
    readonly_fields = ("datetime",)
