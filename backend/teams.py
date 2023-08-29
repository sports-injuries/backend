from flask import Flask, request
from typing import Any

app = Flask(__name__)

Json = dict[int, Any]

class Storage:
    def __init__(self):
        self.teams: dict[int, Json] = {}
        self.last_uid = 0


    def add(self, team: Json) -> Json:
        self.last_uid += 1
        team['uid'] = self.last_uid
        self.teams[self.last_uid] = team
        return team


    def get_all(self) -> list[Json]:
        return list(self.teams.values())


    def get_by_id(self, uid: int) -> Json:
        return self.teams[uid]


    def update(self, team: Json, uid: int) -> Json:
        self.teams[uid] = team
        return team

    def delete(self, uid: int) -> None:
        self.teams.pop(uid)


storage = Storage()


@app.post('/api/teams/')
def add():
    team = request.json
    return storage.add(team), 201


@app.get('/api/teams/')
def get_all():
    return storage.get_all(), 200


@app.get('/api/teams/<int:uid>')
def get_by_id(uid):
    return storage.get_by_id(uid), 200


@app.put('/api/teams/<int:uid>')
def update(uid):
    team = request.json
    return storage.update(team, uid), 200


@app.delete('/api/teams/<int:uid>')
def delete(uid):
    storage.delete(uid)
    return {}, 204
