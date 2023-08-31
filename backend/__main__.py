import logging

from flask import Flask
from pydantic import ValidationError

from backend.teams.errors import AppError
from backend.teams.views import team_view

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_app_error(error: AppError) -> tuple[dict[str, str], int]:
    return {'error': str(error)}, error.code


def handle_validation_error(error: ValidationError) -> tuple[dict[str, str], int]:
    return {'error': str(error)}, 422


app.register_error_handler(AppError, handle_app_error)
app.register_error_handler(ValidationError, handle_validation_error)
app.register_blueprint(team_view, url_prefix='/api/v1/teams')


def main() -> None:
    logger.info('hello world')
    app.run()


if __name__ == '__main__':
    main()
