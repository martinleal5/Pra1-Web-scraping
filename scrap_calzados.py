# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 12:43:07 2022

@author: martin
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
from random import randint
from time import sleep
import os  



# Creamos una lista en la que introducir la info útil que obtengamos
sneakers_list = []

# Recorremos las páginas de la web para extraer información de todos los zapatos
for i in range(1,20):
    r = requests.get(f'https://www.sivasdescalzo.com/es/calzado?p={i}')
    soup = BeautifulSoup(r.content, 'lxml')

    # Creamos lista de los productos
    product_list = soup.find_all('div', class_ = 'product-card__info product details product-item-details')

    # Extraemos la info que nos interesa de cada producto
    for product in product_list:
        name = product.find('a', class_ = 'set-product-storage').text
        model = product.find('a', class_ = 'product-item-link set-product-storage').text
        # price_list contiene el precio del artículo
        # En caso de que se le aplique un descuento, contiene el precio actual, el original y el descuento
        price_list = product.find('span', class_ = 'price').text.replace('\xa0€', '').split()
        act_price = price_list[0]
        try:
            old_price = price_list[1]
            try: 
                discount = price_list[2]
            except:
                discount = '0%'
                
        except:
            old_price = act_price
            discount = '0%'
        
        # Almacenamos la info en un diccionario
        sneaker = {
            'name': name,
            'model': model,
            'actual price (€)': act_price,
            'old price (€)': old_price,
            'discount(%)': discount
            }
        sneakers_list.append(sneaker)
    
    # Esperamos un tiempo para realizar la siguiente búsqueda y evitar bloqueos
    sleep(randint(1, 4))

# Almacenamos los datos en un data frame
df = pd.DataFrame(sneakers_list)

# Creamos un directorio donde guardar el dataset en formato csv 
os.makedirs('data', exist_ok=True)
df.to_csv('data/SVD_calzados.csv',
          sep=',',
          encoding='utf-8',
          header=['name', 'model', 
                  'actual price', 'old price', 'discount'])
