import argparse
import jaap
import pandas

CITY_URL = 'noord+holland/groot-amsterdam/amsterdam'
PRICE_RANGE = '0-2000'
QTY_PAGES = None

args = None

def main():

	df_apartments_ams = jaap.get_apartments_city(city=args.city_url, price=args.price_range, qty_pages=args.qty_pages)
	df_apartments_ams.to_pickle('ams.pkl')


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = 'Scrape data from JAAP')
    parser.add_argument('--city_url', help='URL from City to be scraped e.g. noord+holland/groot-amsterdam/amsterdam', default=CITY_URL)
    parser.add_argument('--price_range', help='price range', default=PRICE_RANGE)
    parser.add_argument('--qty_pages', help='Quantity of result pages to be retrieved', default=QTY_PAGES)
    args = parser.parse_args()

    #Call main function
    main()