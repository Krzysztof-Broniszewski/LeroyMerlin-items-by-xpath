# Napisz dla Amazona program, który automatycznie wyciąga wybrane informacje z wybranych stron internetowych, na przykład nazwy produktów ze stron Leroy Merlin. Użytkownik podaje jedynie adres strony oraz ścieżkę xpath, którą może łatwo skopiować w przeglądarce.

# 1. Użyj biblioteki click, aby łatwiej było Ci odczytać url oraz xpath.

# 2. Podziel kod na funkcje tak, aby można było go łatwo testować.

# 3. Napisz kilka testów. Zacznij od tzw. happy path, tzn. najprostszego przypadku, a następnie przetestuj przypadki brzegowe.

# 4. Wyciągając z HTML tekst, usuń białe znaki z początku i końca (poszukaj odpowiedniej metody na stringach) oraz zamień znaki końca linii na spacje.

# 5. Wyświetl każdy znaleziony item HTML w osobnej linii.

# 6. Użyj docstringów, aby udokumentować Twój kod. Jakie informacje Twoim zdaniem warto tam zawrzeć?

# Hint: W razie problemów z cudzysłowami w XPATH pod Windows, możesz zamienić je na apostrofy, np.:
#     "//div[@id='wartosc']" 
# zamiast 
#     '//div[@id="wartosc"]'

import requests

from lxml.html import fromstring

import click

""" USAGE
     python M05L20_projekt.py <url> <elements from html>

     python M05\M05L20_projekt.py https://www.leroymerlin.pl/izolacja-budynkow/kleje-uszczelniacze-izolacje,a395.html //*[@id="product-listing"]/div/a/h3

Printing all name of items from given web site
     
"""


def scrape(url):
    """
    Scraping url adress from shell
    
    """
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.text
    elif resp.status_code == 404:
        click.secho(f"ERROR 404 -> Missing {url}", fg="red")
    else:
        click.secho(f"ERROR: {resp.status_code}", fg="red")
   

final_items = []
def beautification(items):
    """
    
    Changing the items to better visualization:
        - removing the tabulation and new line characters
        - giving the clear list of elements 

    """
    PUNCTUATION = ["\n","\t"]
    for item in items:
        for punc in PUNCTUATION:
            item = item.replace(punc, " ").strip()
        final_items.append(item)
    return final_items


def display(items):
    """
    Display the final form on elements in green color.

    """
    click.secho("-" * 100, fg="blue")
    for item_f in items:
        click.secho(f"-> {item_f}", fg="green")
    click.secho("-" * 100, fg="blue")

@click.command()
@click.argument('url')
@click.argument('elements')


def show_elements(url, elements):
    """
    This is the main function with other smaller functions inside
    Changing the html and xpath to the lists and showing the final result.

    """

    html = scrape(url)
    
    dom = fromstring(html)

    lines = dom.xpath('//*[@id="product-listing"]/div/a/h3')  # Musialem podac recznie xpath bo poniższa sekwencja nie dziala...
    # lines = dom.xpath(elements)  # Wiem, ze tak to powinno wygladac, ale to mi nie dziala i nie wiem dlaczego ?? Bez znaczenia czy wpisze argument w wierszu polecen w cudzyslowach czy bez.... przypuszczam, że chodzi o cudzyslowy i apostrofy... probowalem z r' i tez nie udalo sie. Przeszukałem cały internet i nie znalazlem rozwiazania)

    items = [line.text for line in lines]

    beautification(items)
    display(final_items)

if __name__ == "__main__":
    show_elements()

# PUNCTUATION = ["\n","\t"]

# url = "https://www.leroymerlin.pl/izolacja-budynkow/kleje-uszczelniacze-izolacje,a395.html"

# request = requests.get(url)

# text = request.text

# dom = fromstring(text)
# print(dom)

#     # if elements == None:
# elements = dom.xpath('//*[@id="product-listing"]/div/a/h3')

# elements_list = [item for item in elements]
# print(f"LISTA: {elements_list}")
# for element_li in elements_list:
#     print(element_li.text)

# for item in elements_list:
#     for char in item:
#         for punc in PUNCTUATION:
#             item = item.replace(punc, " ").strip()
#     print("-", item.text_content())

# print(html.text_content())


