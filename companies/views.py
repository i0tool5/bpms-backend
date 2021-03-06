from rest_framework.viewsets import ModelViewSet

from companies.serializers import (
    Company, Contact,
    CompanySerializer,
    ContactSerializer
)


class CompanyApiView(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ContactApiView(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
