from abc import ABC, abstractmethod

source_feeds = []


class SourceFeedMetaClass(type):
    def __new__(cls, clsname, superclasses, attributedict):
        enabled = attributedict.get("enabled", False)
        new_cls = super().__new__(cls, clsname, superclasses, attributedict)
        if enabled:
            source_feeds.append(new_cls)
        return new_cls


class SourceFeed(ABC, metaclass=SourceFeedMetaClass):
    @abstractmethod
    def fetch_feed(self):
        pass
