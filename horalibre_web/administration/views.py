# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Imports
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from datetime import datetime

# Project Imports
from login.views import redirect_home
from records.models import Professional, Secretary, Patient, Record, Case
from .forms import (ProfessionalForm, ProfessionalListForm, SecretaryForm,
                    PatientForm, CaseForm, PatientListForm, SecretaryListForm,
                    CaseListForm)


def admin_home(request):
    if request.user.is_authenticated:
        return render(request, 'administration/home.html', {})
    else:
        return render(request, 'login/login.html')


@csrf_protect
def create_professional(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = ProfessionalForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                dni = form.cleaned_data['dni']
                phone_number = form.cleaned_data['phone_number']
                profession = form.cleaned_data['profession']
                is_coordinator = form.cleaned_data['is_coordinator']

                entered_username = User.objects.filter(username=username).first()
                if entered_username is None:
                    new_user = User.objects.create_user(username=username,
                                                        email=email,
                                                        password=password,
                                                        first_name=first_name,
                                                        last_name=last_name)
                    new_user.save()
                    new_professional = Professional.objects.create(
                        user=new_user,
                        dni=dni,
                        phone_number=phone_number,
                        profession=profession,
                        is_coordinator=is_coordinator)
                    new_professional.save()
                    return HttpResponseRedirect('/administration/')
                else:
                    # We prepopulate the form with the previous values
                    # except the username, and return an error message
                    pre_data = {'email': email,
                                'first_name': first_name,
                                'last_name': last_name,
                                'dni': dni, 'phone_number': phone_number,
                                'profession': profession,
                                'is_coordinator': is_coordinator}
                    form = ProfessionalForm(initial=pre_data)
                    error_message = ("El nombre de usuario ingresado ya " +
                                     "existe, elija otro")
                    return render(request, 'administration/create_professional.html',
                                  {'form': form,
                                   'error_message': error_message})
        # if a GET (or any other method) we'll create a blank form
        else:
            form = ProfessionalForm()
        return render(request, 'administration/create_professional.html',
                      {'form': form})
    else:
        return render(request, 'login/login.html')


@csrf_protect
def modify_proff_menu(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = ProfessionalForm(request.POST)
            # Check whether is valid:
        #    if form.is_valid():
        #        professional = form.cleaned_data['professional']
            return render(request, 'administration/modify_proff_menu.html',
                          {'form': form})
        # if a GET (or any other method) we'll create a blank form
        else:
            form = ProfessionalListForm()
            return render(request, 'administration/modify_proff_menu.html',
                          {'form': form})
    else:
        return render(request, 'login/login.html')


@csrf_protect
def modify_proff(request, proff_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print "POSTT"
            proff = Professional.objects.get(id=proff_id)
            # Create a form instance and populate it with data from the request
            pre_data = {'email': proff.user.email, 'dni': proff.dni,
                        'first_name': proff.user.first_name,
                        'last_name': proff.user.last_name,
                        'phone_number': proff.phone_number,
                        'profession': proff.profession,
                        'is_coordinator': proff.is_coordinator}
            form = ProfessionalForm(initial=pre_data)
            return render(request, 'administration/modify_proff.html',
                          {'form': form, 'proff_id': proff.id})
        # if a GET (or any other method) we'll create a blank form
        else:
            proff = Professional.objects.get(id=proff_id)
            # Create a form instance and populate it with data from the request
            pre_data = {'email': proff.user.email,
                        'first_name': proff.user.first_name,
                        'last_name': proff.user.last_name, 'dni': proff.dni,
                        'phone_number': proff.phone_number,
                        'profession': proff.profession,
                        'is_coordinator': proff.is_coordinator}
            form = ProfessionalForm(initial=pre_data)
            return render(request, 'administration/modify_proff.html',
                          {'form': form, 'proff_id': proff.id})
    else:
        return render(request, 'login/login.html')


def delete_professional(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = ProfessionalListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                professional = form.cleaned_data['professional']
                professional.user.delete()
                professional.delete()
            return HttpResponseRedirect('/administration/')
        # if a GET (or any other method) we'll create a blank form
        else:
            form = ProfessionalListForm()
            return render(request, 'administration/delete_professional.html',
                          {'form': form})
    else:
        return render(request, 'login/login.html')


# Secretary
@csrf_protect
def create_secretary(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = SecretaryForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                dni = form.cleaned_data['dni']
                phone_number = form.cleaned_data['phone_number']

                entered_username = User.objects.filter(username=username).first()
                if entered_username is None:
                    new_user = User.objects.create_user(username=username,
                                                        email=email,
                                                        password=password,
                                                        first_name=first_name,
                                                        last_name=last_name)
                    new_user.save()
                    new_secretary = Secretary.objects.create(
                        user=new_user,
                        dni=dni,
                        phone_number=phone_number)

                    new_secretary.save()
                    return HttpResponseRedirect('/administration/')
                else:
                    # We prepopulate the form with the previous values
                    # except the username, and return an error message
                    pre_data = {'email': email,
                                'first_name': first_name,
                                'last_name': last_name, 'dni': dni,
                                'phone_number': phone_number}
                    form = SecretaryForm(initial=pre_data)
                    error_message = ("El nombre de usuario ingresado ya " +
                                     "existe, elija otro")
                    return render(request, 'administration/create_secretary.html',
                                  {'form': form,
                                   'error_message': error_message})
        # if a GET (or any other method) we'll create a blank form
        else:
            form = SecretaryForm()
        return render(request, 'administration/create_secretary.html',
                      {'form': form})
    else:
        return render(request, 'login/login.html')


def modify_secretary(request):
    pass


def delete_secretary(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = SecretaryListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                secretary = form.cleaned_data['secretary']
                secretary.delete()
            return HttpResponseRedirect('/administration/')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = SecretaryListForm()
            return render(request, 'administration/delete_secretary.html',
                          {'form': form})
    else:
        return render(request, 'login/login.html')


# Patients
def create_patient(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = PatientForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                birthdate = form.cleaned_data['birthdate']
                health_insurance = form.cleaned_data['health_insurance']
                dni = form.cleaned_data['dni']
                phone_number = form.cleaned_data['phone_number']

                entered_dni = Patient.objects.filter(dni=dni).first()
                if entered_dni is None:
                    new_patient = Patient.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        birthdate=birthdate,
                        health_insurance=health_insurance,
                        dni=dni,
                        phone_number=phone_number)

                    new_patient.save()
                    return HttpResponseRedirect('/administration/')
                else:
                    # We prepopulate the form with the previous values
                    # except the DNI, and return an error message
                    pre_data = {'first_name': first_name,
                                'last_name': last_name,
                                'health_insurance': health_insurance,
                                'birthdate': birthdate,
                                'phone_number': phone_number}
                    form = PatientForm(initial=pre_data)
                    error_message = ("El DNI del paciente ingresado ya " +
                                     "existe en el sistema.")
                    return render(request,
                                  'administration/create_patient.html',
                                  {'form': form,
                                   'error_message': error_message})
        # if a GET (or any other method) we'll create a blank form
        else:
            current_date_data = {'birthdate': datetime.now()}
            form = PatientForm(initial=current_date_data)
        return render(request, 'administration/create_patient.html',
                      {'form': form})
    else:
        return render(request, 'login/login.html')


def modify_patient(request):
    pass


def delete_patient(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = PatientListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                patient = form.cleaned_data['patient']
                patient.delete()
            return HttpResponseRedirect('/administration/')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = PatientListForm()
            return render(request, 'administration/delete_patient.html',
                          {'form': form})
    else:
        return render(request, 'login/login.html')


# Cases
def create_case(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = CaseForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                new_case = form.save(commit=False)
                patient = new_case.patient
                professional = new_case.professional
                coordinator = new_case.coordinator

                entered_case = Case.objects.filter(patient=patient,
                                                   professional=professional,
                                                   coordinator=coordinator).first()
                if entered_case is None:
                    new_case = Case.objects.create(
                        patient=patient,
                        professional=professional,
                        coordinator=coordinator)
                    new_case.save()
                    return HttpResponseRedirect('/administration/')
                else:
                    # We prepopulate the form with the previous values
                    # except the DNI, and return an error message
                    form = CaseForm()
                    error_message = "El caso ya existe."
                    return render(request, 'administration/create_case.html',
                                  {'form': form,
                                   'error_message': error_message})
        # if a GET (or any other method) we'll create a blank form
        else:
            form = CaseForm()
        return render(request, 'administration/create_case.html',
                      {'form': form})
    else:
        return render(request, 'login/login.html')


def modify_case(request):
    pass


def delete_case(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = CaseListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                case = form.cleaned_data['case']
                case.delete()
            return HttpResponseRedirect('/administration/')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = CaseListForm()
            return render(request, 'administration/delete_case.html',
                          {'form': form})
    else:
        return render(request, 'login/login.html')
