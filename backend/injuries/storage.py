from backend.db import db_session
from backend.errors import NotFoundError
from backend.injuries.schema import InjurySchema
from backend.models import Injury


class Storage:
    def add(self, injury: InjurySchema) -> InjurySchema:
        entity = Injury(name=injury.name, description=injury.description)

        db_session.add(entity)
        db_session.commit()

        return InjurySchema(uid=entity.uid, name=entity.name, description=entity.description)

    def get_all(self) -> list[InjurySchema]:
        entities = Injury.query.all()
        return [
            InjurySchema(uid=entity.uid, name=entity.name, description=entity.description)
            for entity in entities
        ]

    def get_by_id(self, uid: int) -> InjurySchema:
        entity = Injury.query.get(uid)

        if not entity:
            raise NotFoundError('injury', uid)

        return InjurySchema(uid=entity.uid, name=entity.name, description=entity.description)

    def update(self, injury: InjurySchema, uid: int) -> InjurySchema:
        entity = Injury.query.get(uid)

        if not entity:
            raise NotFoundError('injury', uid)

        entity.name = injury.name
        entity.description = injury.description

        db_session.commit()

        return InjurySchema(uid=entity.uid, name=entity.name, description=entity.description)

    def delete(self, uid: int) -> None:
        entity = Injury.query.get(uid)

        if not entity:
            raise NotFoundError('injury', uid)

        db_session.delete(entity)
        db_session.commit()
