from src.applications.base.application.BoruvkaBaseApplication import BoruvkaBaseApplication
from src.applications.hello.application.BoruvkaHelloApiApplication import BoruvkaHelloApiApplication
from src.applications.auth.application.BoruvkaAuthApiApplication import BoruvkaAuthApiApplication


class BoruvkaDispatcherApiApplication(BoruvkaBaseApplication):
    def _set_routes(self):
        self.mapper.connect(
            'hello',
            '/api/hello{path_info:.*}',
            app=BoruvkaHelloApiApplication,
        )
        self.mapper.connect(
            'auth',
            '/api/auth{path_info:.*}',
            app=BoruvkaAuthApiApplication,
        )

    def _get_route(self, **kwargs):
        match = kwargs['match']
        return match['app'](**self.config)
