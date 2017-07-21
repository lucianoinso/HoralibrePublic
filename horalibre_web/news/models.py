# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField("Texto", null=True, blank=True, max_length=5000)
    author = models.ForeignKey(User,  related_name='article_author',
                               on_delete=models.SET_NULL, null=True)
    is_draft = models.BooleanField(default=False)
    creation_date = models.DateField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.is_draft:
            draft = "(BORRADOR)"
        else:
            draft = ""

        if self.author is None:
            return (str(self.creation_date) + " , " + self.title + " - " +
                    "Autor eliminado, resumen: " + self.content[:20] + "...")
        else:
            return (str(self.creation_date) + " - Titulo:" + self.title[:30] + "..." +" - Autor:" + 
                    self.author.get_full_name() + draft)
