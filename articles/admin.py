from django.contrib import admin
from django.db.models import Count
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db import models
from django.forms import Textarea, TextInput
from .source_feeds import base
from .tasks import generate_article, generate_video
from .models import (
    Source,
    ArxivSource,
    WebSource,
    Article,
    ArticleTag,
    UserArticleHistory,
    ArticleVideo,
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
    source_feeds = base.source_feeds
    print(source_feeds)
    for source_feed in source_feeds:
        source_feed().fetch_feed()


@admin.action(description="Update tags for selected articles")
def update_tags(modeladmin, request, queryset):
    for article in queryset:
        article.update_tags()


@admin.action(description="Generate videos for the selected articles")
def make_video_from_article(modeladmin, request, queryset):
    tasks = []
    print("Starting to queue article generation tasks...")
    for article in queryset:
        print(f"Queuing article generation for Article ID: {article.id}")
        tasks.append(generate_video.delay(article.id))

    if len(tasks) > 0:
        progress_url = reverse("article_generation_progress")
        return HttpResponseRedirect(f"{progress_url}?task_id={tasks[0].id}")


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
    description="Create Articles for sources which have no corresponding articles, limit 32 at a time"
)
def make_missing_articles(modeladmin, request, queryset):
    annotated_sources = Source.objects.annotate(article_count=Count("articles"))

    missing_articles_sources = annotated_sources.filter(article_count=0).order_by("?")[
        :32
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


@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")
    list_filter = ("name",)

    fieldsets = (
        (
            None,
            {
                # Single field per tuple
                "fields": (("name", "description"),),
            },
        ),
    )


@admin.register(ArticleVideo)
class ArticleVideoAdmin(admin.ModelAdmin):
    list_display = ("article",)
    search_fields = ("article",)
    list_filter = ("article",)


# --- Article Admin ---
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin configuration for the main Article model."""

    list_display = ("id", "title", "based_on", "created_at")
    search_fields = ("title", "lead_paragraph", "research_question")
    list_filter = ("created_at",)
    actions = [update_tags, make_video_from_article]

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
                "fields": (("lead_paragraph",),),
                # Note: 'description' here is correct for ModelAdmin fieldsets
                "description": "The core narrative elements of the article.",
            },
        ),
        (
            "Metadata",
            {
                "fields": ("created_at", "tags"),
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
