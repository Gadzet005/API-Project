from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet


router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
