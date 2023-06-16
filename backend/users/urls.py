from django.urls import path, include

from users.views import UserViewSet
from users.routers import UsersRouter


router = UsersRouter()
router.register("users", UserViewSet, "users")

urlpatterns = [
    path('', include(router.urls)),
]
