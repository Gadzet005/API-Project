from django.contrib import admin
from django.urls import path, include

from config.settings import config


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('posts.urls')),
]

if config.STATE == "DEV":
    urlpatterns.append(
        path("__debug__/", include("debug_toolbar.urls"))
    )
