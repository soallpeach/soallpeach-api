from django.db import models
from django_mysql.models import JSONField, Model


class Round(Model):
    id = models.IntegerField(primary_key=True)
    challenge_name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=30, choices=[('STARTED', 'STARTED'), ('FINISHED', 'FINISHED')],
                             default='STARTED')
    updated = models.DateTimeField(auto_now=True)


class Score(Model):
    nickname = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    result = JSONField()
    state = models.CharField(max_length=30, choices=[('PASSED', 'PASSED'), ('FAILED', 'FAILED')])
    round = models.ForeignKey(to=Round, on_delete=models.CASCADE, default=None, null=True)
