class DRPCGenericError(Exception):
    def __init__(self, message: str = ''):
        super().__init__(message or 'An error has occured during runtime.')


class InvalidID(DRPCGenericError):
    def __init__(self):
        super().__init__('Client ID is Invalid')


class InvalidPipe(DRPCGenericError):
    def __init__(self):
        super().__init__('Pipe Not Found - Is Discord Running?')


class InvalidArgument(DRPCGenericError):
    def __init__(self, expected, received, longdesc: str = None):
        longdesc = '\n{0}'.format(longdesc) if longdesc else ''
        super().__init__('Bad argument passed. Expected {0} but got {1} instead{2}'.format(expected, received, longdesc))


class ServerError(DRPCGenericError):
    def __init__(self, message: str):
        super().__init__(message.replace(']', '').replace('[', '').capitalize())


class DiscordError(DRPCGenericError):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__('Error Code: {0} Message: {1}'.format(code, message))