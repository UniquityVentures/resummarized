from .rss import RssSourceFeed

class MetaSourceFeed(RssSourceFeed):
    enabled = True
    urls = ["https://research.facebook.com/feed/"]

