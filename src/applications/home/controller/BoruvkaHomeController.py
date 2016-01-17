from src.applications.auth.controller.BoruvkaAuthorizedController import BoruvkaAuthorizedController
from src.applications.user.api.BoruvkaUserApi import BoruvkaUserApi
from src.applications.home.view.BoruvkaHomeView import BoruvkaHomeView
from src.applications.setting.query.BoruvkaSettingQuery import BoruvkaSettingQuery
from webob import Response


# Open database connection
class BoruvkaHomeController(BoruvkaAuthorizedController):
    def get(self):
        user_id = self.session['user_id']
        user_api = BoruvkaUserApi(self.dao)
        user = user_api.get_user(id=user_id)

        setting_query = BoruvkaSettingQuery(self.dao)
        user_settings = setting_query.get_user_settings(user_id)
        translation = user_settings['language']
        view = BoruvkaHomeView(translation)

        view.user = user
        view._color = user_settings['color']

        response = Response()
        response.body = view.render()
        return response
