import pandas as pd
import json
import requests
from lxml import etree
import time
import numpy as np

HEADERS = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1'}
SLEEP_TIME_BETWEEN_PAGES = 10
SLEEP_TIME_BETWEEN_APARTMENTS = 3

def get_apartment_urls(html_tree):
    
    apartments = html_tree.xpath('//a[contains(@class, "property-inner")]/@href')
    
    return apartments

def get_script_data(html_apartment):
    
    list_json = []
    df = pd.DataFrame()
    
    try:
    
        list_json = html_apartment.xpath('//script[contains(@id, "page-data")]/text()')

        if (len(list_json) > 0 ):
            json_page_data = json.loads(list_json[0].strip())
            #print(json_page_data)
            df = pd.DataFrame.from_dict(json_page_data, orient='index')
            
    except:
        print('Error running get_script_data')
        
    return df

def get_table_data(primary_pois, pois_distances):
    
    df_poi = pd.DataFrame()
    df_pois = pd.DataFrame()
    key = primary_pois.xpath('a/@data-label')
    
    if (len(key) > 0):
        
        key = primary_pois.xpath('a/@data-label')[0].strip()
        name = primary_pois.xpath('a/text()')[0]
        distance = pois_distances.xpath('text()')[0]

        if (len(str(distance).split('kilometer')) > 1):
            distance = str(distance).replace('kilometer', '')
            distance = float(distance.replace('\xa0', '').replace(',','.'))*1000
        else:
            distance = str(distance).replace('meter', '').replace('\xa0', '').replace(',', '.')
            distance = float(distance)

        df_poi['{}_name'.format(key)] = [name]
        df_poi['{}_distance'.format(key)] = [distance]

        df_pois = pd.concat([df_pois, df_poi], axis=1, sort=False)
    
    return df_pois

def get_apartment_info(url):
    
    df_pois = pd.DataFrame()
    df = pd.DataFrame()
    request = requests.get(url, headers=HEADERS)
    print(url)
    html_apartment = etree.HTML(request.text)
    
    description = html_apartment.xpath('//div[contains(@id, "long-description")]/text()')
    kamers = html_apartment.xpath('//div[contains(@class, "detail-tab-content kenmerken")]/descendant::td[contains(@class, "value")][12]/text()')
    
    if len(kamers) > 0:
        kamers = kamers[0].strip()
        
    df = get_script_data(html_apartment)
    
    primary_pois = html_apartment.xpath('//td[contains(@class, "value-1-2")]')
    pois_distances = html_apartment.xpath('//td[contains(@class, "value-2-2")]') 
    
    if ((len(primary_pois) > 0) & (len(pois_distances) > 0)):
        
        df_pois = pd.DataFrame()
        list_pois = []
        
        for i in range(0, len(primary_pois)):
            
            df_poi = get_table_data(primary_pois[i], pois_distances[i])
            df_pois = pd.concat([df_pois, df_poi], axis=1, sort=False)
        
    
    df_apartment = pd.concat([df.transpose(), df_pois], axis=1)
    df_apartment['description'] = str(description).strip()
    df_apartment['kamers'] = str(kamers)
    
    return df_apartment


def get_apartments_city(city, price, qty_pages = None):

    
	initial_url = 'https://www.jaap.nl/huurhuizen/{}/{}/p{}'
	url = initial_url.format(city, price, 1)

	request = requests.get(url=url, headers=HEADERS)
	html = etree.HTML(request.text)

	nav_items = html.xpath('//a[contains(text(), "q")]')
	final_page = int(nav_items[0].xpath('@href')[0].split('amsterdam/{}/p'.format(price))[1])

	if (qty_pages is None):
	    qty_pages = final_page

	df_apartments = pd.DataFrame()

	for i in range(1, qty_pages + 1):

	    time.sleep(SLEEP_TIME)

	    print(url)

	    apartment_urls = html.xpath('//a[contains(@class, "property-inner")]/@href')

	    for apartment_url in apartment_urls:

	    	time.sleep(SLEEP_TIME_BETWEEN_APARTMENTS)
	        df_apartment = get_apartment_info(apartment_url)
	        df_apartments = pd.concat([df_apartments, df_apartment], axis=0)

	    url = initial_url.format(city, price, i+1)
	    request = requests.get(url, headers=HEADERS)
	    html = etree.HTML(request.text)

	    i += 1
	    
	return df_apartments
