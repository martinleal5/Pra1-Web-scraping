import requests
from bs4 import BeautifulSoup
import pandas as pd
from random import randint
from time import sleep


class Scraper:
    """
    Class to scrape the sneakers from Sivasdescalzo.com
    """
    sneakers_list = []
    product_links = []

    def set_product_links(self):
        """
        Function that iterates through the shoe pages, obtaining a file in lxml format.
        In this file it executes a search by href obtaining the links of each one of the products.
        """
        for page in range(0, 10):
            r = requests.get(f'https://www.sivasdescalzo.com/es/calzado?p={page}')

            soup = BeautifulSoup(r.content, 'lxml')
            self.product_list = soup.find_all('div', class_='product-item-info product-card')

            for item in self.product_list:
                for link in item.find_all('a', href=True):
                    self.product_links.append(link['href'])

            sleep(randint(1, 8))

    def get_product_links(self):
        """
        Product links getter.

        :return: a list with the product links.
        """
        return self.product_links

    def set_product_attributes(self):
        """
        Function that iterates through the different products obtaining an lmxl file,
        where it performs a search and extracts its different attributes:
        [name, model, price, discount, description]
        """
        for link in self.product_links:
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
            self.sneakers_list.append(sneakers)
            sleep(randint(1, 5))

    def get_attributes(self):
        """
        Product attributes getter.

        :return: a list with the product attributes.
        """
        return self.product_list

    def transform_to_csv(self):
        """
        Function that transforms data to pandas DataFrame object and
        comma separated value.

        :return: a pandas DataFrame object.
        """
        df = pd.DataFrame(self.sneakers_list)
        df.to_csv('../data/sneakers.csv', sep=',',
                  encoding='utf-8', header=['id', 'name', 'model',
                                            'price', 'discount', 'description'])
        return df


if __name__ == '__main__':
    scrape = Scraper()
    scrape.set_product_links()
    scrape.set_product_attributes()
    scrape.transform_to_csv()
