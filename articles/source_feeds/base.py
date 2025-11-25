from abc import ABC, abstractmethod

source_feeds = []

def register_source_feed(cls):
    source_feeds.append(cls)
    return cls

class SourceFeed(ABC):
    @abstractmethod
    def fetch_feed(self):
        pass
