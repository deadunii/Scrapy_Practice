import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['www.tradebox.dn.ua']
    start_urls = ['http://www.tradebox.dn.ua/']

    def parse(self, response):
        for link in response.css("ul.clear li li a::attr(href)").extract():
            yield response.follow(link, callback=self.parse_pages)

    def parse_pages(self, response):
        for link in response.css("div.pagination a::attr(href)").extract():
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):
        for link in response.css("a.card__title::attr(href)").extract():
            yield response.follow(link, callback=self.parse_page)


    def parse_page(self, response):
        yield {
            "category": ' / '.join(response.css('div.breadcrumbs a::text').extract()),
            "item": response.css('div.product__content h1::text').get(),
            "price": ' '.join(response.css("div.product__price span::text").extract()),
            "link": response.url}
