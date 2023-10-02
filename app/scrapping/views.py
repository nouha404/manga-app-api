from rest_framework import generics, authentication, permissions, status
from .models import Informations, Pages
from .permissions import NoCreatePermission
from .serializers import InformationsSerializer, PagesSerializer
from pathlib import Path
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
    pages = Pages.objects.filter(name__contains=chapter) #ok

    if not pages or chapter == str(0):
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


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_only_chapter_with_his_number(request, chapter: str, chapter_number:str):
    """
    Filtre for getting chapter with this number
    :param HTTP request:
    :param chapter:
    :param chapter_number:
    :return: Response with only chapter link
    """
    pages = Pages.objects.filter(name__contains=chapter) #dupliquer hein
    if not pages or chapter == str(0):
        return Response(
            {'error': f'Chapter {chapter} not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializers_pages = []
    for _ in pages:
        serializers_pages = PagesSerializer(pages, many=True).data


    number_valide = []
    for chapterInSerializersPages in serializers_pages:
        errors = {
            'error': f'Chapter number invalide for chapter {chapter}',
            'chapter number valide': [vld for vld in number_valide if vld != 'None']
        }
        for chapters in chapterInSerializersPages['chapters']:
            if chapters is None:
                chapters = str(chapters)
            extract_url = Path(chapters)
            number_valide.append(extract_url.stem)

            chapter_numberValid = f'chapitre-{chapter}/{chapter_number}.webp'

            specifique_url = []
            if str(1) <= chapter <= str(109) or str(11) <= chapter <= str(99):
                page = Pages.objects.filter(name__contains=chapter)
                s = PagesSerializer(page, many=True)
                nbValide = []
                for url in s.data[-1]['chapters']:
                    if url is not None:
                        specifique_url.append(url)
                        err = Path(url)
                        if chapter_numberValid in url:
                            return Response(url)
                        nbValide.append(err.stem)
                    else:
                        ERR = {
                        'error': f'Chapter number invalide for chapter {chapter}',
                        'chapter number valide': [vld for vld in nbValide]
                        }
                        return Response(ERR,status=status.HTTP_404_NOT_FOUND)
            if chapter_numberValid in chapters:
                return Response(chapters)
        return Response(errors,status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_number_valide(request, chapter: str):
    """
    Get valide numbers for specifique chapter
    :param HTTP request:
    :param searching chapter:
    :return Response with an array who content valid number:
    """
    pages = Pages.objects.filter(name__contains=chapter) #dupliquer hein
    if not pages or chapter == str(0):
        return Response(
            {'error': f'Chapter {chapter} not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializers_pages = []
    for _ in pages:
        serializers_pages = PagesSerializer(pages, many=True).data

    number_valide = []

    for chapterInSerializersPages in serializers_pages:

        for chapters in chapterInSerializersPages['chapters']:
            if chapters is None:
                chapters = str(chapters)
            extract_url = Path(chapters)
            number_valide.append(extract_url.stem)
    errors = {
        f' Number valide for chapter {chapter}': [vld for vld in number_valide if vld != 'None']
    }
    return Response(errors,status=status.HTTP_404_NOT_FOUND)