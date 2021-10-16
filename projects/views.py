from django.shortcuts import render
from .models import *


def getProjectsAsManager(user_id):
    return list(Project.objects.filter(
        manager__id=user_id).order_by('-created'))


def getProjectsAsDeveloper(user_id):
    return list(Project.objects.filter(
        developers__id=user_id).order_by('-created'))


def getProjectsAsReporter(user_id):
    p_ids = set(Thread.objects.filter(
        reporter__id=user_id).values_list('project__id', flat=True))
    print(p_ids)
    return list(set(Project.objects.filter(
        pk__in=p_ids).order_by('-created')))


def projectDashboard(request):
    user = request.user
    user_id = user.id
    pm = getProjectsAsManager(user_id)
    pd = getProjectsAsDeveloper(user_id)
    pr = getProjectsAsReporter(user_id)
    print('As Manager:', pm)
    print('As Developer:', pd)
    print('As Reporter:', pr)
    projects = {
        "pm": pm, "pd": pd, "pr": pr
    }
    return render(request, 'dashboard.html', context=projects)


def explore(request):
    return render(request, 'explore.html')
