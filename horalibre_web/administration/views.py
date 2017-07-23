# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Python imports
from datetime import datetime
import os
import errno

# Django Imports
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

# Project Imports
from login.views import redirect_home
from records.models import Professional, Secretary, Patient, Record, Case
from .forms import (ProfessionalForm, ProfessionalListForm, ChangePasswordForm,
                    ProfessionalEditForm, SecretaryForm, PatientForm, CaseForm,
                    PatientListForm, SecretaryListForm, SecretaryEditForm,
                    CaseListForm)


def create_dir(path):
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def create_logfile(log):
    logfile_name = str(datetime.now().strftime('%d-%m-%Y')) + ".txt"
    year = (datetime.now().strftime('%Y'))
    month = (datetime.now().strftime('%m'))
    log_dir = settings.LOGS_DIR + "/" + year + "-" + month

    if not os.path.isdir(log_dir):
        create_dir(log_dir)

    log += "\n"
    logfile_obj = open(log_dir + "/" + logfile_name, "a")
    logfile_obj.write(log)
    logfile_obj.close()


def add_log(username, event, model, model_key):
    """
        Example:
        [24/07/17 - 14:23:01] 'vivibalsamo' modified "sol_secre" [Secretary]
    """
    events = {
                "add" : "added",
                "mod" : "modified",
                "chpwd" : "changed password of",
                "del" : "deleted",
    }

    models = {
                "prof": "Professional",
                "secr": "Secretary",
                "patient": "Patient",
                "case": "Case",
                "news": "Article",
    }

    timestamp = str(datetime.now().strftime('[%d/%m/%y - %H:%M:%S]'))
    log = (timestamp + " \'" + str(username) + "\' " + str(events[event]) + " " + "\"" + model_key + "\" " + "[" + str(models[model]) + "]")
    create_logfile(log)


def admin_home(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'administration/home.html', {})
    elif request.user.is_authenticated:
        return redirect_home()
    else:
        return render(request, 'login/login.html')

@csrf_protect
def change_pwd_prof(request, prof_id):
    if request.user.is_authenticated and request.user.is_staff:
        prof = Professional.objects.get(id=prof_id)
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                prof.user.set_password(form.cleaned_data['password'])
                prof.user.save()
                prof.save()
                add_log(request.user.username, "chpwd", "prof", prof.user.username)
                return HttpResponseRedirect('/administration/')
            else:
                error_message = "Elija una contraseña valida"
                return render(request, 'administration/prof_change_pwd.html',
                             {'form': form,
                              'prof_id': prof_id,
                              'error_message': error_message})
        else:
            form = ChangePasswordForm()
            return render(request, 'administration/prof_change_pwd.html',
                          {'form':form, 'prof_id': prof.id})
    else:
        return render(request, 'login/login.html')


@csrf_protect
def change_pwd_secr(request, secretary_id):
    if request.user.is_authenticated and request.user.is_staff:
        secretary = Secretary.objects.get(id=secretary_id)
        if request.method == 'POST':
            form = ChangePasswordForm(request.POST)
            if form.is_valid():
                secretary.user.set_password(form.cleaned_data['password'])
                secretary.user.save()
                secretary.save()
                add_log(request.user.username, "chpwd", "secr", secretary.user.username)
                return HttpResponseRedirect('/administration/')
            else:
                error_message = "Elija una contraseña valida"
                return render(request, 'administration/secr_change_pwd.html',
                             {'form': form,
                              'secretary_id': secretary_id,
                              'error_message': error_message})
        else:
            form = ChangePasswordForm()
            return render(request, 'administration/secr_change_pwd.html',
                          {'form':form, 'secretary_id': secretary.id})
    else:
        return render(request, 'login/login.html')

# Professionals
def professional_detail(request, prof_id):
    if request.user.is_authenticated and request.user.is_staff:
        try:            
            prof = Professional.objects.get(id=prof_id)
            return render(request, 'administration/prof_detail.html',
                              {'prof': prof })
        except ObjectDoesNotExist as e:
            print(e)
            return redirect_home()

        except Exception as e:
            return HttpResponse(e)
    else:
        return render(request, 'login/login.html')

