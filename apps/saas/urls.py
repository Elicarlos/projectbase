from rest_framework.routers import DefaultRouter
from .views import PlanViewSet, OrganizationViewSet, OrganizationDashboardView
from django.urls import path, include

router = DefaultRouter()

router.register('plans', PlanViewSet)
router.register('organizations', OrganizationViewSet)
router.register('dashboard', OrganizationDashboardView)



urlpatterns = [
    path('', include(router.urls))

]