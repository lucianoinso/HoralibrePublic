# -*- coding: utf-8 -*-
from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from datetime import datetime

# Project imports
from records.models import Professional, Secretary
from .models import Article


class ArticleListForm(forms.Form):
    article = forms.ModelChoiceField(queryset=Article.objects.all().order_by('creation_date'),
                                     label='Novedades')


class ArticleForm(ModelForm):
#    is_draft = models.BooleanField(initial=False, required=False, label="Es borrador")
    class Meta:
        model = Article
        fields = ['title', 'content', 'is_draft']
        labels = {
            'title': 'Titulo',
            'content': 'Contenido',
            'is_draft': 'Es borrador',
        }
        error_messages = {
            'title': {
                'max_value': "El titulo ingresado es demasiado largo.",
                'invalid': "El titulo ingresado es invalido.",
            },
        }


class ArticleEditForm(ModelForm):
#    article_year_choices = set((year) for year in range(datetime.now().year - 110, datetime.now().year + 1))
#    creation_date = forms.DateField(widget=forms.SelectDateWidget(years=article_year_choices),
#                                    label='Fecha del artículo')
#    is_draft = models.BooleanField(initial=False, required=False, label="Es borrador")

    class Meta:
        model = Article
        fields = ['title', 'content', 'is_draft']
        labels = {
            'title': 'Titulo',
            'content': 'Contenido',
#            'creation_date': 'Fecha del articulo',
            'is_draft': 'Es borrador',
        }
        error_messages = {
            'title': {
                'max_value': "El titulo ingresado es demasiado largo.",
                'invalid': "El titulo ingresado es invalido.",
            },
        }
