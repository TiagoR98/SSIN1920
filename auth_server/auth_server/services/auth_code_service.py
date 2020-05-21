from auth_server.models import AuthorizationCode
from datetime import datetime

class AuthCodeService:

    @staticmethod
    def check_code(code):
        return AuthorizationCode.objects.filter(code=code).filter(expiration__gt=datetime.now()).exists()

    @staticmethod
    def get_scope(code):
        code = AuthorizationCode.objects.get(code=code)
        return code.scope
