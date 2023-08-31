from typing import Any

from flask import Blueprint, request

from backend.teams.errors import AppError
from backend.teams.schemas import Team
from backend.teams.storage import Storage

team_view = Blueprint('teams', __name__)


storage = Storage()


@team_view.post('/')
def add() -> tuple[dict[str, Any], int]:
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1
    team = Team(**payload)
    team = storage.add(team)
    return team.dict(), 201


@team_view.get('/')
def get_all():
    teams = storage.get_all()
    return [team.dict() for team in teams], 200


@team_view.get('/<int:uid>')
def get_by_id(uid):
    team = storage.get_by_id(uid)
    return team.dict(), 200


@team_view.put('/<int:uid>')
def update(uid):
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    team = Team(**payload)
    team = storage.update(team, uid)
    return team.dict(), 200


@team_view.delete('/<int:uid>')
def delete(uid):
    storage.delete(uid)
    return {}, 204
