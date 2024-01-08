from django.urls import path
from .views import HomeView, MangaInfosView, ApiView, MangaDetailView, MangaSearchView, MangaChapterPagesView, MangaSpecifiqueChapter

from django.views import View

urlpatterns = [
    path("", HomeView.as_view(), name="manga-index"),
    path("manga/", MangaInfosView.as_view(), name="manga-view"),
    path("manga/<int:pk>/", MangaDetailView.as_view(), name="manga-details"),
    path('api/', ApiView.as_view(), name="api-view"),
    path("manga/only/", MangaSearchView.as_view(), name="manga-filtre"),
    path("manga/chapter/<str:pk>/", MangaChapterPagesView.as_view(), name="manga-chapters"),
    path("manga/spe/<str:manga_title>/<str:pk>/", MangaSpecifiqueChapter.as_view(), name="manga-spe-chapter"),

]
