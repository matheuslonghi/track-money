import os

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

_engine: Engine | None = None
_session_local: sessionmaker | None = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        if not os.getenv("DATABASE_URL"):
            raise ValueError("DATABASE_URL environment variable is not set.")
        
        _engine = create_engine(os.getenv("DATABASE_URL"))
    return _engine

def get_session_local() -> sessionmaker:
    global _session_local
    if _session_local is None:
        _session_local = sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine()
        )
    return _session_local

def get_db():
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS authentication"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS movement"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS subscription"))
        conn.commit()

def create_tables():
    engine = get_engine()
    from track_money.app.authentication._user import (
        User,  # noqa: F401 - Import reqquired for SQLAlchemy model discovery
    )
    from track_money.app.movement.bank._bank_account import (
        BankAccount,  # noqa: F401 - Import required for SQLAlchemy model discovery
    )
    from track_money.app.subscription.plan._plan import (
        Plan,  # noqa: F401 - Import required for SQLAlchemy model discovery
    )
    from track_money.app.subscription.user._user import (
        User,  # noqa: F401 - Import required for SQLAlchemy model discovery
    )
    from track_money.app.subscription.user._user_plan import (
        UserPlan,  # noqa: F401 - Import required for SQLAlchemy model discovery
    )

    Base.metadata.create_all(bind=engine) 