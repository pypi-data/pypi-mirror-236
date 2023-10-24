from django_generic_contact.models import Contact
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from drf_generic_contact.rest.serializers import ContactSerializer

__all__ = [
    "ContactViewSet",
]


class ContactViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Contact.objects.none()
    serializer_class = ContactSerializer
