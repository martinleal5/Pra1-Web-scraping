import requests
from bs4 import BeautifulSoup
import pandas as pd

sneakerslist = []
productlinks = []
for page in range(1, 6):
    r = requests.get(f'https://www.sivasdescalzo.com/es/calzado?p={page}')

    soup = BeautifulSoup(r.content, 'lxml')

    productlist = soup.find_all('div', class_='product-item-info product-card')

    for item in productlist:
        for link in item.find_all('a', href=True):
            productlinks.append(link['href'])

for link in productlinks:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')
    name = soup.find('span', class_='product-data__brand-name').text
    model = soup.find('span', class_='product-data__model').text
    price = soup.find('span', class_='price').text
    try:
        discount = soup.find('span', class_='price-discount-percent').text
    except:
        discount = '0 %'
    description = soup.find('div', class_='product-data__short-desc').text.replace('Más información', ' ')
    sneakers = {
        'name': name,
        'model': model,
        'price': price,
        'discount': discount,
        'description': description
    }
    print(sneakers)
    sneakerslist.append(sneakers)

df = pd.DataFrame(sneakerslist)


