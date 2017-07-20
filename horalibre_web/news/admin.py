# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Project imports
from .models import Article

# Register your models here.

admin.site.register(Article)