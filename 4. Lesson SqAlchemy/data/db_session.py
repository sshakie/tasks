import sqlalchemy
from sqlalchemy.orm import *

SqlAlchemyBase = declarative_base()
_factory = None


def global_init(db_file):
    global _factory
    if _factory:
        return

    if not db_file or not db_file.strip():
        raise Exception('Необходимо указать файл базы данных.')

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    engine = sqlalchemy.create_engine(conn_str, echo=False)
    _factory = sessionmaker(bind=engine)

    from data._all_modules import User, Jobs
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global _factory
    return _factory()
