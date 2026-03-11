from src.main.domain.models.user import User
from src.main.domain.output_ports.user_ports import UserRepository
from src.main.application.validators.user_validators import UserBasicValidator

from src.main.utils.auth import hash_password, verify_password

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        self.validator = UserBasicValidator(repository)

    # ========= CREATE =========
    def create_user(self, name: str, email: str, password: str) -> User:
        # 1. Check the email
        self.validator.check_unique_email(email)
        
        # 2. Packaging of variables
        hashed_password = hash_password(password)
        user = User(id=0, name=name, email=email, password=hashed_password)

        return self.repository.save(user)
    
    # ========= READ =========
    def find_user_id(self, user_id: int) -> User:
        return self.validator.find_id(user_id)

    # ========= UPDATE =========
    def update_user(self, user_id: int, name: str | None = None, email: str | None = None, password: str | None = None) -> User:
        # 1. Check the user exists
        current_user = self.validator.find_id(user_id)

        # 2. Verify email only when is provided
        if email is not None and email != current_user.email:
            self.validator.check_unique_email(email, exclude_id=user_id)

        # 3. Prepare data to update
        final_name = name if name is not None else current_user.name
        final_email = email if email is not None else current_user.email

        # 4. Handle of the password
        final_password = ""
        if password is not None:
            hashed_password = hash_password(password)
            final_password = hashed_password
        else:
            final_password = current_user.password

        # 5. Packaging of variables
        user_to_update = User(
            id=current_user.id,
            name=final_name,
            email=final_email,
            password=final_password
        )

        return self.repository.update(user_to_update)

    # ========= DELETE =========
    def delete_user(self, user_id: int, password: str) -> None:
        # 1. Check if the user exists
        current_user = self.validator.find_id(user_id)

        # 2. Comparision of password
        verify_password(password, current_user.password)

        return self.repository.delete_id(current_user.id)
