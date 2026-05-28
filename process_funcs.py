import csv
# Pentru procesarea textului cu expresii regulate
import re

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
