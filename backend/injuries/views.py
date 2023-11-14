from typing import Any

from flask import Blueprint, request

from backend.errors import AppError
from backend.injuries.schema import InjurySchema
from backend.injuries.storage import Storage

injury_view = Blueprint('injuries', __name__)

storage = Storage()


@injury_view.post('/<int:player_id>/injuries/')
def add(player_id: int) -> tuple[dict[str, Any], int]:
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1
    injury = InjurySchema(**payload)
    entity = storage.add(
        injury.name,
        injury.description,
        injury.start_date,
        injury.end_date,
        player_id,
    )
    injury = InjurySchema.from_orm(entity)

    return injury.dict(), 201


@injury_view.get('/<int:player_id>/injuries/')
def get_for_player(player_id: int) -> tuple[list[dict[str, Any]], int]:
    entities = storage.get_for_player(player_id)
    injuries = [InjurySchema.from_orm(entity) for entity in entities]

    return [injury.dict() for injury in injuries], 200


@injury_view.delete('/<int:player_id>/injuries/<int:uid>')  # type: ignore
def delete(player_id: int, uid: int) -> tuple[dict[None, None], int]:
    storage.delete(uid)
    return {}, 204
