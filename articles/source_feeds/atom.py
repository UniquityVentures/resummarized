from .base import SourceFeed
from rss_parser import AtomParser
from articles.models import WebSource, Source
from requests import get  # noqa
from django.db import transaction
from typing import List


class AtomSourceFeed(SourceFeed):
    urls: List[str]
    custom_schema = None

    def per_item(self, item):
        if WebSource.objects.all().filter(url__in=[link.content for link in item.links]).exists():
            return
        source = Source.objects.create(name=item.title.content)
        for link in item.links:
            WebSource.objects.create(url=link.content, source=source)

    def fetch_rss(self, url):
        return get(url)

    def fetch_feed(self):
        for url in self.urls:
            response = self.fetch_rss(url)

            if self.custom_schema is not None:
                rss = AtomParser.parse(response.text, schema=self.custom_schema)
            else:
                rss = AtomParser.parse(response.text)

            with transaction.atomic():
                for item in rss.feed.entries:
                    self.per_item(item)
