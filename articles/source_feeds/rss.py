from .base import SourceFeed
from rss_parser import RSSParser
from articles.models import WebSource, Source
from requests import get  # noqa
from django.db import transaction
from typing import List


class RssSourceFeed(SourceFeed):
    urls: List[str]
    custom_schema = None

    def per_item(self, item):
        if WebSource.objects.all().filter(url__in=[link.content for link in item.links]).exists():
            return
        source = Source.objects.create(name=item.title.content)
        for link in item.links:
            WebSource.objects.create(url=link.content, source=source)

    def fetch_feed(self):
        for url in self.urls:
            print(url)
            response = get(url)

            if self.custom_schema is not None:
                rss = RSSParser.parse(response.text, schema=self.custom_schema)
            else:
                rss = RSSParser.parse(response.text)


            with transaction.atomic():
                for item in rss.channel.items:
                    self.per_item(item)
