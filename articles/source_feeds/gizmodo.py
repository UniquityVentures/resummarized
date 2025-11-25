from .rss import RssSourceFeed


class GizmodoSourceFeed(RssSourceFeed):
    enabled = True
    urls = ["https://gizmodo.com/feed"]
