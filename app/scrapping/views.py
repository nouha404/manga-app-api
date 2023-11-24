from django.utils.text import slugify
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
from pprint import pprint


class InformationsListView(generics.ListAPIView):
    """
        InformationsListView is a view that provides a list of manga information entries.

    This view allows authenticated users to retrieve a list of manga information entries stored in the database.
    It does not support the creation of new entries.

    Attributes:
        serializer_class (class): The serializer class used to serialize the retrieved data.
        authentication_classes (list): The authentication classes required for access.
        permission_classes (list): The permission classes required for access.
        queryset (QuerySet): The set of manga information entries to be retrieved.

    Usage:
        To access the list of manga information entries, make a GET request to the corresponding endpoint.

    Example:
        ```
        GET /api/informations/
        ```

     Note:
    - Authentication with a valid token is required to access this view.
    - Only users with the 'IsAuthenticated' permission are allowed to retrieve data.
    - This view does not support the creation of new entries.
    """
    serializer_class = InformationsSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, NoCreatePermission]

    queryset = Informations.objects.all()


class PagesListView(generics.ListAPIView):
    """
        Get all pages with a specific manga title.

    This view returns a list of pages for a specified manga title. It requires authentication
    and only allows authenticated users to access it. Additionally, it enforces a permission
    called 'NoCreatePermission,' which restricts users from creating new pages.

    Attributes:
        serializer_class (PagesSerializer): The serializer class used for serializing page data.
        authentication_classes (list): The authentication classes used for this view.
        permission_classes (list): The permission classes applied to this view.

    Methods:
        get_queryset(): Returns a queryset of pages filtered by the specified manga title.
        list(): Retrieves the queryset, checks if it's empty, and returns serialized data or a 404 error.

     Usage:
        To access a list of pages for a specific manga title, make a GET request to the corresponding endpoint, providing
        the manga title as a URL parameter.

    Example:
        ```
        GET /api/pages/?manga_title=my_manga
        ```

    Note:
    - Authentication with a valid token is required to access this view.
    - Only users with the 'IsAuthenticated' permission are allowed to retrieve data.
    - This view enforces the 'NoCreatePermission,' preventing users from creating new pages.

    """
    serializer_class = PagesSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, NoCreatePermission]

    def get_queryset(self):
        manga_title = self.kwargs['manga_title']
        queryset = Pages.objects.filter(informations__manga_title__icontains=manga_title)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if not queryset:
            return Response(
                {'error': f'{self.kwargs["manga_title"]} not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(queryset, many=True)
        for item in serializer.data:
            informations = item.get('informations')
            if informations and isinstance(informations, dict):
                manga_title = informations.get('manga_title')
                if manga_title and isinstance(manga_title, str):
                    item['informations']['manga_title'] = manga_title.title()
        return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_specifique_information(request, manga_name: str):
    """
        Get specific manga information by name.

    This view allows authenticated users to retrieve manga information entries with a specific manga name. It requires
    a valid token for authentication and enforces the 'IsAuthenticated' permission.

    Parameters:
        :type request: object
        :param manga_name: (str): The manga name to search for. Case-insensitive.

    Returns:
        A list of manga information entries with matching manga names.

    Usage:
        To access manga information for a specific manga name, make a GET request to the corresponding endpoint,
        providing the manga name as a URL parameter.

    Example:
        ```
        GET /api/get_specific_information/?manga_name=my_manga
        ```

    Note:
    - Authentication with a valid token is required to access this view.
    - Only users with the 'IsAuthenticated' permission are allowed to retrieve data.
    - The manga name is treated in a case-insensitive manner.
    - If the manga name is not found, a 404 error response is returned.

    """
    manga_name = manga_name.title()

    informations = Informations.objects.filter(manga_title__contains=manga_name)
    serializers_infos = InformationsSerializer(informations, many=True).data

    finding_infos = []
    is_founding = False

    for info in serializers_infos:
        if manga_name in info['manga_title']:
            finding_infos.append(info)
            is_founding = True

    if not is_founding:
        return Response(
            {'error': f' {manga_name} not found, write the name correctly."'},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(finding_infos)


def filtre_pages_by_chapter(chapter):
    return Pages.objects.filter(name__contains=chapter)


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_specifique_chapter(request, manga_title: str, chapter: str):
    """
    Get images about number chapitre  of manga title

    This view takes a manga title and chapter number as input and retrieves images for the specified chapter.
    It first searches for pages containing the chapter number and validates the manga title.
    If the manga title is "One Piece," it handles it as a special case.
    If valid chapters are found, it returns a list of images for that chapter.
    If no valid chapters are found, it returns an HTTP 404 error with a message indicating the issue.

    Parameters:
        :type request: object
        :param manga_title: (str): The title of the manga.
        :param chapter: (str) : The chapter number to search for.

    Returns:
        A list of images for the specified chapter.

    Usage:
        To access images for a specific chapter of a manga, make a GET request to the corresponding endpoint,
        providing the manga title and chapter number as URL parameters.

    Example:
        ```
        GET /api/get_specifique_chapter/?manga_title=my_manga&chapter=5
        ```

    Note:
        - Authentication with a valid token is required to access this view.
        - Only users with the 'IsAuthenticated' permission are allowed to retrieve data.
        - The manga title is case-insensitive.
        - If the manga title or chapter is not found, a 404 error response is returned.
    """
    pages = filtre_pages_by_chapter(chapter)
    serializers_pages = PagesSerializer(pages, many=True).data

    slug_manga_title = slugify(manga_title)

    if manga_title == 'one piece' or manga_title.lower() == 'one piece':
        slug_manga_title = 'one_piece'
    chaptre_valid = f'chapitre-{chapter}/'

    finding_chapters = []
    is_founding = False
    for chaptr in serializers_pages:
        for cpt in chaptr['chapters']:
            if cpt is not None and slug_manga_title in cpt and chaptre_valid in cpt:
                finding_chapters.append(cpt)
                is_founding = True

    if not is_founding:
        return Response(
            {'error': f' {manga_title} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    if not pages:
        return Response(
            {'error': f'Chapter {chapter} not found, check for valid chapters.'},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(finding_chapters)


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_specifique_chapter_title(request, manga_title: str, chapter: str):
    """
        Get the full title of a specific chapter of a manga.

        This view takes a manga title and chapter number as input and retrieves the full title of the specified chapter.
        It first searches for pages containing the chapter number and validates the manga title.
        If the manga title is "One Piece," it handles it as a special case.
        If valid chapters are found, it returns the full title of the chapter.
        If no valid chapters are found, it returns an HTTP 404 error with a message indicating the issue.

        Parameters:
            :type request: object
            :param manga_title: (str): The title of the manga.
            :param chapter: (str) : The chapter number to search for.

        Returns:
            The full title of the specified chapter as a string.

        Usage:
            To retrieve the full title of a specific chapter of a manga, make a GET request to the corresponding endpoint,
            providing the manga title and chapter number as URL parameters.

        Example:
            ```
            GET /api/get_specifique_chapter_title/?manga_title=my_manga&chapter=5
            ```
        Note:
            - Authentication with a valid token is required to access this view.
            - Only users with the 'IsAuthenticated' permission are allowed to retrieve data.
            - The manga title is case-insensitive.
            - If the manga title or chapter is not found, a 404 error response is returned.
    """
    pages = filtre_pages_by_chapter(chapter)
    serializers_pages = PagesSerializer(pages, many=True).data

    finding_chapters = []
    is_founding = False
    for chaptr in serializers_pages:
        for cpt in chaptr['name']:
            if cpt:
                finding_chapters.append(cpt)
                is_founding = True

    full_title = ''.join(finding_chapters)
    if not is_founding:
        return Response(
            {'error': f' {manga_title} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    if not pages:
        return Response(
            {'error': f'Chapter {chapter} not found, check for valid chapters.'},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response(full_title)



@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_all_manga_present(request):
    """
        Get a list of all valid mangas present in our database.

    This view retrieves a list of all valid manga titles present in our database.
    It requires authentication and is only accessible to authenticated users.
    It returns a list of manga titles as a response.

    Returns:
        A list of all manga titles present in the database.

    Usage:
        To access a list of all valid manga titles in the database, make a GET request to the corresponding endpoint.

    Example:
        ```
        GET /api/get_all_manga_present/
        ```

    Note:
    - Authentication with a valid token is required to access this view.
    - Only users with the 'IsAuthenticated' permission are allowed to retrieve data.
    """
    manga_titles = Informations.objects.values_list('manga_title', flat=True).distinct()
    return Response(manga_titles)


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def get_chapter_name(request, manga_title: str, chapter: str, page_number: str):
    """
        Get the image URL and information about a specific chapter of a manga.

    This view retrieves the image URL and other information about a specific page of a manga chapter. It requires
    authentication and is accessible only to authenticated users. Users can provide the manga title, chapter number,
    and page number as parameters. The view searches for the corresponding image URL and returns information about
    the chapter and the image URL as a response. If the provided chapter or page number is invalid, it returns an
    error response.

     Parameters:
        :type request: object
        :param manga_title: (str): The title of the manga.
        :param chapter: (str): The chapter number.
        :param page_number: (str): The page number.

    Returns:
        Information about the chapter and URL of the image for the specified page.

    Usage:
        To access information and the image URL for a specific page of a manga chapter, make a GET request to the
        corresponding endpoint, providing the manga title, chapter number, and page number as URL parameters.

    Example:
        ```
        GET /api/get_chapter_name/?manga_title=my_manga&chapter=5&page_number=1
        ```

    Note:
    - Authentication with a valid token is required to access this view.
    - Only users with the 'IsAuthenticated' permission are allowed to retrieve data.
    """
    pages = Pages.objects.filter(name__contains=chapter)
    serializers_pages = PagesSerializer(pages, many=True).data

    slug_manga_title = slugify(manga_title)

    if manga_title == 'one piece' or manga_title.lower() == 'one piece':
        slug_manga_title = 'one_piece'

    chaptre_valid = f'chapitre-{chapter}/'
    number_valid = []
    finding_chapters = []
    is_founding = False
    for chaptr in serializers_pages:
        for cpt in chaptr['chapters']:

            if cpt is not None and slug_manga_title in cpt and chaptre_valid in cpt:
                finding_chapters.append(cpt)
                extract_url = Path(cpt)
                number_valid.append(extract_url.stem)
                is_founding = True

                if page_number == str(0):
                    return Response(
                        {'error': f'Chapter {page_number} not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
                elif page_number in extract_url.stem:
                    return Response(
                        {
                            'id': chaptr['id'],
                            'title': chaptr['name'],
                            'image': cpt
                        }
                    )
    if not is_founding:
        return Response(
            {'error': f' {manga_title} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    else:
        ERR = {
            'error': f'page number {page_number} invalide for chapter {chapter}',
            'chapter number valide': [vld for vld in number_valid]
        }
        return Response(ERR, status=status.HTTP_404_NOT_FOUND)
