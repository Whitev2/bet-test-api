from passlib.context import CryptContext
from cryptography.fernet import Fernet
from pydantic.main import BaseModel

from src.config import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class VerifiOut(BaseModel):
    email: str
    user_id: str
    site_role: str


class Security:

    @classmethod
    def hash_password(cls, password: str) -> str:
        return pwd_context.hash(password)

    @classmethod
    def verify_password(cls, password: str, hash_str: str) -> bool:
        return pwd_context.verify(password, hash_str)
