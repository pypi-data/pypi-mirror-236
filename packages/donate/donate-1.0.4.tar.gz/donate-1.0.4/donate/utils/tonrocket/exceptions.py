class Unauthorized(Exception):
    def __init__(self, message="[Error]: Unauthorized"):
        self.message = message
        super().__init__(self.message)


def check_exceptions(code=0):
    if int(code) == 401:
        raise Unauthorized