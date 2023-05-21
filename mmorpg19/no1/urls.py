from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from .views import PostList, Postview

urlpatterns = [
    path('', PostList.as_view(), name='all'),
    path('<int:pk>', Postview.as_view()),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)