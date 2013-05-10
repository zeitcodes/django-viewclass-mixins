from django.db import models


class TestModel(models.Model):
    name = models.CharField(max_length=100, default='Name')
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name