import requests
from bs4 import BeautifulSoup
import pandas as pd
from random import randint
from time import sleep
import os


class Scraper:
    """
    Class to scrape the sneakers from Sivasdescalzo.com
    """

    sneakers_list = []

    def __init__(self):
        self.product_links = None

    def set_product_attributes(self, product_info):
        """
        Function that iterates through HTTP requests, extracting the
        different attributes needed.
        """
        for products in product_info:
            name = products.find('a', class_='set-product-storage').text
            model = products.find('a', class_='product-item-link set-product-storage').text
            # Here we get a list with different prices that we unpack, replace for character error.
            prices = products.find('span', class_='price').text.replace('\xa0€', '').split()
            act_price = prices[0]
            try:
                old_price = prices[1]
                try:
                    discount = prices[2]
                except:
                    discount = '0%'
            except:
                old_price = act_price
                discount = '0%'

            sneakers = {
                'name': name,
                'model': model,
                'actual price (€)': act_price,
                'old price (€)': old_price,
                'discount': discount
            }
            print(sneakers)
            self.sneakers_list.append(sneakers)

    def scrape_product_info(self):
        """
        Function that iterates through the shoe pages doing HTTP requests,
        to obtain a BeautifulSoup object to do searches by tag, scrapping
        the information needed.
        """
        for page in range(1, 20):
            r = requests.get(f'https://www.sivasdescalzo.com/es/calzado?p={page}')
            soup = BeautifulSoup(r.content, 'lxml')
            self.product_links = soup.find_all('div',
                                               class_='product-card__info product details product-item-details')
            self.set_product_attributes(self.product_links)
            # Handling anti-scraping mechanism
            sleep(randint(1, 4))

    def get_product_attributes(self):
        """
        Product attributes getter.

        :return: a list with the product attributes.
        """
        return self.sneakers_list

    def create_data_folder(self):
        """
        Function that creates a folder to store the scrapped data.
        """
        if not os.path.exists('../data/'):
            os.mkdir('../data/')

    def transform_to_csv(self):
        """
        Function that transforms data to pandas DataFrame object and
        comma separated value.

        :return: a pandas DataFrame object.
        """
        df = pd.DataFrame(self.sneakers_list)
        self.create_data_folder()
        df.to_csv('../data/SVD_sneakers.csv', sep=',',
                  encoding='utf-8',
                  header=['name', 'model',
                          'actual price', 'old price', 'discount']
                  )
        return df


if __name__ == '__main__':
    scrape = Scraper()
    scrape.scrape_product_info()
    scrape.transform_to_csv()
