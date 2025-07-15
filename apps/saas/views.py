from datetime import datetime

from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.billing.services import StripeService

from .models import Organization, Plan, Project, Task
from .permissions import IsOrganizationAdmin, IsOrganizationMember
from .serializers import (
    OrganizationSerializer,
    PlanSerializer,
    ProjectSerializer,
    TaskSerializer,
)
from .utils import can_create_project, is_trial_expired


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer
    permission_classes = [permissions.AllowAny]


class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        return Organization.objects.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [IsOrganizationAdmin]
        else:
            self.permission_classes = [IsOrganizationMember]
        return super().get_permissions()

    def perform_create(self, serializer):
        # This viewset is for managing the Organization itself, not Projects.
        # The can_create_project logic should be in a Project creation view.
        # For Organization creation, we need to ensure the user doesn't already own one.
        if Organization.objects.filter(owner=self.request.user).exists():
            raise PermissionDenied("Você já possui uma organização.")
        organization = serializer.save(owner=self.request.user)
        # Create Stripe customer for the organization
        stripe_customer = StripeService.create_customer(organization)
        organization.stripe_customer_id = stripe_customer.id
        organization.save()


class OrganizationDashboardView(APIView):
    permission_classes = [IsOrganizationMember]

    def get(self, request):
        try:
            org = request.organization  # Use the organization from middleware

        except AttributeError:  # If middleware didn't set it
            return Response(
                {"detail": "Organização não encontrada"}, status=404
            )

        plan = org.plan
        user_count = org.user_set.count()
        project_count = org.project_set.count()

        user_limit = plan.user_limit
        project_limit = org.project_limit

        def nearing_limit(count, limit):
            return limit > 0 and count >= 0.8 * limit

        alerts = []
        if nearing_limit(user_count, user_limit):
            alerts.append(
                f"Você está usando {user_count}/{user_limit} usuários permitidos."
            )
        if nearing_limit(project_count, project_limit):
            alerts.append(
                f"Você está usando {project_count}/{project_limit} projetos permitidos."
            )

        invoice_date = None
        if org.stripe_customer_id:
            last_invoice_ts = StripeService.get_last_invoice_date(
                org.stripe_customer_id
            )
            if last_invoice_ts:
                invoice_date = datetime.fromtimestamp(
                    last_invoice_ts
                ).strftime("%Y-%m-%d %H:%M")

        data = {
            "organization": org.name,
            "slug": org.slug,
            "plan": org.plan.name if org.plan else None,
            "limits": {
                "users": org.plan.user_limit,
                "projects": org.plan.project_limit,
                "storage_mb": org.plan.storage_limit_mb,
            },
            "usage": {
                "users": org.user_set.count(),
                "projects": org.project_set.count(),
                # "storage_mb": get_storage_usage(org)  # se aplicável
            },
            "status": {
                "is_active": org.is_active,
                "is_trial": org.is_trial,
                "trial_ends_at": org.trial_ends_at,
                "trial_expired": is_trial_expired(org),
            },
            "billing": {
                "stripe_customer_id": org.stripe_customer_id,
                "last_invoice_date": invoice_date,
            },
        }

        return Response(data)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects_in_org.get_queryset(self.request.organization)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsOrganizationAdmin]
        else:
            self.permission_classes = [IsOrganizationMember]
        return super().get_permissions()

    def perform_create(self, serializer):
        org = self.request.organization
        if not can_create_project(org):
            raise PermissionDenied(
                "Limite de projetos atingido para esta organização."
            )
        serializer.save(organization=org)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        # Ensure tasks are filtered by the project's organization
        return Task.objects_in_org.get_queryset(self.request.organization)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsOrganizationAdmin]
        else:
            self.permission_classes = [IsOrganizationMember]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Ensure the project belongs to the user's organization
        project = serializer.validated_data.get("project")
        if project and project.organization != self.request.organization:
            raise PermissionDenied("O projeto não pertence à sua organização.")
        serializer.save()
