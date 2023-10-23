from .http_exception import (
     ExpectationFailed, InternalServerError
)
from .response import Response

KEEPALIVE_OR_CLOSE = {
    True: b'keep-alive',
    False: b'close'
}
KEEPALIVE_OR_UPGRADE = {
    False: b'keep-alive',
    True: b'upgrade'
}


class HTTPResponse(Response):
    __slots__ = ('header',
                 'http_chunked',
                 '_request',
                 '_status',
                 '_content_type')

    def __init__(self, request):
        super().__init__(request)

        self.header = [b'', bytearray()]
        self.http_chunked = False

        self._request = request
        self._status = []
        self._content_type = []

    def headers_sent(self, sent=False):
        if sent:
            self.header = None

        return self.header is None

    def append_header(self, value):
        self.header[1].extend(value)

    def set_header(self, name, value=''):
        if isinstance(name, str):
            name = name.encode('latin-1')

        if isinstance(value, str):
            value = value.encode('latin-1')

        if b'\n' in name or b'\n' in value:
            raise InternalServerError

        self.header[1].extend(b'%s: %s\r\n' % (name, value))

    def set_status(self, status=200, message=b'OK'):
        if isinstance(message, str):
            message = message.encode('latin-1')

        if not isinstance(status, int) or b'\n' in message:
            raise InternalServerError

        self._status.append((status, message))

    def get_status(self):
        if self._status:
            status_tuple = self._status.pop()
            status_code, status_message = status_tuple
            return (status_code, status_message)
        else:
            return (200, b'OK')

    def set_content_type(self, content_type=b'application/json'):
        if isinstance(content_type, str):
            content_type = content_type.encode('latin-1')

        if b'\n' in content_type:
            raise InternalServerError

        self._content_type.append(content_type)

    def get_content_type(self):
        try:
            return self._content_type.pop()
        except IndexError:
            return b''

    def close(self, keepalive=False):
        if not keepalive:
            # this will force the TCP connection to be terminated
            self._request.http_keepalive = False

        super().close()

    async def send_continue(self):
        if self._request.http_continue:
            if (self._request.content_length >
                    self._request.protocol.options['client_max_body_size']):
                raise ExpectationFailed

            await self.send(
                b'HTTP/%s 100 Continue\r\n\r\n' % self._request.version,
                throttle=False
            )
            self.close(keepalive=True)

    async def end(self, data=b'', **kwargs):
        if self.headers_sent():
            await self.write(data, throttle=False)
        else:
            status = self.get_status()
            content_length = len(data)

            if content_length > 0 and (
                        self._request.method == b'HEAD' or
                        status[0] in (204, 205, 304) or 100 <= status[0] < 200
                    ):
                data = b''

            await self.send(
                b'HTTP/%s %d %s\r\nContent-Type: %s\r\nContent-Length: %d\r\n'
                b'Connection: %s\r\n%s\r\n%s' % (
                    self._request.version,
                    *status,
                    content_length,
                    KEEPALIVE_OR_CLOSE[self._request.http_keepalive],
                    self.header[1],
                    data), throttle=False, **kwargs
            )

            self.headers_sent(True)

        self.close(keepalive=True)

    async def write(self, data, buffer_size=16 * 1024, **kwargs):
        kwargs['buffer_size'] = buffer_size

        if not self.headers_sent():
            if self.header[0] == b'':
                status = self.get_status()
                no_content = (status[0] in (204, 205, 304) or
                              100 <= status[0] < 200)
                chunked = kwargs.get('chunked')

                if chunked is None:
                    self.http_chunked = (self._request.version == b'1.1' and
                                         self._request.http_keepalive and
                                         not no_content)
                else:
                    self.http_chunked = chunked

                if self.http_chunked:
                    self.append_header(b'Transfer-Encoding: chunked\r\n')

                self.header[0] = b'HTTP/%s %d %s\r\n' % (
                    self._request.version, *status)

                if no_content and status[0] not in (101, 426):
                    self.append_header(b'Connection: close\r\n\r\n')
                else:
                    if chunked is None and not self.http_chunked and not (
                            self._request.version == b'1.1' and (
                                status[0] in (101, 426) or
                                b'range' in self._request.headers)):
                        self._request.http_keepalive = False

                    if status[0] == 101:
                        self._request.upgraded = True

                    self.append_header(
                        b'Connection: %s\r\n\r\n' % KEEPALIVE_OR_UPGRADE[
                            status[0] in (101, 426)]
                    )

                if self._request.method == b'HEAD' or no_content:
                    if status[0] not in (101, 426):
                        self._request.http_keepalive = False

                    data = None
                else:
                    self._request.protocol.set_watermarks(
                        high=buffer_size * 4,
                        low=kwargs.get('buffer_min_size', buffer_size // 2)
                    )

            header = b''.join(self.header)

            await self.send(header, throttle=False)
            self.headers_sent(True)

        if (self.http_chunked and not self._request.upgraded and
                data is not None):
            await self.send(b'%X\r\n%s\r\n' % (len(data), data), **kwargs)
        else:
            await self.send(data, **kwargs)