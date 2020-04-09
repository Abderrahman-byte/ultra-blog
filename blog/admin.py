from django.contrib import admin

from .models import Article, Tag, Clap

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin) :
    list_display = ['title', 'author', 'get_tags']

admin.site.register(Tag)
admin.site.register(Clap)