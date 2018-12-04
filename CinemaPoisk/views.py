from django.shortcuts import render, redirect
from PIL import Image
from django.contrib import auth
import json
from datetime import datetime, timedelta

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
    currentDate = datetime.today().strftime("%d.%m.%Y")
    return render(request, 'pages/cinemas.html', {"cinemas": cinemas,
                                                  "username": auth.get_user(request).username,
                                                  "currentDate": currentDate})


def cinemaRender(request, cinemaid):
    for cinema in cinemas:
        if cinema["id"] == cinemaid:
            if request.GET.get('date', '01.01.1970'):
                currentDate = request.GET.get('date', '01.01.1970')
            if request.GET.get('change', 'no') == 'yes':
                file = open("templates/db/favorites_db.json", "r", encoding="utf8")
                favorites = json.loads(file.read())
                file.close()
                for favorite in favorites:
                    if favorite["username"] == auth.get_user(request).username:
                        favorites.remove(favorite)
                        if cinema["id"] in favorite["favorites_cinemas_id"]:
                            favorite["favorites_cinemas_id"].remove(cinema["id"])
                        else:
                            favorite["favorites_cinemas_id"].append(cinema["id"])
                        favorites.append(favorite)
                        file = open("templates/db/favorites_db.json", "w", encoding="utf8")
                        file.write(json.dumps(favorites))
                        file.close()
                        return redirect("/cinema/" + str(cinema["id"]) + "?date=" + currentDate)
            else:
                im = Image.open("static/" + cinema[
                    "image"])  # Это библиотека для работы с изображениями. Я получаю размер, чтобы потом корректно отображать на странице
                (width, height) = im.size
                right_size = 900 - 15 - width
                file = open("templates/db/favorites_db.json", "r", encoding="utf8")
                favorites = json.loads(file.read())
                file.close()
                for favorite in favorites:
                    if favorite["username"] == auth.get_user(request).username:
                        if cinema["id"] in favorite["favorites_cinemas_id"]:
                            isInFavorites = True
                        else:
                            isInFavorites = False
                today = datetime.today().strftime("%d.%m.%Y")
                date = datetime.strptime(currentDate, "%d.%m.%Y")
                nextDays = []
                for i in range(1, 5):
                    nextDays.append((date + timedelta(days=i)).strftime("%d.%m.%Y"))
                schedule = []
                for day in cinema["schedule"]:
                    if day["date"] == currentDate:
                        schedule = day["sessions"]
                        break
                return render(request, 'pages/cinema.html', {"cinema": cinema,
                                                             "image_width": width,
                                                             "image_height": height,
                                                             "right_size": right_size,
                                                             "movies": movies,
                                                             "isInFavorites": isInFavorites,
                                                             "username": auth.get_user(request).username,
                                                             "currentDate": currentDate,
                                                             "nextDays": nextDays,
                                                             "today": today,
                                                             "schedule": schedule})
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
                                                        "staffs": staffs,
                                                        "username": auth.get_user(request).username})
    return render(request, '')


def personRender(request, personid):
    for person in staffs:
        if person["id"] == personid:
            if person["image"]:
                im = Image.open("static/" + person[
                    "image"])  # Это библиотека для работы с изображениями. Я получаю размер, чтобы потом корректно отображать на странице
                (width, height) = im.size
                right_size = 900 - 15 - width
            else:
                width = 300
                height = 400
                right_size = 900 - 15 - width
            return render(request, 'pages/person.html', {"person": person,
                                                         "image_width": width,
                                                         "image_height": height,
                                                         "right_size": right_size,
                                                         "movies": movies,
                                                         "username": auth.get_user(request).username})
    return render(request, '')


def favoritesRender(request):
    username = auth.get_user(request).username
    currentDate = datetime.today().strftime("%d.%m.%Y")
    if username == "":
        return render(request, 'pages/favorites.html', {"login_error": "Вы не вошли в систему",
                                                        "username": auth.get_user(request).username,
                                                        "currentDate": currentDate})
    else:
        file = open("templates/db/favorites_db.json", "r", encoding="utf8")
        favorites = json.loads(file.read())
        file.close()
        for user in favorites:
            if username == user["username"]:
                cinemas_for_render = []
                for cinema_id in user["favorites_cinemas_id"]:
                    for cinema in cinemas:
                        if cinema["id"] == cinema_id:
                            cinemas_for_render.append(cinema)
                return render(request, 'pages/favorites.html', {"cinemas": cinemas_for_render,
                                                                "username": auth.get_user(request).username,
                                                                "currentDate": currentDate})
