# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import requests
from bs4 import BeautifulSoup
import re

PAGE = 'https://www.e-katalog.ru/list/206/'


def parsing_site(start_page):
    pages = get_all_pages(get_html(start_page), start_page)
    prices = []
    # i = 0
    for page in pages:
        # i += 1
        prices += get_prices(get_html(page))
        # if i == 2:
            # break
    print_info(prices)


def get_html(url):
    response = requests.get(url)
    return response.text


def get_all_pages(html, start_page):
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.find('div', class_='ib page-num').find_all('a')
    count_pages = 0
    for element in elements:
        try:
            page = int(element.getText())
            if page > count_pages:
                count_pages = page
        except ValueError:
            pass
    pages = [start_page]
    for i in range(1, count_pages):
        pages.append(start_page + str(i) + "/")
    return pages


def get_prices(html):
    soup = BeautifulSoup(html, 'html.parser')
    elements = soup.select('div.model-price-range span')
    print(elements)
    prices = []
    i = 0
    print('------------------------')
    while i < len(elements):
        price_1 = re.sub('\W+', '', elements[i].getText())
        print('price_1:', price_1)
        i += 1
        price_2 = re.sub('\W+', '', elements[i].getText())
        print('price_2:', price_2)
        if price_2.isnumeric():
            prices.append((float(price_1) + float(price_2)) / 2)
            i += 2
        else:
            prices.append(float(price_1))
            i += 1
    return prices


def print_info(prices):
    sum_price = 0
    for price in prices:
        sum_price += price
    print(prices)
    print("Средняя цена:", round(sum_price / len(prices), 2), 'руб.')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parsing_site(PAGE)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
