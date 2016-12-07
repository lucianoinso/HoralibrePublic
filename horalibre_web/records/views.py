from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from login.views import redirect_home
from .models import Patient, Record, Professional
from commentary.models import Comment


def patient_list(request, username="Anonymous"):
    if request.user.is_authenticated:
        if request.user.username == username:
            try:
                user = User.objects.get(username=username)
                record_list = Record.objects.filter(professional=user).distinct('patient')
            except Exception as e:
                return HttpResponse("Hubo un problema")

            return render(request, 'records/patient_list.html', {
                'record_list': record_list,
                'username': username,
                })
        else:
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")


def record_list(request, username, patient_id):
    if request.user.is_authenticated:
        if request.user.username == username:
            try:
                user = User.objects.get(username=username)
                patient = Patient.objects.get(pk=patient_id)
                record_list = Record.objects.filter(professional=user).filter(patient=patient)
            except Exception as e:
                return HttpResponse("Hubo un problema")

            return render(request, 'records/record_list.html', {
                'record_list': record_list,
                'username': username,
                'patient_id': patient_id,
                })
        else:
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")


def record_detail(request, username, patient_id, record_id):
    if request.user.is_authenticated:
        if request.user.username == username:
            try:
                record = Record.objects.get(pk=record_id)
            except Exception as e:
                return HttpResponse("Hubo un problema")

            return render(request, 'records/record_detail.html', {
                'record': record,
                })
        else:
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")


def create_record_from_patient(request, username, patient_id):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        if request.user == user:
            patient = Patient.objects.get(pk=patient_id)
            if request.method == "POST":
                record = Record(session_datetime=request.POST.get("session_datetime"),
                                session_resume=request.POST.get("session_resume"),
                                professional=user, patient=patient,
                                session_duration = request.POST.get("session_duration"))
                record.save()
                # check why username is the id, request.user.username is the user
                return redirect_patient_records(request.user.username, patient_id)
            else:
                return render(request, 'records/create_record_from_patient.html', {'user': user, 'patient': patient })
    else:
        return HttpResponseRedirect("/login")


def create_record(request, username):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        patient_list = Patient.objects.all()

        if request.user == user:
            if request.method == "POST":
                patient = Patient.objects.get(pk=request.POST.get("patient_from_list"))
                record = Record(session_datetime=request.POST.get("session_datetime"),
                                session_resume=request.POST.get("session_resume"),
                                professional=user, patient=patient,
                                session_duration = request.POST.get("session_duration"))
                record.save()
                return redirect_patient_list(request.user.username)
            else:
                return render(request, 'records/create_record.html', {'user': user, 'patient_list': patient_list })
        else:
            return redirect_patient_records(request.user.username, patient_id)
    else:
        return HttpResponseRedirect("/login")


def edit_record(request, username, patient_id, record_id):
    if request.user.is_authenticated:
        record = get_object_or_404(Record, pk=record_id)
        if request.user == record.professional:
            if request.method == "POST":
                if request.POST.get("session_datetime"):
                    record.session_datetime = request.POST.get("session_datetime")
                if request.POST.get("session_duration"):
                    record.session_duration = request.POST.get("session_duration")
                if request.POST.get("session_resume"):
                    record.session_resume = request.POST.get("session_resume")
                record.save()
                return redirect_record(username, patient_id, record_id)
            else:
                return render(request, 'records/edit_record.html', {'record': record})
    else:
        return HttpResponseRedirect("/login")


def delete_record(request, username, patient_id, record_id):
    if request.user.is_authenticated:
        record = get_object_or_404(Record, pk=record_id)
        if request.user == record.professional:
            amount_records = (Record.objects.all().filter(patient=patient_id).filter(professional=record.professional).count())
            record.delete()
            if amount_records == 1:
                return redirect_patient_list(username)
            else:
                return redirect_patient_records(request.user.username, patient_id)
    else:
        return HttpResponseRedirect("/login")


"""
def patient_list(request, username):
    if request.user.is_authenticated:
        
        goal = get_object_or_404(Goal, pk=goal_id)
        if request.user == goal.owner:
            comments = (Comment.objects.all().filter(goal=goal)
                               .order_by('-create_date'))
            return render(request, 'goal/detail.html',
                          {'goal': goal, 'comments': comments})
    return redirect_home(request.user)


def new_record(request):
    if request.user.is_authenticated:
        try:
            user = User.objects.get(username=request.user.username)
        except Exception as e:
            return HttpResponse("El usuario no existe")
        if request.method == "POST":
            finish_date = request.POST.get("finish_date")
            if finish_date == '':
                finish_date = timezone.now()
            record = record.objects.create(record_text=request.POST.get("record_text"),
                                       finish_date=finish_date,
                                       create_date=timezone.now(),
                                       priority=request.POST.get("priority"),
                                       state=request.POST.get("state"),
                                       owner=user
                                       )
            record.save()
            return redirect_home(request.user.username)
        else:
            return render(request, 'record/new_record.html')
    else:
        return HttpResponseRedirect("/login")



def detail_record(request, record_id):
    if request.user.is_authenticated:
        record = get_object_or_404(record, pk=record_id)
        if request.user == record.owner:
            comments = (Comment.objects.all().filter(record=record)
                               .order_by('-create_date'))
            return render(request, 'record/detail.html',
                          {'record': record, 'comments': comments})
    return redirect_home(request.user)
"""

def redirect_patient_list(username):
    return HttpResponseRedirect("/home/{}/patients/".format(username))


def redirect_record(username, patient_id, record_id):
    return HttpResponseRedirect("/home/{}/patients/{}/record/{}".
                                format(username, patient_id, record_id))

def redirect_patient_records(username, patient_id):
    return HttpResponseRedirect("/home/{}/patients/{}".format(username, patient_id))