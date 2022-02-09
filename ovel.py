from os import write
import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def get_all_links(html):
    links = []
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find('div', class_ = 'browse-view').find_all('div', class_ = 'product floatleft width25 vertical-separator')
    for deputy in divs:
        part_link = deputy.find('a').get('href')
        full_link = "https://mebelpl.kg" + part_link
        links.append(full_link)
    return links

def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    div = soup.find('div', class_ = 'productdetails-view')
    name = div.find('h1').text
    price =  div.find('span', class_ ='PricesalesPrice').text
    text1 = div.find('div', class_ = "product-description gk-product-tab").text
    # size = div.find('')
    data = {
        'name':name,
        'price':price,
        'text':text1
    }
    return data

def write_csv(data):
    with open('deputy.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(
            (data['name'],
            data['price'],
            data['text'])
        )

def main():
    url = f"https://mebelpl.kg/upholstered-furniture/sofas"
    html = get_html(url)
    mebel = get_all_links(html)
    for link in mebel:
        mebel_html = get_html(link)
        data = get_data(mebel_html)
        write_csv(data)
main()