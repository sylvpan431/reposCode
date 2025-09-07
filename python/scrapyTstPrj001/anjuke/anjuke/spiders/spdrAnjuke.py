import scrapy


class SpdranjukeSpider(scrapy.Spider):
    name = "spdrAnjuke"
    allowed_domains = ["anjuke.com"]
    start_urls = ["https://m.anjuke.com/cc/sale/"]

    def parse(self, response):
        print(response.text)
        fangList = response.xpath('//ul[@class="list"]/li')
        for fang in fangList:
            fangTitle = fang.xpath('./a/div[@class="content-wrap"]/div[@class="title-wrap lines2"]/span[@class="content-title"]/text()').extract_first()
            fangHuxing = fang.xpath('./a/div[@class="content-wrap"]/div[@class="desc-wrap-community"]/span[@class="content-desc"]/text()').extract_first()
            fangSize = ""
            try:
                fangSize = fang.xpath('./a/div[@class="content-wrap"]/div[@class="desc-wrap-community"]/span[@class="content-desc"]/text()')[1].extract()
            except Exception as e:
                pass
            #fangHuxing = fang.xpath('./a/div[@class="content-wrap"]/div[@class="desc-wrap-community"]/span[@class="content-desc"]/text()').extract_first()
            print(fangTitle)
            print(fangHuxing)
            print(fangSize)
        pass
