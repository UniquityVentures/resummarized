from .atom import AtomSourceFeed
from bs4 import BeautifulSoup
import requests
from articles.models import WebSource, Source

headers = {"User-Agent": "MyCustomUserAgent/1.0"}

class RedditSourceFeed(AtomSourceFeed):
    enabled = True
    urls = ["https://old.reddit.com/r/science/.rss", "https://old.reddit.com/r/science/.rss"]

    def fetch_rss(self, url):
        return requests.get(url, headers=headers)

    def per_item(self, item):
        soup = BeautifulSoup(item.content.content.content, 'html.parser')
        external_urls = [anchor.get("href") for anchor in soup.select(':-soup-contains-own("[link]")')]
        if len(external_urls) == 0:
            return

        if WebSource.objects.all().filter(url__in=external_urls).exists():
            return
        source = Source.objects.create(name=item.title.content.strip())
        for link in external_urls:
            WebSource.objects.create(url=link, source=source)
