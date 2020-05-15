from auth_server.models import User


class LoginService:

    @staticmethod
    def add_credentials(username, password):
        new_user = User(username=username, password=password)
        new_user.save()

    @staticmethod
    def check_credentials(username, password):
        return User.objects.filter(username=username, password=password).exists()
