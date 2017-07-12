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
                return redirect_home()

    return render(request, 'login/login.html')


def logout(request):
    logout_user(request)
    return HttpResponseRedirect("/login")


def is_valid(request):
    return (request.POST.get("username") and
            request.POST.get("password")) is not ''


def home(request):
    if request.user.is_authenticated:
        try:
            user = User.objects.get(username=request.user.username)
        except Exception as e:
            return HttpResponse("El usuario no existe")
        
        print user.groups
        #user.user_permissions = 1
        #user.save()
        #print user.user_permissions
        return render(request, 'login/home.html', {
            'user': user,
            })
    else:
        return HttpResponseRedirect("/login")


def redirect_home():
    return HttpResponseRedirect("/home/")
