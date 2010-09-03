from django.db import models
from django.db.models import Avg, Max, Min, Count

class Dog(models.Model):
    username = models.CharField()
    password = models.CharField()
    host = models.CharField()

    def __unicode__(self):
        return "%s" % self.username
    class Meta:
        db_table = 'dogs'
        app_label = "dogclients"
