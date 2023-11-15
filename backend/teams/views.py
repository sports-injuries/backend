from http import HTTPStatus
from typing import Any

from flask import Blueprint, request

from backend.errors import AppError
from backend.players.schema import PlayerSchema
from backend.players.storage import Storage as PlayerStorage
from backend.teams.schema import TeamSchema
from backend.teams.storage import Storage as TeamStorage

team_view = Blueprint('teams', __name__)

Team = dict[str, Any]
Player = dict[str, Any]

team_storage = TeamStorage()
player_storage = PlayerStorage()


@team_view.post('/')
def add() -> tuple[Team, int]:
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1
    team = TeamSchema(**payload)
    team = team_storage.add(team)
    return team.dict(), 201


@team_view.get('/')
def get() -> tuple[list[Team], int]:
    name = request.args.get('name')
    if name:
        teams = team_storage.find_by_name(name)
    else:
        teams = team_storage.get_all()

    return [team.dict() for team in teams], 200


@team_view.get('/<int:uid>')
def get_by_id(uid: int) -> tuple[Team, int]:
    team = team_storage.get_by_id(uid)
    return team.dict(), 200


@team_view.get('<int:team_id>/players/')
def get_all_players(team_id: int) -> tuple[list[dict[str, Any]], HTTPStatus]:
    entities = player_storage.get_for_team(team_id)
    players = [PlayerSchema.from_orm(entity) for entity in entities]
    return [player.dict() for player in players], HTTPStatus.OK


@team_view.put('/<int:uid>')
def update(uid: int) -> tuple[Team, int]:
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    team = TeamSchema(**payload)
    team = team_storage.update(team, uid)
    return team.dict(), 200


@team_view.delete('/<int:uid>')  # type: ignore
def delete(uid: int) -> tuple[dict[None, None], int]:
    team_storage.delete(uid)
    return {}, 204
