from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.db import Base, engine


class Team(Base):
    __tablename__ = 'teams'

    uid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)

    players = relationship('Player')


class Player(Base):
    __tablename__ = 'players'

    uid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    team_id = Column(Integer, ForeignKey('teams.uid'), nullable=False)


class Injury(Base):
    __tablename__ = 'injuries'

    uid = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
