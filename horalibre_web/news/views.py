# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Django Imports
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import Group
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Project Imports
from login.views import redirect_home
from records.models import Professional, Secretary
from administration.views import add_log
from .models import Article
from .forms import ArticleForm, ArticleListForm, ArticleEditForm


def news_home(request):
    if request.user.is_authenticated:
        try:
            article_list = (Article.objects.filter(is_draft=False).order_by('-creation_date'))

            paginator = Paginator(article_list, 5) # Show 5 records per page
            page = request.GET.get('page')
            article_page = paginator.page(page)

        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            article_page = paginator.page(1)

        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            article_page = paginator.page(paginator.num_pages)

        except Exception as e:
            return HttpResponse(e)

        return render(request, 'news/home.html', {
            'article_page': article_page,
            })
    else:
        return HttpResponseRedirect("/login")

def article_detail(request, article_id):
    if request.user.is_authenticated:
        try:
            article = Article.objects.get(id=article_id)
        except Exception as e:
            return redirect_home()

        return render(request, 'news/article_detail.html', {
                      'article': article,
#                'comments': comments,
                })
    else:
        return HttpResponseRedirect("/login")


@csrf_protect
def create_article(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = ArticleForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                title = form.cleaned_data['title']
                content = form.cleaned_data['content']
                is_draft = form.cleaned_data['is_draft']

                new_article = Article.objects.create(
                    author=request.user,
                    title=title,
                    content=content,
                    is_draft=is_draft)
                new_article.save()

                add_log(request.user.username, "add", "news", new_article.log_str())
                return HttpResponseRedirect('/news/')
            else:
                form = ArticleForm()
                error_message = ("Error en los datos ingresados.")
                return render(request, 'news/create_article.html',
                              {'form': form,
                               'error_message': error_message})
        # if a GET (or any other method) we'll create a blank form
        else:
            form = ArticleForm()
        return render(request, 'news/create_article.html',
                      {'form': form})
    else:
        return render(request, 'login/login.html')


@csrf_protect
def modify_article_menu(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = ArticleListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                article = form.cleaned_data['article']
                return redirect('news:modify_article', article_id=article.id)
            else:
                return HttpResponseRedirect('/news/')
        # if a GET (or any other method) we'll create a blank form
        else:
            form = ArticleListForm()
            return render(request, 'news/modify_article_menu.html',
                          {'form': form})
    else:
        return render(request, 'login/login.html')
    



@csrf_protect
def modify_article(request, article_id):
    if request.user.is_authenticated and request.user.is_staff:
        article = Article.objects.get(id=article_id)
        if request.method == 'POST':
            form = ArticleEditForm(request.POST)

            if form.is_valid():
                article.title = form.cleaned_data['title']
                article.content = form.cleaned_data['content']
                article.is_draft = form.cleaned_data['is_draft']
                article.save()
                add_log(request.user.username, "mod", "news", article.log_str())
                return HttpResponseRedirect('/news/')
            else:
                error_message = "Entradas invalidas."
                return render(request, 'news/modify_article.html',
                      {'form': form, 'article_id': article_id,
                        'error_message': error_message})

        # if a GET (or any other method) we'll create the populated form
        else:
            # Create a form instance and populate it with data from the request
            pre_data = {'title': article.title,
                        'content': article.content,
                        'is_draft': article.is_draft,
                        }
            form = ArticleEditForm(initial=pre_data)
            return render(request, 'news/modify_article.html',
                          {'form': form, 'article_id': article.id})
    else:
        return render(request, 'login/login.html')


@csrf_protect
def delete_article(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == 'POST':
            # Create a form instance and populate it with data from the request
            form = ArticleListForm(request.POST)
            # Check whether is valid:
            if form.is_valid():
                article = form.cleaned_data['article']
                add_log(request.user.username, "del", "news", article.log_str())
                article.delete()
            return HttpResponseRedirect('/news/')
        # if a GET (or any other method) we'll create a blank form
        else:
            form = ArticleListForm()
            return render(request, 'news/delete_article.html',
                          {'form': form })
    else:
        return render(request, 'login/login.html')
