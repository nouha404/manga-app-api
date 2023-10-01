from rest_framework import generics, authentication, permissions, status
from .models import Informations, Pages
from .permissions import NoCreatePermission
from .serializers import InformationsSerializer, PagesSerializer

from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)


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


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_specifique_chapter(request, chapter: str):
    pages = Pages.objects.filter(name__contains=chapter)

    if not pages:
        return Response(
            {'error': f'Chapter {chapter} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    elif str(1) <= chapter <= str(109) or str(11) <= chapter <= str(99):
        page = Pages.objects.filter(name__contains=chapter)
        s = PagesSerializer(page, many=True)
        return Response(s.data[-1])

    serializer = PagesSerializer(pages, many=True)
    return Response(serializer.data)
