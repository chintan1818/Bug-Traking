from django.urls import path, include
from .views import *

urlpatterns = [
    path('signin/', signin, name='signin'),
    path('signup/', signup, name='signup'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('signout/', signout, name='signout')
]
