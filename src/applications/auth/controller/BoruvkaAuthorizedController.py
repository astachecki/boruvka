from src.applications.base.controller.BoruvkaBaseController import BoruvkaBaseController
from src.applications.auth.api.BoruvkaAuthApi import BoruvkaAuthApi

from webob import exc, Response


class BoruvkaAuthorizedController(BoruvkaBaseController):
    def __before__(self):
        # One might be authorized either via session (web) or Token (api)
        if self.request.path.startswith("/api"):
            authorization_header = self.request.authorization
            if authorization_header is None:
                # Return unauthorized
                return exc.HTTPUnauthorized()
            elif len(authorization_header) > 1 and authorization_header[0] == 'Token':
                return self.__verify_token(authorization_header[1])
            else:
                return exc.HTTPUnauthorized()
        elif 'user_id' in self.session:
            return Response()
        else:
            return self.__authorize()

    def __authorize(self):
        response = exc.HTTPMovedPermanently(location='/auth/login')
        return response

    def __verify_token(self, token):
        api = BoruvkaAuthApi(self.dao)
        token_valid = api.verify_token(token)
        if token_valid:
            return Response()
        return exc.HTTPUnauthorized()
