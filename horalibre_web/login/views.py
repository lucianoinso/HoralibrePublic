# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def login(request):
    # Si esta logueado lo redirecciono al home.
    error_message = ""
    if request.user.is_authenticated:
        return redirect_home()
    # Si es una solicitud de login, checkeo que este bien.
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if is_valid(request):
            user = authenticate(username=username,
                                password=password)
            if user is not None:
                login_user(request, user)
                # Expire on browser close
                request.session.set_expiry(0)
                return redirect_home()
            else:
                error_message = "Nombre de usuario y/o contraseña invalidos"
        else:
            error_message = "Nombre de usuario y/o contraseña invalidos"

    return render(request, 'login/login.html', {'error_message': error_message, })


def logout(request):
    logout_user(request)
    return HttpResponseRedirect("/login")


def is_valid(request):
    return (request.POST.get("username") and
            request.POST.get("password")) is not ''


def redirect_home():
    return HttpResponseRedirect("/news/")
