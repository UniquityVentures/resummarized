from .rss import RssSourceFeed


class TechCrunchSourceFeed(RssSourceFeed):
    enabled = True
    urls = [
        "https://techcrunch.com/feed/"
    ]
