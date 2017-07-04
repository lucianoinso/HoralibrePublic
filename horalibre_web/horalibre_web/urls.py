"""horalibre_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

# project views
from login import views as login_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', include('login.urls')),
    url(r'^$', login_views.login, name='login'),
    url(r'^logout$', login_views.logout, name='logout'),
    url(r'^new_user$', login_views.new_user, name='new_user'),
    url(r'^home/(?P<username>[\w.@+-]+)/$', login_views.home, name='home'),
    url(r'^home/$', login_views.home, name='home'),
    url(r'^home/(?P<username>[\w.@+-]+)/records/', include('records.urls', namespace='records')),
    url(r'^administration/', include('administration.urls', namespace='administration')),
]