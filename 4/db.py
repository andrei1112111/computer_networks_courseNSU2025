import atexit
from typing import Optional

from sqlalchemy import Connection, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, TEXT, JSON
from sqlalchemy.dialects.postgresql import insert as insert

engine = create_engine(
    "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        "andrejalekseevic",
        "",
        "localhost",
        5432,
        "andrejalekseevic",
    ),
    pool_size=5,
    max_overflow=10,
    echo=False,
    pool_logging_name="engine",
    logging_name="engine",
)

conn: Optional[Connection] = None

Session = sessionmaker(bind=engine)
session = Session()
atexit.register(session.close)

Base = declarative_base()


def connect_db():
    engine.connect()
    Base.metadata.create_all(engine)


def disconnect_db():
    if conn is not None:
        conn.close()


connect_db()
atexit.register(disconnect_db)


class StackOverflowDB(Base):
    __tablename__ = "stackoverflow"

    url = Column(TEXT, primary_key=True)
    data = Column(JSON)


def insertDB(url, data):
    record = insert(StackOverflowDB).values(url=url, data=data).on_conflict_do_update(
        index_elements=["url"],
        set_={"data": data}
    )
    session.execute(record)
    session.commit()


def getDB(url):
    return session.query(StackOverflowDB).filter_by(url=url).first()
