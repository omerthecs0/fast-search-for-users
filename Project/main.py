
class Product:
    def __init__(self, kategori="", marka="", ilanismi="", fiyat="", seller="", other_sellers="", ratings="", reviews="", answers="", genel=""):
        self.kategori = kategori
        self.marka = marka
        self.ilanismi = ilanismi
        self.fiyat = fiyat
        self.seller = seller
        self.other_sellers = other_sellers
        self.ratings = ratings
        self.reviews = reviews
        self.answers = answers
        self.genel = genel


import trendyol
import hepsiburada
import teknosa


def main():
    search = take_search()
    len_search = len(search.split(" "))
    trendyol.main(search, len_search)
    hepsiburada.main(search)
    teknosa.main(search)


def take_search():
    return input("Enter your search: ")


if __name__ == "__main__":
    main()
