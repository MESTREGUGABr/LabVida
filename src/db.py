from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.config import get_database_url


class Base(DeclarativeBase):
    pass


# pool_pre_ping: descarta conexão morta por timeout do Postgres antes de usá-la,
# em vez de deixar a primeira query da sessão estourar.
# pool_recycle: recicla a conexão antes do limite típico de idle do servidor.
engine = create_engine(get_database_url(), pool_pre_ping=True, pool_recycle=1800)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@contextmanager
def session_scope() -> Iterator[Session]:
    """Sessão de trabalho com rollback garantido.

    Sem o rollback, uma exceção no meio de um service que já deu flush deixava a
    transação suja até o `close()` — a próxima operação na mesma conexão herdava
    o estado abortado. O commit continua sendo responsabilidade do service.
    """
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
