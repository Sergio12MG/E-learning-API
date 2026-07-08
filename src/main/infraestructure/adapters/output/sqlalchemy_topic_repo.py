from typing import List

from sqlalchemy.orm import Session

from src.main.domain.models.course import Topic
from src.main.domain.output_ports.topic_ports import TopicRepository
from src.main.infraestructure.db.models import Topic as ORMTopic

class Entity_Converter:
    @staticmethod
    def Domain_to_ORM(domain: Topic) -> ORMTopic:
        return ORMTopic(
            title=domain.title,
            content=domain.content,
            order=domain.order,
            topic_type=domain.topic_type,
            resource_url=domain.resource_url,
            module_id=domain.module_id
        )
    
    @staticmethod
    def ORM_to_Domain(orm: ORMTopic) -> Topic:
        return Topic(
            id=orm.id,
            title=orm.title,
            content=orm.content,
            order=orm.order,
            topic_type=orm.topic_type,
            resource_url=orm.resource_url,
            module_id=orm.module_id
        )
    
class SQLAlchemy_TopicRepository(TopicRepository):
    def __init__(self, db: Session):
        self.db = db

    # ========= CREATE =========
    def save(self, topic: Topic) -> Topic:
        # Conversion Domain -> ORM
        orm_topic = Entity_Converter.Domain_to_ORM(topic)

        self.db.add(orm_topic)
        self.db.commit()
        self.db.refresh(orm_topic)

        # Conversion ORM -> Domain
        return Entity_Converter.ORM_to_Domain(orm_topic)
    
    # ========= READ =========
    # By ID
    def find_by_id(self, topic_id: int) -> Topic | None:
        orm_topic = self.db.get(ORMTopic, topic_id)

        if not orm_topic:
            return None
        
        return Entity_Converter.ORM_to_Domain(orm_topic)
    
    # By title
    def find_by_title(self, title: str) -> Topic | None:
        orm_topic = self.db.query(ORMTopic).filter(ORMTopic.title == title).first()

        if orm_topic:
            return Entity_Converter.ORM_to_Domain(orm_topic)
        
        return None
    
    # All topics by a given module
    def find_all_by_module(self, module_id: int) -> List[Topic] | None:
        orm_topics = self.db.query(ORMTopic).filter(ORMTopic.module_id == module_id).all()

        return [Entity_Converter.ORM_to_Domain(orm_topic) for orm_topic in orm_topics]
    
    # ========= UPDATE =========
    def update(self, topic: Topic) -> Topic:
        orm_topic = self.db.get(ORMTopic, topic.id)

        if not orm_topic:
            return None

        orm_topic.title = topic.title
        orm_topic.content = topic.content
        orm_topic.order = topic.order
        orm_topic.topic_type = topic.topic_type
        orm_topic.resource_url = topic.resource_url

        self.db.commit()
        self.db.refresh(orm_topic)

        return Entity_Converter.ORM_to_Domain(orm_topic)
    
    # ========= DELETE =========
    def delete_id(self, topic_id: int) -> None:
        orm_topic = self.db.get(ORMTopic, topic_id)

        if orm_topic:
            self.db.delete(orm_topic)
            self.db.commit()

        return None
