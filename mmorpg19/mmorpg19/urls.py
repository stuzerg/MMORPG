"""mmorpg19 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import path, include

from no1.views import ListUserPosts, Kreator, PostEdit, PostDelete,ReviewKreator, ReviewList, review_action, SubsView, PostList

urlpatterns = [
    path('', PostList.as_view()),
    path('subscribe/', SubsView.as_view(), name='rvws'),
    path('review_action/<int:pk>', review_action),
    path('review/', ReviewList.as_view(), name='rvws'),
    path('review/<int:pk>', ReviewKreator.as_view(), name='revs'),
    path('edit/<int:pk>', PostEdit.as_view(), name='edit'),
    path('kill/<int:pk>', PostDelete.as_view(), name='kill'),
    path('all/', include('no1.urls'), name='main'),
    path('user/<int:pk>', ListUserPosts.as_view(), name='user'),
    path('create/', Kreator.as_view(), name='kreator'),
    path('login/', include('loginapp.urls')),
    path('logout/', LogoutView.as_view(template_name = 'logout.html'), name='logout'),
    path('admin/', admin.site.urls),
    path('sign/', include('sign.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/login/', include('loginapp.urls'))
]
