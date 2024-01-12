from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.api import UserAPIViewSet

router = DefaultRouter()
router.register("", UserAPIViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "users/add_team/", UserAPIViewSet.as_view({"post": "add_team"}), name="add-team"
    ),
    path(
        "users/leave_team/",
        UserAPIViewSet.as_view({"post": "leave_team"}),
        name="leave_team",
    ),
]
