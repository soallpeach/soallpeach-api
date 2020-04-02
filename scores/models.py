from django.db import models
from django_mysql.models import JSONField, Model


class Score(Model):
    nickname = models.CharField(max_length=200)
    challenge_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    run_id = models.IntegerField()
    result = JSONField()
