from abc import ABC, abstractmethod

class SourceFeed(ABC):
    @abstractmethod
    def fetch_feed(self):
        pass


