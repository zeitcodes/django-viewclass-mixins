from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=100, default='Name')
    created = models.DateTimeField(default=datetime.now())
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class Book(models.Model):
    author = models.ForeignKey(Author)
    title = models.CharField(max_length=100, default='Title')
    created = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return self.title