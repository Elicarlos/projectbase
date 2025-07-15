from django.db import models
from .current_organization import get_current_organization


class OrganizationManager(models.Manager):
    def get_queryset(self):
        organization = get_current_organization()
        if not organization:
            raise Exception("No organization set in current context.")
        return super().get_queryset().filter(organization=organization)

    def _base_queryset(self):
        """Returns the unfiltered queryset. Use with caution."""
        return super().get_queryset()
