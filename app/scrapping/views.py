from rest_framework import generics, authentication, permissions
from .models import Informations, Pages
from .permissions import NoCreatePermission
from .serializers import InformationsSerializer, PagesSerializer


class InformationsListView(generics.ListAPIView):
    serializer_class = InformationsSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, NoCreatePermission]

    queryset = Informations.objects.all()


class PagesListView(generics.ListAPIView):
    serializer_class = PagesSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, NoCreatePermission]

    queryset = Pages.objects.all()
