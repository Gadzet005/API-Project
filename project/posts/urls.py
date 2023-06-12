from django.urls import path

from posts.views import PostListAPIView, PostAPIView


app_name = "posts"

urlpatterns = [
    path("list/", PostListAPIView.as_view(), name="list"),
    path("post/<int:post_id>/", PostAPIView.as_view(), name="post"),
]
