from .rss import RssSourceFeed


class TechRadarSourceFeed(RssSourceFeed):
    enabled = True
    urls = [
        "https://www.techradar.com/feeds/tag/computing",
        "https://www.techradar.com/feeds/tag/computing-components",
        "https://www.techradar.com/feeds/tag/internet",
        "https://www.techradar.com/feeds/tag/software",
        "https://www.techradar.com/feeds/tag/gaming",
        "https://www.techradar.com/feeds/tag/entertainment",
    ]
