"""fj2025 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from core.views import home, terms
urlpatterns = [
    path('javi/', admin.site.urls),
    path('',include('accounts.urls')),
    path('',include('core.urls')),
    # path('',home, name='home'),
    # path('terms_and_conditions',terms, name='terms'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

      #changing password URLs
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
    name='password_change'),
    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
    name='password_change_done'),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
