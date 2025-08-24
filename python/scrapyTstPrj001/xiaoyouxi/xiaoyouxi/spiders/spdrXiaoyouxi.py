import scrapy


class SpdrxiaoyouxiSpider(scrapy.Spider):
    name = "spdrXiaoyouxi"
    allowed_domains = ["4399.com"]
    start_urls = ["https://www.4399.com/flash/"]

    def parse(self, response):
        #print(response.text)
        fangLisnt = response.xpath("//ul[@class='n-game cf']/li")
        for fang in fangLisnt:
            name = fang.xpath("./a/b/text()")[0]
            print(name)
