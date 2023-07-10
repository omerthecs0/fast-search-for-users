import requests
from bs4 import BeautifulSoup
import re
from main import Product
from openpyxl import Workbook, load_workbook



product = Product()


def edit_search(url,search, len_search):
    
    s_words = search.split(" ")
    
    for i  in range(len_search-1):
        url = url + s_words[i]
        url += "%20"
    url += s_words[len_search-1]
    url += "&qt="
    for i  in range(len_search-1):
        url = url + s_words[i]
        url += "%20"
    url += s_words[len_search-1]
    url += "&st="
    for i  in range(len_search-1):
        url = url + s_words[i]
        url += "%20"
    url += s_words[len_search-1]
    url += "&os=1"
    take_html(url)




def take_html(url):
    sayfa = requests.get(url)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find_all("div", class_="p-card-chldrn-cntnr card-border")
    edit_html(isim)


def edit_html(isim):
    # satır satır yazdırıyorum hepsini
    with open("links.txt", "w") as file:
        for i in range(len(isim)):
            x = f"{isim[i]}\n"
            file.write(x)


    # ürün linki haline getiriyorum
    with open("links.txt", "r") as file:
        lines = file.readlines()

    with open("links.txt", "w") as file:
        for line in lines:
            line = re.sub(r'(<div class="p-card-chldrn-cntnr card-border"><a href=")', "", line)
            line = re.sub(r'("><div class=").*', "", line)
            line = "https://www.trendyol.com/" + line
            file.writelines(line)
    



def take_product_info():
    with open("links.txt", "r") as file:
        lines = file.readlines()
    create_excel()
    x = 2
    for line in lines:
        product = Product(take_kategori(line), take_marka(line), take_ilanismi(line), take_fiyat(line), take_seller(line), take_yorum(line), take_soru(line), take_genel(line))
        edit_excel(product, x)
        x += 1

def take_kategori(link):
    sayfa = requests.get(link)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find("div", class_="product-detail-breadcrumb full-width").getText()
    return str(isim)
def take_marka(link):
    sayfa = requests.get(link)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find("a", class_="product-brand-name-with-link").getText()
    return str(isim)
def take_ilanismi(link):
    sayfa = requests.get(link)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find("h1", class_="pr-new-br").getText()
    return str(isim)
def take_fiyat(link):
    sayfa = requests.get(link)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find("div", class_="pr-bx-nm with-org-prc").getText()
    return str(isim)
def take_seller(link):
    sayfa = requests.get(link)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find("div", class_="flex-container").getText()
    seller = re.search(r"Bu ürün (.+?) tarafından", isim).group(1)
    return str(seller)
def take_yorum(link):
    pass
def take_soru(link):
    pass
def take_genel(link):
    sayfa = requests.get(link)
    html_sayfa = BeautifulSoup(sayfa.content, "html.parser")
    isim = html_sayfa.find("div", class_="flex-container").getText()
    return str(isim)



def main(search, len_search):
    url = "https://www.trendyol.com/sr?q="
    edit_search(url, search, len_search)
    take_product_info()
    

def create_excel():
    file = Workbook()
    sheet = file.active
    sheet['A1'] = 'Categori'
    sheet['B1'] = 'Brand'
    sheet['C1'] = 'Ad Name'
    sheet['D1'] = 'Price'
    sheet['E1'] = 'Seller'
    sheet['F1'] = 'Comments'
    sheet['G1'] = 'Questions'
    sheet['H1'] = 'General'
    file.save("products.xlsx")

def edit_excel(product, x):
    file = load_workbook("products.xlsx")
    sheet = file.active

    sheet[f"A{x}"].value = f'{product.kategori}'
    sheet[f"B{x}"].value = f'{product.marka}'
    sheet[f"C{x}"].value = f'{product.ilanismi}'
    sheet[f"D{x}"].value = f'{product.fiyat}'
    sheet[f"E{x}"].value = f'{product.seller}'
    sheet[f"F{x}"].value = f'{product.yorum}'
    sheet[f"G{x}"].value = f'{product.soru}'
    sheet[f"H{x}"].value = f'{product.genel}'
    sheet[f"I{x}"].value = 'TRENDYOL'

    file.save("products.xlsx")
