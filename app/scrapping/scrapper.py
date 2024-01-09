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


def get_informations(url_manga_specifique: str):
    response = requests.get(url_manga_specifique, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    infos = soup.find('dl', class_='dl-horizontal')
    search_date_release = infos.find('dt', text='Date de sortie')
    search_category_dt = infos.find('dt', text='Catégories')

    release_date = search_date_release.find_next_sibling('dd').text
    author = infos.findAll('dd')[2].text.replace('\n', '')
    category = search_category_dt.find_next_sibling('dd').text
    resume = soup.find('div', class_='well').p.text
    manga_title = soup.find('h2', class_='widget-title').text
    image = soup.find("img", class_="img-responsive")
    image_src = image.get("src")

    existing_info = Informations.objects.filter(
        release_date=release_date,
        author=author,
        category=category,
        resume=resume,
        manga_title=manga_title,
        image_link=image_src
    ).first()
    if not existing_info:
        informations = Informations.objects.create(
            release_date=release_date,
            author=author,
            resume=resume,
            category=category,
            manga_title=manga_title,
            image_link=image_src
        )
        return informations
    else:
        return existing_info





def get_all_chapters(url_manga_specifique: str):
    response = requests.get(url_manga_specifique, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    chapters = soup.find('ul', class_='chapters')
    all_chapters = chapters.findAll('a')

    CHAPTERS = []
    for src in all_chapters:
        links = src['href']
        CHAPTERS.append(links)
    return CHAPTERS


# refactoring of old process
"""one_piece_all_chapters = get_all_chapters(url_piece)
"""


def get_scan_names(informations, all_chapters: list):
    informations = (
        Informations.objects.first()
        if informations is None
        else informations
    )
    for url_in_alchaptre in all_chapters:
        print(f'recuperation des nom dans {url_in_alchaptre}')
        response = requests.get(url_in_alchaptre, headers=headers)
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
            existing_page = Pages.objects.filter(
                informations=informations,
                name=name,
                chapters=IMAGES
            ).first()

            if not existing_page:

                Pages.objects.create(
                    informations=informations,
                    name=name,
                    chapters=IMAGES
                )


# refactoring of old process
"""get_scan_names(mha_informations, mha_all_chapters)
"""

urls = [
    ('One Piece', 'https://www.scan-vf.net/one_piece'),
    ('My Hero Academia', 'https://www.scan-vf.net/my-hero-academia'),
    ('Jujutsu Kaisen', 'https://www.scan-vf.net/jujutsu-kaisen'),
    ('Kingdom', 'https://www.scan-vf.net/kingdom'),
    ('Boruto', 'https://www.scan-vf.net/boruto'),
    ('Black Clover', 'https://www.scan-vf.net/black-clover'),
    ('Attaque des titans', 'https://www.scan-vf.net/attaque-des-titans'),
    ('Bleach', 'https://www.scan-vf.net/bleach'),
    ('One Punch Man', 'https://www.scan-vf.net/one-punch-man'),
    ('Manhwa Solo Leveling', 'https://www.scan-vf.net/solo-leveling'),
    ('Hunter X Hunter', 'https://www.scan-vf.net/hunter-x-hunter'),
]

# refactoring of old process
"""url_piece = 'https://www.scan-vf.net/one_piece'
one_piece_informations = get_informations(url_piece)
"""

for manga_name, url in urls:
    existing_informations = get_informations(url)

    all_chapters_for_specifique_url = get_all_chapters(url)

    if all_chapters_for_specifique_url:
        get_scan_names(existing_informations, all_chapters_for_specifique_url)
    else:
        print(f'Aucun nouveau chapitre trouvé pour {manga_name}.')


# Fonction pour télécharger et enregistrer les images




def remove_duplicate_pages():
    all_pages = Pages.objects.all()

    # Créer un ensemble vide pour stocker les pages uniques
    unique_pages = set()
    duplicate_pages = []

    for page in all_pages:
        # Créer une clé unique pour chaque page en utilisant le nom et le chapitre
        page_key = (page.name, str(page.chapters))

        if page_key in unique_pages:
            duplicate_pages.append(page)
        else:
            unique_pages.add(page_key)

    for duplicate_page in duplicate_pages:
        duplicate_page.delete()

    print(f"{len(duplicate_pages)} pages en double supprimées.")


remove_duplicate_pages()
