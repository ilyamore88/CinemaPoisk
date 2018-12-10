from django.contrib.auth.forms import UserCreationForm
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
