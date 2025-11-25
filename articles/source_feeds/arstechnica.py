from .rss import RssSourceFeed
from .base import register_source_feed


@register_source_feed
class ArsTechnicaSourceFeed(RssSourceFeed):
    enabled = True
    urls = [
        "https://feeds.arstechnica.com/arstechnica/technology-lab",
        "https://feeds.arstechnica.com/arstechnica/gaming",
        "https://feeds.arstechnica.com/arstechnica/science",
        "https://feeds.arstechnica.com/arstechnica/staff-blogs",
    ]
