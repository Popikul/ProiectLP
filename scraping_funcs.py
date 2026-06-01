# ne ajuta sa obtinem datele HTML de la un anumit site
import requests
from bs4 import BeautifulSoup


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
            # Acesta este inlocui cu " " pentru  avea o structura constanta
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
