from django.contrib import admin
from . models import Plan, Organization


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_limit', 'project_limit', 'storage_limit_mb', 'is_active')
    list_filter = ('is_active',)
    search_filter = ('name', 'price_id')


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "owner", "plan", "is_trial", "trial_ends_at", "is_active")
    list_filter = ("plan", "is_trial", "is_active")
    search_fields = ("name", "slug", "owner__email")
    autocomplete_fields = ('owner',)
