from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView, ListView, DetailView

from scrapping.models import Informations
from .forms import SearchMangaForm

from django.views import View


# Create your views here.


class HomeView(TemplateView):
    template_name = "manga/base.html"


class MangaView(ListView):
    # queryset = Informations.objects.filter(publish=True)
    model = Informations
    template_name = "manga/mangas.html"
    context_object_name = "informations"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchMangaForm()
        return context




class ApiView(TemplateView):
    template_name = "manga/mainApi.html"


class MangaDetailView(DetailView):
    model = Informations
    template_name = "manga/details.html"
    context_object_name = "info"

    # un autre contexte



""""
class MangaSearchView(View):
    La partie recherche
    template_name = 'manga/results.html'
"""


def searchManga(request):
   pass


class MangaSearchView(View):
    template_name = 'manga/mangas.html'
    template_for_resultat = 'manga/search.html'

    # Traitement du get/post du filtre
    def post(self, request, *args, **kwargs):
        form = SearchMangaForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search']

            # Filtrer les informations basées sur le terme de recherche
            results = Informations.objects.filter(manga_title__icontains=search_term)
            context = {'informations': results, 'form': form}
            if results:
                if request.is_ajax():

                    html_content = render_to_string(self.template_for_resultat, context)
                    return JsonResponse({'html': html_content})
                else:
                    return render(request, self.template_for_resultat, context)

                #return render(request, self.template_for_resultat, context)

        context = {'form': form}
        return render(request, self.template_name, context)
