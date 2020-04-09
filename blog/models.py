from django.db import models
from django.contrib.auth.models import User

import uuid

class Tag(models.Model) :
    name = models.CharField(max_length=200)

    def __str__(self) :
        return self.name

class Article(models.Model) :
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    overview = models.TextField(max_length=5000)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    class Meta :
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'], name='non_duplicated_titles'),
            models.UniqueConstraint(fields=['content'], name='unique_article_content')
        ]

    def __str__(self) :
        return f'{self.title} by {self.author.username}'

    def get_tags(self) :
        return ' '.join(['#' + tag.name.replace(' ', '_') for tag in self.tags.all()])

    get_tags.short_description = 'Tags'

class Clap(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta :
        constraints = [
            models.UniqueConstraint(fields=['user', 'article'], name='unique_clap_user_article')
        ]