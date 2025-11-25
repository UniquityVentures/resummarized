from .rss import RssSourceFeed

class GoogleSourceFeed(RssSourceFeed):
    enabled = True
    urls = ["https://research.google/blog/rss/"]

