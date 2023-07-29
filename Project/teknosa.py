import requests
from bs4 import BeautifulSoup
import re
from main import Product
from openpyxl import Workbook, load_workbook
from requests.exceptions import ConnectionError
import time
import requests



def retry(func, retries=3):
    def retry_wrapper(*args, **kwargs):
        attempts = 0
        while attempts < retries:
            try:
                return func(*args, **kwargs)
            except ConnectionError as e:
                print(attempts)
                time.sleep(2)
                attempts += 1
    return retry_wrapper

@retry
def get_page_content(link):
    return requests.get(link.strip())



def edit_link(search):
    url = "https://www.teknosa.com/arama/?s="
    search = re.sub(r" ", "+", search)
    url += search
    take_links(url)


def take_links(url):
    sayfa = get_page_content(url)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find_all("div", class_="products")


    x = re.findall(r'href="(.+)" title', str(isim))
    x = x[:12]
    linkler = []
    for i in x:
        linkler.append("https://www.teknosa.com" + re.sub(r"\?shopId=.+", "", i))

    with open("links.txt", "w") as file:
        for i in range(12):
            file.writelines(linkler[i] + "\n")



def take_product_info():
    with open("links.txt", "r") as file:
        lines = file.readlines()

    x = 35
    for link in lines:
        print(x)
        product = Product(take_kategori(link), take_marka(link), take_ilanismi(link), take_fiyat(link), take_seller(link), take_other_sellers(link), take_ratings(link), take_reviews(link), take_answers(link), take_genel(link))
        edit_excel(product, x, link)
        x += 1


def take_kategori(link):
    sayfa = get_page_content(link)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find("ol", class_="breadcrumb").getText()

    isim = isim.strip().splitlines()
    categori = ""
    for line in isim:
        if line != "":
            categori += line + " / "
    return categori[:-3]

def take_marka(link):
    sayfa = get_page_content(link)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find("h1", class_="pdp-title")
    x = re.findall(r".+><b>(.+?)</b></a>  (.+?)</h1>", str(isim))
    return x[0][0]

def take_ilanismi(link):
    sayfa = get_page_content(link)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find("h1", class_="pdp-title")
    x = re.findall(r".+><b>(.+?)</b></a>  (.+?)</h1>", str(isim))
    return x[0][1]

def take_fiyat(link):
    sayfa = get_page_content(link)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find("span", class_="prc prc-last").getText()
    return isim

def take_seller(link):
    sayfa = get_page_content(link)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find("div", class_="pdp-seller-info").getText()
    isim = isim.splitlines()
    text = isim[0] + ": " + isim[1]
    return text

def take_other_sellers(link):
    sayfa = get_page_content(link)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find_all("div", class_="pds active")
    isim += html_sayfa.find_all("div", class_="pds hide")
    if isim == []:
        return "No more sellers"
    else:
        sellers = re.findall(r'"><b>(.+?)</b></a>', str(isim))
        links = re.findall(r'data-prod-seller-url="(.+?)">', str(isim))
        for i in range(len(links)):
            if "teknosa" in links[i]:
                sellers.insert(i, "Teknosa")
        prices = re.findall(r'class="prc prc-last">(.+?)</span>', str(isim))
        text = ""
        for i in range(len(isim)):
            text += f"Satıcı {i+2}: {sellers[i]} - Fiyat: {prices[i]} - Link: {links[i]}\n"
        return (text)

def take_ratings(link):
    sayfa = get_page_content(link)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find("div", class_="pdp-rating").getText()
    isim = isim.strip().splitlines()

    tx = []
    for i in isim:
        if i != "":
            tx.append(i.strip())
    return ("Ürün Puanı: " + tx[0]+ " " + tx[1])

def take_reviews(link):
    pass
        
def take_answers(link):
    pass

def take_genel(link):
    sayfa = get_page_content(link)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find_all("p", class_="")
    text = ""
    for i in isim:
        text += i.getText()
    return (text)




def main(search):
    edit_link(search)
    take_product_info()


def edit_excel(product, x, link):
    file = load_workbook("products.xlsx")
    sheet = file.active

    sheet[f"A{x}"].value = f'{product.kategori}'
    sheet[f"B{x}"].value = f'{product.marka}'
    sheet[f"C{x}"].value = f'{product.ilanismi}'
    sheet[f"D{x}"].value = f'{product.fiyat}'
    sheet[f"E{x}"].value = f'{product.seller}'
    sheet[f"F{x}"].value = f'{product.ratings}'
    sheet[f"G{x}"].value = f'{product.reviews}'
    sheet[f"H{x}"].value = f'{product.answers}'
    sheet[f"I{x}"].value = f'{product.genel}'
    sheet[f"J{x}"].value = 'TEKNOSA'
    sheet[f"K{x}"].value = f'{link}'
    sheet[f"L{x}"].value = f'{product.other_sellers}'

    file.save("products.xlsx")
