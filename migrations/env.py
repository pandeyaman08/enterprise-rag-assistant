import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from app.core.config import get_settings
from app.modules.auth.models.permission import Permission  # noqa: F401
from app.modules.auth.models.role import Role  # noqa: F401

# Import every model module here so Base.metadata knows about all tables.
# Alembic's autogenerate compares this metadata against the live database.
from app.modules.auth.models.user import User  # noqa: F401
from app.modules.chat.models.chat import Chat  # noqa: F401
from app.modules.chat.models.message import Message  # noqa: F401
from app.modules.documents.models.chunk import Chunk  # noqa: F401
from app.modules.documents.models.document import Document  # noqa: F401
from app.modules.organizations.models.member import OrganizationMember  # noqa: F401
from app.modules.organizations.models.organization import Organization  # noqa: F401
from app.modules.organizations.models.project import Project  # noqa: F401
from app.modules.organizations.models.workspace import Workspace  # noqa: F401
from app.modules.providers.models.provider_config import ProviderConfig  # noqa: F401
from app.shared.database.base import Base
from app.shared.models.audit_log import AuditLog  # noqa: F401

config = context.config
settings = get_settings()

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
