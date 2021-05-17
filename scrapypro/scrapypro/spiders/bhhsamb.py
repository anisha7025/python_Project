import scrapy
from bs4 import BeautifulSoup as bs



class BhhsambSpider(scrapy.Spider):
    name = 'bhhsamb'
    allowed_domains = ['bhhsamb.com']
    start_urls = ['http://bhhsamb.com/agents/']

    def parse(self, response):
        soup = bs(response.text)
        links = soup.findAll('span', attrs={'class': 'agent-name'})
        for link in links:
            # print(self.start_urls[0]+link.a['href'][8:])
            yield scrapy.Request(self.start_urls[0] + link.a['href'][8:], callback=self.parse_details)

    def parse_details(self,response):

        divs = response.xpath("//div[@class='agent-details col-sm-24 kill-padding']")

        name = divs.xpath("//div[@class='row']/h1/text()").get()

        yield {
            'name': name
        }