from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all ORM models.

    Every table model in the application inherits from this class.
    SQLAlchemy uses it to discover all mapped tables — Alembic later
    reads this same metadata to autogenerate migrations by comparing
    it against the actual database schema.
    """

    pass
