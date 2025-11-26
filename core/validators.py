from rest_framework.exceptions import ValidationError

from core.models import Tag


def validate_existing_name_tag(value, user):
    if Tag.objects.filter(name=value, owner=user).exists():
        raise ValidationError({"name": "Tag com este nome já existe"})
