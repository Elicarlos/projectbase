from django.shortcuts import render
from rest_framework import viewsets
from .models import Plan, Organization
from .serializers import PlanSerializer, OrganizationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionsDenied
from datetime import datetime
from apps.billing.services import StripeService



class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.filter(is_active=True)
    serializer_classs = PlanSerializer
    permission_classes = [permissions.AllowAny]


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        org = self.request.user.organization
        if not can_create_project(org):
            raise PermissionsDenied('Limite de Projetos Atingidos')

        serializer.save(organization=org)

class OrganizationDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            org = Organization.objects.get(owner=request.user)

        except Organization.DoesNotExist:
            return Response({'detail': 'Empresa nao encontrada', status=404})

        plan org.plan
        user_count = org.user_set.count()
        project_count - org.project_set.count()

        user_limit = plan.user_limit
        project_limit = org.project_limit

        def nearing_limit(count, limit):
            return limit > 0 and count >= 0.8 * limit
            

        alerts = []
        if nearing_limit(user_count, user_limit):
            alerts.append(f"Você está usando {user_count}/{user_limit} usuários permitidos.")
        if nearing_limit(project_count, project_limit):
            alerts.append(f"Você está usando {project_count}/{project_limit} projetos permitidos.")

        invoice_date = None
        if org.stripe_customer_id:
            last_invoice_ts = StripeService.get_last_invoice_date(org.stripe_customer_id)
            if last_invoice_ts:
                invoice_date = datetime.fromtimestamp(last_invoice_ts).strftime("%Y-%m-%d %H:%M")


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
            }
        }

        return Response(data)


