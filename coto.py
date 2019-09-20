# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from datetime import datetime, timedelta

import urllib, json, mysql.connector

import requests
from bs4 import BeautifulSoup
import sys
import re

reload(sys)

sys.setdefaultencoding('utf-8')

# API Core

######## COTO ########
rCoto = requests.get('https://www.cotodigital3.com.ar/sitios/cdigi/#')
soupCoto = BeautifulSoup(rCoto.text, "html.parser")

regexCategoriasCoto = re.compile('(\w*thrd_level_catv\w*)')
categoriasCoto = soupCoto.find_all(id=regexCategoriasCoto)

## Función que recorre cada producto
def recorreProducto(producto):
    for i in producto:
        descripcion = i.find(class_='span_productName').find(class_='descrip_full').get_text()
        ## Recorro todos los precios que haya
        key = -1
        precios = []
        for item in i.find_all_next(string=True):
            key = key+1
            if (item.find('$') != -1):
                precios.append(i.find_all_next(string=True)[key].replace('\n', '').strip())
        
        ## 0: Precio x kilo
        ## 1: Precio al contado
        ## 2: Precio con oferta
        precio = precios[1]
        print(descripcion + ' - ' + precio)
    pass

## Entro a las categorías
try:
    for cat in categoriasCoto:
        linksCoto = cat.find_all('a')
        for link in linksCoto:
            print(link.get_text().strip())

            href = link.get('href')
            rHref = requests.get('https://www.cotodigital3.com.ar'+href)
            soupPage = BeautifulSoup(rHref.text, "html.parser")

## Entro a cada página
            ulPaginadoCoto = soupPage.find(class_='atg_store_pagination')
            # Si tiene paginado
            if (ulPaginadoCoto):
                li = ulPaginadoCoto.find_all('li')
                for pagina in li:
                    # Si no está seleccionada la página
                    print("Pagina: " + pagina.get_text().replace('\n', ''))
                    if (pagina.find('a') and pagina.find('a').get('href')):
                        rPage = pagina.find('a').get('href')
                        
                        rHrefPage = requests.get('https://www.cotodigital3.com.ar'+rPage)
                        soupPageHref = BeautifulSoup(rHrefPage.text, "html.parser")

                        ## Título del producto: 
                        productos = soupPageHref.find_all(class_='product_info_container')
                        recorreProducto(productos)
                    # Si la página está seleccionada lo hago una vez
                    elif (pagina.find('a') and not pagina.find('a').get('href')):
                        ## Título del producto: 
                        productos = soupPage.find_all(class_='product_info_container')
                        recorreProducto(productos)
            # Si no tiene paginado
            else:
                print("Pagina: 1")
                ## Título del producto: 
                productos = soupPage.find_all(class_='product_info_container')
                recorreProducto(productos)
except Exception, e:
    print(e)
    