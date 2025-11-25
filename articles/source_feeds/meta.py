from .rss import RssSourceFeed
from .base import register_source_feed


@register_source_feed
class MetaSourceFeed(RssSourceFeed):
    enabled = True
    urls = ["https://research.facebook.com/feed/"]

