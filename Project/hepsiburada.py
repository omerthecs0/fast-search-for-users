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
    d = "https://www.hepsiburada.com/ara?q="
    x = re.sub(r" ", "+", search)
    url = d + x
    take_links(url)


def take_links(url):
    service = Service("./chromediver.exe")
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()
    driver.get(url)
    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    links = []
    for a_tag in soup.find_all('a'):
        link = a_tag.get('href')
        if link:
            links.append(link)
    x = []
    for link in links:
        if link[0] == "/":
            x.append(link)
    del links
    with open("links.txt", "w") as file:
        for i in x:
            if i != "/":
                file.write("https://www.hepsiburada.com" + i + "\n")


def take_product_info():
    with open("links.txt", "r") as file:
        links = file.readlines()
    
    x = 18
    for link in links:
        product = Product(take_kategori(link), take_marka(link), take_ilanismi(link), take_fiyat(link), take_seller(link), take_variants(link), take_ratings(link), take_reviews(link), take_answers(link), take_genel(link), take_other_sellers(link))
        edit_excel(product, x, link)
        x += 1


def take_kategori(link):
    service = Service("./chromediver.exe")
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()
    driver.get(link)

    x = driver.find_element(By.CLASS_NAME, "breadcrumbs")
    x = x.get_attribute("outerHTML")
    html = BeautifulSoup(x, "html.parser")
    text = html.text

    text = text.splitlines()
    x = ""
    for line in text:
        if line != "":
            x += line + " > "
    del text
    return x[:-3]

def take_marka(link):
    service = Service("./chromediver.exe")
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()
    driver.get(link)

    x = driver.find_element(By.CLASS_NAME, "brand-name")
    x = x.get_attribute("outerHTML")
    html = BeautifulSoup(x, "html.parser").getText()

    return html.strip()

def take_ilanismi(link):
    service = Service("./chromediver.exe")
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()
    driver.get(link)

    x = driver.find_element(By.ID, "product-name")
    x = x.get_attribute("outerHTML")
    html = BeautifulSoup(x, "html.parser").getText()
    html = html.strip()
    return html

def take_fiyat(link):
    service = Service("./chromediver.exe")
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()
    driver.get(link)

    x = driver.find_element(By.ID, "offering-price")
    x = x.text
    return x

def take_seller(link):
    service = Service("./chromediver.exe")
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()
    driver.get(link)

    x = driver.find_element(By.CLASS_NAME, "seller")
    x = x.text.splitlines()[1]
    return x

def take_variants(link):
    service = Service("./chromediver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get(link)

    ka = driver.find_elements(By.CLASS_NAME, 'variants-wrapper') ##Opsiyon kategorileri
    a = driver.find_elements(By.CLASS_NAME, "variants-content") ##Varyant html
    variants = [] ##Varyant isimleri
    for i in range(len(a)):
        var_names = a[i].find_elements(By.CLASS_NAME, "variant-name")
        for k in range(len(var_names)):
            variants.append(var_names[k].text)
    choices = re.findall(r'data-value="(.+?)" for', ka[-1].get_attribute("outerHTML"))##Seçenek isimleri
    text = "VARİANTS\n" 
    prices = []
    for i in range(len(ka)):
        time.sleep(5)
        buttons =driver.find_elements(By.CSS_SELECTOR, 'div[data-bind*="setActiveVariantContainer"], input[data-bind*="variantProperties().observe(&quot;Seçenek&quot;)"]') ##Tıklanabilir öğeler.
        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(3)
        buttons[-i-1].click()
        time.sleep(2)
        var_prices = driver.find_elements(By.CLASS_NAME, "variant-property-price") ##Varyantların fiyatları
        for l in range(len(var_prices)):
            prices.append(var_prices[l].text)
        text += f"    {choices[-i-1]}: "
        for i in range(len(variants)):
            text += f"Varyant{i+1}: {variants[i]} {prices[i]} - \n"
        prices = []
    text += "\n(Eğer varyantın fiyatı bulunmuyorsa ürünün o varyantında fiyat bilgisi ve stok sayısı yoktur.)"
    return text

def take_ratings(link):
    service = Service("./chromediver.exe")
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()
    driver.get(link)

    puan = driver.find_element(By.CLASS_NAME, "rating-star")
    puan = puan.text
    rev = driver.find_element(By.ID, "comments-container")
    rev = rev.text
    try:
        rate = driver.find_element(By.CLASS_NAME, "hermes-KeyFeatureBox-module-iQ2SXvuWN9weDMaTCqTR")
        rate = rate.get_attribute("outerHTML")
        rate = BeautifulSoup(rate, "html.parser").getText()

        text =re.sub(r"\)", ") - ", rate)
        return (puan + " Satıcı Puanı \n" + rev + " \n" + text)
    except NoSuchElementException:
        return (puan + " Satıcı Puanı\n" + rev + "\n" + "Features are unavaible for this product")

def take_reviews(link):
    service = Service("./chromediver.exe")
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()
    driver.get(link)

    puan = driver.find_elements(By.CLASS_NAME, "hermes-ReviewCard-module-KaU17BbDowCWcTZ9zzxw")
    x = 1
    tx = ""
    for text in puan:
        text = text.get_attribute("outerHTML")
        text = BeautifulSoup(text, "html.parser")
        text = text.text
        tx += (f"Review {x} -> " + text + "\n")
        x += 1
    return tx
        
def take_answers(link):
    pass

def take_genel(link):
    service = Service("./chromediver.exe")
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()
    driver.get(link)

    puan1 = driver.find_elements(By.CLASS_NAME, "no-border")
    puan1 = puan1[2].get_attribute("outerHTML")
    text1 = BeautifulSoup(puan1, "html.parser").getText()

    puan2 = driver.find_elements(By.CLASS_NAME, "no-border")
    puan2 = puan2[3].get_attribute("outerHTML")
    text2 = BeautifulSoup(puan2, "html.parser").getText()

    x = text2.strip().splitlines()
    txt = []
    for line in x:
        if line != "" and line != "Diğer":
            txt.append(line)
    text2 = ""
    x = 0
    while True:
        text2 += f"{txt[x]} - {txt[x+1]}\n"
        x += 2
        if x == len(txt):
            break
    return text1 + "\n" + text2

def take_other_sellers(link):
    service = Service("./chromediver.exe")
    driver = webdriver.Chrome(service=service)
    driver.minimize_window()
    driver.get(link)

    puan = driver.find_element(By.CLASS_NAME, "chevron-list-container")
    puan = puan.get_attribute("outerHTML")
    with open("anan.txt", "w") as file:
        file.write(puan)
    sellers = re.findall(r'<span data-bind="text: merchantName">(.+?)</span>', puan)
    ratings = re.findall(r'merchantRatingSummary.cssClass">(.+?)</span>', puan)
    prices = re.findall(r'style="text-decoration: none">(.+?)</span>', puan)
    for i in range(len(sellers)):
        if sellers[i] == "Hepsiburada":
            ratings.insert(i, "-")
            break

    text = ""
    for i in range(len(sellers)):
        try:
            text += f"Satıcı {i+2}: {sellers[i]} - {ratings[i]} - Ürün fiyatı: {prices[i]} \n"
        except IndexError:
            text += f"Satıcı {i+2}: {sellers[i]} -  - Ürün fiyatı: {prices[i]} \nSatıcı puanlarında kayma meydana geldi!!"
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
    sheet[f"K{x}"].value = 'HEPSİBURADA'
    sheet[f"L{x}"].value = f'{link}'
    sheet[f"M{x}"].value = f'{product.other_sellers}'

    file.save("products.xlsx")

