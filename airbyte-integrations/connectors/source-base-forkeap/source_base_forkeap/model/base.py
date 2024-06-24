from abc import ABC, abstractmethod

class Base(ABC):

    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def to_dict(self):
        pass

