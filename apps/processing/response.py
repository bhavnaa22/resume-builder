class ProcessResponse:
    def __init__(self):
        self.data = {}
        self.keywords = []
        self.matched_skills = []
        self.suggestions = []
    
    def to_dict(self):
        return {
            'data': self.data,
            'keywords': self.keywords,
            'matched_skills': self.matched_skills,
            'suggestions': self.suggestions
        }