from backend.teams.errors import AppError
import logging


from backend.teams.views import app
from pydantic import ValidationError


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_app_error(e: AppError) -> dict[str, str]:
    return {'error': str(e)}, e.code


def handle_validation_error(e: ValidationError) -> dict[str, str]:
    return {'error': str(e)}, 422


app.register_error_handler(AppError, handle_app_error)
app.register_error_handler(ValidationError, handle_validation_error)


def main():
    logger.info('hello world')
    app.run()


if __name__ == '__main__':
    main()
