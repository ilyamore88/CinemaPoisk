from django.shortcuts import render, redirect
from django.contrib import auth
from django.template.context_processors import csrf
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
