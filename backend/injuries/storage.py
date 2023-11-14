from datetime import datetime

from sqlalchemy.exc import IntegrityError

from backend.db import db_session
from backend.errors import ConflictError, NotFoundError
from backend.models import Injury, Player


class Storage:
    name = 'injuries'

    def add(
        self,
        name: str,
        description: str | None,
        start_date: datetime,
        end_date: datetime | None,
        player_id: int,
    ) -> Injury:
        entity = Injury(
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            player_id=player_id,
        )

        try:
            db_session.add(entity)
            db_session.commit()
        except IntegrityError:
            raise ConflictError(self.name)

        return entity

    def get_for_player(self, player_id: int) -> list[Injury]:
        player = Player.query.get(player_id)

        if not player:
            raise NotFoundError('injury', player_id)

        return player.injuries

    def delete(self, uid: int) -> None:
        entity = Injury.query.get(uid)

        if not entity:
            raise NotFoundError('injury', uid)

        db_session.delete(entity)
        db_session.commit()
