from sqlalchemy.orm import Session

from src.main.domain.models.user import User
from src.main.domain.output_ports.user_ports import UserRepository
from src.main.infraestructure.db.models.User import User as ORMUser

class Entity_Converter:
    @staticmethod
    def Domain_to_ORM(domain: User) -> ORMUser:
        return ORMUser(
            name=domain.name,
            email=domain.email,
            password=domain.password
        )
    
    @staticmethod
    def ORM_to_Domain(orm: ORMUser) -> User:
        return User(
            id=orm.id,
            name=orm.name,
            email=orm.email,
            password=orm.password
        )

class SQLAlchemy_UserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    # ========= CREATE =========
    def save(self, user: User) -> User:
        # Conversion Domain -> ORM
        orm_user = Entity_Converter.Domain_to_ORM(user)

        self.db.add(orm_user)
        self.db.commit()
        self.db.refresh(orm_user)

        # Conversion ORM -> Domain        
        return Entity_Converter.ORM_to_Domain(orm_user)
    
    # ========= READ =========
    def find_by_id(self, user_id: int) -> User | None:
        orm_user = self.db.get(ORMUser, user_id)

        if not orm_user:
            return None
        
        return Entity_Converter.ORM_to_Domain(orm_user)
    
    def find_by_email(self, email: str) -> User | None:
        orm_user = self.db.query(ORMUser).filter(ORMUser.email == email).first()

        if orm_user:
            return Entity_Converter.ORM_to_Domain(orm_user)
        
        return None
    
    # ========= UPDATE =========
    def update(self, user: User) -> User:
        # 1. Get the current user from the DB
        orm_user = self.db.get(ORMUser, user.id)

        # 2. Update attributes on the persistent instance
        orm_user.name = user.name
        orm_user.email = user.email
        if user.password:
            orm_user.password = user.password

        self.db.commit()
        self.db.refresh(orm_user)

        # Conversion ORM -> Domain       
        return Entity_Converter
    
    # ========= DELETE =========
    def delete_id(self, user_id: int) -> None:
        orm_user = self.db.get(ORMUser, user_id)

        if orm_user:
            self.db.delete(orm_user)
            self.db.commit()

        return None
