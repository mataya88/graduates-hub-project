"""
URL configuration for graduateshub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
import debug_toolbar
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "GraduatesHub Administration"
admin.site.site_title = "GraduatesHub Admin"
admin.site.index_title = "Database Administration Page"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hub/', include("hub.urls")),
    path('__debug__/', include('debug_toolbar.urls')),
    path('register/', accounts_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='authenticate/login.html'), name='login'),
    path('',auth_views.LoginView.as_view(template_name='authenticate/login.html'), name='root'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authenticate/logout.html'), name='logout'),
    path('profile/me', accounts_views.profile, name='my-profile')

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT )
