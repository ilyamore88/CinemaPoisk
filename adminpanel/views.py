from django.shortcuts import render, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from datetime import datetime
import json


def adminpanel(request):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif currentUser["permissions"] == "superuser":
        return adminpage(request)
    elif currentUser["permissions"] == "moderator":
        return moderatorpage(request)
    else:
        auth.logout(request)
        return redirect('/adminpanel/loginerror')


def adminpage(request):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif currentUser["permissions"] != "superuser":
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    return render(request, 'admins_page.html', {"username": currentUser["username"],
                                                "currentUserPermissions": currentUser["permissions"]})


def moderatorpage(request):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif currentUser["permissions"] != "moderator":
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    return render(request, 'moderators_page.html', {"username": currentUser["username"],
                                                    "currentUserPermissions": currentUser["permissions"]})


def addmoderator(request):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif currentUser["permissions"] != "superuser":
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    args = {}
    args.update(csrf(request))
    args["username"] = currentUser["username"]
    args["permissions"] = currentUser["permissions"]
    if request.POST:
        username = request.POST.get('username', '')
        userModerator = {}
        for user in users:
            if user["username"] == username:
                userModerator = user
                users.remove(user)
                break
        if userModerator != {}:
            userModerator["permissions"] = "moderator"
            users.append(userModerator)
            file = open("templates/db/users_db.json", "w", encoding="utf8")
            file.write(json.dumps(users))
            file.close()
            return redirect('/adminpanel')
        else:
            args["input_error"] = "Пользователь не найден"
            return render(request, 'editing/addmoderator.html', args)
    else:
        return render(request, 'editing/addmoderator.html', args)


def deletemoderator(request):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif currentUser["permissions"] != "superuser":
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    args = {}
    args.update(csrf(request))
    args["username"] = currentUser["username"]
    args["permissions"] = currentUser["permissions"]
    if request.POST:
        username = request.POST.get('username', '')
        userModerator = {}
        for user in users:
            if user["username"] == username:
                userModerator = user
                users.remove(user)
                break
        if userModerator != {}:
            userModerator["permissions"] = "user"
            users.append(userModerator)
            file = open("templates/db/users_db.json", "w", encoding="utf8")
            file.write(json.dumps(users))
            file.close()
            return redirect('/adminpanel')
        else:
            args["input_error"] = "Пользователь не найден"
            return render(request, 'editing/deletemoderator.html', args)
    else:
        return render(request, 'editing/deletemoderator.html', args)


def deleteuser(request):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif currentUser["permissions"] != "superuser":
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    args = {}
    args.update(csrf(request))
    args["username"] = currentUser["username"]
    args["permissions"] = currentUser["permissions"]
    if request.POST:
        username = request.POST.get('username', '')
        isUserFind = False
        for user in users:
            if user["username"] == username:
                users.remove(user)
                isUserFind = True
                break
        if isUserFind:
            file = open("templates/db/users_db.json", "w", encoding="utf8")
            file.write(json.dumps(users))
            file.close()
            return redirect('/adminpanel')
        else:
            args["input_error"] = "Пользователь не найден"
            return render(request, 'editing/deleteuser.html', args)
    else:
        return render(request, 'editing/deleteuser.html', args)


def addstuff(request):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif (currentUser["permissions"] != "superuser") and (currentUser["permissions"] != "moderator"):
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    args = {}
    args.update(csrf(request))
    args["username"] = currentUser["username"]
    args["permissions"] = currentUser["permissions"]
    if request.POST:
        id = int(request.POST.get('id', ))
        last_name = str(request.POST.get('last_name', ''))
        first_name = str(request.POST.get('first_name', ''))
        middle_name = str(request.POST.get('middle_name', ''))
        image_name = ("images/staffs/" + request.POST.get('image', '')) if request.POST.get('image', '') != '' else ""
        actor_films_id = list(map(int, request.POST.get('actor_films_id', '').split(','))) if request.POST.get(
            'actor_films_id', '') != '' else []
        director_films_id = list(map(int, request.POST.get('director_films_id', '').split(','))) if request.POST.get(
            'director_films_id', '') != '' else []
        file = open("templates/db/staffs_db.json", "r", encoding="utf8")
        staffs = json.loads(file.read())
        file.close()
        isID = False
        for stuff in staffs:
            if id == stuff["id"]:
                isID = True
                break
        if isID == False:
            staffs.append({"id": id, "last_name": last_name, "middle_name": middle_name, "first_name": first_name,
                           "image": image_name, "actor_films_id": actor_films_id,
                           "director_films_id": director_films_id})
            file = open("templates/db/staffs_db.json", "w", encoding="utf8")
            file.write(json.dumps(staffs, ensure_ascii=False))
            file.close()
            file = open("templates/db/movies_db.json", "r", encoding="utf8")
            movies = json.loads(file.read())
            file.close()
            for movie in movies:
                if movie["id"] in actor_films_id:
                    movie["actors_id"].append(id)
                if movie["id"] in director_films_id:
                    movie["director_id"].append(id)
            file = open("templates/db/movies_db.json", "w", encoding="utf8")
            file.write(json.dumps(movies, ensure_ascii=False))
            file.close()
            return redirect('/adminpanel')
        else:
            args["input_error"] = "Человек с таким ID уже существует!"
            return render(request, 'editing/addstuff.html', args)
    else:
        return render(request, 'editing/addstuff.html', args)


def deletestuff(request):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif (currentUser["permissions"] != "superuser") and (currentUser["permissions"] != "moderator"):
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    args = {}
    args.update(csrf(request))
    args["username"] = currentUser["username"]
    args["permissions"] = currentUser["permissions"]
    if request.POST:
        id = int(request.POST.get('id', ''))
        file = open("templates/db/staffs_db.json", "r", encoding="utf8")
        staffs = json.loads(file.read())
        file.close()
        isID = False
        for stuff in staffs:
            if id == stuff["id"]:
                isID = True
                break
        if isID:
            staffs.remove(stuff)
            file = open("templates/db/movies_db.json", "r", encoding="utf8")
            movies = json.loads(file.read())
            file.close()
            for movie in movies:
                if movie["id"] in stuff["actor_films_id"]:
                    movie["actors_id"].remove(id)
                if movie["id"] in stuff["director_films_id"]:
                    movie["director_id"].remove(id)
            file = open("templates/db/movies_db.json", "w", encoding="utf8")
            file.write(json.dumps(movies, ensure_ascii=False))
            file.close()
            file = open("templates/db/staffs_db.json", "w", encoding="utf8")
            file.write(json.dumps(staffs, ensure_ascii=False))
            file.close()
            return redirect('/adminpanel')
        else:
            args["input_error"] = "Такой человек не найден"
            return render(request, 'editing/deletestuff.html', args)
    else:
        return render(request, 'editing/deletestuff.html', args)


def addmovie(request):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif (currentUser["permissions"] != "superuser") and (currentUser["permissions"] != "moderator"):
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    args = {}
    args.update(csrf(request))
    args["username"] = currentUser["username"]
    args["permissions"] = currentUser["permissions"]
    if request.POST:
        id = int(request.POST.get('id', ))
        name = str(request.POST.get('name', ''))
        image_name = ("images/movies/" + request.POST.get('image', '')) if request.POST.get('image', '') != '' else ""
        duration = str(request.POST.get('duration', ''))
        description = str(request.POST.get('description', ''))
        age_rating = str(request.POST.get('age_rating', ''))
        director_id = int(request.POST.get('director_id', ''))
        actors_id = list(map(int, request.POST.get('actors_id', '').split(','))) if request.POST.get(
            'actors_id', '') != '' else []
        file = open("templates/db/movies_db.json", "r", encoding="utf8")
        movies = json.loads(file.read())
        file.close()
        isID = False
        for movie in movies:
            if id == movie["id"]:
                isID = True
                break
        if isID == False:
            movies.append({"id": id, "name": name,
                           "image": image_name, "age_rating": age_rating, "duration": duration,
                           "description": description, "actors_id": actors_id,
                           "director_id": director_id})
            file = open("templates/db/movies_db.json", "w", encoding="utf8")
            file.write(json.dumps(movies, ensure_ascii=False))
            file.close()
            file = open("templates/db/staffs_db.json", "r", encoding="utf8")
            staffs = json.loads(file.read())
            file.close()
            for stuff in staffs:
                if stuff["id"] in actors_id:
                    stuff["actor_films_id"].append(id)
                if stuff["id"] == director_id:
                    stuff["director_films_id"].append(id)
            file = open("templates/db/staffs_db.json", "w", encoding="utf8")
            file.write(json.dumps(staffs, ensure_ascii=False))
            file.close()
            return redirect('/adminpanel')
        else:
            args["input_error"] = "Фильм с таким ID уже существует!"
            return render(request, 'editing/addmovie.html', args)
    else:
        return render(request, 'editing/addmovie.html', args)


def deletemovie(request):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif (currentUser["permissions"] != "superuser") and (currentUser["permissions"] != "moderator"):
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    args = {}
    args.update(csrf(request))
    args["username"] = currentUser["username"]
    args["permissions"] = currentUser["permissions"]
    if request.POST:
        id = int(request.POST.get('id', ''))
        file = open("templates/db/movies_db.json", "r", encoding="utf8")
        movies = json.loads(file.read())
        file.close()
        isID = False
        for movie in movies:
            if id == movie["id"]:
                isID = True
                break
        if isID:
            movies.remove(movie)
            file = open("templates/db/staffs_db.json", "r", encoding="utf8")
            staffs = json.loads(file.read())
            file.close()
            for stuff in staffs:
                if stuff["id"] in movie["actors_id"]:
                    stuff["actor_films_id"].remove(id)
                if stuff["id"] == movie["director_id"]:
                    stuff["director_films_id"].remove(id)
            file = open("templates/db/staffs_db.json", "w", encoding="utf8")
            file.write(json.dumps(staffs, ensure_ascii=False))
            file.close()
            file = open("templates/db/movies_db.json", "w", encoding="utf8")
            file.write(json.dumps(movies, ensure_ascii=False))
            file.close()
            return redirect('/adminpanel')
        else:
            args["input_error"] = "Такой фильм не найден"
            return render(request, 'editing/deletemovie.html', args)
    else:
        return render(request, 'editing/deletemovie.html', args)


def addcinema(request):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif (currentUser["permissions"] != "superuser") and (currentUser["permissions"] != "moderator"):
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    args = {}
    args.update(csrf(request))
    args["username"] = currentUser["username"]
    args["permissions"] = currentUser["permissions"]
    if request.POST:
        id = int(request.POST.get('id', ))
        name = str(request.POST.get('name', ''))
        image_name = ("images/cinemas/" + request.POST.get('image', '')) if request.POST.get('image', '') != '' else ""
        tel = str(request.POST.get('tel', ''))
        description = request.POST.get('description', []).split("\r\n")
        subway = str(request.POST.get('subway', ''))
        address = str(request.POST.get('address', ''))
        file = open("templates/db/cinemas_db.json", "r", encoding="utf8")
        cinemas = json.loads(file.read())
        file.close()
        isID = False
        for cinema in cinemas:
            if id == cinema["id"]:
                isID = True
                break
        if isID == False:
            cinemas.append({"id": id, "name": name,
                            "image": image_name, "tel": tel, "address": address,
                            "description": description, "subway": subway,
                            "schedule": []})
            file = open("templates/db/cinemas_db.json", "w", encoding="utf8")
            file.write(json.dumps(cinemas, ensure_ascii=False))
            file.close()
            return redirect('/adminpanel')
        else:
            args["input_error"] = "Кинотеатр с таким ID уже существует!"
            return render(request, 'editing/addcinema.html', args)
    else:
        return render(request, 'editing/addcinema.html', args)


def deletecinema(request):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif (currentUser["permissions"] != "superuser") and (currentUser["permissions"] != "moderator"):
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    args = {}
    args.update(csrf(request))
    args["username"] = currentUser["username"]
    args["permissions"] = currentUser["permissions"]
    if request.POST:
        id = int(request.POST.get('id', ''))
        file = open("templates/db/cinemas_db.json", "r", encoding="utf8")
        cinemas = json.loads(file.read())
        file.close()
        isID = False
        for cinema in cinemas:
            if id == cinema["id"]:
                isID = True
                break
        if isID:
            cinemas.remove(cinema)
            file = open("templates/db/cinemas_db.json", "w", encoding="utf8")
            file.write(json.dumps(cinemas, ensure_ascii=False))
            file.close()
            return redirect('/adminpanel')
        else:
            args["input_error"] = "Такой кинотеатр не найден"
            return render(request, 'editing/deletecinema.html', args)
    else:
        return render(request, 'editing/deletecinema.html', args)


def addsession(request):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif (currentUser["permissions"] != "superuser") and (currentUser["permissions"] != "moderator"):
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    args = {}
    args.update(csrf(request))
    args["username"] = currentUser["username"]
    args["permissions"] = currentUser["permissions"]
    if request.POST:
        id_cinema = int(request.POST.get('id_cinema', ))
        id_movie = int(request.POST.get('id_movie', ))
        date = str(request.POST.get('date', '01.01.1970'))
        time = str(request.POST.get('time', ''))
        price = int(request.POST.get('price', 0))
        format = str(request.POST.get('format', ''))

        day, month, year = list(map(int, date.split('.')))
        hour, minute = list(map(int, time.split(':')))

        if (day < 1) or (day > 31) or (month < 0) or (month > 12) or (year < 1970) or (hour < 0) or (hour > 23) or (
                minute < 0) or (minute > 59):
            args["input_error"] = "Проверьте корректность введённых данных"
            return render(request, 'editing/addsession.html', args)

        file = open("templates/db/cinemas_db.json", "r", encoding="utf8")
        cinemas = json.loads(file.read())
        file.close()
        file = open("templates/db/movies_db.json", "r", encoding="utf8")
        movies = json.loads(file.read())
        file.close()
        for cinema in cinemas:
            if id_cinema == cinema["id"]:
                for movie in movies:
                    if id_movie == movie["id"]:
                        for dateInSessions in cinema["schedule"]:
                            if date == dateInSessions["date"]:
                                dateInSessions["sessions"].append(
                                    {"film_id": id_movie, "time": time, "price": price, "format": format})
                                file = open("templates/db/cinemas_db.json", "w", encoding="utf8")
                                file.write(json.dumps(cinemas, ensure_ascii=False))
                                file.close()
                                return redirect('/adminpanel')
                        cinema["schedule"].append({"date": date, "sessions": [
                            {"film_id": id_movie, "time": time, "price": price, "format": format}]})
                        file = open("templates/db/cinemas_db.json", "w", encoding="utf8")
                        file.write(json.dumps(cinemas, ensure_ascii=False))
                        file.close()
                        return redirect('/adminpanel')

        args["input_error"] = "Проверьте корректность введённых данных"
        return render(request, 'editing/addsession.html', args)
    else:
        return render(request, 'editing/addsession.html', args)


def deletesession(request):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif (currentUser["permissions"] != "superuser") and (currentUser["permissions"] != "moderator"):
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    args = {}
    args.update(csrf(request))
    args["username"] = currentUser["username"]
    args["permissions"] = currentUser["permissions"]
    if request.POST:
        id_cinema = int(request.POST.get('id_cinema', ))
        date = str(request.POST.get('date', '01.01.1970'))
        time = str(request.POST.get('time', ''))

        day, month, year = list(map(int, date.split('.')))
        hour, minute = list(map(int, time.split(':')))

        if (day < 1) or (day > 31) or (month < 0) or (month > 12) or (year < 1970) or (hour < 0) or (hour > 23) or (
                minute < 0) or (minute > 59):
            args["input_error"] = "Проверьте корректность введённых данных"
            return render(request, 'editing/deletesession.html', args)

        file = open("templates/db/cinemas_db.json", "r", encoding="utf8")
        cinemas = json.loads(file.read())
        file.close()
        for cinema in cinemas:
            if id_cinema == cinema["id"]:
                for dateInSessions in cinema["schedule"]:
                    if date == dateInSessions["date"]:
                        for sessionInDate in dateInSessions["sessions"]:
                            if time == sessionInDate["time"]:
                                dateInSessions["sessions"].remove(sessionInDate)
                                file = open("templates/db/cinemas_db.json", "w", encoding="utf8")
                                file.write(json.dumps(cinemas, ensure_ascii=False))
                                file.close()
                                return redirect('/adminpanel')
        args["input_error"] = "Проверьте корректность введённых данных"
        return render(request, 'editing/deletesession.html', args)
    else:
        return render(request, 'editing/deletesession.html', args)


