# Django imports
from django.contrib import admin

# Project imports
from .models import Comment

admin.site.register(Comment)