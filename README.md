# fast-search-for-users

TR
Bu projede yazmış olduğum kod, kullanıcıların e-ticaret sitelerinde gereğinden fazla zaman kaybetmeden ürün araştırması yapmalarını sağlamaktadır.

Kod şu şekilde çalışmaktadır; kullanıcıdan aldığı arama kelimesi ile e-ticaret sitelerinde arama yaparak, arama sonucu çıkan tüm ürünlein linkini alır ve tüm liklere gider. Bu gitmiş olduğu web sitelerde web scraping(web sitelerinin html kodlarından site içerisindeki verileri almak ) yaparak aldığı verilerle bir .xlsx dosyasında tablo şeklinde verileri kaydeder. Web sitelerinden aldığı bilgiler;
      Ürün kategorisi, markası, ismi, fiyatı, değerlendirmeleri, genel bilgileri, satıcı adı, diğer satıcılar(değerlendirmeleri ve ürün ücretleri dahil)...
      
Bu program ile birlikte kullanıcılar teker teker e-ticaret sitelerinde istedikleri ürünü aramak için zaman kaybetmekten, enerji harcamaktan ve aradıkları ürünler arasında kararsız kalmaktan kurtuluyor. Çünkü bu program birkaç dakika içerisinde kullanıcıya arama sonuçlarını excel dosyası olarak tablo halinde düzenli bir şekilde sunmaktadır.


PROJENİN GENEL DURUMU:    Şu anda sadece trendyol, hepsiburada, teknosa ve mediamarkt siteleri için sonuç getirmektedir. Diğer siteler ve google alışveriş aramaları için hala çalışıyorum. "iphone 11" araması yapıldığında ortaya çıkan sonuç şudur -> https://github.com/omerthecs0/fast-search-for-users/blob/main/products.xlsx

-------------------------------------------------------------------------------------------------------------------------------------------------------------------

EN
In this project, the code I have written enables users to conduct product research on e-commerce websites without wasting excessive time. The code works as follows: It takes a search keyword from the user and performs searches on e-commerce websites. It collects all the links of products from the search results and visits each link one by one. Upon visiting these websites, it performs web scraping, extracting data from the HTML codes of the websites to gather relevant information about the products. This information is then stored in a .xlsx file in tabular form.

The data collected from the websites includes product category, brand, name, price, reviews, general details, seller name, and other sellers' information (including reviews and product prices).

With this program, users are relieved from the time-consuming, energy-draining, and indecisive process of individually searching for their desired products on e-commerce websites. Because this program presents search results to the user within a few minutes, in the form of a well-organized table in an Excel file..

CURRENT STATE OF THE PROJECT: Currently, the code is working for trendyol, hepsiburada, teknosa ve mediamarkt websites. I am still working on adding support for other websites and Google Shopping searches. When the search keyword "iphone 11" is used, the results obtained can be found at this link: https://github.com/omerthecs0/fast-search-for-users/blob/main/products.xlsx

