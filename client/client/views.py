import random
import string
import datetime

from collections import Counter
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from django.shortcuts import render, redirect

client_id = "client_app"
client_secret = "client_secret"

auth_server_url = "localhost:8000"
grant_type = "authorization_code"

class InitialView(APIView):

    current_state = ""

    def get(self, request):
        lettersAndDigits = string.ascii_letters + string.digits
        InitialView.current_state = ''.join((random.choice(lettersAndDigits) for i in range(15)))
        return render(request, 'main.html', {'auth_server_host' : auth_server_url, 'client_id': client_id, 'redirect_uri': "http://{}/get-token".format(request.META['HTTP_HOST']),
                                             'state': InitialView.current_state})


class GetTokenView(APIView):

    def get(self, request):

        if 'error' in request.GET:
            return render(request, 'error.html', {'host': request.META['HTTP_HOST'], 'client_id': client_id, 'error': request.GET['error']})

        #CSRF protection
        if request.GET['state'] != InitialView.current_state:
            return render(request, 'error.html',
                          {'host': request.META['HTTP_HOST'], 'client_id': client_id, 'error': "invalid_state"})


        #Get token from authorization code
        return render(request, 'authorized.html', {
            'auth_server_host' : auth_server_url, 
            'grant_type' : grant_type,
            'code' : request.GET['code'],
            'client_id' : client_id,
            'client_secret' : client_secret,
            'redirect_uri' : "http://{}/get-resource".format(request.META['HTTP_HOST'])
        })

class RefreshTokenView(APIView):

    def get(self, request):

        if 'error' in request.GET:
            return render(request, 'error.html', {'host': request.META['HTTP_HOST'], 'client_id': client_id, 'error': request.GET['error']})

        #Get token from authorization code
        return render(request, 'token-refreshed.html', {
            'access' : request.GET['access'],
            'client_id' : client_id,
        })        


class GetResourceView(APIView):

    def get(self, request):

        if 'error' in request.GET:
            return render(request, 'error.html', {'host': request.META['HTTP_HOST'], 'client_id': client_id, 'error': request.GET['error']})

        return render(request, 'token-received.html', {
            'access' : request.GET['access'],
            'refresh' : request.GET['refresh'],
            'client_id' : client_id,
            'client_secret' : client_secret,
            'redirect_uri' : "http://{}/refresh-token".format(request.META['HTTP_HOST']),
            'auth_server_host' : auth_server_url,
        })
