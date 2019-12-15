"""hammerdirt_api URL Configuration


"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path, re_path
from hammerdirtApi.views import api_home
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_home, name='index'),
    path('api/', include('hammerdirtApi.urls')),
]


if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
