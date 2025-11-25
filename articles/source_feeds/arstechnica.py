from .rss import RssSourceFeed


class ArsTechnicaSourceFeed(RssSourceFeed):
    enabled = True
    urls = [
        "https://feeds.arstechnica.com/arstechnica/technology-lab",
        "https://feeds.arstechnica.com/arstechnica/gaming",
        "https://feeds.arstechnica.com/arstechnica/science",
        "https://feeds.arstechnica.com/arstechnica/staff-blogs",
    ]
