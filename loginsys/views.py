from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import auth
from django.template.context_processors import csrf
import json


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args["login_error"] = "Пользователь не найден"
            return render(request, 'login.html', args)
    else:
        return render(request, 'login.html', args)


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    args = {}
    args.update(csrf(request))
    args["form"] = UserCreationForm(request.POST)
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data["username"],
                                        password=newuser_form.cleaned_data["password2"])
            auth.login(request, newuser)
            file = open("templates/db/favorites_db.json", "r", encoding="utf8")
            favorites = json.loads(file.read())
            file.close()
            favorites.append({"username": str(newuser_form.cleaned_data["username"]), "favorites_cinemas_id": []})
            file = open("templates/db/favorites_db.json", "w", encoding="utf8")
            file.write(json.dumps(favorites))
            file.close()
            return redirect("/")
        else:
            args["form"] = newuser_form
    return render(request, "register.html", args)
