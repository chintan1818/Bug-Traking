from os import name
from django.contrib.auth.models import User
from django.db import models


class TimeStamps:
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Project(TimeStamps, models.Model):
    name = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=1024)
    manager = models.OneToOneField(User)
    developers = models.ManyToManyField(User)
    tags = models.CharField(max_length=1024)


class Thread(TimeStamps, models.Model):
    BUG_TYPE_CHOICES = (('bug', 'Bug'), ('query', 'Query'))
    BUG_PRIORITY_CHOICES = (
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ('NA', 'Not Applicable'),
        ('enhancement', 'Enhancement'),
    )

    bug_type = models.CharField(choices=BUG_TYPE_CHOICES, default='bug')
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    bug_priority = models.CharField(
        choices=BUG_PRIORITY_CHOICES, default='low')
    closed = models.BooleanField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Comment(TimeStamps, models.Model):
    ROLE_CHOICES = (
        ('contributor', 'Contributor'),
        ('developer', 'Developer'),
        ('project_manager', 'Project Manager'),
    )
    body = models.CharField(max_length=1024)
    author = models.OneToOneField(User)
    author_role = models.CharField(choices=ROLE_CHOICES, default='contributor')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
