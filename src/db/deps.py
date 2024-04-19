import logging
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.db.base import Base

logger = logging.getLogger(__name__)

here = Path(__name__).resolve().parent
sqlite_db_path = f'{here}/db.db'
db_url: str = f'sqlite:///{sqlite_db_path}'

engine = create_engine(db_url)
maker = sessionmaker(bind=engine)


def init_db():
    if os.path.exists(sqlite_db_path):
        os.remove(sqlite_db_path)

    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db_session_context() -> Iterator[Session]:
    db_session = maker()
    try:
        yield db_session
    except Exception as e:
        db_session.rollback()
        logger.error(str(e))
        logger.warning('rollback db session')
        raise e
    finally:
        db_session.close()
