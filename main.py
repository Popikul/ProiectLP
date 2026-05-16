"""
Programul foloseste BeautifulSoup si requests pentru a face web scraping
de pe Google Academic. Se folosete keyword-ul "python programming"

Resurse folosite:
Google Scholar Scraping: https://medium.com/@darshankhandelwal12/scrape-google-scholar-using-python-3f35a3a6597b
"""

from bs4 import BeautifulSoup

# ne ajuta sa obtinem datele HTML de la un anumit site
import requests

def getWebData():
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

rezultate = getWebData()
print(rezultate)