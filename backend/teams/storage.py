from backend.teams.schemas import Team as TeamSchemas
from backend.teams.errors import NotFoundError
from models import Team
from db import db_session


class Storage:
    def __init__(self) -> None:
        self.teams: dict[int, TeamSchemas] = {}
        self.last_uid = 0


    def add(self, team: TeamSchemas) -> TeamSchemas:
        self.last_uid +=1
        team = Team(name=team.name, description=team.description)
        db_session.add(team)
        db_session.commit()
        team = Team.query.filter(Team.uid==self.last_uid)
        team = TeamSchemas(uid=team.uid, name=team.name, description=team.description)
        return team

        # self.last_uid += 1
        # team.uid = self.last_uid
        # self.teams[self.last_uid] = team
        # return team


    def get_all(self) -> list[TeamSchemas]:
        return list(self.teams.values())


    def get_by_id(self, uid: int) -> TeamSchemas:
        if uid not in self.teams:
            raise NotFoundError('team', uid)
        return self.teams[uid]


    def update(self, team: TeamSchemas, uid: int) -> TeamSchemas:
        if uid not in self.teams:
            raise NotFoundError('team', uid)

        self.teams[uid] = team
        return team

    def delete(self, uid: int) -> None:
        if uid not in self.teams:
            raise NotFoundError('team', uid)
        self.teams.pop(uid)
