from src.main.domain.output_ports.topic_ports import TopicRepository
from src.main.domain.exceptions import Topic_NotFound_Exception

class Topic_Validator():
    def __init__(self, repository: TopicRepository):
        self.repository = repository
    
    def find_id(self, topic_id: int):
        topic = self.repository.find_by_id(topic_id)

        if topic is None:
            raise Topic_NotFound_Exception(f"Tema no encontrado con el ID {topic_id}.")
        
        return topic
    
    def find_title(self, title: str):
        topic = self.repository.find_by_title(title)

        if topic is None:
            raise Topic_NotFound_Exception(f"Tema no encontrado con el título {title}.")
        
        return topic
    
