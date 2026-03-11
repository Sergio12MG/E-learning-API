from datetime import timedelta
from src.main.domain.models.user import User
from src.main.domain.output_ports.user_ports import UserRepository
from src.main.utils.auth import verify_password, create_access_token

class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def authenticate_user(self, email: str, password: str) -> User | None:
        # Verify the user credentials
        user = self.repository.find_by_email(email)

        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        
        return user
    
    def create_token_for_user(self, user: User) -> str:
        # Generate an access token for the user
        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "name": user.name
        }

        access_token = create_access_token(
            data=token_data,
            expires_delta=timedelta(minutes=30)
        )

        return access_token