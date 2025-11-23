from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import models
from django.contrib import admin
from django.forms import Textarea, TextInput
from .source_feeds.google import GoogleSourceFeed
from .source_feeds.meta import MetaSourceFeed
from .source_feeds.reddit import RedditSourceFeed
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

    formfield_overrides = {
        models.TextField: {"widget": TextInput(attrs={"size": 80})},
    }


class WebSourceInline(admin.TabularInline):
    """Inline for WebSource linked to Source."""

    model = WebSource
    extra = 1
    fields = ("url",)
    can_delete = True

    formfield_overrides = {
        models.TextField: {"widget": TextInput(attrs={"size": 80})},
    }


@admin.action(description="Fetch sources from feeds")
def update_sources(modeladmin, request, queryset):
    source_feeds = [GoogleSourceFeed, MetaSourceFeed, RedditSourceFeed]
    for source_feed in source_feeds:
        source_feed().fetch_feed()


@admin.action(description="Create Articles from selected Sources")
def make_article_from_source(modeladmin, request, queryset):
    tasks = []
    print("Starting to queue article generation tasks...")
    for source in queryset:
        print(f"Queuing article generation for Source ID: {source.id}")
        tasks.append(generate_article.delay(source.id))

    if len(tasks) > 0:
        progress_url = reverse("article_generation_progress")

        return HttpResponseRedirect(f"{progress_url}?task_id={tasks[0].id}")


@admin.action(
    description="Create Articles for sources which have no corresponding articles, limit 10 at a time"
)
def make_missing_articles(modeladmin, request, queryset):
    annotated_sources = Source.objects.annotate(article_count=Count("articles"))

    missing_articles_sources = annotated_sources.filter(article_count=0).order_by("?")[
        :8
    ]

    for source in missing_articles_sources:
        generate_article.delay(source.id)


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
    actions = [make_article_from_source, update_sources, make_missing_articles]


# --- Article Admin ---
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin configuration for the main Article model."""

    list_display = ("id", "title", "based_on", "created_at")
    search_fields = ("title", "lead_paragraph", "research_question")
    list_filter = ("created_at",)

    fieldsets = (
        (
            None,
            {
                # Single field per tuple
                "fields": (("title",), ("based_on",)),
            },
        ),
        (
            "Core Narrative",
            {
                # Single field per tuple
                "fields": (
                    ("lead_paragraph",),
                    ("background_context",),
                    ("research_question",),
                ),
                # Note: 'description' here is correct for ModelAdmin fieldsets
                "description": "The core narrative elements of the article.",
            },
        ),
        (
            "Study Details",
            {
                # Single field per tuple
                "fields": (
                    ("simplified_methods",),
                    ("core_findings",),
                    ("surprise_finding",),
                    ("study_limitations",),
                ),
                "description": "In-depth information about the study.",
            },
        ),
        (
            "Forward Look",
            {
                # Single field per tuple
                "fields": (("future_implications",), ("next_steps",)),
                "description": "Impact and future work.",
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )

    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"size": 80})},
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
