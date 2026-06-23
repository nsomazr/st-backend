from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Service
from .serializers import ServiceSerializer


class ServiceListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ServiceSerializer
    queryset = Service.objects.filter(is_active=True)
