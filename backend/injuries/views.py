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

    return entity.dict(), 201


@injury_view.get('/')
def get_all() -> tuple[list[dict[str, Any]], int]:
    injuries = storage.get_all()
    return [injury.dict() for injury in injuries], 200


@injury_view.get('/<int:uid>')
def get_by_id(uid: int) -> tuple[dict[str, Any], int]:
    injury = storage.get_by_id(uid)
    return injury.dict(), 200


@injury_view.put('/<int:uid>')
def update(uid: int) -> tuple[dict[str, Any], int]:
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    injury = InjurySchema(**payload)
    injury = storage.update(injury, uid)

    return injury.dict(), 200


@injury_view.delete('/<int:uid>')  # type: ignore
def delete(uid: int) -> tuple[dict[None, None], int]:
    storage.delete(uid)
    return {}, 204
