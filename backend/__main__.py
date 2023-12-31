import logging

from flask import Flask
from pydantic import ValidationError

from backend.db import db_session
from backend.errors import AppError
from backend.players.views import player_view
from backend.teams.views import team_view

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def shutdown_session(exception=None):
    db_session.remove()


def handle_app_error(error: AppError) -> tuple[dict[str, str], int]:
    return {'error': str(error)}, error.code


def handle_validation_error(error: ValidationError) -> tuple[dict[str, str], int]:
    return {'error': str(error)}, 422


app.register_error_handler(AppError, handle_app_error)
app.register_error_handler(ValidationError, handle_validation_error)

app.register_blueprint(team_view, url_prefix='/api/v1/teams')
app.register_blueprint(player_view, url_prefix='/api/v1/players')

app.teardown_appcontext(shutdown_session)


def main() -> None:
    logger.info('Run')
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
