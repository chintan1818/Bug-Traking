from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *


def withLogin(view, login_url='/auth/signin'):
    return login_required(view, login_url=login_url)


urlpatterns = [
    path('', withLogin(projectDashboard), name='dashboard'),
    path('explore', explore, name='explore'),
    path('<int:pk>/', ProjectDetail.as_view(), name='project_details'),
    path('<int:pk>/threads',ThreadList,name='thread_list'),
    path('threads/<int:pk>',ThreadDetail.as_view(),name='thread_details'),
    path('threads/<int:pk>/comment',CommentList, name='comment_list')
]
