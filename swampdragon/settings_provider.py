from tornado.web import RequestHandler
from swampdragon.default_settings import SwampDragonSettings


class SettingsHandler(RequestHandler):
    def set_default_headers(self):
        self.set_header("Content-Type", "application/javascript")

    def get(self, *args, **kwargs):
        protocol = self.request.headers.get('X-Forwarded-Proto', self.request.protocol).lower()

        data = '''window.swampdragon_settings = {settings};
window.swampdragon_host = "{protocol}://{host}:{port}";
'''.format(**{
            'settings': SwampDragonSettings().to_dict(),
            'host': self.request.headers['Host'],
            'port': self.request.headers.get('X-Forwarded-Port', 443 if protocol == 'https' else 80),
            'protocol': protocol,
        })
        self.write(data)
