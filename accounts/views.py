from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse

from .forms import CreateUserForm, UpdateProfilForm, UpdateFavtagsForm
from .decoretors import unauthenticated_only
from blog.models import Tag

import json

@unauthenticated_only
def loginView(request) :
    if request.method == 'GET' :
        next = request.GET.get('next')
        return render(request, 'accounts/login.html', { 'next': next })
    
    if request.method == 'POST' :
        next = request.POST.get('next')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None :
            login(request, user)
            if next is not None :
                return redirect(next)
            else :
                return redirect(reverse('blog:index'))

        else :
            messages.error(request, 'username or password is wrong')
            return redirect(reverse('auth:login'))

@unauthenticated_only
def registerView(request) :
    if request.method == 'GET' :
        form = CreateUserForm()
        return render(request, 'accounts/register.html', { 'form': form })

    if request.method == 'POST' :
        form = CreateUserForm(request.POST)

        if form.is_valid() :
            user = form.save()
            login(request, user)
            return redirect(reverse('auth:profil'))
        
        else :
            for error in form.errors :
                messages.error(request, form.errors.get(error)[0])
            return render(request, 'accounts/register.html', { 'form': form })

def logoutView(request) :
    logout(request)
    return redirect(reverse('auth:login'))

@login_required(login_url='auth:login')
def SettingsView(request) :
    if request.method == 'GET' :
        profil = request.user.profil
        tags = Tag.objects.all()
        fav_tags = profil.fav_tags.all()
        p_form = UpdateProfilForm(instance=profil)
        return render(request, 'accounts/profil.html', { 'form': p_form, 'tags': tags, 'favs': fav_tags })

    if request.method == 'POST' :
        profil = request.user.profil
        p_form = UpdateProfilForm(request.POST, request.FILES, instance=profil)

        if p_form.is_valid() :
            p_form.save()
            return redirect('auth:profil')

@login_required(login_url='auth:login')
def UpdateFavTags(request) :
    if request.method == 'POST' :
        body = json.loads(request.body)
        profil = request.user.profil
        form = UpdateFavtagsForm(body, instance=profil)
        form.save()

        return HttpResponse('Updated successfully', status=200)

@login_required(login_url='auth:login')
def ProfilView(request) :
    user_id = request.user.id
    return redirect(reverse('blog:user_profil', args=[user_id]))