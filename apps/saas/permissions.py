from rest_framework import permissions

from .models import OrganizationMember, Role


class IsOrganizationAdmin(permissions.BasePermission):
    """Custom permission to only allow organization admins to access an object."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request, "organization"):
            return False

        member = OrganizationMember.objects.filter(
            organization=request.organization,
            user=request.user,
            role=Role.ADMIN,
        ).first()

        return member is not None


class IsOrganizationMember(permissions.BasePermission):
    """Custom permission to only allow organization members to access an object."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request, "organization"):
            return False

        member = OrganizationMember.objects.filter(
            organization=request.organization,
            user=request.user,
        ).first()

        return member is not None


class IsOrganizationOwner(permissions.BasePermission):
    """Custom permission to only allow organization owner to access an object."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not hasattr(request, "organization"):
            return False

        return request.organization.owner == request.user
