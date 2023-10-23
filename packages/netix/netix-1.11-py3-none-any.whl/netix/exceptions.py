class NetixException(Exception):
    message = 'NetixException'

    def __init__(self, *args):
        self.args = args

    def __str__(self):
        if self.args:
            return ' '.join(self.args)

        return self.message


class ASGIException(NetixException):
    message = 'ASGIException'


class LifespanError(ASGIException):
    pass


class LifespanProtocolUnsupported(ASGIException):
    message = 'ASGI Lifespan Protocol is not supported by your application'
