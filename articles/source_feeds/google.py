from .rss import RssSourceFeed
from .base import register_source_feed


@register_source_feed
class GoogleSourceFeed(RssSourceFeed):
    enabled = True
    urls = ["https://research.google/blog/rss/"]

