import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['mobi-like.com']
    start_urls = ['http://mobi-like.com/']

    def parse(self, response):
        for link in response.css("a.dy--PopularCategoryMain__link::attr(href)").extract():
            yield response.follow(link, callback=self.parse_category)

    def parse_category(self, response):

        for link in response.css("a.product-item__name::attr(href)").extract():
            yield response.follow(link, callback=self.parse_page)

        if response.css("a.linkPage::attr(href)").get() is not None:
            yield response.follow(response.css("a.linkPage::attr(href)").get(), callback=self.parse_category)


    def parse_page(self, response):
        yield {
            "article": response.css('span.c-product__code--span.label-article.code::text').get().replace('\n','').replace(' ',''),
            "item": response.css('h1.product__title::text').get().replace('\n','').replace('/A','').replace('                                        ',''),
            "price": response.css("span.product__price::text").get().replace('\n','').replace(' ',''),
            "link": response.url,
            "description": response.css("div.discription-cart p::text").get()
        }