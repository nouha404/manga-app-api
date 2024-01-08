from pathlib import Path

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import TemplateView, ListView, DetailView
import requests
from rest_framework.views import APIView

from scrapping.models import Informations, Pages
from .forms import SearchMangaForm

from django.views import View


# Create your views here.


class HomeView(TemplateView):
    template_name = "manga/base.html"


class MangaInfosView(ListView):
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
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        informations = context['info']
        # Récupérez l'objet Pages lié à cet objet Informations
        page = informations.pages_set.first()
        # Ajoutez l'ID de la page au contexte
        context['page_id'] = page.id if page else None
        return context


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

                # return render(request, self.template_for_resultat, context)

        context = {'form': form}
        return render(request, self.template_name, context)


# TEST

class MangaChapterPagesView(DetailView):
    model = Pages
    template_name = "manga/chapters.html"
    context_object_name = "page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manga_title = self.object.informations.manga_title
        context['manga_title'] = manga_title

        api_url = f'http://0.0.0.0:8000/api/mangas/api/{manga_title}/pages/'
        context['api_url'] = api_url

        response = requests.get(api_url, headers={'Authorization': 'Token 2ca3d1d7f650ba231b01a28a574f58fabc9d004b'})
        context['response'] = response

        if response.status_code != 200:
            context['api_error'] = f"API Request Failed. Status code: {response.status_code}"

        # Pagination des chapitres
        chapters = response.json() if response.status_code == 200 else []
        chapter_data = []
        for chapter in chapters:
            chapter_name = chapter['name']
            chapter_number = ''.join(filter(str.isdigit, chapter_name))
            chapter_data.append({'name': chapter_name, 'number': chapter_number})

        paginator = Paginator(chapter_data, 5)
        page = self.request.GET.get('page', 1)

        try:
            chapter_data = paginator.page(page)
        except PageNotAnInteger:
            chapter_data = paginator.page(1)
        except EmptyPage:
            chapter_data = paginator.page(paginator.num_pages)
        context['chapters'] = chapter_data

        return context


class MangaSpecifiqueChapter(DetailView):
    model = Pages
    template_name = "manga/chapterDetail.html"
    context_object_name = "page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manga_title = self.kwargs.get('manga_title', None)

        context['manga_title'] = manga_title
        chapter_name = self.object.chapters_name
        chapter_number = ''.join(filter(str.isdigit, chapter_name))
        context["chapter_number"] = chapter_number

        return context

    def get(self, request, *args, **kwargs):
        manga_title = kwargs.get('manga_title')

        #extraire le numero du chapitre depuis le lien actuel
        current_url = self.request.build_absolute_uri()
        chapter_number = Path(current_url)

        api_url = f'http://0.0.0.0:8000/api/mangas/api/search/{manga_title}/{chapter_number.parts[-1]}/'

        # Effectuez la requête à l'API
        headers={'Authorization': 'Token 2ca3d1d7f650ba231b01a28a574f58fabc9d004b'}
        response = requests.get(api_url, headers=headers)

        # Vérifiez le statut de la réponse
        if response.status_code == 200:
            chapters = response.json()

            context = {
                'manga_title': manga_title,
                'chapter_info': chapters,
            }
            return render(request, 'manga/speciqueChapter.html', context)

        else:
            error_message = f"API Request Failed. Status code: {response.status_code}"
            return HttpResponse(error_message)



