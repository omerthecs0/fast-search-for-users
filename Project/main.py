##Class for products.
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


##Import e-comemrce site product finder files.
import trendyol
import hepsiburada
import teknosa
import mediamarkt
import ciceksepeti
import vatancomputer



##Main, initialization function.
def main():
    search = take_search() ## Take search text from user.

    ## Initialize the files to take products info
    trendyol.main(search)
    hepsiburada.main(search)
    teknosa.main(search)
    mediamarkt.main(search)
    ciceksepeti.main(search)
    vatancomputer.main(search)


## Take search from user.
def take_search():
    return input("Enter your search: ")



if __name__ == "__main__":
    main()
