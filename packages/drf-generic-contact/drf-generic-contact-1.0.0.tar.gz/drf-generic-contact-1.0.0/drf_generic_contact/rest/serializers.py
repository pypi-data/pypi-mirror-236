from django_generic_contact.models import Contact
from django_generic_contact.utils import get_help_text, get_validators
from rest_framework import serializers
from rest_framework.fields import JSONField

__all__ = [
    "ContactSerializer",
]


class ContactSerializer(serializers.ModelSerializer):
    data = JSONField(help_text=get_help_text(), validators=get_validators())

    class Meta:
        model = Contact
        fields = (
            "name",
            "message",
            "data",
        )
