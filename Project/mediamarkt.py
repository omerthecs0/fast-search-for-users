import requests
from bs4 import BeautifulSoup
import re
from main import Product
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from openpyxl import Workbook, load_workbook
from selenium.common.exceptions import NoSuchElementException
import time




def edit_link(search):
    x = str(search)
    site = "https://www.mediamarkt.com.tr"
    search_link = "https://www.mediamarkt.com.tr/tr/search.html?query=&searchProfile=onlineshop&channel=mmtrtr"
    search = str(search).split(" ")
    search_link = re.sub(r"query=", f"query={search[0]}", search_link)
    for i in range(len(search)-1):
        search_link = re.sub(r"&", f"+{search[i+1]}&", search_link)
    take_html(x, search_link)


def take_html(x, url):
    html = requests.get(url)
    html = BeautifulSoup(html.content, "html.parser")
    html = html.find_all("div", class_="product-wrapper")
    
    x = x.replace(" ", "-")
    links = []
    for i in range(len(html)):
        link = re.findall(r'<a href="(.+?)" itemprop="url"></a>', str(html[i]))
        if x in link[0]:
            links.append(str(link[0].strip()))
    
    
        
    with open("links.txt", "w") as file:
        for link in links:
            file.write(link + "\n")


def take_product_info():
    with open("links.txt", "r") as file:
        links = file.readlines()

    x = 35
    for link in links:
        link = link.strip()
        product = Product(take_kategori(link), take_marka(link), take_ilanismi(link), take_fiyat(link), take_seller(link), take_variants(link), take_ratings(link), take_reviews(link), take_answers(link), take_genel(link), take_other_sellers(link))
        edit_excel(product, x, link)
        x += 1


def take_kategori(link):
    html = requests.get(link)
    html = BeautifulSoup(html.content, "html.parser")
    html = html.find("ul", class_="breadcrumbs").getText()
    text = ""
    for line in html.splitlines():
        if line != "":
            text += " > " + line
    return text

def take_marka(link):
    html = requests.get(link)
    html = BeautifulSoup(html.content, "html.parser")
    html = html.find("div", class_="model")
    html = html.img["alt"]
    return html

def take_ilanismi(link):
    html = requests.get(link)
    html = BeautifulSoup(html.content, "html.parser")
    html = html.find("div", class_="details")
    html = html.h1.getText()
    return html

def take_fiyat(link):
    html = requests.get(link)
    html = BeautifulSoup(html.content, "html.parser")
    html = html.find("div", class_="price big").getText()
    return html.replace(",-", "TL")


def take_seller(link):
    return "MediaMarkt"

def take_variants(link):
    return "Variants are on the excel lines"

def take_other_sellers(link):
    return "There is no other sellers on MediaMarkt."

def take_ratings(link):
    service = Service("./chromediver.exe")
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()
    driver.get(link.strip())
    time.sleep(3)
    x = driver.find_element(By.CLASS_NAME, "content5")
    x = x.get_attribute("outerHTML")
    html = BeautifulSoup(x, "html.parser")
    text = ""
    puan = html.find("dd", class_="bv-rating-ratio-number").getText() + "Değerlendirme Puanı"
    yorum_sayisi = html.find("a", class_="bv-rating-label bv-text-link bv-focusable").getText() + "Değerlendirme Puanı"
    yorum_sayisi = yorum_sayisi.replace(" Bu eylem, değerlendirmelere götürür. Değerlendirme Puanı", "")
    text += puan + yorum_sayisi
    return text

def take_reviews(link):
    service = Service("./chromediver.exe")
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()
    driver.get(link.strip())
    x = driver.find_element(By.CLASS_NAME, "content5")
    x = x.get_attribute("outerHTML")
    html = BeautifulSoup(x, "html.parser")
    headers = html.find_all("h3", class_="bv-content-title")
    headers = re.findall(r'itemprop="headline">   (.+?) </h3>', str(html))
    comments = html.find_all("div", class_="bv-content-summary-body-text")
    comments = re.findall(r'class="bv-content-summary-body-text"> <p>(.+?)</p> </div>', str(html))
    text = ""
    text += "Değerlendirmeler \n" 
    for i in range(len(headers)):
        text += f"    {i+1}.: {headers[i]} - {comments[i]} \n"
    return text


def take_answers(link):
    return "Answer-reply is not avaible for MediaMarkt products"

def take_genel(link):
    service = Service("./chromediver.exe")
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()
    driver.get(link.strip())
    time.sleep(1)
    x = driver.find_element(By.CLASS_NAME, "content3")
    x = x.get_attribute("outerHTML")
    html = BeautifulSoup(x, "html.parser")
    headers = []
    heads = html.find_all("h2")[1:]
    for head in heads:
        headers.append(head.getText())

    categories = html.find_all("section")
    text = ""
    for categori in categories:
        specs = []
        x = categori.getText().splitlines()
        for a in x:
            if a != "":
                specs.append(a)
        
        text += specs[0] + "\n  "
        i = 0
        for _ in range(int((len(specs)-1)/2)):
            text += f"{specs[i+1]} {specs[i+2]} \n  "
            i+=2
        text += "\n"
    return text




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
    sheet[f"K{x}"].value = 'MEDİAMARKT'
    sheet[f"L{x}"].value = f'{link}'
    sheet[f"M{x}"].value = f'{product.other_sellers}'

    file.save("products.xlsx")

