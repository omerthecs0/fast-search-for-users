import requests
from bs4 import BeautifulSoup
import re
from main import Product
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from openpyxl import Workbook, load_workbook
from selenium.common.exceptions import NoSuchElementException





def edit_link(search):
    url = "https://www.ciceksepeti.com/arama?query="
    search = search.strip().split(" ")
    search = "%20".join(search)
    url += search + "&qt=" + search + "&choice=2"
    take_links(url)


def take_links(url): 
    sepet_link = "https://www.ciceksepeti.com"
    html = requests.get(url)
    html = BeautifulSoup(html.content, "html.parser")
    products = html.find_all("div", class_="products__item-inner")
    links = []
    for product in products:
        link = product.a.get("href")
        links.append(sepet_link + link.strip())
    
    links = links[:12]
    with open("links.txt", "w") as file:
        for link in links:
            file.writelines(link + "\n")


def take_product_info():
    with open("links.txt", "r") as file:
        lines = file.readlines()

    x = 48
    for link in lines:
        link = link.strip()
        html = requests.get(link)
        html = BeautifulSoup(html.content, "html.parser")
        products = html.find("p", class_="page404__text-error")
        if products == None:
            product = Product(take_kategori(link), take_marka(link), take_ilanismi(link), take_fiyat(link), take_seller(link), take_variants(link), take_ratings(link), take_reviews(link), take_answers(link), take_genel(link), take_other_sellers(link))
            edit_excel(product, x, link)
            x += 1


def take_kategori(link):
    html = requests.get(link)
    html = BeautifulSoup(html.content, "html.parser")
    categori = html.find("ul", class_="js-breadcrumb breadcrumb--product").getText()
    categori = categori.replace("      ", " > ")
    return categori

def take_marka(link):    
    html = requests.get(link.strip())
    html = BeautifulSoup(html.content, "html.parser")
    try:
        brand = html.find("div", class_="product__info-wrapper--left")
        brand = re.findall(r'class="product__info__brand__link js-brand-length" href=".+">(.+?)</a>', str(brand))
        return (brand[0])
    except IndexError:
        return "Seller hasn't identified brand"

def take_ilanismi(link):
    html = requests.get(link)
    html = BeautifulSoup(html.content, "html.parser")
    name = html.find("div", class_="product__info-wrapper--left")
    name = re.findall(r'class="js-product-title js-ellipsize-text">(.+?)</span>', str(name))[0]
    return name

def take_fiyat(link):
    html = requests.get(link)
    html = BeautifulSoup(html.content, "html.parser")
    price = html.find("div", class_="product__info__new-price__integer js-price-integer").getText()
    price += " TL Sepet Fiyatı"
    old_price = html.find("div", class_="product__info__old-price").getText().strip()
    if old_price == "":
        return (price)
    else:
        return (old_price + f" - İmndirimli {price}")

def take_seller(link):
    html = requests.get(link)
    html = BeautifulSoup(html.content, "html.parser")
    seller = html.find("a", class_="product__seller-name").getText()
    seller_point = html.find("span", class_="product__seller-point best").getText()
    return (seller + " " + seller_point)

def take_variants(link):
    service = Service("./chromediver.exe")
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()
    driver.get(link)
    try:
        variants = driver.find_element(By.CLASS_NAME, "product__variants-title").text
        driver.quit()
        return variants
    except NoSuchElementException:
        return "There'is no variants for this product"

def take_ratings(link):
    html = requests.get(link)
    html = BeautifulSoup(html.content, "html.parser")
    try:
        ratings = html.find("div", class_="dropdown product__dropdown-evaluation js-dropdown-evaluation").getText()
        ratings = re.findall(r'(.+?)yıldız ', str(ratings))[0].strip() + " yıldız"
        return ratings
    except AttributeError:
        return "There's no ratings for this product."
    except IndexError:
        return "There's no ratings for this product."

def take_reviews(link):
    html = requests.get(link)
    html = BeautifulSoup(html.content, "html.parser")

    try:
        reviews = html.find_all("div", class_="ns-reviews--item-comment")
        text = ""
        i = 1
        for review in reviews:
            text += f"Yorum {i} - " + review.getText().strip() + "\n"
            i+=1
        if text != "":
            return text
        else:
            return "There's no comments(reviews) for this product."
    except AttributeError:
        return ("There's no comments(reviews) for this product.")

def take_answers(link):
    pass

def take_genel(link):
    html = requests.get(link)
    html = BeautifulSoup(html.content, "html.parser")
    summary = html.find("div", class_="product__property__box").getText() + "\n"
    exp = html.find("div", class_="product__description").getText().strip() + "\n"
    specs = html.find_all("div", class_="product__specifications__table-row")
    features = ""
    for spec in specs:
        features += (spec.getText().strip()) + "\n"
    return (summary + exp + features)

def take_other_sellers(link):
    pass



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
    sheet[f"F{x}"].value = f'{product.variants}'
    sheet[f"G{x}"].value = f'{product.ratings}'
    sheet[f"H{x}"].value = f'{product.reviews}'
    sheet[f"I{x}"].value = f'{product.answers}'
    sheet[f"J{x}"].value = f'{product.genel}'
    sheet[f"K{x}"].value = 'ÇİÇEKSEPETİ'
    sheet[f"L{x}"].value = f'{link}'
    sheet[f"M{x}"].value = f'{product.other_sellers}'

    file.save("products.xlsx")

