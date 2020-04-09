from django.urls import path

from . import views

app_name = 'auth'

urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('register/', views.registerView, name='register'),
    path('logout/', views.logoutView, name='logout'),
    path('settings/', views.SettingsView, name='settings'),
    path('profil/', views.ProfilView, name='profil'),

    path('fav_tags/update/', views.UpdateFavTags, name='update_tags')
]