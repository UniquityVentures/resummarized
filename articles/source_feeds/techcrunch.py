from .rss import RssSourceFeed
from .base import register_source_feed


@register_source_feed
class TechCrunchSourceFeed(RssSourceFeed):
    enabled = True
    urls = [
        "https://techcrunch.com/feed/"
    ]
