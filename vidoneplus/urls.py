"""vidoneplus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from vidoneplus.views import *

urlpatterns = [
    path('', index, name="index"),
    path('validate_course/', validate_course),
    path('admin/', admin.site.urls),
    path('accounts/', include('client.urls')),
    path('course/', include('course.urls')),
    path('order/', include('order.urls')),
    path('page_not_found/', page_not_found, name='page_not_found'),
    path('page_not_found/<str:text>/', page_not_found, name='page_not_found'),
    path('page_not_found/<str:text>/<str:previous_url>/', page_not_found, name='page_not_found'),
]
