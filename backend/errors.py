class AppError(Exception):
    code = 500

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class NotFoundError(AppError):
    code = 404

    def __init__(self, resource: str, uid: int) -> None:
        super().__init__(f'{resource} [{uid}] not found')
        self.name = resource
        self.uid = uid
