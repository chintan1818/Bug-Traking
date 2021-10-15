from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.


def signin(request):
    return HttpResponse('Signin')


def signup(request):
    return HttpResponse('Signup')
