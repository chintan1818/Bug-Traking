from django.urls import path, include
from .views import *

urlpatterns = [
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    # path('signout/', name='signout')
]
