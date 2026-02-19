from __future__ import annotations
from datetime import UTC, datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class User(Base):
    # we are creating a "user" model
    __tablename__ = "users" # tells sqlalchemy name of the table

    # Mapped[int] is a type hint for our IDE and mapped_column defines the actual column
    # username and email should be unique for each user
    # nullable = False means it cannot be null
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
        default=None,
    )

    # The "Post" inside list is the class "Post" defined below
    posts: Mapped[list[Post]] = relationship(back_populates="author")


    @property   
    def image_path(self) -> str:
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"
    
class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text,  nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False,
        index=True,
        # Primary keys get indexes automatically, but for foreign keys we need to set the index so that querying is faster; the tradeoff here is the writes will be slightly slower but the retreival will be faster
    )
    date_posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    author: Mapped[User] = relationship(back_populates="posts")

