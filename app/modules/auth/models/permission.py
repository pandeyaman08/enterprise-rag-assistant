import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base


class Permission(Base):
    """
    Represents a single granular action that can be granted to a role.

    Permissions are intentionally fine-grained (e.g. "document:upload"
    rather than a broad "editor" concept) so that roles can be composed
    flexibly without requiring new permission types for every new role.
    """

    __tablename__ = "permissions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    def __repr__(self) -> str:
        return f"<Permission code={self.code}>"
