from typing import Any

from flask import Blueprint, request

from backend.errors import AppError
from backend.teams.schema import TeamSchema
from backend.teams.storage import Storage

team_view = Blueprint('teams', __name__)

Team = dict[str, Any]

storage = Storage()


@team_view.post('/')
def add() -> tuple[Team, int]:
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1
    team = TeamSchema(**payload)
    team = storage.add(team)
    return team.dict(), 201


@team_view.get('/')
def get_all() -> tuple[list[Team], int]:
    teams = storage.get_all()
    return [team.dict() for team in teams], 200


@team_view.get('/<int:uid>')
def get_by_id(uid: int) -> tuple[Team, int]:
    team = storage.get_by_id(uid)
    return team.dict(), 200


@team_view.put('/<int:uid>')
def update(uid: int) -> tuple[Team, int]:
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    team = TeamSchema(**payload)
    team = storage.update(team, uid)
    return team.dict(), 200


@team_view.delete('/<int:uid>')  # type: ignore
def delete(uid: int) -> tuple[dict[None, None], int]:
    storage.delete(uid)
    return {}, 204
