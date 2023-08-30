from typing import Any

from flask import Flask, request
from pydantic import BaseModel, ValidationError

app = Flask(__name__)


class Team(BaseModel):
    uid: int | None
    name: str
    description: str


class Storage:
    def __init__(self):
        self.teams: dict[int, Team] = {}
        self.last_uid = 0


    def add(self, team: Team) -> Team:
        self.last_uid += 1
        team.uid = self.last_uid
        self.teams[self.last_uid] = team
        return team


    def get_all(self) -> list[Team]:
        return list(self.teams.values())


    def get_by_id(self, uid: int) -> Team:
        return self.teams[uid]


    def update(self, team: Team, uid: int) -> Team:
        self.teams[uid] = team
        return team

    def delete(self, uid: int) -> None:
        self.teams.pop(uid)


storage = Storage()


@app.post('/api/teams/')
def add():
    payload = request.json
    try:
        team = Team(**payload)
    except ValidationError as err:
        return {'error': str(err)}, 400
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
    try:
        team = Team(**payload)
    except ValidationError as err:
        return {'error': str(err)}, 400
    team = storage.update(team, uid)
    return team.dict(), 200


@app.delete('/api/teams/<int:uid>')
def delete(uid):
    storage.delete(uid)
    return {}, 204