@csrf_protect
def list_professional(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = ProfessionalListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                prof = form.cleaned_data['professional']
                return redirect('administration:professional_detail', prof_id=prof.id)
            else:
                return HttpResponseRedirect('/administration/')
        else:
            form = ProfessionalListForm()
            return render(request, 'administration/list_professional.html',
                          {'form': form})
    else:
        return render(request, 'login/login.html')


def secretary_detail(request, secretary_id):
    if request.user.is_authenticated and request.user.is_staff:
        try:            
            secretary = Secretary.objects.get(id=secretary_id)
            return render(request, 'administration/secretary_detail.html',
                              {'secretary': secretary })
        except ObjectDoesNotExist as e:
            print(e)
            return redirect_home()

        except Exception as e:
            return HttpResponse(e)
    else:
        return render(request, 'login/login.html')

@csrf_protect
def list_secretary(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = SecretaryListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                secretary = form.cleaned_data['secretary']
                return redirect('administration:secretary_detail', secretary_id=secretary.id)
            else:
                return HttpResponseRedirect('/administration/')
        else:
            form = SecretaryListForm()
            return render(request, 'administration/list_secretary.html',
                          {'form': form})
    else:
        return render(request, 'login/login.html')


def patient_detail(request, patient_id):
    if request.user.is_authenticated and request.user.is_staff:
        try:            
            patient = Patient.objects.get(id=patient_id)
            return render(request, 'administration/patient_detail.html',
                              {'patient': patient })
        except ObjectDoesNotExist as e:
            print(e)
            return redirect_home()

        except Exception as e:
            return HttpResponse(e)
    else:
        return render(request, 'login/login.html')

@csrf_protect
def list_patient(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = PatientListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                patient = form.cleaned_data['patient']
                return redirect('administration:patient_detail', patient_id=patient.id)
            else:
                return HttpResponseRedirect('/administration/')
        else:
            form = PatientListForm()
            return render(request, 'administration/list_patient.html',
                          {'form': form})
    else:
        return render(request, 'login/login.html')


@csrf_protect
def create_professional(request):
    if request.user.is_authenticated and request.user.is_staff:
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
                is_staff = form.cleaned_data['is_staff']
                is_active = form.cleaned_data['is_active']

                entered_username = User.objects.filter(username=username).first()
                if entered_username is None:
                    new_user = User.objects.create_user(username=username,
                                                        email=email,
                                                        password=password,
                                                        first_name=first_name,
                                                        last_name=last_name,
                                                        is_staff=is_staff,
                                                        is_active=is_active,)
                    prof_group = Group.objects.get(name='Profesionales')
                    new_user.groups.add(prof_group)
                    new_user.save()

                    new_professional = Professional.objects.create(
                        user=new_user,
                        dni=dni,
                        phone_number=phone_number,
                        profession=profession,
                        is_coordinator=is_coordinator)
                    new_professional.save()
                    add_log(request.user.username, "add", "prof", new_professional.user.username)
                    return HttpResponseRedirect('/administration/')
                else:
                    # We prepopulate the form with the previous values
                    # except the username, and return an error message
                    pre_data = {'email': email,
                                'first_name': first_name,
                                'last_name': last_name,
                                'dni': dni, 'phone_number': phone_number,
                                'profession': profession,
                                'is_coordinator': is_coordinator,
                                'is_active':is_active,
                                }
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
def modify_professional_menu(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = ProfessionalListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                professional = form.cleaned_data['professional']
                return redirect('administration:modify_professional', prof_id=professional.id)
            else:
                return HttpResponseRedirect('/administration/')
        # if a GET (or any other method) we'll create a blank form
        else:
            form = ProfessionalListForm()
            return render(request, 'administration/modify_prof_menu.html',
                          {'form': form})
    else:
        return render(request, 'login/login.html')


@csrf_protect
def modify_professional(request, prof_id):
    if request.user.is_authenticated and request.user.is_staff:
        prof = Professional.objects.get(id=prof_id)
        if request.method == 'POST':
            form = ProfessionalEditForm(request.POST)

            if form.is_valid():
                # Check if username is available
                new_username = form.cleaned_data['username']
                username_user = Professional.objects.filter(user__username=new_username).exclude(id=prof_id).first()
                # Exclude the professional from the querylist

                if username_user is None:
                    prof.user.username = new_username
                    prof.user.email = form.cleaned_data['email']
                    prof.user.first_name = form.cleaned_data['first_name']
                    prof.user.last_name = form.cleaned_data['last_name']
                    prof.dni = form.cleaned_data['dni']
                    prof.phone_number = form.cleaned_data['phone_number']
                    prof.profession = form.cleaned_data['profession']
                    prof.is_coordinator = form.cleaned_data['is_coordinator']
                    prof.user.is_staff = form.cleaned_data['is_staff']
                    prof.user.is_active = form.cleaned_data['is_active']
                    prof.user.save()
                    prof.save()
                    add_log(request.user.username, "mod", "prof", prof.user.username)
                    return HttpResponseRedirect('/administration/')
                else:
                    error_message = "El nombre de usuario ya existe, elija otro"
                    return render(request, 'administration/modify_professional.html',
                          {'form': form, 'prof_id': prof_id,
                            'error_message': error_message})

        # if a GET (or any other method) we'll create the populated form
        else:
            # Create a form instance and populate it with data from the request
            pre_data = {'username': prof.user.username,
                        'email': prof.user.email,
                        'first_name': prof.user.first_name,
                        'last_name': prof.user.last_name,
                        'dni': prof.dni,
                        'phone_number': prof.phone_number,
                        'profession': prof.profession,
                        'is_coordinator': prof.is_coordinator,
                        'is_staff': prof.user.is_staff,
                        'is_active': prof.user.is_active,
                        }
            form = ProfessionalEditForm(initial=pre_data)
            return render(request, 'administration/modify_professional.html',
                          {'form': form, 'prof_id': prof.id})
    else:
        return render(request, 'login/login.html')


@csrf_protect
def delete_professional(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = ProfessionalListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                professional = form.cleaned_data['professional']
                add_log(request.user.username, "del", "prof", professional.user.username)
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
    if request.user.is_authenticated and request.user.is_staff:
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
                is_active = form.cleaned_data['is_active']

                entered_username = User.objects.filter(username=username).first()
                if entered_username is None:
                    new_user = User.objects.create_user(username=username,
                                                        email=email,
                                                        password=password,
                                                        first_name=first_name,
                                                        last_name=last_name,
                                                        is_staff=True,
                                                        is_active=is_active,)
                    secr_group = Group.objects.get(name='Secretarias')
                    new_user.groups.add(secr_group)

                    new_user.save()
                    new_secretary = Secretary.objects.create(
                        user=new_user,
                        dni=dni,
                        phone_number=phone_number)
                    new_secretary.save()
                    add_log(request.user.username, "add", "secr", new_secretary.user.username)
                    return HttpResponseRedirect('/administration/')
                else:
                    # We prepopulate the form with the previous values
                    # except the username, and return an error message
                    pre_data = {'email': email,
                                'first_name': first_name,
                                'last_name': last_name, 'dni': dni,
                                'phone_number': phone_number,
                                'is_active': is_active,
                               }
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


@csrf_protect
def modify_secretary_menu(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = SecretaryListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                secretary = form.cleaned_data['secretary']
                return redirect('administration:modify_secretary', secretary_id=secretary.id)
            else:
                return HttpResponseRedirect('/administration/')
        # if a GET (or any other method) we'll create a blank form
        else:
            form = SecretaryListForm()
            return render(request, 'administration/modify_secr_menu.html',
                          {'form': form})
    else:
        return render(request, 'login/login.html')


@csrf_protect
def modify_secretary(request, secretary_id):
    if request.user.is_authenticated and request.user.is_staff:
        secr = Secretary.objects.get(id=secretary_id)
        if request.method == 'POST':
            form = SecretaryEditForm(request.POST)
            if form.is_valid():
                # Check if username is available
                # remove the current secretary from the querylist

                new_username = form.cleaned_data['username']
                username_user = Secretary.objects.filter(user__username=new_username).exclude(id=secretary_id).first()

                if username_user is None:
                    secr.user.username = new_username
                    secr.user.email = form.cleaned_data['email']
                    secr.user.first_name = form.cleaned_data['first_name']
                    secr.user.last_name = form.cleaned_data['last_name']
                    secr.user.is_active = form.cleaned_data['is_active']
                    secr.dni = form.cleaned_data['dni']
                    secr.phone_number = form.cleaned_data['phone_number']
                    secr.user.save()
                    secr.save()
                    add_log(request.user.username, "mod", "secr", secr.user.username)
                else:
                    error_message = "El nombre de usuario ya existe, elija otro"
                    return render(request, 'administration/modify_secretary.html',
                          {'form': form, 'secretary_id': secretary_id,
                            'error_message': error_message})
            else:
                error_message = "Entrada(s) invalida(s)"
                return render(request, 'administration/modify_secretary.html',
                          {'form': form, 'secretary_id': secretary_id,
                            'error_message': error_message})
            return HttpResponseRedirect('/administration/')
        # if a GET (or any other method) we'll create the populated form
        else:
            # Create a form instance and populate it with data from the request
            pre_data = {'username': secr.user.username,
                        'email': secr.user.email,
                        'first_name': secr.user.first_name,
                        'last_name': secr.user.last_name,
                        'dni': secr.dni,
                        'phone_number': secr.phone_number,
                        'is_active': secr.user.is_active,
                        }
            form = SecretaryEditForm(initial=pre_data)
            return render(request, 'administration/modify_secretary.html',
                          {'form': form, 'secretary_id': secretary_id})
    else:
        return render(request, 'login/login.html')


@csrf_protect
def delete_secretary(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = SecretaryListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                secretary = form.cleaned_data['secretary']
                add_log(request.user.username, "del", "secr", secretary.user.username)
                secretary.user.delete()
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
@csrf_protect
def create_patient(request):
    if request.user.is_authenticated and request.user.is_staff:
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
                    add_log(request.user.username, "add", "patient", new_patient.__str__())
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


@csrf_protect
def modify_patient_menu(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = PatientListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                patient = form.cleaned_data['patient']
                return redirect('administration:modify_patient', patient_id=patient.id)
            else:
                return HttpResponseRedirect('/administration/')
        else:
            form = PatientListForm()
            return render(request, 'administration/modify_patient_menu.html',
                          {'form': form})
    else:
        return render(request, 'login/login.html')


@csrf_protect
def modify_patient(request, patient_id):
    if request.user.is_authenticated and request.user.is_staff:
        patient = Patient.objects.get(id=patient_id)
        if request.method == 'POST':
            form = PatientForm(request.POST)
            if form.is_valid():
                # CHECK IF DNI IS AVAILABLE
                dni = form.cleaned_data['dni']
                dni_patient = Patient.objects.filter(dni=dni).exclude(id=patient_id).first()
                # We remove the current dni from the queryset so it doesn't
                # take it as if it is already in the database
                if dni_patient is None:
                    patient.dni = dni
                    patient.first_name = form.cleaned_data['first_name']
                    patient.last_name = form.cleaned_data['last_name']
                    patient.birthdate = form.cleaned_data['birthdate']
                    patient.health_insurance = form.cleaned_data['health_insurance']
                    patient.phone_number = form.cleaned_data['phone_number']
                    patient.save()
                    add_log(request.user.username, "mod", "patient", patient.__str__())
                else:
                    error_message = "El DNI del paciente ya existe, elija otro"
                    return render(request, 'administration/modify_patient.html',
                          {'form': form, 'patient_id': patient_id,
                            'error_message': error_message})
            else:
                error_message = "Entrada(s) invalida(s)"
                return render(request, 'administration/modify_patient.html',
                          {'form': form, 'patient_id': patient_id,
                            'error_message': error_message})
            return HttpResponseRedirect('/administration/')
        # if a GET (or any other method) we'll create the populated form
        else:
            # Create a form instance and populate it with data from the request
            pre_data = {'first_name': patient.first_name,
                        'last_name': patient.last_name,
                        'birthdate': patient.birthdate,
                        'health_insurance': patient.health_insurance,
                        'phone_number': patient.phone_number,
                        'dni': patient.dni}

            form = PatientForm(initial=pre_data)
            return render(request, 'administration/modify_patient.html',
                          {'form': form, 'patient_id': patient_id})
    else:
        return render(request, 'login/login.html')


@csrf_protect
def delete_patient(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = PatientListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                patient = form.cleaned_data['patient']
                add_log(request.user.username, "del", "patient", patient.__str__())
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
@csrf_protect
def create_case(request):
    if request.user.is_authenticated and request.user.is_staff:
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
                    add_log(request.user.username, "add", "case", new_case.log_str())
                    return HttpResponseRedirect('/administration/')
                else:
                    form = CaseForm(request.POST)
                    error_message = "El caso ya existe."
                    return render(request, 'administration/create_case.html',
                                  {'form': form,
                                   'error_message': error_message})
        else:
            form = CaseForm()
        return render(request, 'administration/create_case.html',
                      {'form': form})
    else:
        return render(request, 'login/login.html')


@csrf_protect
def modify_case_menu(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = CaseListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                case = form.cleaned_data['case']
                return redirect('administration:modify_case', case_id=case.id)
            else:
                return HttpResponseRedirect('/administration/')
        else:
            form = CaseListForm()
            return render(request, 'administration/modify_case_menu.html',
                          {'form': form})
    else:
        return render(request, 'login/login.html')


@csrf_protect
def modify_case(request, case_id):
    if request.user.is_authenticated and request.user.is_staff:
        case = Case.objects.get(id=case_id)

        if request.method == 'POST':
            form = CaseForm(request.POST)
            if form.is_valid():
                # Check if the case is already in the database
                patient = form.cleaned_data['patient']
                professional = form.cleaned_data['professional']
                coordinator = form.cleaned_data['coordinator']
                new_case = Case.objects.filter(patient=patient).filter(professional=professional).filter(coordinator=coordinator).exclude(id=case_id).first()

                # We remove the current dni from the queryset so it doesn't
                # take it as if it is already in the database
                if new_case is None:
                    case.patient = patient
                    case.professional = professional
                    case.coordinator = coordinator
                    case.save()
                    add_log(request.user.username, "mod", "case", case.log_str())
                else:
                    error_message = "El caso ya existe, elija otra combinación"
                    return render(request, 'administration/modify_case.html',
                          {'form': form, 'case_id': case_id,
                            'error_message': error_message})
            else:
                error_message = "Entrada(s) invalida(s)"
                return render(request, 'administration/modify_case.html',
                          {'form': form, 'case_id': case_id,
                            'error_message': error_message})
            return HttpResponseRedirect('/administration/')
        # if a GET, we'll create the populated form
        else:
            # Create a form instance and populate it with data from the request
            pre_data = {'patient': case.patient,
                        'professional': case.professional,
                        'coordinator': case.coordinator}

            form = CaseForm(initial=pre_data)
            return render(request, 'administration/modify_case.html',
                          {'form': form, 'case_id': case_id})
    else:
        return render(request, 'login/login.html')    

@csrf_protect
def delete_case(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = CaseListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                case = form.cleaned_data['case']
                add_log(request.user.username, "del", "case", case.log_str())
                case.delete()
            return HttpResponseRedirect('/administration/')
        # if a GET (or any other method) we'll create a blank form
        else:
            form = CaseListForm()
            return render(request, 'administration/delete_case.html',
                          {'form': form})
    else:
        return render(request, 'login/login.html')
