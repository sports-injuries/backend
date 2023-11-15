from http import HTTPStatus

import orjson
from flask import Blueprint, Response, request

from backend.errors import AppError
from backend.injuries.schema import InjurySchema
from backend.injuries.storage import Storage

injury_view = Blueprint('injuries', __name__)

storage = Storage()


@injury_view.post('/<int:player_id>/injuries/')
def add(player_id: int) -> Response:
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
    return Response(
        response=orjson.dumps(injury.dict()),
        status=HTTPStatus.CREATED,
        content_type='application/json',
    )


@injury_view.get('/<int:player_id>/injuries/')
def get_for_player(player_id: int) -> Response:
    entities = storage.get_for_player(player_id)
    injuries = [InjurySchema.from_orm(entity) for entity in entities]
    return Response(
        response=orjson.dumps([injury.dict() for injury in injuries]),
        status=HTTPStatus.OK,
        content_type='application/json',
    )


@injury_view.delete('/<int:player_id>/injuries/<int:uid>')  # type: ignore
def delete(player_id: int, uid: int) -> tuple[dict[None, None], int]:
    storage.delete(uid)
    return {}, 204
