from django.contrib.auth.models import User
from django.db import models


class TimeStamps(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Project(TimeStamps):
    name = models.CharField(max_length=128, null=False)
    description = models.CharField(max_length=1024)
    manager = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='manager')
    developers = models.ManyToManyField(User, related_name='developers')
    tags = models.CharField(max_length=1024)

    def __str__(self):
        return self.name


class Thread(TimeStamps):
    BUG_TYPE_CHOICES = (('bug', 'Bug'), ('query', 'Query'))
    BUG_PRIORITY_CHOICES = (
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ('NA', 'Not Applicable'),
        ('enhancement', 'Enhancement'),
    )

    bug_type = models.CharField(
        max_length=20, choices=BUG_TYPE_CHOICES, default='bug')
    title = models.CharField(max_length=256)
    description = models.CharField(max_length=1024)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    bug_priority = models.CharField(max_length=20,
                                    choices=BUG_PRIORITY_CHOICES, default='low')
    closed = models.BooleanField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(TimeStamps):
    ROLE_CHOICES = (
        ('contributor', 'Contributor'),
        ('developer', 'Developer'),
        ('project_manager', 'Project Manager'),
    )
    body = models.CharField(max_length=1024)
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='contributor')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

    def __str__(self):
        return self.author + ':' + self.body
