from abc import ABC, abstractmethod

class InputAbstract(ABC):
    @abstractmethod
    def extract_text(self, filepath):
        pass
    
    @abstractmethod
    def validate_format(self, filepath):
        pass