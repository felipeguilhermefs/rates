class InvalidQueryParam(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

class InvalidContentType(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message