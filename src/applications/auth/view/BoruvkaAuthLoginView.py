from src.applications.base.view.BoruvkaBaseView import BoruvkaBaseView


class BoruvkaAuthLoginView(BoruvkaBaseView):
    __template = 'webroot/html/BoruvkaAuthLoginTemplate.tmpl'

    def __init__(self, translation=None):
        BoruvkaBaseView.__init__(
            self,
            self.__template,
            translation,
        )

        self.login = "Login"
        self.register = "Register"
        self.username = "Username"
        self.password = "Password"
        self.error = None
