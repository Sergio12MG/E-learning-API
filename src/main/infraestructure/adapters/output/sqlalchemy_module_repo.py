from typing import List

from sqlalchemy.orm import Session

from src.main.domain.models.course import CModule, Topic
from src.main.domain.output_ports.module_ports import ModuleRepository
from src.main.infraestructure.db.models import CModule as ORMModule
from src.main.infraestructure.db.models import Topic as ORMTopic
from src.main.infraestructure.adapters.output.sqlalchemy_topic_repo import Entity_Converter as Topic_EC

class Entity_Converter:
    @staticmethod
    def Domain_to_ORM(domain: CModule) -> ORMModule:
        return ORMModule(
            title=domain.title,
            description=domain.description,
            order=domain.order,
            is_published=domain.is_published,
            course_id=domain.course_id,
            parent_id=domain.parent_id
        )

    @staticmethod
    def ORM_to_Domain(orm: ORMModule) -> CModule:
        return CModule(
            id=orm.id,
            title=orm.title,
            course_id=orm.course_id,
            order=orm.order,
            is_published=orm.is_published,
            description=orm.description,
            parent_id=orm.parent_id
        )

class SQLAlchemy_ModuleRepository(ModuleRepository):
    def __init__(self, db: Session):
        self.db = db

    # ========= CREATE =========
    def save(self, module: CModule) -> CModule:
        # Conversion Domain -> ORM
        orm_module = Entity_Converter.Domain_to_ORM(module)

        self.db.add(orm_module)
        self.db.commit()
        self.db.refresh(orm_module)

        # Conversion ORM -> Domain
        return Entity_Converter.ORM_to_Domain(orm_module)
    
    # ========= READ =========
    # By ID
    def find_by_id(self, module_id: int) -> CModule | None:
        orm_module = self.db.get(ORMModule, module_id)

        if not orm_module:
            return None
        
        return Entity_Converter.ORM_to_Domain(orm_module)
    
    # By title
    def find_by_title(self, title: str) -> CModule | None:
        orm_module = self.db.query(ORMModule).filter(ORMModule.title == title).first()

        if orm_module:
            return Entity_Converter.ORM_to_Domain(orm_module)
        
        return None
    
    # Submodules
    def find_submodules(self, parent_id: int) -> List[CModule] | None:
        orm_submodules = self.db.query(ORMModule).filter(ORMModule.parent_id == parent_id).all()
        
        return [Entity_Converter.ORM_to_Domain(orm_sub) for orm_sub in orm_submodules]
        
    # ========= UPDATE =========
    def update(self, module: CModule) -> CModule:
        orm_module = Entity_Converter.Domain_to_ORM(module)

        self.db.commit()
        self.db.refresh(orm_module)

        return Entity_Converter.ORM_to_Domain(orm_module)
    
    # ========= DELETE =========
    def delete_id(self, module_id: int) -> None:
        orm_module = self.db.get(ORMModule, module_id)

        if orm_module:
            self.db.delete(orm_module)
            self.db.commit()

        return None