def editcinema(request, cinemaid):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentDate = datetime.today().strftime("%d.%m.%Y")
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif (currentUser["permissions"] != "superuser") and (currentUser["permissions"] != "moderator"):
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    args = {}
    args.update(csrf(request))
    args["username"] = currentUser["username"]
    args["permissions"] = currentUser["permissions"]
    file = open("templates/db/cinemas_db.json", "r", encoding="utf8")
    cinemas = json.loads(file.read())
    file.close()
    for cinema in cinemas:
        if cinemaid == cinema["id"]:
            args["cinema"] = cinema
            if request.POST:
                cinema["name"] = str(request.POST.get('name', ''))
                cinema["image"] = request.POST.get('image', '')
                cinema["tel"] = str(request.POST.get('tel', ''))
                cinema["description"] = request.POST.get('description', []).split("\r\n")
                cinema["subway"] = str(request.POST.get('subway', ''))
                cinema["address"] = str(request.POST.get('address', ''))
                file = open("templates/db/cinemas_db.json", "w", encoding="utf8")
                file.write(json.dumps(cinemas, ensure_ascii=False))
                file.close()
                return redirect('/cinema/' + str(cinemaid) + "?date=" + currentDate)
            else:
                return render(request, 'editing/editcinema.html', args)
    return redirect('/cinema/' + str(cinemaid) + "?date=" + currentDate)


def editmovie(request, movieid):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif (currentUser["permissions"] != "superuser") and (currentUser["permissions"] != "moderator"):
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    args = {}
    args.update(csrf(request))
    args["username"] = currentUser["username"]
    args["permissions"] = currentUser["permissions"]
    file = open("templates/db/movies_db.json", "r", encoding="utf8")
    movies = json.loads(file.read())
    file.close()
    for movie in movies:
        if movieid == movie["id"]:
            args["movie"] = movie
            if request.POST:
                movie["name"] = str(request.POST.get('name', ''))
                movie["image"] = request.POST.get('image', '')
                movie["duration"] = str(request.POST.get('duration', ''))
                movie["description"] = str(request.POST.get('description', ''))
                movie["age_rating"] = str(request.POST.get('age_rating', ''))
                movie["director_id"] = int(request.POST.get('director_id', ''))
                movie["actors_id"] = list(map(int, request.POST.get('actors_id', '').split(','))) if request.POST.get(
                    'actors_id', '') != '' else []
                file = open("templates/db/movies_db.json", "w", encoding="utf8")
                file.write(json.dumps(movies, ensure_ascii=False))
                file.close()
                return redirect('/movie/' + str(movieid))
            else:
                return render(request, 'editing/editmovie.html', args)
    return redirect('/movie/' + str(movieid))


def editstuff(request, personid):
    username = auth.get_user(request).username
    file = open("templates/db/users_db.json", "r", encoding="utf8")
    users = json.loads(file.read())
    file.close()
    currentUser = {}
    for user in users:
        if username == user["username"]:
            currentUser = user
            break
    if currentUser == {}:
        return redirect('/adminpanel/loginerror')
    elif (currentUser["permissions"] != "superuser") and (currentUser["permissions"] != "moderator"):
        auth.logout(request)
        return redirect('/adminpanel/loginerror')
    args = {}
    args.update(csrf(request))
    args["username"] = currentUser["username"]
    args["permissions"] = currentUser["permissions"]
    file = open("templates/db/staffs_db.json", "r", encoding="utf8")
    staffs = json.loads(file.read())
    file.close()
    for person in staffs:
        if personid == person["id"]:
            args["person"] = person
            if request.POST:
                person["last_name"] = str(request.POST.get('last_name', ''))
                person["first_name"] = str(request.POST.get('first_name', ''))
                person["middle_name"] = str(request.POST.get('middle_name', ''))
                person["image"] = request.POST.get('image', '')
                person["actor_films_id"] = list(
                    map(int, request.POST.get('actor_films_id', '').split(','))) if request.POST.get(
                    'actor_films_id', '') != '' else []
                person["director_films_id"] = list(
                    map(int, request.POST.get('director_films_id', '').split(','))) if request.POST.get(
                    'director_films_id', '') != '' else []
                file = open("templates/db/staffs_db.json", "w", encoding="utf8")
                file.write(json.dumps(staffs, ensure_ascii=False))
                file.close()
                return redirect('/person/' + str(personid))
            else:
                return render(request, 'editing/editstuff.html', args)
    return redirect('/person/' + str(personid))
