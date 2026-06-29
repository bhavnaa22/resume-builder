from abc import ABC, abstractmethod

class ProcessAbstract(ABC):
    @abstractmethod
    def process(self, data):
        pass
    
    @abstractmethod
    def extract_keywords(self, text):
        pass
    
    @abstractmethod
    def match_skills(self, resume_data, job_keywords):
        pass