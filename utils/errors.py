class APIError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code
        self.code = status_code

class TMDbError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code
