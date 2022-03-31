# -*- coding: utf-8 -*-
# Django libs
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q

# Project libs
from login.views import redirect_home
from records.models import Patient, Record, Professional, Case
from .models import Comment
from records.views import redirect_record


def new_comment(request, patient_id, record_id):
    record = get_object_or_404(Record, id=record_id)

    if request.user.is_authenticated:
        professional = Professional.objects.get(user=request.user)
        patient = Patient.objects.get(id=patient_id)
        case = Case.objects.all().filter(Q(professional=professional) | Q(coordinator=professional)
                                        ,Q(patient=patient))

        if case:
            if request.method == "POST":
                if request.POST.get("comment_text"):
                    comment = Comment(owner=professional, record=record, text=request.POST.get("comment_text"))
                    comment.save()
                return redirect_record(patient.id, record.id)
            else:
                return render(request, 'commentary/new_comment.html', {'record': record})
        else:
            return redirect_home()
    else:
        return HttpResponseRedirect("/login")


def edit_comment(request, patient_id, record_id, comment_id):
    record = get_object_or_404(Record, id=record_id)

    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if (request.user == comment.owner.user):
            if request.method == "POST":
                if request.POST.get("comment_text"):
                    comment.text = request.POST.get("comment_text")
                comment.save()

                return redirect_record(patient_id, record.id)
            else:
                return render(request, 'commentary/edit_comment.html',
                              {'record': record, 'comment': comment })
        else:
            return redirect_home()
    else:
        return HttpResponseRedirect("/login")


def delete_comment(request, patient_id, record_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    record = get_object_or_404(Record, id=record_id)
    if request.user.is_authenticated:
        if (request.user == comment.owner.user):
            if request.method == "GET":
                comment.delete()
            return redirect_record(patient_id, record.id)
        else:
            return redirect_home()
    else:
        return HttpResponseRedirect("/login")