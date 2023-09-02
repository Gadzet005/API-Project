from django.urls import path, include
from rest_framework.authtoken import views
from config.settings import STATE


from users.views import UserViewSet
from users.routers import UsersRouter


router = UsersRouter()
router.register('users', UserViewSet, 'user')

urlpatterns = [
    path('', include(router.urls)),
    path('oauth/', views.obtain_auth_token),
]

if STATE == 'DEV':
    urlpatterns.append(
        path('auth/', include('rest_framework.urls'))
    )
