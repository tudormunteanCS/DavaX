from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "sqlite:///./db/identifier.sqlite"
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
