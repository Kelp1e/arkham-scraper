from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from db.setup import get_engine

Base = declarative_base()


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)

    address = Column(String)
    name = Column(String)
    tag = Column(String)
    type = Column(String)
    address_type = Column(String)


if __name__ == '__main__':
    engine = get_engine()
    Base.metadata.create_all(engine)
