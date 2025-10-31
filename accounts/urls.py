from . import views
from django.urls import path

from django.conf import settings

app_name = 'accounts'

urlpatterns = [

    path('login/',views.my_login, name='login'),
    path('add_user/',views.register, name='register'),
    path('add_staff/',views.register2, name='register2')

]
