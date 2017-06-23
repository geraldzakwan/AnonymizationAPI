# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def index(request):
    if (request.method == 'GET'):
        text = 'Welcome to English message anonymization API.' + '\n\n' + 'Sample JSON message: {'+ '\n' + '    message: "My friend, Ibrahim, comes from France."' + '\n' +'}'
        return HttpResponse(text)
    elif (request.method == 'POST'):
        text = request.POST.get('message')
        if (text == None):
            text = 'Wrong JSON format sent.' + '\n\n' + 'Sample JSON message: {'+ '\n' + '    message: "My friend, Ibrahim, comes from France."' + '\n' +'}'
        return HttpResponse(text)
