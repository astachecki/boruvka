from src.applications.user.query.BoruvkaUserQuery import BoruvkaUserQuery
from src.applications.auth.query.BoruvkaAuthQuery import BoruvkaAuthQuery
from src.applications.setting.query.BoruvkaSettingQuery import BoruvkaSettingQuery
from src.applications.base.api.BoruvkaBaseApi import (
    BoruvkaBaseApi,
    jsonize,
)
from time import mktime
from datetime import (
    datetime,
    timedelta,
)
import string
import random
from passlib.hash import pbkdf2_sha1


# TODO: do we need to return json as well, or leave it to apicontrollers?
class BoruvkaAuthApi(BoruvkaBaseApi):
    @jsonize
    def register(self, payload):
        username = payload['username']
        password = payload['password']

        hashed_password = self.hash_password(
            username,
            password,
        )

        user_query = BoruvkaUserQuery(self._dao)
        user = user_query.create_user(
            username=username,
            password=hashed_password,
        )

        settings_query = BoruvkaSettingQuery(self._dao)
        settings_query.create_user_settings(
            user_id=user.id,
        )
        return True

    @jsonize
    def login(self, payload):
        username = payload['username']
        password = payload['password']

        hashed_password = self.hash_password(
            username,
            password,
        )

        user_query = BoruvkaUserQuery(self._dao)
        user = user_query.get_user(
            username=username,
            password=hashed_password,
        )

        if not user:
            return None, None

        auth_query = BoruvkaAuthQuery(self._dao)
        if user.tokenId:
            token = auth_query.get_token(
                id=user.tokenId,
            )
            token_date = datetime.utcfromtimestamp(token.expirationDate)
            if token_date > datetime.now():
                return user.id, token.value

        # generate token
        token_value, token_date = self.__generate_token()

        token = auth_query.create_token(
            value=token_value,
            date=token_date,
        )

        user.tokenId = token.id
        self._dao.update(user)

        # api call returns token, whilst webapp sets cookie
        return user.id, token.value

    def verify_token(self, token_value):
        auth_query = BoruvkaAuthQuery(self._dao)
        token = auth_query.get_token(
            value=token_value,
        )
        if token:
            token_date = datetime.utcfromtimestamp(token.expirationDate)
            if token_date > datetime.now():
                # Possibly return authorized user id/name
                return True
        return False

    def invalidate_token(self, token_value):
        auth_query = BoruvkaAuthQuery(self._dao)
        token = auth_query.get_token(
            value=token_value,
        )
        token.expirationDate = 0
        self._dao.update(token)

    @staticmethod
    def hash_password(username, password):
        count = 0
        salt = ''
        for char in username:
            # every second character is added to salt
            if count % 2 == 0:
                salt += char
            count += 1

        salt = bytes(salt)
        hashed_password = pbkdf2_sha1.encrypt(
            password,
            salt=salt,
        )
        return hashed_password

    def __generate_token(self):
        token_value = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))
        token_date = datetime.now() + timedelta(hours=4)
        token_date = int(mktime(token_date.timetuple()))
        return token_value, token_date
