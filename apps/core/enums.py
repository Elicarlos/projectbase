from django.db.models import TextChoices



class StatusChoices(TextChoices):
    ATIVO = 'ativo', 'Ativo'
    INATIVO  = 'inativo', 'Inativo'
    ARQUIVADO =  'arquivado', 'Arquivado'