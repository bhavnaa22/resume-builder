from abc import ABC, abstractmethod

class OutputAbstract(ABC):
    @abstractmethod
    def save(self, content, filepath):
        pass
    
    @abstractmethod
    def compile_latex(self, tex_path):
        pass