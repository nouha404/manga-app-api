from django.urls import path
from .views import HomeView, MangaView, ApiView, MangaDetailView

from django.views import View

urlpatterns = [
    path("", HomeView.as_view(), name="manga-index"),
    path("manga/", MangaView.as_view(), name="manga-view"),
    path("manga/<int:pk>/", MangaDetailView.as_view(), name="manga-details"),
    # path('search/', MangaSearchView.as_view(), name='search-manga'),
    path('api/', ApiView.as_view(), name="api-view"),
]
