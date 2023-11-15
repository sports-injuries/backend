from http import HTTPStatus
from typing import Any

from flask import Blueprint, request

from backend.errors import AppError
from backend.injuries.views import injury_view
from backend.players.schema import PlayerSchema
from backend.players.storage import Storage

player_view = Blueprint('players', __name__)
player_view.register_blueprint(injury_view, url_prefix='')

storage = Storage()


@player_view.post('/')
def add() -> tuple[dict[str, Any], int]:
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1
    player = PlayerSchema(**payload)
    player = storage.add(player)

    return player.dict(), HTTPStatus.CREATED


@player_view.get('/')
def get() -> tuple[list[dict[str, Any]], int]:
    player = request.args.get('name')
    if player:
        entities = storage.find_by_name(player)
        players = [PlayerSchema.from_orm(entity) for entity in entities]
    else:
        entities = storage.get_all()
        players = [PlayerSchema.from_orm(entity) for entity in entities]

    return [player.dict() for player in players], HTTPStatus.OK


@player_view.get('/<int:uid>')
def get_by_id(uid: int) -> tuple[dict[str, Any], int]:
    player = storage.get_by_id(uid)
    return player.dict(), HTTPStatus.OK


@player_view.put('/<int:uid>')
def update(uid: int) -> tuple[dict[str, Any], int]:
    payload = request.json

    if not payload:
        raise AppError('empty payload')

    player = PlayerSchema(**payload)
    player = storage.update(player, uid)

    return player.dict(), 200


@player_view.delete('/<int:uid>')  # type: ignore
def delete(uid: int) -> tuple[dict[None, None], int]:
    storage.delete(uid)
    return {}, 204
