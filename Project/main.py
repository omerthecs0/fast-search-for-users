import requests
from bs4 import BeautifulSoup
import trendyol


class Product:
    def __init__(self, kategori="", marka="", ilanismi="", fiyat="", seller="", yorum="", soru="", genel=""):
        self.kategori = kategori
        self.marka = marka
        self.ilanismi = ilanismi
        self.fiyat = fiyat
        self.seller = seller
        self.yorum = yorum
        self.soru = soru
        self.genel = genel


def main():
    search = take_search()
    len_search = len(search.split(" "))
    trendyol.main(search, len_search)


def take_search():
    return input("Enter your search: ")


if __name__ == "__main__":
    main()
