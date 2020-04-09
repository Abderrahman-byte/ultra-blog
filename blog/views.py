from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.db.models import Q

from .forms import CreateArticleForm

from markdown2 import Markdown
from .models import Article, Tag, Clap

import json

def index(request) :
    articles = Article.objects.all().order_by('-date_created')
    trends = articles.order_by('-views')
    try :
        fav_tags_ids = [tag.id for tag in request.user.profil.fav_tags.all()]
        recomended = list()

        for article in articles :
            tags = [tag.id for tag in article.tags.all()]
            for fav in fav_tags_ids :
                if fav in tags :
                    recomended.append(article)
                    break
        
        context = { 'recomended': recomended[:4], 'latest': articles[:4], 'trends': trends[:4] }
    except :
        context = { 'recomended': None, 'latest': articles[:4], 'trends': trends }

    return render(request, 'blog/index.html', context)

@login_required(login_url='auth:login')
def userProfilView(request, id) :
    try :
        user = User.objects.get(pk=id)
    except :
        raise Http404()

    articles = user.article_set.all().order_by('-date_created')

    return render(request, 'blog/profil.html', { 'user': user, 'articles': articles })

def articleView(request, id) :
    try :
        article = Article.objects.get(pk=id)
    except :
        raise Http404()

    try :
        user_clap = Clap.objects.get(user=request.user, article=article)
    except :
        user_clap = None

    article.views += 1
    article.save()

    markdowner = Markdown(extras=['fenced-code-blocks'])
    content = markdowner.convert(article.content)
    claps_count = article.clap_set.all().count()

    tags = article.tags.all()
    features = Article.objects.filter(tags__in=tags).exclude(id=str(article.id)).order_by('-views')
    articles = Article.objects.all().order_by('-date_created')

    context = { 
        'article': article, 
        'content': content, 
        'claps_count': claps_count, 
        'user_clap': user_clap, 
        'features': features[0:3],
        'latest': articles[0:3]
    }
    return render(request, 'blog/article.html', context)

@login_required(login_url='auth:login')
def createArticleView(request) :
    if request.method == 'GET' :
        form = CreateArticleForm()
        context = { 'form' : form, 'title': 'Create New Article', 'btn': 'create' }
        return render(request, 'blog/create_article.html', context)

    if request.method == 'POST' :
        user = request.user
        form = CreateArticleForm(request.POST)

        if form.is_valid() :
            d = {**request.POST}
            article = form.save(commit=False)
            article.author = user
            article.save()

            for tag_id in d.get('tags') :
                tag = Tag.objects.get(pk=tag_id)
                article.tags.add(tag)

            return redirect(reverse('blog:article_details', args=[str(article.id)]))

        else :
            for error in form.errors :
                messages.error(request, form.errors.get(error)[0])

            context = { 'form' : form, 'title': 'Create New Article', 'btn': 'create' }
            return render(request, 'blog/create_article.html', context)

@login_required(login_url='auth:login')
def updateArticleView(request, id) :
    try :
        article = Article.objects.get(pk=id)
    except :
        raise Http404()

    if request.user != article.author and not request.user.is_staff :
        return HttpResponse('You not allowed')
    
    elif request.method == 'GET' :
        form = CreateArticleForm(instance=article)
        context = { 'form' : form, 'title': 'Update Article', 'btn': 'save' }
        return render(request, 'blog/create_article.html', context)

    elif request.method == 'POST' :
        form = CreateArticleForm(request.POST, instance=article)

        if form.is_valid() :
            article = form.save()
            return redirect(reverse('blog:article_details', args=[str(article.id)]))
        else :
            for error in form.errors :
                messages.error(request, form.errors.get(error)[0])

            context = { 'form' : form, 'title': 'Update Article', 'btn': 'save' }
            return render(request, 'blog/create_article.html', context)

@login_required(login_url='auth:login')
def deleteArticleView(request, id) :
    try :
        article = Article.objects.get(pk=id)
    except :
        raise Http404()

    if article.author != request.user and not request.user.is_staff :
        return HttpResponse('You are not allowed')

    elif request.method == 'GET' :
        return render(request, 'blog/delete_article.html', { 'article': article })

    elif request.method == 'POST' :
        article.delete()
        return redirect(reverse('blog:index'))

@login_required(login_url='auth:login')
def addClap(request, id) :
    try :
        article = Article.objects.get(pk=id)
    except :
        raise Http404()

    user = request.user 
    clap = Clap.objects.create(article=article, user=user)

    return HttpResponse(json.dumps({'status': 201, 'message': 'clap created'}), status=201)

@login_required(login_url='auth:login')
def deleteClap(request, id) :
    try :
        article = Article.objects.get(pk=id)
        user = request.user
        clap = Clap.objects.get(article=article, user=user)
        clap.delete()
    except :
        raise Http404()

    return HttpResponse(json.dumps({'status': 201, 'message': 'clap deleted'}), status=201)

def searchView(request) :
    query = request.GET.get('q')

    if query != '' :
        users = User.objects.filter(
            Q(first_name__startswith=query) | 
            Q(last_name__startswith=query) | 
            Q(username__startswith=query)
        )

        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(overview__icontains=query)
        )
    else :
        users = []
        articles = []

    context = { 'query': query, 'users': users, 'articles': articles }
    return render(request, 'blog/search.html', context)
