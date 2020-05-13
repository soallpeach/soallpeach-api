from collections import namedtuple

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
    reason = models.CharField(max_length=2000, null=True, default='')
    main_indicator = models.FloatField(default=None, null=True)
    state = models.CharField(max_length=30, choices=[('PASSED', 'PASSED'), ('FAILED', 'FAILED')])
    round = models.ForeignKey(to=Round, on_delete=models.CASCADE)

    @property
    def commit_info(self):
        CommitInfo = namedtuple("CommitInfo", "repository_url hash subject repo_type")
        result = dict(self.result)
        commit_info = result.get('commit_info')
        if commit_info is None:
            return None
        repo_url = str(commit_info['repository_url']).lower()
        if 'github' in repo_url:
            commit_info['repo_type'] = "github"
        elif 'gitlab' in repo_url:
            commit_info['repo_type'] = "gitlab"
        elif 'bitbucket' in repo_url:
            commit_info['repo_type'] = "bitbucket"
        else:
            commit_info['repo_type'] = "unknown"
        return CommitInfo(**commit_info)
