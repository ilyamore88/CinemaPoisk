from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image
import json

file = open("templates/db/cinemas_db.json", "r", encoding="utf8")
cinemas = json.loads(file.read())
file.close()
file = open("templates/db/movies_db.json", "r", encoding="utf8")
movies = json.loads(file.read())
file.close()
file = open("templates/db/staffs_db.json", "r", encoding="utf8")
staffs = json.loads(file.read())
file.close()


def indexRender(request):
    return render(request, 'pages/cinemas.html', {"cinemas": cinemas})


def cinemaRender(request, cinemaid):
    for cinema in cinemas:
        if cinema["id"] == cinemaid:
            im = Image.open("static/" + cinema[
                "image"])  # Это библиотека для работы с изображениями. Я получаю размер, чтобы потом корректно отображать на странице
            (width, height) = im.size
            return render(request, 'pages/cinema.html', {"cinema": cinema,
                                                         "image_width": width,
                                                         "image_height": height,
                                                         "movies": movies})
    return render(request, '')


def movieRender(request, movieid):
    for movie in movies:
        if movie["id"] == movieid:
            im = Image.open("static/" + movie[
                "image"])  # Это библиотека для работы с изображениями. Я получаю размер, чтобы потом корректно отображать на странице
            (width, height) = im.size
            right_size = 900 - 15 - width
            return render(request, 'pages/movie.html', {"movie": movie,
                                                        "image_width": width,
                                                        "image_height": height,
                                                        "right_size": right_size,
                                                        "staffs": staffs})
    return render(request, '')


def personRender(request):
    return render(request, 'pages/person.html', {})


def signinRender(request):
    return render(request, 'pages/signin.html', {})


def signupRender(request):
    return render(request, 'pages/signup.html', {})
