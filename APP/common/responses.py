from fastapi import Response


class BadRequest(Response):
    def __init__(self, content=''):
        super().__init__(status_code=400, content=content)


class NotFound(Response):
    def __init__(self, content=''):
        super().__init__(status_code=404, content=content)

# we have HTTPException with status code=401
# class Unauthorized(Response):
#     def __init__(self, content=''):
#         super().__init__(status_code=401, content=content)


class NoContent(Response):
    def __init__(self):
        super().__init__(status_code=204)


class InternalServerError(Response):
    def __init__(self):
        super().__init__(status_code=500)

class Forbidden(Response):
    def __init__(self, content='Not have required permissions to access the resource'):
        super().__init__(status_code=403, content=content)


# 401 - Not provided authentication credentials
# 401 - Not valid authentication credentials
# 403 Not have required permissions to access the resource
