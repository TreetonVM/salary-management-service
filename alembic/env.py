import os
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncConnection
from alembic import context
from dotenv import load_dotenv
from app.database import engine

# Load environment variables from .env file
load_dotenv()

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
# from app.models import Base
# target_metadata = Base.metadata
target_metadata = None  # Update this with the actual metadata object

# Ensure DATABASE_URL is not None
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set")

# Set the SQLAlchemy URL from the environment variable
config.set_main_option("sqlalchemy.url", database_url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    Configures the context with just a URL and not an Engine, though an Engine is acceptable here as well.
    By skipping the Engine creation we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the script output.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    Creates an Engine and associates a connection with the context.
    """
    connectable = engine

    async def do_run_migrations(connection: AsyncConnection) -> None:
        context.configure(connection=connection, target_metadata=target_metadata)  # type: ignore

        async with connection.begin():
            context.run_migrations()

    async with connectable.connect() as connection:
        await do_run_migrations(connection)


# Choose between offline and online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())
