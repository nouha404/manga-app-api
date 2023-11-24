from django.urls import path
from .views import index,mangaViews


urlpatterns = [
    path("", index, name="manga-index"),
    path("manga/", mangaViews, name="manga-view"),
]