import bcrypt
bcrypt.__about__ = bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


def hash(password : str):
    return pwd_context.hash(password)

def verify(plaintext_password : str, hashed_password : str):
    return pwd_context.verify(plaintext_password, hashed_password)