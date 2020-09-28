from bs4 import BeautifulSoup
import urllib.request
html_link = 'https://www.payngo.co.il/tv-and-entertainment/led-4k-screens/tv-screens.html'
html_doc = urllib.request.urlopen(html_link)

def is_only_page(category_address):
    temp_soup = BeautifulSoup(urllib.request.urlopen(category_address), "lxml")
    return not bool (temp_soup.find("ul", class_="pagination"))

def is_last_page(category_address):
    temp_soup = BeautifulSoup(urllib.request.urlopen(category_address), "lxml")
    return (temp_soup.find("ul", class_="pagination").find("a", class_="next")["href"]==category_address)

def return_category_links(category_address):
    category_links = []
    if is_only_page(category_address):
        category_links.append(category_address)
        return category_links
    p = 1
    while not (is_last_page(category_address+'?p=%s' % p)):
        category_links.append(category_address+'?p=%s' % p)
        p = p+1
    if is_last_page(category_address+'?p=%s' % p):
        category_links.append(category_address+'?p=%s' % p)
    return category_links

def info(item):
        return {
            "id": item.a.get('data-gtm-product-sku'),
            "properties":{
                "category": item.a.get('data-gtm-product-category'),
                "name": item.a.get('data-gtm-product-name'),
                "price": item.a.get('data-gtm-product-price')
        }

    }

def items_in_page(link):
    soup = BeautifulSoup(urllib.request.urlopen(link), "lxml")
    items = soup("div", class_="item")
    page_dict = {}
    for cur_item in items:
        page_dict[info(cur_item)["id"]] = info(cur_item)["properties"]
    return page_dict

def check_category_links(category_links):
    category_dict = {}
    for x in category_links:
        category_dict.update(items_in_page(x))
    return category_dict

links = return_category_links("https://www.payngo.co.il/air-conditioning-all/air-conditioning/central-mini-air-conditioner.html")
print(check_category_links(links))
print(len(check_category_links(links)))

