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
            args["login_error"] = "Пользователь не найден"
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
            args["login_error"] = "Пользователь не найден"
            return render(request, 'editing/deleteuser.html', args)
    else:
        return render(request, 'editing/deleteuser.html', args)
