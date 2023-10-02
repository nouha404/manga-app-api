from django.urls import path
from .views import InformationsListView, PagesListView, get_specifique_chapter, get_only_chapter_with_his_number, get_number_valide

urlpatterns = [
    path(
        'api/informations/',
        InformationsListView.as_view(),
        name='informations-list'
    ),
    path('api/pages/', PagesListView.as_view(), name='pages-list'),
    path(
        'api/pages/search/<str:chapter>/',
        get_specifique_chapter,
        name='pages-detail'
    ),
    path(
        'api/pages/search/<str:chapter>/<str:chapter_number>/',
        get_only_chapter_with_his_number,
        name='chapter-number'
        ),
    path(
        'api/search/<str:chapter>/valide_number/',
        get_number_valide,
        name='valide-number'
    ),
]
