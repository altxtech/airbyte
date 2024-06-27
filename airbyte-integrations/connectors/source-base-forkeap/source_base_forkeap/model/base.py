from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict

@dataclass
class Base(ABC):

    def __post_init__(self):
        self.validate()

    def to_dict(self):
        return asdict(self)

    @abstractmethod
    def validate(self):
        pass


