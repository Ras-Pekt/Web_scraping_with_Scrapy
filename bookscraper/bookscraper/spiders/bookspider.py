import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            next_page = book.css('h3 a').attrib['href']
            book_url = response.urljoin(next_page)
            yield response.follow(book_url, callback=self.parse_book_page)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        book_item = {}

        book_item["url"] = response.url
        book_item["title"] = response.css('h1::text').get()
        book_item["category"] = response.xpath('//*[@id="default"]/div/div/ul/li[3]/a/text()').get()
        book_item["description"] = response.xpath('//*[@id="content_inner"]/article/p/text()').get()

        table = response.css('table, tr')
        book_item["product_type"] = table[2].css('td ::text').get()
        book_item["price_excl_tax"] = table[3].css('td ::text').get()
        book_item["price_incl_tax"] = table[4].css('td ::text').get()
        book_item["tax"] = table[5].css('td ::text').get()
        book_item["availability"] = table[6].css('td ::text').get()
        book_item["number_of_reviews"] = table[7].css('td ::text').get()

        book_item["stars"] = response.css('p.star-rating').attrib['class']
        book_item["price"] = response.css('p.price_color::text').get()

        yield book_item
