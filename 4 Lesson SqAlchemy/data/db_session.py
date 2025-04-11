import sqlalchemy
from sqlalchemy.orm import declarative_base, Session, sessionmaker

SqlAlchemyBase = declarative_base()
__factory = None


def global_init(db_file):
    global __factory
    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception('Необходимо указать файл базы данных.')

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'

    engine = sqlalchemy.create_engine(conn_str, echo=False)
    __factory = sessionmaker(bind=engine)

    from data.__all_models import User, Jobs, Departament
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
