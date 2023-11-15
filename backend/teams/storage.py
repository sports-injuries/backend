from backend.db import db_session
from backend.errors import NotFoundError
from backend.models import Team
from backend.teams.schema import TeamSchema


class Storage:
    def add(self, team: TeamSchema) -> TeamSchema:
        entity = Team(name=team.name, description=team.description)

        db_session.add(entity)
        db_session.commit()

        return TeamSchema(uid=entity.uid, name=entity.name, description=entity.description)

    def get_all(self) -> list[TeamSchema]:
        entities = Team.query.all()
        return [
            TeamSchema(uid=entity.uid, name=entity.name, description=entity.description)
            for entity in entities
        ]

    def get_by_id(self, uid: int) -> TeamSchema:
        entity = Team.query.get(uid)

        if not entity:
            raise NotFoundError('team', uid)

        return TeamSchema(uid=entity.uid, name=entity.name, description=entity.description)

    def find_by_name(self, name: str) -> list[TeamSchema]:
        search = '%{name}%'.format(name=name)
        entities = Team.query.filter(
            Team.name.ilike(search),
        ).all()

        return [
            TeamSchema(uid=entity.uid, name=entity.name, description=entity.description)
            for entity in entities
        ]

    def update(self, team: TeamSchema, uid: int) -> TeamSchema:
        entity = Team.query.get(uid)

        if not entity:
            raise NotFoundError('team', uid)

        entity.name = team.name
        entity.description = team.description

        db_session.commit()

        return TeamSchema(uid=entity.uid, name=entity.name, description=entity.description)

    def delete(self, uid: int) -> None:
        entity = Team.query.get(uid)

        if not entity:
            raise NotFoundError('team', uid)

        db_session.delete(entity)
        db_session.commit()
