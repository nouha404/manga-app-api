from django.urls import path
from .views import InformationsListView, PagesListView

urlpatterns = [
    path(
        'api/informations/',
        InformationsListView.as_view(),
        name='informations-list'
    ),
    path('api/pages/', PagesListView.as_view(), name='pages-list'),
]
