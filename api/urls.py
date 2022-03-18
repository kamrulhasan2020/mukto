from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path(
        "comments/<str:board>/<str:no>/", views.CommentList.as_view(),
        name="comments"
    ),

    path(
        "latest/comment/<str:board>/<str:no>/",
        views.LatestComment.as_view(),
        name="latest_comment",
    ),
]