# Django libs
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

# Project libs
from login.views import redirect_home
from .models import Comment
from records.models import Record
from records.views import redirect_record


def new_comment(request, record_id):
    record = get_object_or_404(Record, pk=record_id)

    if request.user.is_authenticated:
        if (request.user == record.professional):
            user = User.objects.get(username=request.user.username)

            if request.method == "POST":
                if request.POST.get("comment_text"):
                    comment = Comment(professional=user, record=record, text=request.POST.get("comment_text"))
                comment.save()

                return redirect_record(record_id)
            else:
                return render(request, 'commentary/new_comment.html', {'record': record})
        else:
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")

def modify_comment(request, record_id, comment_id):
    record = get_object_or_404(Record, pk=record_id)
    
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user.is_authenticated:
        if (request.user == record.professional):
            if request.method == "POST":
                if request.POST.get("comment_text"):
                    comment.text = request.POST.get("comment_text")
                comment.save()

                return redirect_record(record_id)
            else:
                return render(request, 'commentary/modify_comment.html',
                              {'record': record, 'comment': comment })
        else:
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")

def delete_comment(request, record_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    record = get_object_or_404(Record, pk=record_id)
    if request.user.is_authenticated:
        if (request.user == record.professional):
            if request.method == "GET":
                comment.delete()
            return redirect_record(record_id)
        else:
            return redirect_home(request.user.username)
    else:
        return HttpResponseRedirect("/login")

