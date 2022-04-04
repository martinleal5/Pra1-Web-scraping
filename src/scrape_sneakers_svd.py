import requests
from bs4 import BeautifulSoup
import pandas as pd
from random import randint
from time import sleep


class ScrapeSneakersSVD:
    sneakerslist = []
    productlinks = []

    def set_links(self):
        for page in range(0, 1):
            r = requests.get(f'https://www.sivasdescalzo.com/es/calzado?p={page}')

            soup = BeautifulSoup(r.content, 'lxml')

            self.productlist = soup.find_all('div', class_='product-item-info product-card')

            for item in self.productlist:
                for link in item.find_all('a', href=True):
                    self.productlinks.append(link['href'])
            sleep(randint(1, 5))
        return self.productlinks

    def get_links(self):
        return self.productlinks

    def set_attributes(self):
        for link in self.productlinks:
            r = requests.get(link)
            soup = BeautifulSoup(r.content, 'lxml')
            name = soup.find('span', class_='product-data__brand-name').text
            model = soup.find('span', class_='product-data__model').text
            price = soup.find('span', class_='price').text.replace('\xa0', '')
            try:
                discount = soup.find('span', class_='price-discount-percent').text
            except:
                discount = '0 %'
            description = soup.find('div', class_='product-data__short-desc').text.replace('Más información',
                                                                                           ' ').rstrip()
            sneakers = {
                'name': name,
                'model': model,
                'price': price,
                'discount': discount,
                'description': description
            }
            print(sneakers)
            self.sneakerslist.append(sneakers)
            sleep(randint(1, 3))

    def get_attributes(self):
        return self.productlist

    def raw_to_workable_data(self):
        df = pd.DataFrame(self.sneakerslist)
        df.to_csv('../data/sneakers.csv', sep=',',
                  encoding='utf-8', header=['id', 'name', 'model',
                                            'price', 'discount', 'description'])


if __name__ == '__main__':
    scrape = ScrapeSneakersSVD()
    scrape.set_links()
    scrape.set_attributes()
    scrape.raw_to_workable_data()
