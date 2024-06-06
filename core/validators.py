from rest_framework.exceptions import ValidationError

from core.models import Tag


def validate_existing_name_tag(value):
    if Tag.objects.filter(name=value, owner=value.owner).exists():
        raise ValidationError("Tag com este nome já existe")