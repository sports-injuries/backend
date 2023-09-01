from sqlalchemy import Column, ForeignKey, Integer, String

from backend.db import Base, engine


class Team(Base):
    __tablename__ = 'teams'

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


class Player(Base):
    __tablename__ = 'players'

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    team_uid = Column(Integer, ForeignKey('teams.uid'))


class Injury(Base):
    __tablename__ = 'injuries'

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
