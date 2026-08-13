import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.modules.auth.models.permission import Permission  # noqa: F401
from app.shared.database.base import Base

# Association table for the many-to-many relationship between Role and
# Permission. This table has no model class of its own because it carries
# no extra data beyond the two foreign keys — it exists purely to link them.
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
)


class Role(Base):
    """
    Represents a named collection of permissions (e.g. "Admin", "Member").

    Roles are assigned to users within the context of an Organization
    (see OrganizationMember, added in Day 4) — a single user may hold
    different roles in different organizations.
    """

    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    permissions: Mapped[list["Permission"]] = relationship(
        secondary=role_permissions,
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Role name={self.name}>"
