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
    if request.user.is_authenticated:
        return redirect_home(request.user.username)
    # Si es una solicitud de login, checkeo que este bien.
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if is_valid(request):
            user = authenticate(username=username,
                                password=password)
            if user is not None:
                login_user(request, user)
                return redirect_home(username)

    return render(request, 'login/login.html')


@csrf_protect
def new_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        if is_valid(request):
            user = User.objects.create_user(username=username,
                                            password=password)
            user.save()
            user = authenticate(username=username, password=password)
            login_user(request, user)
            return redirect_home(username)
    return HttpResponseRedirect('/login')


def logout(request):
    logout_user(request)
    return HttpResponseRedirect("/login")


def is_valid(request):
    return (request.POST.get("username") and
            request.POST.get("password")) is not ''


def home(request, username="Anonymous"):
    if request.user.is_authenticated:
        if request.user.username == username:
            try:
                user = User.objects.get(username=username)
            except Exception as e:
                return HttpResponse("El usuario no existe")
            
            return render(request, 'login/home.html', {
                'user': user,
                #'goals': goals,
                })
        else:
            # El usuario quiere ingresar a otro home que no es el suyo.
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")


def redirect_home(username):
    return HttpResponseRedirect("/home/{}".format(username))
