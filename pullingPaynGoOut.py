from bs4 import BeautifulSoup
import urllib.request
import csv
html_link = 'https://www.payngo.co.il/'
html_doc = urllib.request.urlopen(html_link)

def is_only_page(category_address): #returns True if the category has only one page
    temp_soup = BeautifulSoup(urllib.request.urlopen(category_address), "lxml")
    return not bool (temp_soup.find("ul", class_="pagination"))

def is_last_page(category_address): #returns True if the page is the last page of the category
    temp_soup = BeautifulSoup(urllib.request.urlopen(category_address), "lxml")
    return (temp_soup.find("ul", class_="pagination").find("a", class_="next")["href"]==category_address)

def return_category_dict(category_address): #returns category dict after looping through all pages
    category_dict = {}
    if is_only_page(category_address):
        category_dict.update((items_in_page(category_address)))
        return category_dict
    p = 1
    while not (is_last_page(category_address+'?p=%s' % p)):
        category_dict.update(items_in_page(category_address+'?p=%s' % p))
        p = p+1
    if is_last_page(category_address+'?p=%s' % p):
        category_dict.update(items_in_page(category_address+'?p=%s' % p))
    return category_dict

def info(item): #returns all the info in the current <div class=item> as dict
        return {
            "id": item.a.get('data-gtm-product-sku'),
            "properties":{
                "category": item.a.get('data-gtm-product-category'),
                "name": item.a.get('data-gtm-product-name'),
                "price": item.a.get('data-gtm-product-price')
        }

    }

def items_in_page(link): #returns a dict containing all items info in page
    soup = BeautifulSoup(urllib.request.urlopen(link), "lxml")
    items = soup("div", class_="item") #saves a list of <div>s whose class is "item"
    page_dict = {} #saves items info from the page
    for cur_item in items:
        page_dict[info(cur_item)["id"]] = info(cur_item)["properties"]
    return page_dict

def return_categories(index_html):#returns a list of all category links from the index page
    soup = BeautifulSoup(urllib.request.urlopen(index_html), "lxml")
    divs = soup.findAll("div", class_="sub")
    dds=[]
    links=[]
    for x in divs:
        dds = dds + x.findAll("dd")
    for j in dds:
         links.append(j.find("a").get('href'))
    return links

categories = return_categories(html_link)
with open('products.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['id', 'name', 'price', 'category'])
    for i in categories:
        category_dict = return_category_dict(i)
        for d in category_dict:
            writer.writerow([d, category_dict[d]["name"], category_dict[d]["price"], category_dict[d]["category"]])




