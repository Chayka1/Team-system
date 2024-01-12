from django.urls import include, path
from rest_framework.routers import DefaultRouter

from teams.api import TeamAPIViewSet

router = DefaultRouter()
router.register("", TeamAPIViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
