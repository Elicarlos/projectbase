from django.core.exception import ValidationError


def validation_positive(value):
    if not value.isalnum():
        raise ValidationError("O valor deve ser maior que zero")
