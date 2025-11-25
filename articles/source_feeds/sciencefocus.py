from .rss import RssSourceFeed


class ScienceFocusSourceFeed(RssSourceFeed):
    enabled = True
    urls = [
        "https://feeds.purplemanager.com/193c804a-a673-47bd-b09b-11baf4822a17/complete-rss-feed-for-science-focus"
    ]
