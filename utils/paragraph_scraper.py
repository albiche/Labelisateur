import requests
from bs4 import BeautifulSoup
import random


def get_random_paragraph(min_words=45, max_words=90, max_attempts=20):
    functions = [
        get_random_law_article,
        get_random_wikipedia_paragraph,
        get_random_coreight_paragraph
    ]

    attempts = 0

    while attempts < max_attempts:
        attempts += 1
        func = random.choice(functions)

        title, paragraph = func(min_words, max_words)
        if title and paragraph:
            return title, paragraph

    print("Nombre maximal de tentatives atteint.")
    return None, None


def get_random_law_article(min_words, max_words, max_attempts=20):
    base_url = 'https://www.legifrance.gouv.fr'
    codes_url = f'{base_url}/liste/code'

    attempts = 0

    while attempts < max_attempts:
        attempts += 1
        try:
            # Récupération de la page principale des codes
            response = requests.get(codes_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extraction des liens vers les différents codes
            code_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/codes/texte_lc/')]

            if not code_links:
                continue  # Recommencer si aucun lien de code trouvé

            # Sélectionner un code au hasard
            random_code_url = base_url + random.choice(code_links)

            # Récupération de la page du code sélectionné
            response = requests.get(random_code_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extraction des liens vers les sections de ce code
            article_links = [a['href'] for a in soup.find_all('a', href=True) if
                             a['href'].startswith('/codes/section_lc/')]

            if not article_links:
                continue  # Recommencer si aucun lien d'article trouvé

            # Sélectionner une section au hasard
            random_article_url = base_url + random.choice(article_links)

            # Récupération de la page de l'article sélectionné
            response = requests.get(random_article_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extraction du titre de l'article
            title = soup.find('h1').get_text()

            # Extraction du contenu de l'article
            content_divs = soup.find_all('div', {'class': 'content content-abrogated'})

            paragraphs = []
            for div in content_divs:
                paragraphs.extend(div.find_all('p'))

            # Filtrer les paragraphes entre 30 et 150 mots
            suitable_paragraphs = [p.get_text().strip() for p in paragraphs if min_words <= len(p.get_text().split()) <= max_words]

            if not suitable_paragraphs:
                continue  # Recommencer si aucun paragraphe adéquat trouvé

            # Sélectionner un paragraphe au hasard
            selected_paragraph = random.choice(suitable_paragraphs)

            return title, selected_paragraph

        except Exception as e:
            print(f"Erreur rencontrée: {e}. Tentative {attempts} sur {max_attempts}.")
            continue  # Recommencer en cas d'exception

    print("Nombre maximal de tentatives atteint.")
    return None, None


def get_random_wikipedia_paragraph(min_words, max_words, max_attempts=20):
    attempts = 0

    while attempts < max_attempts:
        response = requests.get('https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard')
        soup = BeautifulSoup(response.text, 'html.parser')

        paragraphs = soup.find_all('p')

        for para in paragraphs:
            text = para.get_text()
            word_count = len(text.split())
            if min_words <= word_count <= max_words:
                title = soup.find('h1', {'id': 'firstHeading'}).text
                return title, text

        attempts += 1
    print("Nombre maximal de tentatives atteint.")
    return None, None


def get_random_coreight_paragraph(min_words, max_words, max_attempts=20):
    base_url = 'https://coreight.com'
    random_url = f'{base_url}/random'

    attempts = 0

    while attempts < max_attempts:
        attempts += 1
        try:
            # Aller sur la page aléatoire
            response = requests.get(random_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extraire le lien de l'article et le titre
            article_tag = soup.find('div', {'class': 'views-field views-field-title'}).find('a')
            article_link = article_tag['href']
            article_title = article_tag.get_text().strip()
            article_url = base_url + article_link

            # Aller sur la page de l'article
            response = requests.get(article_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extraire les paragraphes de l'article
            paragraphs = soup.find_all('p')
            suitable_paragraphs = [p.get_text().strip() for p in paragraphs if min_words <= len(p.get_text().split()) <= max_words]

            if suitable_paragraphs:
                # Sélectionner un paragraphe aléatoire
                selected_paragraph = random.choice(suitable_paragraphs)
                return article_title, selected_paragraph
        except Exception as e:
            print(f"Attempt {attempts}: {e}")

    return None, None

