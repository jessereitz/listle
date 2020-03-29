import uuid
from datetime import datetime, timezone


class Record:
    _fields = None

    def __init__(self, request):
        self._request = request
        self.charset = self._request.charset
        self.url = self._request.url
        self.headers = self._request.headers
        self.fields = self._request.json
        self.user_agent = self._request.user_agent

        self.datetime = datetime.now(timezone.utc).isoformat()
        self.id = str(uuid.uuid4())

    def __iter__(self):
        yield from self.as_dict().items()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'<Record {self.uuid}>'

    def ua_as_dict(self):
        ua = self._request.user_agent

        d = {
            'string': ua.string,
            'platform': ua.platform,
            'browser': ua.browser,
            'version': ua.version,
            'language': ua.language,
        }

        return d

    def as_dict(self):
        d = {
            'id': self.id,
            'meta': {
                'charset': self.charset,
                'url': self.url,
                'datetime': self.datetime,
                'headers': dict(self.headers),
                'user_agent': self.ua_as_dict(),
            },
            'fields': self.fields,
        }
        return d
