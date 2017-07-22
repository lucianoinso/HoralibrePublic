from . import views
# from commentary import views as comment_views

urlpatterns = [
    url(r'^$', views.news_home, name='news_home'),
    url(r'^article/(?P<article_id>[0-9]+)$', views.article_detail, name='article_detail'),
    url(r'^create/article$', views.create_article, name='create_article'),
    url(r'^modify/article$', views.modify_article_menu, name='modify_article_menu'),
    url(r'^modify/article/(?P<article_id>[0-9]+)$', views.modify_article, name='modify_article'),
    url(r'^delete/article$', views.delete_article, name='delete_article'),
]
