class Unauthorized(Exception):
    def __init__(self, message="[Error]: Unauthorized"):
        self.message = message
        super().__init__(self.message)

class ExpiredIn(Exception):
    def __init__(self, message="[Error]: ExpiredIn must be at least 60 seconds!"):
        self.message = message
        super().__init__(self.message)


def check_exceptions(code=0):
    if int(code) == 401:
        raise Unauthorized
    elif int(code) == 60:
        raise ExpiredIn
