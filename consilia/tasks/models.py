from django.db import models


class Tasks(models.Model):
    class Status(models.IntegerChoices):
        TODO = 0, 'To do'
        IN_PROGRESS = 1, 'In progress'
        DONE = 2, 'Done'

    title = models.CharField(max_length=255, blank=False)
    content = models.TextField(blank=True)
    status = models.IntegerField(choices=Status)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
