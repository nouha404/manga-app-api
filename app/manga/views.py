
from django.views.generic import TemplateView, ListView, DetailView

from scrapping.models import Informations

from django.views import View


# Create your views here.


class HomeView(TemplateView):
    template_name = "manga/base.html"


class MangaView(ListView):
    # queryset = Informations.objects.filter(publish=True)
    model = Informations
    template_name = "manga/mangas.html"
    context_object_name = "informations"


class ApiView(TemplateView):
    template_name = "manga/mainApi.html"


class MangaDetailView(DetailView):
    model = Informations
    template_name = "manga/details.html"
    context_object_name = "info"


""""
class MangaSearchView(View):
    La partie recherche
    template_name = 'manga/results.html'
"""