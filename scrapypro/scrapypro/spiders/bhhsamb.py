import scrapy
from bs4 import BeautifulSoup as bs



class BhhsambSpider(scrapy.Spider):
    name = 'bhhsamb'
    allowed_domains = ['bhhsamb.com']
    start_urls = ['http://bhhsamb.com/agents/']
    page_number = 2

    def parse(self, response):
        all_links = response.xpath("//div[@class='col-md-8 col-sm-12']")
        for link in all_links:
            url = link.xpath(".//div[@class='agent-info']/span/a/@href").get()
            # print(self.start_urls[0]+url[8:])
            yield scrapy.Request(self.start_urls[0] + url[8:], callback=self.parse_details)


def parse_details(self, response):

        divs = response.xpath("//div[@class='agent-details col-sm-24 kill-padding']")

        name = divs.xpath("//div[@class='row']/h1/text()").get()
        job_title = divs.xpath("//div[@class='text-left medium-text mobile-text-center']/span[@class='big-text']/text()").get()
        image_url = divs.xpath("//img[@class='agent-photo']/@src").get()
        address = divs.xpath("//div[@class='row']/div[@class='text-left medium-text mobile-text-center']//text()").get()

        office = divs.xpath("//a[@data-type='Office']/text()").get()
        cell = divs.xpath("//a[@data-type='Agent']/text()").get()
        email = divs.xpath("//div[@class='text-left medium-text mobile-text-center']/a[@class='agent_email']/@href").get()

        fb = divs.xpath("//div[@class='agent-social-icons social']/a[@class='fb']/@href").get()
        tw = divs.xpath("//div[@class='agent-social-icons social']/a[@class='tw']/@href").get()
        li = divs.xpath("//div[@class='agent-social-icons social']/a[@class='li']/@href").get()
        yt = divs.xpath("//div[@class='agent-social-icons social']/a[@class='yt']/@href").get()
        pi = divs.xpath("//div[@class='agent-social-icons social']/a[@class='pi']/@href").get()
        ig = divs.xpath("//div[@class='agent-social-icons social']/a[@class='ig']/@href").get()

        offices = divs.xpath("//div[@id='team_offices']/a/text()").extract()
        languages = divs.xpath("//div[@class='language-list']/ul/li/text()").extract()
        description = response.xpath("//div[@class='col-sm-24']//following-sibling::p//text()").get()


        yield {
            'name': name,
            'job_title': job_title,
            'image_url': image_url,
            'address': address,
            'contact_details': {
                'office': office,
                'cell': cell,
                'email': email
            },
            'social_contact': {
                'facebook': fb,
                'twitter': tw,
                'linkedin': li,
                'youtube': yt,
                'pinterest': pi,
                'instagram': ig

            },
            'offices': offices,
            'languages': languages,
            'description': description
        }


        new_page = 'https://www.bhhsamb.com/agents?page=' + str(BhhsambSpider.page_number)
        if BhhsambSpider.page_number < 43:
            BhhsambSpider.page_number += 1
            yield response.follow(new_page, callback=self.parse)
