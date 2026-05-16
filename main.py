"""
Programul foloseste BeautifulSoup si requests pentru a face web scraping
de pe Google Academic. Se folosete keyword-ul "python programming"

Resurse folosite:
Google Scholar Scraping: https://medium.com/@darshankhandelwal12/scrape-google-scholar-using-python-3f35a3a6597b
"""
import csv

import result
from bs4 import BeautifulSoup

# ne ajuta sa obtinem datele HTML de la un anumit site
import requests

# Pentru procesarea textului cu expresii regulate
import re

def get_web_data():
    """
    Functia are ca rol obtinerea continutului HTML al paginii web
    Dictionarul heades se foloseste pentru a impersona un browser adevarat
    Fara acesta serverele Google presupun ca sursa request-ului este un bot sau scrip
    :return:
    """
    try:
        url = "https://scholar.google.com/scholar?hl=ro&as_sdt=0%2C5&q=python+programming&oq=Python"

        # nu conteaza ce browser / OS impersonam
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3)AppleWebKit / 537.36(KHTML, like Gecko)Chrome / 100.0.4896.127Safari / 537.36"
        }

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        return soup

    except requests.exceptions.ConnectionError:
        # Nu se poate conecta la internet sau la server
        print("Nu exista conexiune la internet")

    except requests.exceptions.Timeout:
        # Serverul nu a raspuns la timp
        print("Requestul a expirat")

    except requests.exceptions.HTTPError as e:
        # Raspuns HTTP invalid: 403 Forbidden, 404 Not Found, etc.
        print(f"Eroare HTTP: {e.response.status_code}")

    except Exception as e:
        # Orice alta eroare
        print(f"Eroare neasteptata: {e}")

def get_title(r):
    """
    Extrage titlul din articol
    Gaseste toate elementele HTML cu clasa "gs_r" (div-ul principal in care se afla titlul)
    In fiecare rezultat cauta elementul cu tag <a> si clasa "gs_rt", titlul efectiv
    :param r:
    :return titles:
    """
    titles = []
    for elem in r.select(".gs_r"):
        title_elem = elem.select_one(".gs_rt a")
        # Verifica daca titlul exista (nu e NONE)
        if title_elem:
            titles.append(title_elem.text)

    return titles


def get_links(r):
    """
    Extrage link-urile din articol
    Gaseste toate elementele HTML cu clasa "gs_r" (div-ul principal in care se afla link-ul)
    In fiecare rezultat cauta elementul cu tag <a> si clasa "gs_rt", link-ul efectiv
    :param r:
    :return titles:
    """
    links = []
    for elem in r.select(".gs_r"):
        link_elem = elem.select_one(".gs_rt a")
        # Verifica daca titlul exista (nu e NONE)
        if link_elem:
            links.append(link_elem["href"])

    return links


def get_author(r):
    """
    Extrage autorul articolului
    Gaseste toate elementele HTML cu clasa "gs_a", autorul efectiv
    :param r:
    :return authors:
    """

    authors = []
    for elem in r.select(".gs_a"):
        if elem:
            # Unele elemente din lista contin un non-breaking space
            # Acesta este inlocui cu cratima "-" pentru  avea o structura constanta
            # Si pentru a fi mai usoara procesarea ulteriora
            authors.append(elem.text.replace("\xa0", " "))

    return authors


def get_reference_number(r):
    """
    Extrage elementul care contine numarul de citari al articolului
    Gaseste toate elementele HTML cu clasa "gs_flb"
    :param r:
    :return reference_number:
    """
    reference_number = []
    for elem in r.select(".gs_flb"):
        if elem:
            reference_number.append(elem.text)

    return reference_number

def process_authors(author_unprocessed):
    """
    Proceseaza lista bruta de autori si extrage doar numele acestora
    prin pastrarea partii dinaintea primului " - "
    :param author_unprocessed: lista de siruri neprocesate cu autori
    :return: lista doar cu numele autorilor
    """
    processed = []
    for author_text in author_unprocessed:
        parts = author_text.split(" - ")
        author_only = parts[0].strip()
        processed.append(author_only)
    return processed

def process_reference_number(ref_nr_unprocessed):
    """
    Proceseaza lista bruta cu informatii despre citari si extrage doar numarul efectiv.
    :param ref_nr_unprocessed: lista de siruri neprocesate despre citari
    :return: lista cu numarul de citari
    """
    processed_ref = []
    for ref_nr_text in ref_nr_unprocessed:
        match = re.search(r"\d+", ref_nr_text)
        if match:
            processed_ref.append(match.group())
        else:
            # Daca nu exista nici un numar de cititori punem 0
            processed_ref.append(0)
    return processed_ref

def save_to_csv(titles, authors, links, references, filename = 'rezultate.csv'):
    """
    Salveaza datele extrase si procesate intr-un fisier CSV.
    :param titles: Lista cu titlurile articolelor
    :param authors: Lista cu autorii articolelor
    :param links: Lista cu link-urile articolelor
    :param references: Lista cu numarul de citari ale articolelor
    :param filename: Numele fisierului CSV
    :return:
    """
    nr_rows = min(len(titles), len(authors), len(links), len(references))

    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["title", "author", "link", "references"])

        for i in range(nr_rows):
            writer.writerow([titles[i], authors[i], links[i], references[i]])

    print(f"Datele au fost salvate in fisierul: {filename}")

result = get_web_data()

titluri = get_title(result)
linkuri = get_links(result)
autori = process_authors(get_author(result))
nr_referinte = process_reference_number(get_reference_number(result))

save_to_csv(titluri, autori, linkuri, nr_referinte)


