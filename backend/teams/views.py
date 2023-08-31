from flask import Flask, request
from pydantic import ValidationError
from backend.teams.schemas import Team
from backend.teams.storage import Storage
from backend.teams.errors import AppError
from typing import Any


app = Flask(__name__)


storage = Storage()


@app.post('/api/teams/')
def add() -> tuple[dict[str, Any], int]:
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    payload['uid'] = -1
    team = Team(**payload)
    team =  storage.add(team)
    return team.dict(), 201


@app.get('/api/teams/')
def get_all():
    teams = storage.get_all()
    return [team.dict() for team in teams], 200


@app.get('/api/teams/<int:uid>')
def get_by_id(uid):
    team = storage.get_by_id(uid)
    return team.dict(), 200


@app.put('/api/teams/<int:uid>')
def update(uid):
    payload = request.json
    if not payload:
        raise AppError('empty payload')

    team = Team(**payload)
    team = storage.update(team, uid)
    return team.dict(), 200


@app.delete('/api/teams/<int:uid>')
def delete(uid):
    storage.delete(uid)
    return {}, 204
