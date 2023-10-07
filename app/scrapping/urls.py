from django.urls import path
from .views import (
    InformationsListView,
    PagesListView,
    get_specifique_chapter,
    get_chapter_name,
    get_all_manga_present,
)

urlpatterns = [
    path(
        'api/informations/',
        InformationsListView.as_view(),
        name='informations-list'
    ),
    path(
        'api/<str:manga_title>/pages/',
        PagesListView.as_view(),
        name='pages-list'),
    path(
        'api/mangas/names/',
        get_all_manga_present,
        name='mangas-valid'
    ),
    path(
        'api/search/<str:manga_title>/<str:chapter>/',
        get_specifique_chapter,
        name='pages-detail'
    ),
    path(
        'api/pages/<str:manga_title>/<str:chapter>/<str:page_number>/infos_for_specifique_chapter/',
        get_chapter_name,
        name='chapter-name'
    ),
]
