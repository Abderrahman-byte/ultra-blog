from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),

    path('user_profil/<id>/', views.userProfilView, name='user_profil'),

    path('articles/<uuid:id>/', views.articleView, name='article_details'),
    path('articles/<uuid:id>/delete/', views.deleteArticleView, name='delete_article'),
    path('articles/<uuid:id>/edit/', views.updateArticleView, name='update_article'),
    path('articles/new/', views.createArticleView, name='new_article'),

    path('search/', views.searchView, name='search'),

    path('articles/<uuid:id>/clap/', views.addClap, name='add_clap'),
    path('articles/<uuid:id>/clap/delete', views.deleteClap, name='delete_clap'),
]