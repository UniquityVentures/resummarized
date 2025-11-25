from .rss import RssSourceFeed
from .base import register_source_feed


@register_source_feed
class GizmodoSourceFeed(RssSourceFeed):
    enabled = True
    urls = ["https://gizmodo.com/feed"]
