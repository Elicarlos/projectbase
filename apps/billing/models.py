from django.db import models
from apps.accounts.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    default_payment_method = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} ↔ {self.stripe_customer_id}"