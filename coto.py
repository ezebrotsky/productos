# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from datetime import datetime, timedelta

import urllib, json, mysql.connector

import requests
from bs4 import BeautifulSoup
import sys
import re
import time

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
        #time.sleep(10)
        descripcion = i.find(class_='span_productName').find(class_='descrip_full').get_text()
        precio = i.find_next(class_='atg_store_newPrice').get_text().replace('PRECIO CONTADO', '').replace('\n ', '').strip()
        #print(i.find_next(class_='atg_store_productPrice').remove('style'))
        print(descripcion + ' - ' + precio)
    pass

## Entro a las categorías
try:
    for cat in categoriasCoto:
        linksCoto = cat.find_all('a')
        for link in linksCoto:
            print("Producto: " + link.get_text())

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
                    if (pagina.find('a') and pagina.find('a').get('href')):
                        print("Pagina: " + pagina.get_text().replace('\n', ''))

                        rPage = pagina.find('a').get('href')
                        
                        rHrefPage = requests.get('https://www.cotodigital3.com.ar'+rPage)
                        soupPageHref = BeautifulSoup(rHrefPage.text, "html.parser")

                        ## Título del producto: 
                        productos = soupPageHref.find_all(class_='product_info_container')
                        recorreProducto(productos)
                    # Si la página está seleccionada lo hago una vez
                    else:
                        ## Título del producto: 
                        productos = soupPage.find_all(class_='product_info_container')
                        recorreProducto(productos)
            # Si no tiene paginado
            else:
                ## Título del producto: 
                productos = soupPage.find_all(class_='product_info_container')
                recorreProducto(productos)
except Exception, e:
    print(e)
    