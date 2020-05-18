import random
import string
import datetime

from collections import Counter
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from django.shortcuts import render, redirect

from auth_server.services.login_service import LoginService
from auth_server.services.client_service import ClientService
from auth_server.services.auth_code_service import AuthCodeService
from auth_server.services.token_service import TokenService
from auth_server.models import AuthorizationCode

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

logs = [
    "Auth server service initiated.",
]

class AuthorizationView(APIView):

    scopes = ["read","write","delete"]

    def get(self, request):
        updateLogs("[GET] "+request.path)

        if not AuthorizationView.validate_authorization_request(request):
            updateLogs("Invalid authorization request")
            return redirect("{}?error={}".format(request.GET['redirect_uri'], "invalid_request"))

        received_scopes = request.GET['scope'].split(" ")
        received_scopes = received_scopes[:-1]

        if not all(elem in AuthorizationView.scopes  for elem in received_scopes) or len(received_scopes) == 0:
            updateLogs("Invalid scope")
            return redirect("{}?error={}".format(request.GET['redirect_uri'], "invalid_scope"))

        if request.GET['response_type'] != "code":
            updateLogs("Unsupported response type")
            return redirect("{}?error={}".format(request.GET['redirect_uri'], "unsupported_response_type"))

        return render(request, 'authorize.html', {'client_id': request.GET['client_id'],
                                                  'redirect_uri': request.GET['redirect_uri'],
                                                  'scope': request.GET['scope'],
                                                  'scope_list': received_scopes,
                                                  'state': request.GET['state']})


    def post(self, request):
        updateLogs("[POST] "+request.path)

        if LoginService.check_credentials(request.POST['username'], request.POST['password']):
            updateLogs("User credentials are valid")
            
            code = AuthorizationView.generate_authorization_code(request.GET['client_id'], request.GET['redirect_uri'], request.GET['scope'])

            updateLogs("Auth code generated: "+code)

            return redirect("{}?code={}&state={}".format(request.GET['redirect_uri'], code, request.GET['state']))
        else:
            updateLogs("Invalid User credentials")

            return redirect("{}?error={}".format(request.GET['redirect_uri'], "access_denied"))


    @staticmethod
    def generate_authorization_code(client_id, redirect_uri, scope):
        lettersAndDigits = string.ascii_letters + string.digits
        code = ''.join((random.choice(lettersAndDigits) for i in range(15)))
        now = datetime.datetime.now()
        expiration = now + datetime.timedelta(minutes=10)
        new_code = AuthorizationCode(code=code, client_id=client_id, scope=scope, redirect_uri=redirect_uri,expiration=expiration)
        new_code.save()

        return new_code.code


    @staticmethod
    def validate_authorization_request(request):
        if 'response_type' not in request.GET:
           return False

        if 'client_id' not in request.GET:
           return False

        if 'redirect_uri' not in request.GET:
           return False

        if 'scope' not in request.GET:
           return False

        if 'state' not in request.GET:
           return False

        return True

class AddAccountView(APIView):

    def post(self, request):
        updateLogs("[POST] "+request.path)

        LoginService.add_credentials(request.POST['username'], request.POST['password'])
        updateLogs("User "+request.POST['username']+" created")

        return HttpResponse(status=204)

class AddClientView(APIView):

    def post(self, request):
        updateLogs("[POST] "+request.path)

        ClientService.add_credentials(request.POST['id'], request.POST['secret'])
        updateLogs("Client "+request.POST['id']+" created")

        return HttpResponse(status=204)

class GenerateTokenView(APIView):

    def post(self, request):
        updateLogs("[POST] "+request.path)

        client_id = request.POST['client_id']
        client_secret = request.POST['client_secret']
        code = request.POST['code']
        redirect_uri = request.POST['redirect_uri']

        if not ClientService.check_credentials(client_id, client_secret):
            updateLogs("Invalid Client credentials")
            return redirect("{}?error={}".format(redirect_uri, "invalid_client_credentials"))

        if not AuthCodeService.check_code(code):
            updateLogs("Invalid auth code")
            return redirect("{}?error={}".format(redirect_uri, "invalid_auth_code"))

        client = ClientService.get_client(client_id)
        
        token = TokenService.add_token(client)
        updateLogs("New token created: "+token.access)

        return redirect("{}?access={}&refresh={}".format(redirect_uri, token.access, token.refresh))


class RefreshTokenView(APIView):

    def post(self, request):
        updateLogs("[POST] "+request.path)

        client_id = request.POST['client_id']
        client_secret = request.POST['client_secret']
        refresh_token = request.POST['refresh_token']
        redirect_uri = request.POST['redirect_uri']

        if not ClientService.check_credentials(client_id, client_secret):
            updateLogs("Invalid client credentials")
            return redirect("{}?error={}".format(redirect_uri, "invalid_client_credentials"))

        client = ClientService.get_client(client_id)

        if not TokenService.check_refresh_token(refresh_token, client):
            updateLogs("Invalid refresh token")
            return redirect("{}?error={}".format(redirect_uri, "invalid_refresh_token"))

        token = TokenService.refresh_token(refresh_token, client)
        updateLogs("Refreshed token, new one: "+token.access)

        return redirect("{}?access={}&refresh={}".format(redirect_uri, token.access, token.refresh))

class LoggerView(APIView):

    def get(self, request):
        updateLogs("[GET] "+request.path)

        return render(request, 'logger.html', {
            'logs' : logs
        })

class LogsView(APIView):

    def get(self, request):

        htmlLogs = []
        for log in logs:
            htmlLogs.append('<p class="log">'+log+'</p>')

        return HttpResponse(htmlLogs)

    def post(self, request):

        updateLogs(request.POST['log'])

def updateLogs(log):

    if len(logs) >= 19:
            logs.pop()

    logs.insert(0, log)
