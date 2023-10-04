import requests
from bs4 import BeautifulSoup
# from tinydb import TinyDB
# from pathlib import Path
from pprint import pprint
from scrapping.models import (
    Informations,
    Pages
)


headers = {
    'user-agent': (
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 '
        'Mobile Safari/537.36 Edg/105.0.1343.33'
    )
}

def get_informations(url: str):

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    infos = soup.find('dl', class_='dl-horizontal')
    search_date_release = infos.find('dt', text='Date de sortie')
    search_category_dt = infos.find('dt', text='Catégories')

    #ârtie date chapitre a gerer



    manga_title = soup.find('h2', class_='widget-title').text
    release_date = search_date_release.find_next_sibling('dd').text
    author = infos.findAll('dd')[2].text.replace('\n', '')
    category = search_category_dt.find_next_sibling('dd').text
    resume = soup.find('div', class_='well').p.text

    existing_info = Informations.objects.filter(
        release_date=release_date,
        author=author,
        category=category,
        resume=resume
    ).first()
    if not existing_info:
        informations = Informations.objects.create(
            manga_title=manga_title,
            release_date=release_date,
            author=author,
            resume=resume,
            category=category
        )
        return informations



url_piece = 'https://www.scan-vf.net/one_piece'
url_mha = 'https://www.scan-vf.net/my-hero-academia'
url_jujutsu = 'https://www.scan-vf.net/jujutsu-kaisen'
url_kingdom = 'https://www.scan-vf.net/kingdom'
url_boruto = 'https://www.scan-vf.net/boruto'
url_black_clover = 'https://www.scan-vf.net/black-clover'
url_snk = 'https://www.scan-vf.net/attaque-des-titans'
url_bleach = 'https://www.scan-vf.net/bleach'


one_piece_informations = get_informations(url_piece)
mha_informations = get_informations(url_mha)
jujutsu_kaisen_informations = get_informations(url_jujutsu)
kingdom_informations = get_informations(url_kingdom)
boruto_informations = get_informations(url_boruto)
black_clover_informations = get_informations(url_black_clover)
snk_informations = get_informations(url_snk)
bleach_informations = get_informations(url_bleach)



def get_all_chapters(url: str):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    chapters = soup.find('ul', class_='chapters')
    all_chapters = chapters.findAll('a')

    CHAPTERS = []
    for src in all_chapters:
        links = src['href']
        CHAPTERS.append(links)
    return CHAPTERS



one_piece_all_chapters = get_all_chapters(url_piece)
mha_all_chapters = get_all_chapters(url_mha)
jujutsu_all_chapters = get_all_chapters(url_jujutsu)
kingdom_all_chapters = get_all_chapters(url_kingdom)
boruto_all_chapters = get_all_chapters(url_boruto)
black_clover_all_chapters = get_all_chapters(url_black_clover)
snk_all_chapters = get_all_chapters(url_snk)
bleach_all_chapters = get_all_chapters(url_bleach)


def get_scan_names(informations, all_chapters : list):
    informations = (
        Informations.objects.first()
        if informations is None
        else informations
    )
    for url in all_chapters:
        print(f'recuperation des nom dans{url}')
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        # get names
        names_class = soup.findAll('div', class_='page-header')
        NAMES = []
        for name in names_class:
            name_extracted = name.find('b').text
            NAMES.append(name_extracted)
        print(NAMES)

        # get images
        images_class = soup.findAll('img', class_='img-responsive')
        IMAGES = []
        for img_src in images_class:
            image_extracted = img_src.get('data-src')
            IMAGES.append(image_extracted)
            print(f'Extraction de tous les images de {image_extracted} ...')

        for name, chapter in zip(NAMES, IMAGES):
            Pages.objects.create(
                informations=informations,
                name=name,
                chapters=IMAGES
            )


get_scan_names(mha_informations, mha_all_chapters)
get_scan_names(jujutsu_kaisen_informations, jujutsu_all_chapters)
get_scan_names(kingdom_informations, kingdom_all_chapters)
get_scan_names(one_piece_informations, one_piece_all_chapters)
get_scan_names(boruto_informations, boruto_all_chapters)
get_scan_names(black_clover_informations, black_clover_all_chapters)
get_scan_names(snk_informations, snk_all_chapters)
get_scan_names(bleach_informations, bleach_all_chapters)