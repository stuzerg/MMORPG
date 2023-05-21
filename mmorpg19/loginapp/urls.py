from django.contrib.auth.views import LoginView

from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import views
from .views import my_login1, my_login2

urlpatterns = [
    path('', views.my_login2,name='login'),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)