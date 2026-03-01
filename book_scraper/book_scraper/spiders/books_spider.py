import scrapy
from book_scraper.items import BookItem

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ["http://books.toscrape.com/catalogue/page-1.html"]

    def parse(self, response):
        # loop through each book on the page
        for book in response.css("article.product_pod"):
            title = book.css("h3 > a::attr(title)").get()

            # remove the pound sign and convert to float
            price_text = book.css("p.price_color::text").get()
            price = float(price_text.replace("£", "").replace("Â", "").strip())

            # get availability text and clean whitespace
            avail_parts = book.css("p.availability::text").getall()
            availability = " ".join(avail_parts).strip()

            # rating is a word in the class name e.g. "star-rating Three"
            rating_class = book.css("p.star-rating::attr(class)").get()
            rating_word = rating_class.split()[-1]
            rating_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            rating = rating_map.get(rating_word, 0)

            yield BookItem(
                title=title,
                price=price,
                availability=availability,
                rating=rating
            )

        # go to next page if it exists
        next_page = response.css("li.next > a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
