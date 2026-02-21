
from sqlmodel import SQLModel, create_engine
from .config import settings

# Create engine lazily - don't connect until actually used
engine = create_engine(str(settings.DATABASE_URL), echo=False, pool_pre_ping=True)


def init_db() -> None:
    # minimal: create tables automatically (later we'll switch to Alembic migrations)
    SQLModel.metadata.create_all(engine)