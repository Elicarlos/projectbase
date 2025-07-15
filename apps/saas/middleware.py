from django.http import JsonResponse

from .current_organization import (
    clear_current_organization,
    set_current_organization,
)
from .models import Organization
from .utils import is_trial_expired


class CurrentOrganizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        response = None

        try:
            if user and user.is_authenticated:
                try:
                    org = Organization.objects.get(owner=user)
                    if not org.is_active or is_trial_expired(org):
                        return JsonResponse(
                            {
                                "detail": "Organização inativa ou trial expirado."
                            },
                            status=403,
                        )

                    request.organization = org
                    set_current_organization(org)

                except Organization.DoesNotExist:
                    return JsonResponse(
                        {"detail": "Organização não encontrada"}, status=403
                    )

            response = self.get_response(request)
        finally:
            clear_current_organization()

        return response
