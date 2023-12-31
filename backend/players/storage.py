from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import ConflictError, NotFoundError
from backend.models import Player, Team
from backend.players.schema import PlayerSchema


class Storage():
    name = 'player'

    def add(self, player: PlayerSchema) -> PlayerSchema:
        entity = Player(name=player.name, description=player.description, team_id=player.team_id)

        try:
            db_session.add(entity)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)

        return PlayerSchema(
            uid=entity.uid,
            name=entity.name,
            description=entity.description,
            team_id=entity.team_id,
        )

    def get_all(self) -> list[Player]:
        return Player.query.all()

    def get_by_id(self, uid: int) -> PlayerSchema:
        entity = Player.query.get(uid)

        if not entity:
            raise NotFoundError(self.name, uid)

        return PlayerSchema(
            uid=entity.uid,
            name=entity.name,
            description=entity.description,
            team_id=entity.team_id,
        )

    def update(self, player: PlayerSchema, uid: int) -> PlayerSchema:
        entity = Player.query.get(uid)

        if not entity:
            raise NotFoundError(self.name, uid)

        entity.name = player.name
        entity.description = player.description

        db_session.commit()

        return PlayerSchema(
            uid=entity.uid,
            name=entity.name,
            description=entity.description,
            team_id=entity.team_id,
        )

    def delete(self, uid: int) -> None:
        entity = Player.query.get(uid)

        if not entity:
            raise NotFoundError(self.name, uid)

        db_session.delete(entity)
        db_session.commit()

    def get_for_team(self, uid: int) -> list[Player]:
        team = Team.query.get(uid)

        if not team:
            raise NotFoundError('team', uid)

        return team.players

    def find_by_name(self, player: str) -> list[Player]:
        search = '{player}%'.format(player=player)
        entity = Player.query.filter(Player.name.ilike(search)).all()

        if not entity:
            raise NotFoundError(self.name, player)

        return entity



