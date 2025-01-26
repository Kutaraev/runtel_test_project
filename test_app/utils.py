import db


from passlib.context import CryptContext
from sqlalchemy import select
from test_app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
