from . import views
from django.urls import path

from django.conf import settings

app_name = 'core'

urlpatterns = [

    path('dashboard',views.dashboard, name='dashboard'),
    path('',views.user_list, name='user_list'),
    path('admin_list/',views.admin_list, name='admin_list'),
    path('add_guest/',views.add_guest, name='add_guest'),
    path('profile/<int:pk>',views.profile, name='profile'),
    path('send_invite/<int:pk>',views.send_invite_email, name='send_invite_email'),
    path('delet_user/<int:pk>',views.delet_user, name='delet_user'),
    path('delet_user2/<int:pk>',views.delet_user2, name='delet_user2'),
    path('upload/',views.upload, name='upload'),
    path('toggle_blacklist/<int:pk>/', views.toggle_blacklist, name='toggle_blacklist'),
    path('checkin/<int:pk>/', views.checkin, name='checkin'),
    path('batch_upload_guests/', views.batch_upload_guests, name='batch_upload_guests'),
    path('send_invite_to_all_guests/', views.send_invite_to_all_guests, name='send_invite_to_all_guests'),
]
