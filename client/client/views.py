import random
import string
import datetime

from collections import Counter
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from django.shortcuts import render, redirect

client_id = "client_app"

auth_server_url = "localhost:8000"

class InitialView(APIView):

    def get(self, request):
        return render(request, 'main.html', {'auth_server_host' : auth_server_url, 'client_id': client_id, 'redirect_uri': "http://{}/get-token".format(request.META['HTTP_HOST'])})


class GetTokenView(APIView):

    def get(self, request):

        if 'error' in request.GET:
            return render(request, 'error.html', {'host': request.META['HTTP_HOST'], 'client_id': client_id, 'error': request.GET['error']})

        # TODO: Get token from authorization code
        return HttpResponse("Processing token with authorization code {}".format(request.GET['code']))

