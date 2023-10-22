from abc import ABC, abstractmethod
from dotalib import Match


class BaseMatchParser(ABC):
    """
    Not thread-safe in each new thread create new class instead using prebound functions
    """
    @abstractmethod
    def parse_match(self, content: str) -> Match:
        pass