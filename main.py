import csv
import requests
from bs4 import BeautifulSoup

MAIN_URL = 'https://www.mashina.kg/search/all/'

def get_page(url):
    headers ={"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
    response = requests.get(url)
    return response.text
    
def get_soup(page_content):
    soup = BeautifulSoup(page_content, 'lxml')
    return soup

def get_last_page_number(soup):
    pagination_list = soup.find('ul', class_='pagination').find_all('li')
    item = pagination_list[-1]
    last_page_num = item.find('a').get('href').split('=')[-1]
    return int(last_page_num)

def get_product_cards(soup):
    product_list = soup.find('div', class_='table-view-list')
    products = product_list.find_all('div', class_='list-item')
    return products

def write_to_csv(data):
    with open('cars.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, delimiter='/')
        writer.writerow((data['title'],
                        data['price'],
                        data['images'],
                        data['info']))

def get_data_from_card(products):
    for car in products:
        try:
            product_title_element = car.find('h2').text    
            title = product_title_element.strip()
        except:
            title = ''

        try:
            product_price_element = car.find('p', class_='price').text
            price = product_price_element.replace(' ', '').replace('\n', ' ').strip()
        except:
            price = ''

        try:
            images = car.find('a').find('img').get('data-src')
        except:
            images = ''
        try:
            product_information_element = car.find('div', class_='item-info-wrapper').text
            info = product_information_element.replace(' ', '').replace('\n', '').strip().rstrip('назад')
        except:
            info = ''

        data = {'title': title, 'price': price, 'images': images, 'info': info}
        write_to_csv(data)

def main():
    page_func = get_page(MAIN_URL)
    soup = get_soup(page_func)
    last_page_num = get_last_page_number(soup)

    for page in range(1, last_page_num + 1): 
        page_url = MAIN_URL + '?page=' + str(page)
        page_content = get_page(page_url)
        soup = get_soup(page_content)
        cards = get_product_cards(soup)
        get_data_from_card(cards)
        
        
if __name__ == '__main__':
    main()







