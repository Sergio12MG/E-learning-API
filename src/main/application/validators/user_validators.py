from src.main.domain.exceptions import AccessDenied_Error, User_EmailRepeated_Error, User_NotFound_Error
from src.main.domain.output_ports.user_ports import UserRepository

class UserBasicValidator:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def find_id(self, user_id: int):
        user = self.repository.find_by_id(user_id)

        if user is None:
            raise User_NotFound_Error(f"No existe un usuario con el ID {user_id}.")
        
        return user

    def check_unique_email(self, email: str, exclude_id: int | None = None):
        current_user = self.repository.find_by_email(email)

        if current_user:
            # Si es el mismo usuario que se está actualizando, permitir
            if exclude_id and current_user.id == exclude_id:
                return
            # Lanzar excepción correctamente
            raise User_EmailRepeated_Error(f"El email {email} ya está registrado")
        
        return
    
    def check_course_owner(self, user_id: int, course_owner_id: int):
        current_user = self.repository.find_by_id(user_id)

        if course_owner_id != current_user.id:
            raise AccessDenied_Error(f"Este curso pertenece a otro usuario.")
        
        return
