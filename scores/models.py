from django.db import models
from django_mysql.models import JSONField, Model


class Score(Model):
    nickname = models.CharField(max_length=200)
    result = JSONField()
