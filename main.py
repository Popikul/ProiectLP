"""
Programul foloseste BeautifulSoup si requests pentru a face web scraping
de pe Google Academic. Se folosete keyword-ul "python programming"

Resurse folosite:
Google Scholar Scraping: https://medium.com/@darshankhandelwal12/scrape-google-scholar-using-python-3f35a3a6597b
"""

from scraping_funcs import *
from process_funcs import *

result = get_web_data()

titluri = get_title(result)
linkuri = get_links(result)
autori = process_authors(get_author(result))
nr_referinte = process_reference_number(get_reference_number(result))

save_to_csv(titluri, autori, linkuri, nr_referinte)
