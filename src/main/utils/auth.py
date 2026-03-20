import os
from typing import Optional
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import jwt, JWTError
import bcrypt

load_dotenv()

# BASE CONFIG
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ---------- Password helpers ----------
# Check that the password is no longer than 72 bytes
def _ensure_bcrypt_safe(password: str) -> None:
    b = password.encode("utf-8")

    if len(b) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña es demasiado larga (más de 72 bytes). Usa una contraseña más corta (<= 64 caracteres)."
        )

def hash_password(password: str) -> str:
    try:
        _ensure_bcrypt_safe(password)
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed.decode("utf-8")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña excede el límite seguro de longitud."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar la contraseña."
        )

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except Exception:
        return False


# ---------- JWT helpers ----------
# Generate a token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # 1. Copy the credential ('data' param) to avoid modifying the originals
    to_encode = data.copy()

    # 2. Add the expiration date
    if expires_delta:
        # Use the provided deadline
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Use the default expiration time
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 3. Assing the expiration time to the token
    to_encode.update({"exp": expire})

    # 4. Convert the credential into a token and sign it with the secret key
    token = jwt.encode(to_encode, str(SECRET_KEY), algorithm=ALGORITHM)

    return token

# Decode a token
def decode_token(token: str) -> dict | None:
    try:
        # Extract the credential from the token, verifying the secret key
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise None
    
