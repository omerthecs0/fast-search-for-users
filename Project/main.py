class Product:
    def __init__(self, kategori="", marka="", ilanismi="", fiyat="", seller="", variants="", ratings="", reviews="", answers="", genel="", other_sellers=""):
        self.kategori = kategori
        self.marka = marka
        self.ilanismi = ilanismi
        self.fiyat = fiyat
        self.seller = seller
        self.variants = variants
        self.ratings = ratings
        self.reviews = reviews
        self.answers = answers
        self.genel = genel
        self.other_sellers = other_sellers


import trendyol
import hepsiburada
import teknosa
import mediamarkt
import ciceksepeti


def main():
    search = take_search() ## Take search text from user.

    trendyol.main(search)
    hepsiburada.main(search)
    teknosa.main(search)
    mediamarkt.main(search)
    ciceksepeti.main(search)


def take_search():
    return input("Enter your search: ")



if __name__ == "__main__":
    main()
