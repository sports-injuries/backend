from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
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
    injuries = relationship('Injury')


class Injury(Base):
    __tablename__ = 'injuries'

    uid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))

    player_id = Column(Integer, ForeignKey('players.uid'), nullable=False)


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
