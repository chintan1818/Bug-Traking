from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import *


def withLogin(view, login_url='/auth/signin'):
    return login_required(view, login_url=login_url)


urlpatterns = [
    path('', withLogin(projectDashboard), name='dashboard'),
    re_path(r'^explore/$', explore, name='explore'),
    path('create', withLogin(ProjectCreate.as_view()), name='create'),
    path('<int:pk>/', ProjectDetail.as_view(), name='project_details'),
    path('<int:pk>/edit', withLogin(ProjectEdit.as_view()), name='project_edit'),
    path('<int:pk>/delete', withLogin(projectDelete), name='project_delete'),
    path('<int:projectId>/threads', ThreadList, name='thread_list'),
    path('<int:projectId>/threads/<int:pk>',
         ThreadDetail.as_view(), name='thread_details'),
    path('<int:projectId>/threads/create',
         withLogin(ThreadCreate.as_view()), name='thread_create'),
    path('<int:projectId>/threads/<int:pk>/delete',
         withLogin(threadDelete), name='thread_delete'),
    path('<int:projectId>/threads/<int:pk>/edit',
         withLogin(ThreadEdit.as_view()), name='thread_edit'),
    path('<int:projectId>/threads/<int:pk>/comment',
         withLogin(CommentCreate.as_view()), name='comment_create'),
    path('<int:projectId>/threads/<int:pk>/<int:commentId>/delete',
         withLogin(commentDelete), name='comment_delete')
]
