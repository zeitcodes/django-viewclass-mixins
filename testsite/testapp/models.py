from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import utc


class TestModel(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100, default='Name')
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return self.name

class OtherTestModel(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100, default='Name')
    visible = models.BooleanField(default=True)
    created = models.DateTimeField(default=datetime.now())

    def __unicode__(self):
        return self.name