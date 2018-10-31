from django.http import HttpResponse
from django.shortcuts import render
import json


def indexRender(request):
    return render(request, 'base.html', {})


def cinemaRender(request):
    return render(request, 'pages/cinema.html', {})


def movieRender(request):
    return render(request, 'pages/movie.html', {})


def personRender(request):
    return render(request, 'pages/person.html', {})


def signinRender(request):
    return render(request, 'pages/signin.html', {})


def signupRender(request):
    return render(request, 'pages/signup.html', {})
