from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

from .base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    profile = relationship("Profile", back_populates="user", uselist=False)
    animals = relationship("Animal", back_populates="user", uselist=True)
