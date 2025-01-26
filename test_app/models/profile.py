from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Profile(Base):
    __tablename__ = "profiles"
    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str]
    lastname: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="profile", uselist=False)
