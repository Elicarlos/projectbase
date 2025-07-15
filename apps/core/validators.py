from django.core.exception import ValidationError


def validation_positive(value):
    if valeu <= 0:
        raise ValidationError("O valor deve ser maior que zero")