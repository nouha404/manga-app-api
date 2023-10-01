from django.urls import path
from .views import InformationsListView, PagesListView, get_specifique_chapter

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
]
