from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    OrganizationDashboardView,
    OrganizationViewSet,
    PlanViewSet,
    ProjectViewSet,
    TaskViewSet,
)

router = DefaultRouter()

router.register("plans", PlanViewSet)
router.register("organizations", OrganizationViewSet, basename="organization")
router.register("projects", ProjectViewSet, basename="project")
router.register("tasks", TaskViewSet, basename="task")


urlpatterns = [
    path("", include(router.urls)),
    path(
        "dashboard/",
        OrganizationDashboardView.as_view(),
        name="organization-dashboard",
    ),
]
