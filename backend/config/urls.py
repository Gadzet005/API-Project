from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from posts.views import PostViewSet
from users.views import UserViewSet


router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")
router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
