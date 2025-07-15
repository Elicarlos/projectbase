from django.conf import settings
from django.db import models

from apps.core.models import BaseModel

from .managers import OrganizationManager


class Role(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    MEMBER = "MEMBER", "Member"


class Plan(models.Model):
    name = models.CharField(max_length=50)
    price_id = models.CharField(max_length=100)
    user_limit = models.IntegerField(default=1)
    project_limit = models.IntegerField(default=3)
    storage_limit_mb = models.IntegerField(
        default=500
    )  ## exemplo de um projeto que trabalhe com armazenamento
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Organization(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_organizations",
    )
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)

    stripe_customer_id = models.CharField(
        max_length=255, blank=True, null=True
    )
    stripe_subscription_id = models.CharField(
        max_length=255, blank=True, null=True
    )

    is_trial = models.BooleanField(default=True)
    trial_ends_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class OrganizationMember(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=20, choices=Role.choices, default=Role.MEMBER
    )

    def __str__(self):
        return f"{self.user} on {self.organization}"


class Project(BaseModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    objects = OrganizationManager()

    def __str__(self):
        return self.name


class Task(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    objects = OrganizationManager()

    def __str__(self):
        return self.name
