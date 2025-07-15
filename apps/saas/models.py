from django.db import models
from core.models import BaseModel


class Plan(models.Model):
    name = models.CharField(max_length=50)
    price_id = models.IntegerField(max_length=100)
    user_limit = models.IntegerField(default=1)
    project_limit = models.IntegerField(default=3)
    storage_limit_mb = models.IntegerField(default=500) ## exemplo de um projeto que trabalhe com armazenamento
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name

class Organization(BaseModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    owner = models.ForeingKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeingKey(Plan, on_delete=models.SET_NULL, null=True)

    stripe_customer_id = models.Charfield(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)

    is_trial = models.BooleanField(default=True)
    trial_ends_at = models.DateTimeField(blank=True, null=True)
    is_active = model.BooleanField(default=True)

    def __str__(self):
        return self.name
