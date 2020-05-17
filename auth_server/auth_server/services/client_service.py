from auth_server.models import Client
from django.contrib.auth import authenticate

class ClientService:

    @staticmethod
    def add_credentials(client_id, client_secret):
        client = Client.objects.create_user(username=client_id, password=client_secret)
        client.save()

    @staticmethod
    def check_credentials(client_id, client_secret):
        return authenticate(username=client_id, password=client_secret) is not None

    @staticmethod
    def get_client(client_id):
        return Client.objects.get(username = client_id)