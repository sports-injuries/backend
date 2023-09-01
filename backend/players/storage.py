from backend.db import db_session
from backend.errors import NotFoundError
from backend.models import Player
from backend.players.schema import PlayerSchema


class Storage():
    def add(self, player: PlayerSchema) -> PlayerSchema:
        entity = Player(name=player.name, description=player.description)

        db_session.add(entity)
        db_session.commit()

        return PlayerSchema(uid=entity.uid, name=entity.name, description=entity.description)

    def get_all(self) -> list[PlayerSchema]:
        entities = Player.query.all()
        return [
            PlayerSchema(uid=entity.uid, name=entity.name, description=entity.description)
            for entity in entities
        ]

    def get_by_id(self, uid: int) -> PlayerSchema:
        entity = Player.query.get(uid)

        if not entity:
            raise NotFoundError('player', uid)

        return PlayerSchema(uid=entity.uid, name=entity.name, description=entity.description)

    def update(self, player: PlayerSchema, uid: int) -> PlayerSchema:
        entity = Player.query.get(uid)

        if not entity:
            raise NotFoundError('player', uid)

        entity.name = player.name
        entity.description = player.description

        db_session.commit()

        return PlayerSchema(uid=entity.uid, name=entity.name, description=entity.description)

    def delete(self, uid: int) -> None:
        entity = Player.query.get(uid)

        if not entity:
            raise NotFoundError('player', uid)

        db_session.delete(entity)
        db_session.commit()
