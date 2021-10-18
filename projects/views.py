from django.shortcuts import render
from .models import *
from django.views.generic import DetailView


def getProjectsAsManager(user_id):
    return list(Project.objects.filter(
        manager__id=user_id).order_by('-created'))


def getProjectsAsDeveloper(user_id):
    return list(Project.objects.filter(
        developers__id=user_id).order_by('-created'))


def getProjectsAsReporter(user_id):
    p_ids = set(Thread.objects.filter(
        reporter__id=user_id).values_list('project__id', flat=True))
    return list(set(Project.objects.filter(
        pk__in=p_ids).order_by('-created')))


def projectDashboard(request):
    user = request.user
    user_id = user.id
    pm = getProjectsAsManager(user_id)
    pd = getProjectsAsDeveloper(user_id)
    pr = getProjectsAsReporter(user_id)
    projects = {
        "pm": pm, "pd": pd, "pr": pr
    }
    return render(request, 'dashboard.html', context=projects)


def explore(request):
    return render(request, 'explore.html')


class ProjectDetail(DetailView):
    model = Project
    template_name = 'project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        pr = ctx['project']
        ctx['isManager'] = pr.manager.id == self.request.user.id
        return ctx


def ThreadList(request, projectId):
    threads = list(Thread.objects.filter(
        project__id=projectId).order_by('-created'))
    print(threads)
    project = Project.objects.get(id=projectId)
    return render(request, 'thread_list.html', context={"threads": threads, "project": project})


class ThreadDetail(DetailView):
    model = Thread
    template_name = 'thread_details.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comments'] = list(Comment.objects.filter(
            thread__id=ctx['thread'].id).order_by('-created'))
        return ctx


def CommentList(request, pk):
    comments = list(Comment.objects.filter(
        thread__id=pk).order_by('-created'))
    print(comments)
    return render(request, 'comment_list.html', context={"comments": comments})
