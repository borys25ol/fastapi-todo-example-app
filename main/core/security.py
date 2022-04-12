import base64

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """
    Convert user password to hash string.
    """
    return pwd_context.hash(secret=password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check if the user password from request is valid.
    """
    return pwd_context.verify(secret=plain_password, hash=hashed_password)


def get_basic_auth_token(username: str, password: str) -> str:
    """
    Return base64 auth token.
    """
    return base64.b64encode(s=f"{username}:{password}".encode()).decode()
